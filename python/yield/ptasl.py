#!/usr/bin/python
# coding=utf-8

### 此脚本在linux中运行良好，但是在mac下，需要设置参数GEVENT_RESOLVER=dnspython设置成python模式，线程模式有问题（TODO 后续有空去修复)
import gevent
from gevent import monkey
monkey.patch_all()

import base64
import csv


import signal

import jsonpath

import requests
import time
from gevent.pool import Pool
# from concurrent import futures
from gevent.queue import Queue

import six

queue = Queue()
# proc_num = multiprocessing.cpu_count()
proc_num = 500
# create_executor = ThreadPoolExecutor(max_workers=proc_num)  #创建线程池，可以修改线程数量
# query_executor = ThreadPoolExecutor(max_workers=proc_num)   #查询线程池，可以修改线程数量

create_report_pool = Pool(size=proc_num)  # 创建生成报告线程池
query_report_pool = Pool(size=proc_num)  # 查询生成报告线程池


def read_from_csv(file_path, mapper):
    """从csv文件中读取需要渲染的数据

    :param file_path:
    :param mapper:
    :return:
    """
    params = []
    if file_path:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                new_param = get_request_param_according_mapper(row, mapper)
                params.append(new_param)
    return params


def get_request_param_according_mapper(origin_param, mapper):
    if not mapper:
        return origin_param

    new_param = {}
    for (name, value) in six.iteritems(mapper):
        if value.startswith('$.'):
            new_param[name] = jsonpath.jsonpath(origin_param, value)[0]
        else:
            new_param[name] = value
    return new_param


def generate_request(create_url, query_url, method, header, params):
    requests = []
    for param in params:
        request = {
            "url": create_url,
            "method": method,
            "header": header,
            "param": param,
            "query_url": query_url
        }
        requests.append(request)
    return requests


def schedule_task(request_list):
    # 创建报告
    # for request in request_list:
    #     create_executor.submit(run_task, request, create_callback)
    for r in request_list:
        create_report_pool.spawn(run_task, r, create_callback)

    print('finish submit create task, total: {}'.format(len(request_list)))

    # 查询报告
    greenlets_to_task_query = schedule_query_task()
    results = []
    for glet in greenlets_to_task_query:
        task = greenlets_to_task_query[glet]
        try:
            # data = glet.result()
            data = glet.value
            if data:
                results.append(data)

        except Exception as e:
            print('task run failed, task: {}, {}'.format(task, e))

    print('all tasks are finished, total: {}, success: {}'.format(len(request_list), len(results)))
    return results


def run_task(request, callback, retry=3):
    query_type = request['method']
    url = request['url']
    param = request['param']
    headers = request['header']

    try:
        for i in range(retry):
            response = None
            try:
                if 'get' == query_type:
                    response = requests.get(url, param, headers=headers)
                else:
                    response = requests.post(url, param, headers=headers)
            except Exception as e:
                print('run task failed, err={}, retry={}'.format(e, i))
                if i >= 2:
                    raise e

            if response and response.status_code == 401:
                print(response.content)
                break

            if response and response.json():
                data = response.json()
                code = data['code']
                if code == 0 or code == 4005:
                    return callback(request, response)
                else:
                    gevent.sleep(2)
    except Exception as e:
        print('max run task failed, {}, param: {}, headers: {}'.format(e, param, headers))

    return None


def create_callback(request, response):
    if not response and not response.json():
        return None

    data = response.json()
    result = jsonpath.jsonpath(data, '$.report_id')
    report_id = result[0] if result[0] else None
    new_param = {
        'report_id': report_id,
        'user_mobile': request['param']['user_mobile'],
        'identity_code': request['param']['identity_code'],
        'real_name': request['param']['real_name']
    }

    new_request = {'header': request.get('header'),
                   'url': request.get('query_url'),
                   'param': new_param,
                   'method': request.get('method')}
    queue.put_nowait(new_request)


def schedule_query_task():
    greenlets_to_task = {}
    # 查询报告
    valid_count = 0

    while True:
        try:
            param = queue.get(timeout=1)
            if not check_and_wait(param):
                continue

            glet = query_report_pool.spawn(run_task, param, query_callback)
            # future = query_executor.submit(run_task, param, query_callback)
            greenlets_to_task[glet] = param
            valid_count += 1
            if valid_count % 1000 == 0:
                print('already finish {}'.format(valid_count))
        except Exception as e:
            import queue as l_queue
            if not isinstance(e, l_queue.Empty):
                print('error message {}, type: {}'.format(e, type(e)))
            break
    else:
        print(any((not g.ready() for g in create_report_pool.greenlets)), queue.qsize())

    print('finish submit query task, total: {}'.format(valid_count))
    return greenlets_to_task


def check_and_wait(request):
    report_id = get_by_path(request, '$.param.report_id')
    if report_id:
        report_time = time.strptime(report_id[12: 26], '%Y%m%d%H%M%S')
        report_seconds = int(time.mktime(report_time))
        time_now = int(time.time())
        delt_seconds = time_now - report_seconds
        delay_seconds = delt_seconds - 24 * 3600 if delt_seconds > 24 * 3600 else delt_seconds

        if 0 < delay_seconds < 10:
            gevent.sleep(1)
            # time.sleep(delay_seconds)
        return True

    print('create failed, no report_id, param: %s' % request)
    return False


def query_callback(request, response):
    if not response and not response.json():
        return None

    data = response.json()
    code = data['code']
    if code == 0:
        user_mobile = request['param']['user_mobile']
        identity_code = request['param']['identity_code']
        real_name = request['param']['real_name']
        report_data = get_by_path(data, '$.data.report_data')

        if report_data:
            report_data['user_mobile'] = user_mobile
            report_data['identity_code'] = identity_code
            report_data['real_name'] = real_name

            return report_data

    return None


def get_by_path(target, path):
    if target and path:
        data = jsonpath.jsonpath(target, path)
        return data[0] if data else None
    return None


def write_to_csv(result_list, file_path):
    with open(file_path, 'w') as file:
        fields = list(result_list[0].keys())
        fields.remove('user_mobile')
        fields.remove('identity_code')
        fields.remove('real_name')
        fields.sort()
        fields.insert(0, 'real_name')
        fields.insert(0, 'identity_code')
        fields.insert(0, 'user_mobile')

        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(result_list)


def get_index(name, passwd, input_file, output_file):
    poc_start = int(time.time())

    # 需要在zues上面申请proxy权限，目标系统为talos-report
    # create_url = 'http://10.58.10.112:8098/task/poc/create'
    create_url = 'https://talos-report-idnu-s.proxy.tongdun.cn/task/poc/create'
    query_url = 'https://talos-report-idnu-s.proxy.tongdun.cn/task/poc/query'
    # query_url = 'http://10.58.10.112:8098/task/poc/query'

    # 客户在魔盒开的账号
    encode_str = base64.encodebytes('{}:{}'.format(name, passwd).encode()).decode().replace('\n', '')
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic {}'.format(encode_str),
        'PARAMS-PARTNER-CODE': 'mobox_mohe'
    }

    # 从文件读取数据，并拼凑成参数列表
    create_param_mapper = {
        'channel_type': 'REPORT',
        'channel_code': '109001',
        'user_mobile': '$.mobile',
        'identity_code': '$.nik',
        'real_name': '$.name',
        'report_time': '$.report_time'
    }
    create_param_list = read_from_csv(input_file, create_param_mapper)

    # 调度创建任务
    create_requests = generate_request(create_url, query_url, 'post', header, create_param_list)
    results = schedule_task(create_requests)

    output_fields = [
        'user_mobile', 'identity_code', 'real_name',
        'multiplatform_apply_1month_total', 'multiplatform_apply_3month_total', 'multiplatform_apply_6month_total',
        'multiplatform_apply_1month_applycycle', 'multiplatform_apply_3month_applycycle',
        'multiplatform_apply_6month_applycycle', 'multiplatform_apply_1month_count', 'multiplatform_apply_3month_count',

        'multiplatform_grant_1month_total', 'multiplatform_grant_3month_total', 'multiplatform_grant_6month_total',
        'multiplatform_grant_1month_grantcycle', 'multiplatform_grant_3month_grantcycle',
        'multiplatform_grant_6month_grantcycle',
        'multiplatform_grant_1month_count', 'multiplatform_grant_3month_count'

        # 'emerger_loan_contact1_3month_multigrant_count', 'emerger_loan_contact2_3month_multigrant_count'
    ]

    result = filter_fields(results, output_fields)
    # 保存结果
    write_to_csv(result, output_file)

    poc_end = int(time.time())
    print('total_cost: %ss' % (poc_end - poc_start))


def filter_fields(result_list, filter_fields):
    """字段映射， 获取需要的指定字段."""
    final_results = []

    for result in result_list:
        data = {}
        for field in filter_fields:
            data[field] = result.get(field)
        final_results.append(data)
    return final_results


def do_analyse(result_file, analysis_file):
    total_count = 0
    total_grant_count = 0
    apply_count_dict = {}

    with open(result_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                total_count += 1
                multiplatform_grant_6month_total = row['multiplatform_grant_6month_total']
                if multiplatform_grant_6month_total and multiplatform_grant_6month_total != '-999' and \
                   multiplatform_grant_6month_total != '0':
                    total_grant_count += 1

                multiplatform_apply_3month_count = row['multiplatform_apply_3month_count']
                if multiplatform_apply_3month_count != '-999' and multiplatform_apply_3month_count != '0':
                    add_count(apply_count_dict, multiplatform_apply_3month_count)
            except Exception as e:
                print(e)

    result_list = []
    row = {"name": "去重样本数", "value": total_count}
    result_list.append(row)

    row = {"name": "授权样本数", "value": total_grant_count}
    result_list.append(row)

    row = {"name": "授权覆盖度", "value": total_grant_count * 1.0 / total_count}
    result_list.append(row)

    items = list(six.iteritems(apply_count_dict))
    items.sort(key=lambda x: x[0])

    for item in items:
        row = {'name': '{}家申请数'.format(item[0]), 'value': item[1]}
        result_list.append(row)

    fields = ['name', 'value']

    with open(analysis_file, 'w', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writerows(result_list)


def add_count(count_dic, key):
    if key not in count_dic:
        count_dic[key] = 1
    else:
        count_dic[key] = count_dic[key] + 1


def handler_sigquit():
    print('Got SIGQUIT')
    gevent.killall(create_report_pool.greenlets)
    gevent.killall(query_report_pool.greenlets)

if __name__ == '__main__':
    gevent.signal(signal.SIGQUIT, handler_sigquit)
    _input = '/tmp/tmp.csv'
    output = '/tmp/result.csv'
    analysis_file = '/tmp/analysis.csv'
    get_index('xxx', 'xxx', _input, output)
    do_analyse(output, analysis_file)

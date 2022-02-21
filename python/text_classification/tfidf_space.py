from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pickle
from sklearn.datasets.base import Bunch

# 读取bunch对象
def read_bunch(path):
    with open(path, "rb") as fp:
        bunch = pickle.load(fp)           # joblib 同样可用于存储模型文件
    return bunch

# 读取文件对象
def read_file(path):
    with open(path, "rb") as fp:
        bunch = fp.read()
    return bunch

# 写入bunch对象
def write_bunch(path,bunch):
    with open(path, "wb") as fp:
        pickle.dump(bunch,fp)

# 训练集
def train_tfidf_space(stopword_path, train_bunch_path, train_tfidf_data):
    '''
    stopword_path: 停用词路径
    train_bunch_path: 训练集语料路径
    train_tfidf_data: 训练集tfidf数据路径
    '''
    bunch = read_bunch(train_bunch_path)
    stopwords = read_file(stopword_path).splitlines()   # 读取停用词
    tfidf_space = Bunch(label=bunch.label, filepath=bunch.filepath, contents=bunch.contents, tdm=[], space={})

    vectorizer = TfidfVectorizer(stop_words=stopwords, sublinear_tf=True, max_df=0.5)
#max_df 严格忽略高于给出阈值的文档频率的词条 ，sublinear 应用线性缩放TF
    tfidf_space.tdm = vectorizer.fit_transform(bunch.contents)
    tfidf_space.space = vectorizer.vocabulary_

    write_bunch(train_tfidf_data,tfidf_space)

# 测试集
def test_tfidf_space(stopword_path, test_bunch_path, test_tfidf_data, train_tfidf_data):
    '''
    stopword_path: 停用词路径
    test_bunch_path: 测试集语料路径
    test_tfidf_data: 测试集tfidf数据路径
    train_tfidf_data: 训练集tfidf数据路径,将训练集的词向量空间坐标赋值给测试集
    '''
    bunch = read_bunch(test_bunch_path)
    stopwords = read_file(stopword_path).splitlines()     # 读取停用词
    tfidf_space = Bunch(label=bunch.label, filepath=bunch.filepath, contents=bunch.contents, tdm=[], space={})
# 权重矩阵tdm，其中，权重矩阵是一个二维矩阵，tdm[i][j]表示，第j个词（即词典中的序号）在第i个类别中的IF-IDF值

    train_bunch = read_bunch(train_tfidf_data)   #训练集tfidf数据
    tfidf_space.space = train_bunch.space        #将训练集的词向量空间坐标赋值给测试集
#使用TfidVectorizer初始化向量空间模型
    vectorizer = TfidfVectorizer(stop_words=stopwords, sublinear_tf=True, max_df=0.5, vocabulary=train_bunch.space)
#文本转为词频矩阵，单独保存字典文件
    tfidf_space.tdm = vectorizer.fit_transform(bunch.contents)
#创建词袋的持久化
    write_bunch(test_tfidf_data, tfidf_space)

if __name__ == '__main__':
    # 训练集数据处理
    stopword_path = "./chinese_stop_words.txt"  # 停用词表的路径
    train_bunch_path = './train_bunch_bag.dat'
    train_tfidf_data = './train_tfdifspace.dat'
    train_tfidf_space(stopword_path, train_bunch_path,train_tfidf_data)

    # 测试集数据处理
    test_bunch_path = './test_bunch_bag.dat'
    test_tfidf_data = './test_tfidfspace.dat'
    test_tfidf_space(stopword_path, test_bunch_path, test_tfidf_data,train_tfidf_data)
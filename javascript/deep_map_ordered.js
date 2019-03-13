datas = {
   "HZ": {
     "sandbox": {
       "matrix": {
         "vm": 2,
         "container": 2,
         "sum": 4,
         "vm_done": 2,
         "container_done": 2,
         "hosts": [
           "192.168.125.253",
           "192.168.127.226"
         ]
       }
     },
     "production": {
       "matrix": {
         "vm": 2,
         "container": 2,
         "sum": 4,
         "vm_done": 2,
         "container_done": 2,
         "hosts": [
           "192.168.125.253",
           "192.168.127.226"
         ]
       }
     },
     "staging": {
       "matrix": {
         "vm": 2,
         "container": 2,
         "sum": 4,
         "vm_done": 2,
         "container_done": 2,
         "hosts": [
           "192.168.125.253",
           "192.168.127.226"
         ]
       }
     },
   },
   "SH": {
     "production": {
       "matrix": {
         "vm": 2,
         "container": 0,
         "sum": 2,
         "vm_done": 2,
         "container_done": 0,
         "hosts": [
           "10.21.35.169",
           "10.21.78.176"
         ]
       }
     }
   }
 }
const envSequentially = {
   staging: 1,
   production: 2,
   sandbox: 3
};
let orderMap = {};
for (let k in datas) {
    let ordered = new Map();
    Object.keys(datas[k]).sort((e1, e2) => {return envSequentially[e1] - envSequentially[e2]}).forEach((key) => {
        ordered.set(key, datas[k][key])
    });
    orderMap[k] = ordered
}
// var promise = new Promise(function (resolve){
//     console.log("inner promise"); // 1
//     resolve(42);
// });
// promise.then(function(value){
//     console.log(value); // 3
// });
// console.log("outer promise"); // 2



// var preloadImage = function(path) {
//     return new Promise(function(resolve, reject) {
//         var iamge = new Image();
//         image.onload = resolve;
//         image.onerror = reject;
//         image.src = path;
//     });
// };

// preloadImage("https://dn-anything-about-doc.qbox.me/teacher/QianDuan.png").
// then(function() {
//     console.log('图片加载成功');
// }, function() {
//     console.log('图片加载失败');
// });
function search(term) {
    var url = `http://www.baidu.com/search?q=${term}`;
    var xhr = new XMLHttpRequest();
    var result;
    var p = new Promise(function(resolve, reject) {
        xhr.open('GET', url, true);
        xhr.onload = function(e) {
            if (this.status === 200) {
                result = JSON.parse(this.responseText);
                resolve(result);
            }
        };
        xhr.onerror = function(e) {
            reject(e);
        };
        xhr.send();
    });
    return p;
}
search('Hello world').then(console.log, console.error);


/**
* 将文件转换成2进制数据
**/
function transFile2ByteArray(file) {
    let fr = new FileReader();
    fr.readAsDataURL(file);
    fr.addEventListener(
      "load",
      () => {
        let arr = fr.result.split(",");
        let bstr = atob(arr[1]);
        let n = bstr.length;
        // 承载二进制文件信息，可以使用此信息
        let u8arr = new Uint8Array(n);
        while (n--) {
          u8arr[n] = bstr.charCodeAt(n);
        }
        // TODO 设置文件存储路径
      },
      false
    );
}

/**
* 将文件转换成2进制数据，方法2
**/
function transFile2ByteArray(file) {
    let fr = new FileReader();
    fr.readAsArrayBuffer(file);
    fr.addEventListener(
      "load",
      () => {
          //fr.result，承载文件二进制信息
      },
      false
    );
}


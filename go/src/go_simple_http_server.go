package main

import (
	"net/http"
	"time"
)

func hello(w http.ResponseWriter, req *http.Request) {
	time.Sleep(5 * time.Second)
	w.Write([]byte("Hello"))
}
func say(w http.ResponseWriter, req *http.Request) {
	w.Write([]byte("Hello"))
}
func main() {
	http.HandleFunc("/", hello)
	http.Handle("/handle", http.HandlerFunc(say))
	http.ListenAndServe("127.0.0.1:8088", nil)
	select {} // 阻塞进程
}

package main

import (
	"bytes"
	"fmt"
	"os"
)

func main() {
	s := []byte(" world")
	buf := bytes.NewBufferString("hello")
	fmt.Println(buf.String()) //buf.String()
	buf.Write(s)
	fmt.Println(buf.String())
}

func writeTo() {
	file, _ := os.Create("text.txt")
	buf := bytes.NewBufferString("hello")
	buf.WriteTo(file)
	fmt.Fprintln(file, buf.String())
}

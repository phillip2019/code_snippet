package main

import (
	//"encoding/base64"
	//"fmt"
	"strings"
	"fmt"
	"encoding/base64"
)


func main() {
	//str := `MFxEHBnFFUC8t7XAxFqXLVkSUW5y9a3mR52K7UvzcRT/Wpo9NCTMDGCLfZJa5WBtVF 6UeglfdJCLDF6hFxP7Hv/P1Ukme0UxfxtGC Zyr DOiwoAY4foaJSrVc6BsJj5gy6l aQbDtXfgDLlRSsRSd7U6Bg9vJozg5tCFOfkX0`
	//data, err := base64.StdEncoding.DecodeString(str)
/*	data, err := base64DecodeStripped(str)
	if err != nil {
		fmt.Println("error:", err)
		return
	}
	fmt.Printf("%q\n", data)*/
	commits := map[string]int{
		"rsc": 3711,
		"r":   2138,
		"gri": 1908,
		"adg": 912,
	}
	for k, v := range commits {fmt.Printf("%s=%d;", k, v)}
}

func base64DecodeStripped(s string) (string, error) {
	if i := len(s) % 4; i != 0 {
		s += strings.Repeat("=", 4-i)
	}
	decoded, err := base64.StdEncoding.DecodeString(s)
	return string(decoded), err
}
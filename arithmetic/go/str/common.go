package main

import (
	"fmt"
	"unicode/utf8"
)

// 字符串：倒置算法
func reverse(s []string) {
	for i, j := 0, len(s) - 1; i < j; i, j = i+1, j-1 {
		s[i], s[j] = s[j], s[i]
	}
}

// 字符串：倒置算法，数组指针法
func reverseArray(s *[9]string) {
	for i, j := 0, len(s) - 1; i < j; i, j = i+1, j-1 {
		s[i], s[j] = s[j], s[i]
	}
}


// 比较slice是否相等
func equalSlice(x, y []string) bool {
	if len(x) != len(y) {
		return false
	}
	for i := range x {
		if x[i] != y[i] {
			return false
		}
	}
	return true
}


// 比较map是否相等
func equalMap(x, y map[string]int) bool {
	if len(x) != len(y) {
		return false
	}
	for k, xv := range x {
		if yv, ok := y[k]; !ok || xv != yv {
			return false
		}
	}
	return true
}

// 字符串数组旋转
// n 字符长度，k旋转个数， s输入切片
func rotateSlice(n, k int, s []string) {
	t := make([]string, k)
	copy(t, s[len(s)-k:])
	for i := len(s) - 1; i >= k; i-- {
		s[i] = s[i - k]
	}
	copy(s[:k], t)
}

func main() {
	a := [...]string{"1", "2", "3", "4", "5", "6", "7", "8", "9"}
	reverse(a[:])
	fmt.Println(a)

	b := [...]string{"1", "2", "3", "4", "5", "6", "7", "8", "9"}
	reverseArray(&b)
	fmt.Println(b)

	c := [...]string{"1", "2", "3", "4", "5", "6", "7", "8", "9"}
	rotateSlice(9, 3, c[:])
	fmt.Println(c)
}
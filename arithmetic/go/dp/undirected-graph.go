package main

import (
	"fmt"
	"math"
)

func main() {
	var w [6][6]int64
	var d [6]int64
	// 初始化，边不存在
	for i := 1; i < 6; i++ {
		for j := 1; j < 6; j++ {
			if i == j {
				w[i][j] = 0
			} else {
				w[i][j] = -1
			}
		}
	}
	initGraph(&w)
	for i := 0; i < 6; i++ {
		for j := 0; j < 6; j++ {
			fmt.Print(w[i][j], "\t")
		}
		fmt.Println()
	}

	for i := 2; i < 6; i++ {
		d[i] = math.MaxInt64
		for j := 1; j < i; j++ {
			if w[j][i] != -1 && d[j] + w[j][i] < d[i] {
				d[i] = d[j] + w[j][i]
			}
		}
	}

	if d[5] != math.MaxInt64 {
		fmt.Println(d[5])
	} else {
		fmt.Println("不存在!")
	}

}


func initGraph(w *[6][6]int64) {
	(*w)[1][2] = 1
	(*w)[1][4] = 5
	(*w)[2][1] = 1
	(*w)[2][3] = 1
	(*w)[2][4] = -1
	(*w)[3][2] = 1
	(*w)[3][4] = 4
	(*w)[4][1] = 5
	(*w)[4][2] = -1
	(*w)[4][3] = 4
	(*w)[4][5] = 3
	(*w)[5][4] = 3
}
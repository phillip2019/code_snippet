package main

import (
	"flag"
	"fmt"
	"math/rand"
)

/*使用快速排序的区间大小临界值*/
const (
	MAX_THRESH = 4
)

/*元素交换*/
func swap(a *int,  b *int) {
	t := *a
	*a = *b
	*b = t
}

/*插入排序*/
func insertSort(A []int, N int) {
	// 优化后的插入排序
	j, p, temp := 0, 0, 0
	for p = 1; p < N; p++ {
		temp = A[p]
		for j = p; j > 0 && A[j-1] > temp; j-- {
			A[j] = A[j-1]
		}
		A[j] = temp
	}
}

/*三数中值法选择基准*/
func medianPivot(A []int, left int, right int) int {
	center := (left + right) / 2
	//对三数进行排序
	if A[left] > A[center] {
		swap(&A[left], &A[right])
	}
	if A[left] > A[right] {
		swap(&A[left], &A[right])
	}
	if A[center] > A[right] {
		swap(&A[center], &A[right])
	}
	// 此时，最后一个元素一定大于基准元素
	swap(&A[center], &A[right - 1])
	return A[right - 1]
}


func partition(A []int, left int, right int) int {
	i, j := left, right - 1
	// 获取基准值
	pivot := medianPivot(A, left, right)
	for {
		for ; A[i] < pivot; i++ {}
		for ; A[j] > pivot; j-- {}
		if i < j {
			swap(&A[i], &A[j])
		} else {
			break
		}
	}
	// 交换基准元素和i指向的元素
	swap(&A[i], &A[right-1])
	return i
}

func QSort(A []int, left int, right int) {
	i := 0
	arr := A
	if right - left >= MAX_THRESH  {
		// 分割操作
		i = partition(arr, left, right)
		QSort(arr, left, i-1)
		QSort(arr, i+1, right)
	} else {
		// 数据量较小时，使用插入排序
		insertSort(arr[left:], right - left + 1)
	}
}

func main() {
	qSortNum := 0
	flag.IntVar(&qSortNum, "N", 0, "-N quick sort num\n")
	flag.Parse()

	fmt.Printf("sort for %d numbers\n", qSortNum)
	// 随机产生输入数量的数据
	A := make([]int, qSortNum)
	i := 0
	for ; i < qSortNum; i++ {
		A[i] = rand.Int()
	}
	fmt.Println()
	fmt.Println("befor sort:")
	fmt.Print(A)
	QSort(A, 0, qSortNum - 1)
	fmt.Println("after sort:")
	fmt.Print(A)
}
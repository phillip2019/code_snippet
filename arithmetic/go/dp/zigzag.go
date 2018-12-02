package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	//Enter your code here. Read input from STDIN. Print output to STDOUT、
	var N, z int
	var A, d []int
	fmt.Scanln(&N)
	reader := bufio.NewReader(os.Stdin)
	input, _ := reader.ReadString('\n')
	inputs := strings.Split(input, " ")
	for i, s := range inputs {
		if i == N-1 {
			s = strings.Replace(s, "\n", "", -1)
		}
		a, _ := strconv.Atoi(s)
		A = append(A, a)
	}

	for i := 0; i < N; i++ {
		d = append(d, 1)
	}

	for i := 1; i < N; i++ {
		if A[i-1] < A[i] {
			d[i] = d[i-1] + 1
		} else if d[i-1] >= 3 {
			z += d[i-1] - 2
		}
	}
	fmt.Println(z)
}

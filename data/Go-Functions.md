# Go 002 - Functions in Go

Functions in Go operate similarly to functions in other languages, with the noticeable detail that the keyword used to define them is not `function` but `func`. Also, note how the return type is specified *after* the name of the function. Here is an example:

<pre>
package main

import "fmt"

func add(x int, y int) int {
	return x + y
}

func main() {
	fmt.Println(add(42, 13))
}
</pre>

Note that the `Println` function is a member of the `fmt` package here, which has been imported at the top of this example. This is how Go's package management works. You can also define your own packages at the top of your file and import them elsewhere, but we'll cover this in a later task.

## Task

Following the time-honoured tradition, see if you can create a recursive Fibonacci sequence generator in Go. Use [this](https://pythonexamples.org/fibonacci-series-in-python-using-recursion/#2) reference (written in Python) as a reference for the algorithm to use.

Some hints:

- If blocks have interesting formatting - See [here](https://gobyexample.com/if-else)
- You may want to use `append()` with slices to build your sequence - see [here](https://www.tutorialspoint.com/go/go_slice.htm )

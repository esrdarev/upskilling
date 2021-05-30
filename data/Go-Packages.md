# Go 003 - Packages

Go, like a lot of langauges, operates on the principle of reusable pieces of code named Packages, however Go also uses the concept of Go Modules, which is an extra distinct layer in the hierarchy above packages. A Go Module is a collection of Go Packages.

## Creating a Go Module

In your terminal, create a new directory named "MyFibModule", and navigate to it. Next, run the command `go mod init MyFibModule`. This will create a new file named `go.mod`, which is the basic definition of your new module. 

The directory structure will look like this:

- MyFibModule
    - go.mod

Next, create a folder named Fib, and in here create a file named Fib.go. Now, move the code from the previous task, P-002, for creating an arbitrary Fibonacci sequence into this file and add a package name to the top, so it looks like this:

<pre>
package fib

func FibRecurse(n int) int {
    // Your own code will be here
}
</pre>

The directory structure will now look like this:

- MyFibModule
    - go.mod
    - Fib
        - Fib.go

Next, create a main function to use your new package. Create `main.go` inside the top-level `MyFibModule` folder, and move the main function from the previous task into here. Next, you need to import your new module:

<pre>
package main
import (
    "fmt"
    "MyFibMod/Fib"
)

func main() {
    //Existing code.
}
</pre>

Finally, change the the call to your recursive function. Let's assume you named your function FibRecurse(...) and it's now happily inside `MyFibModule/Fib/Fib.go`. To call that function from your module, after it has been imported, you would call `Fib.FibRecurse(...)`. 

## Caveat!

Note that you **must** start your function name with a capital letter! In Go, only functions that start with a capital letter are exported, and therefore available outside of the package itself for use.

## Resources

See the following links for help and more info:

- [Official Go Tutorial for creating a Go module](https://golang.org/doc/tutorial/create-module)
- [Call your module code from another module](https://golang.org/doc/tutorial/call-module-code)
- [Callicoder - A beginners guide to Packages in golang](https://www.callicoder.com/golang-packages/)

# Go 001 - Hello, world!

Welcome to the first upskilling task in the Project Snowden directed upskilling platform. In this task, you will need to set up your Go environment, create a basic script and then run it to make sure you're setup is ready to go.

## Installing Go

- Download the latest Stable Release (1.16.3) for your platform from [here](https://golang.org/dl/). You 
  will most likely need the 64-bit version of the Windows Installer package.
- Once you have installed Go, open up Windows Powershell and run the command `go version`.
  Make sure the reported version matches the version you had just installed.

## First steps

First, create a new file, `my-test.go`, and place the following in it:
```
package main
import ("fmt")

func main() {
  fmt.Println("Hello world!")
}
```

Now from a new Powershell window navigated to the folder where `my-test.go` resides, run:
```
go run my-test.go
```

You should see some output!

## Building

Go can run files, but can also compile them into native binaries to execute on your system. To do this, from Powershell, run the command:
```
go build my-test.go
```

You should see a new binary created, which on Windows will be `my-test.exe`. You can execute this directly and the operation should be identical. You can also distribute this binary and expect it to run precisely the same somewhere else providing the platform (architecture and OS) are the same.

# Golang Assessment Questions with Answers

`Turing`

<br>

## Question 1: Implicit Repetition in a const Block

**Problem Statement**

What is the output of the following code?

```go
package main

import "fmt"

const (
	i = 7
	j
	k
)

func main() {
	fmt.Println(i, j, k)
}
```

**Correct Answer**

```ini
7 7 7
```

**Explanation**

- Inside a `const` block, an identifier declared without an expression **repeats the previous expression**.
- So `j` and `k` both inherit `= 7` from `i`.
- <mark>This is the same mechanism that makes `iota` work across multiple lines.</mark>

<br><br>

## Question 2: What Is a Slice

**Problem Statement**

What is a slice in Golang?

**Options**

- A) An abstraction over normal arrays
- B) Pointer variable
- C) A set data structure
- D) An array

**Correct Answer**

`A) An abstraction over normal arrays`

**Explanation**

- A slice is a lightweight descriptor holding three fields: a **pointer** to an underlying array, a **length**, and a **capacity**.
- It gives a dynamically sized, flexible view into that array.
- The slice itself is not the data, it only points to it.

<br><br>

## Question 3: Length and Capacity After append

**Problem Statement**

```go
a := [...]int{1, 2, 3, 4, 5, 6, 7, 8, 9}
s := a[2:4]
newS := append(s, 55, 66)
fmt.Printf("len=%d, cap=%d\n", len(newS), cap(newS))
```

What will be the output after this code is executed?

**Options**

- A) 4, 9
- B) 2, 7
- C) 2, 9
- D) 4, 7

**Correct Answer**

`D) 4, 7`

**Explanation**

- The array `a` has 9 elements (indexes 0 to 8).
- `a[2:4]` gives `s` with `len = 4 - 2 = 2` and `cap = 9 - 2 = 7` (from the start index to the end of the array).
- Appending 2 elements makes `len = 4`.
- Since the new length (4) still fits inside the capacity (7), <mark>no reallocation happens and the capacity stays 7.</mark>

**Dry Run**

```ini
a    = [1 2 3 4 5 6 7 8 9]
s    = [3 4]            len=2  cap=7
newS = [3 4 55 66]      len=4  cap=7
```

<br><br>

## Question 4: copy Into a nil Slice

**Problem Statement**

```go
var s1 []int
s2 := []int{1, 2, 3}
n1 := copy(s1, s2)
fmt.Printf("n1=%d, s1=%v, s2=%v\n", n1, s1, s2)
fmt.Println("s1 == nil", s1 == nil)
```

What will be the output after this code is executed?

**Options**

- A) `n1=0, s1=[], s2=[1 2 3]` and `s1 == nil true`
- B) `n1=3, s1=[1 2 3], s2=[1 2 3]` and `s1 == nil false`
- C) `n1=0, s1=[], s2=[]` and `s1 == nil true`
- D) `n1=3, s1=[1 2 3], s2=[]` and `s1 == nil false`

**Correct Answer**

`A) n1=0, s1=[], s2=[1 2 3]` and `s1 == nil true`

**Explanation**

- `var s1 []int` declares a `nil` slice with `len = 0` and `cap = 0`.
- `copy(dst, src)` copies `min(len(dst), len(src))` elements, which here is `min(0, 3) = 0`.
- <mark>`copy` never grows the destination, so nothing is copied and `s1` stays `nil`.</mark>
- Printing a `nil` slice with `%v` shows `[]`.

**Output**

```ini
n1=0, s1=[], s2=[1 2 3]
s1 == nil true
```

<br><br>

## Question 5: Empty select in main

**Problem Statement**

What will be the output of the following program?

```go
package main

import "fmt"

func service() {
	fmt.Println("Hello from service!")
}

func main() {
	fmt.Println("main() started")
	go service()
	select {}
	fmt.Println("main() stopped")
}
```

**Options**

- A) Blocks the main thread and hangs
- B) Throws a compilation error: not a valid statement
- C) Throws a runtime error: all goroutines are asleep, deadlock
- D) Works like a charm

**Correct Answer**

`C) Throws a runtime error: all goroutines are asleep - deadlock!`

**Explanation**

- `select {}` with no cases blocks the current goroutine **forever**.
- The `service` goroutine runs, prints, and then exits.
- With no runnable goroutine left, the Go runtime detects a deadlock and panics.
- `fmt.Println("main() stopped")` is never reached.

**Output**

```ini
main() started
Hello from service!
fatal error: all goroutines are asleep - deadlock!
```

<br><br>

## Question 6: Non Blocking Channel Operations

**Problem Statement**

Which of the following creates a non blocking channel?

**Options**

- A) Using the statement `for {}`
- B) Using a `default` case in `select {}`
- C) Using the statement `select {}`
- D) All channels are non blocking by default

**Correct Answer**

`B) Using default case in select{}`

**Explanation**

- Channel send and receive operations in Go are **blocking by default**.
- Wrapping the operation in a `select` with a `default` case makes it non blocking.
- If no channel case is ready, the `default` branch runs immediately instead of waiting.

```go
select {
case msg := <-ch:
	fmt.Println(msg)
default:
	fmt.Println("no value ready, moving on")
}
```

<br><br>

## Question 7: Passing an Array to a Function

**Problem Statement**

```go
package main

import "fmt"

func makeSquares(array [10]int) {
	for index, elem := range array {
		array[index] = elem * elem
	}
}

func main() {
	a := [10]int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
	makeSquares(a)
	fmt.Println(a)
}
```

If we pass the array to `makeSquares()`, what is the output?

**Options**

- A) Array can't be passed as value
- B) `[0 1 2 3 4 5 6 7 8 9]`
- C) `[0 1 4 9 16 25 36 49 64 81]`
- D) `[]`

**Correct Answer**

`B) [0 1 2 3 4 5 6 7 8 9]`

**Explanation**

- <mark>In Go, arrays are value types, so passing one to a function copies the entire array.</mark>
- `makeSquares` squares the elements of its own local copy.
- The original array `a` in `main` is untouched.
- To modify the original, pass a **slice** (`[]int`) or a pointer (`*[10]int`).

<br><br>

## Question 8: Comparing an Interface With a Concrete Type

**Problem Statement**

```go
package main

import "fmt"

type Shape interface {
	Area() float64
	Perimeter() float64
}

type Rect struct {
	width  float64
	height float64
}

func (r Rect) Area() float64      { return r.width * r.height }
func (r Rect) Perimeter() float64 { return 2 * (r.width + r.height) }

func main() {
	var s Shape
	s = Rect{5.0, 4.0}
	r := Rect{5.0, 4.0}
	fmt.Println(s == r)
}
```

What will be the output after this code is executed?

**Options**

- A) Invalid comparison of types
- B) False
- C) Compilation error
- D) True

**Correct Answer**

`D) True`

**Explanation**

- Go allows comparing an interface value with a concrete value when that concrete type is comparable and implements the interface.
- The comparison is true only when both conditions hold:
  - the interface's **dynamic type** equals the concrete type (`Rect` in both cases)
  - the underlying **values** are equal (`{5.0, 4.0}` in both cases)
- Both hold here, so the result is `true`.

<br><br>

## Question 9: Pointer Receiver and Method Sets

**Problem Statement**

```go
package main

import "fmt"

type Shape interface {
	Area() float64
	Perimeter() float64
}

type Rect struct {
	width  float64
	height float64
}

func (r *Rect) Area() float64     { return r.width * r.height }
func (r Rect) Perimeter() float64 { return 2 * (r.width + r.height) }

func main() {
	r := Rect{5.0, 4.0}
	var s Shape = r
	area := s.Area()
	fmt.Println(area)
}
```

What will be the output after this code is executed?

**Options**

- A) `<nil>`
- B) Runtime error: Rect does not implement Shape (Area method has pointer receiver)
- C) Compile time error: Rect does not implement Shape (Area method has pointer receiver)
- D) 20

**Correct Answer**

`C) Compile-time error: Rect does not implement Shape (Area method has pointer receiver)`

**Explanation**

- `Area()` is declared with a pointer receiver `*Rect`, while `Perimeter()` uses a value receiver.
- <mark>The method set of `Rect` contains only value receiver methods, while the method set of `*Rect` contains both.</mark>
- So `*Rect` satisfies `Shape`, but plain `Rect` does not.
- Interface satisfaction is checked at compile time, so this fails to build.
- Fix: use `var s Shape = &r`.

<br><br>

## Question 11: Fixing a nil Map and Key Lookup

**Problem Statement**

Correct the mistakes in lines A and B.

```go
package main

func main() {
	var m map[string]int // A
	m["a"] = 1

	if v := m["b"]; v != nil { // B
		println(v)
	}
}
```

**Options**

- A) A: `m := make(map[string]int)` and B: `if v, ok := m["b"]; ok`
- B) There is no mistake, the program will compile fine
- C) A: `m := map[string]int` and B: `if v, ok := m["b"]; ok`
- D) A: `var m map[string]int{}` and B: `if k, v := m["b"]; v != nil`

**Correct Answer**

`A) A: m := make(map[string]int)` and `B: if v, ok := m["b"]; ok`

**Explanation**

- **Line A:** `var m map[string]int` declares a `nil` map. Reading from a `nil` map is fine, but <mark>writing to a `nil` map panics at runtime, so it must be initialised with `make`.</mark>
- **Line B:** A missing key returns the **zero value** of the value type, which is `0` for `int`, not `nil`. Comparing an `int` to `nil` is also a compile error.
- The correct existence check is the comma ok idiom: `v, ok := m["b"]`.

**Corrected Code**

```go
m := make(map[string]int)
m["a"] = 1

if v, ok := m["b"]; ok {
	println(v)
}
```

<br><br>

## Question 12: Comparing Two Interfaces Holding Pointers

**Problem Statement**

```go
package main

import "fmt"

type S struct {
	a, b, c string
}

func main() {
	x := interface{}(&S{"a", "b", "c"})
	y := interface{}(&S{"a", "b", "c"})
	fmt.Println(x == y)
}
```

What will be the output after this code is executed?

**Options**

- A) False
- B) True
- C) Nil
- D) Compilation error

**Correct Answer**

`A) False`

**Explanation**

- Both `x` and `y` hold values of the same dynamic type `*S`, so the types match.
- For pointer types, equality compares **memory addresses**, not the pointed to contents.
- `&S{...}` is evaluated twice, producing two separate allocations at different addresses.
- Comparing the structs themselves (`*x.(*S) == *y.(*S)`) would give `true`.

<br><br>

## Question 13: Setting a Slice to nil

**Problem Statement**

```go
a := []string{"A", "B", "C", "D", "E"}
a = nil
fmt.Println(a, len(a), cap(a))
```

**Options**

- A) `[], 0, 0`
- B) `nil, 0, 0`
- C) `[], 0, 5`
- D) `nil, 0, 5`

**Correct Answer**

`A) [] 0 0`

**Explanation**

- Assigning `nil` throws away the slice header entirely, including the pointer to the underlying array.
- Both length and capacity reset to `0`.
- `fmt.Println` prints a `nil` slice as `[]`, not as the word `nil`.

<br><br>

## Question 14: Call by Value in Go

**Problem Statement**

Which of the following is true about the call by value method of parameter passing in Go?

**Options**

- A) All are correct
- B) None is correct
- C) Changes made to the parameter inside the function have no effect on the argument
- D) This method copies the actual value of an argument into the formal parameter of the function

**Correct Answer**

`A) All are correct`

**Explanation**

- Option D describes the mechanism: the argument's value is copied into the parameter.
- Option C describes the consequence: modifying the copy leaves the caller's variable unchanged.
- Both statements are true, so option A is correct.
- <mark>Go is always call by value. Passing a pointer still copies the pointer, it just copies an address that both sides share.</mark>

<br><br>

## Question 15: Reslicing With a[:0]

**Problem Statement**

```go
a := []string{"A", "B", "C", "D", "E"}
a = a[:0]
fmt.Println(a, len(a), cap(a))
```

**Options**

- A) `nil, 0, 0`
- B) `[], 0, 0`
- C) `nil, 0, 5`
- D) `[], 0, 5`

**Correct Answer**

`D) [] 0 5`

**Explanation**

- `a[:0]` only changes the length field to `0`, so the slice prints as `[]`.
- The pointer to the underlying array is kept, so capacity stays `5`.
- This is the standard trick for **reusing a slice's buffer** without reallocating.
- Contrast with Question 13: `a = nil` drops the array, `a = a[:0]` keeps it.
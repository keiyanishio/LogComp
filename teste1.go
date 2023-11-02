var i int
var n int
var f int
n = Scanln()
f = 1
for i = 2; i < n + 1; i = i + 1 {
	f = f * i
}
Println(f)

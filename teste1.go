var x int
var y int
x = 3+1
y = x
if x > 1 {
    x = 5-1
}
if (x == 3) {
} else {
    x = 3
}
for x = 3; x < 5; x = x + 1 {
    y = x - 1
}
Println(x)
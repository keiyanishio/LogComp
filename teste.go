
// func soma(x int, y int) int {
// 	var a int 
// 	a = x + y
// 	Println(a)
// 	return a
// }

// func main() int{
// 	var a int
// 	var b int
// 	a = 3
// 	b = soma(a, 4)
// 	Println(a)
// 	Println(b)
// }

func soma(x int, y int) int {
    return x + y
}

func read() int {
    return Scanln()
}

func main() int {
    var a int
    a = read()
    Println(a)
}

func concat(a string, b string) string {
    return a . b
}

func main() int {
    var x_1 int
    x_1 = soma(read()-1, 1)
    soma(2, 1)

    Println(x_1)

    if (x_1 > 1 && !!!(x_1 < 1)) || x_1 == 3 {
        x_1 = 2
    } 

    var x int = 3+6/3   *  2 -+-  +  2*4/2 + 0/1 -((6+ ((4)))/(2)) // Teste // Teste 2
    var y_1 int = 3
    y_1 = soma(y_1, x_1)
    var z__ int
    z__ = soma(x, y_1)

    if x_1 == 2 {
        x_1 = 2
    }

    if x_1 == 3 {
        x_1 = 2
    } else {
        x_1 = 3
    }

    for x_1 = 0; x_1 < 1 || x == 2; x_1 = soma(x_1, 1) {
        Println(x_1)
    } 



    // Saida final
    Println(x_1)
    Println(x)
    Println(z__+1)

    // All bool and int operations
    var y int = 2
    var z int
    z = (y == 2)
    Println(y+z)
    Println(y-z)
    Println(y*z)
    Println(y/z)
    Println(y == z)
    Println(y < z)
    Println(y > z)

    // All str operations 
    var a string 
    var b string

    x_1 = 1 
    y = 1 
    z = 2
    a = "abc"
    b = "def"
    Println(concat(a."",b.""))
    Println(a.x_1)
    Println(x_1.a)
    Println(y.z)
    Println(a.(x_1==1))
    Println(a == a)
    Println(a < b)
    Println(a > b)
}






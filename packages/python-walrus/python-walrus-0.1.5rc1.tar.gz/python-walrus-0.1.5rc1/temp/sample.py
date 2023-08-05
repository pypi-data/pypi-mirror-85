x = 66
y = 77


def foo():

    z = 1

    class A:
        global x
        nonlocal z

        x = 99
        print(x := x + 1 + z)
        print(y := x + 10)
        print(y + 100)
        y = 999
        print(y)

    print(x)
    print(y)


foo()

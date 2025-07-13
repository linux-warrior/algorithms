from __future__ import annotations


class QuadraticFunction:
    a: int
    b: int
    c: int

    def __init__(self, *, a: int, b: int, c: int) -> None:
        self.a = a
        self.b = b
        self.c = c

    def evaluate(self, *, x: int) -> int:
        return x * (self.a * x + self.b) + self.c


def main() -> None:
    a, x, b, c = map(int, input().strip().split())
    quadratic_function = QuadraticFunction(a=a, b=b, c=c)
    print(quadratic_function.evaluate(x=x))


if __name__ == '__main__':
    main()

from time import sleep


def slow_add(a: int, b: int) -> int:
    sleep(4)
    return a + b

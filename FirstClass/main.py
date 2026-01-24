#!/usr/bin/env -S uv run --script

from RunningTotal import RunningTotal


def main():
    a = RunningTotal()
    b = RunningTotal.from_list([2,34,23,34,23])
    a.add_number(10)
    a.add_number(20)
    a.add_number(-120)
    a.add_number(300)
    
    print(a.average())
    print(a.min,a.max)
    print(b.average())
    print(b.min,b.max)
    


if __name__ == "__main__":
    main()

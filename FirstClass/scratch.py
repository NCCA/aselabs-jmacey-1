#!/usr/bin/env -S uv run --script
#
class NoAttr:
    def __init__(self):
        print(dir(self))

    def add_new(self):
        self.a = 99


a = NoAttr()
b = NoAttr()
a.add_new()
print(a.a)
a.new_attr = "dynamic attr added"
print(a.new_attr)
print(b.new_attr)

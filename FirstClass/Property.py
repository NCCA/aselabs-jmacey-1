class Person:
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self._name = name
        else:
            raise ValueError("Name needs to be a string")


me = Person("Jon")
print(me.name)

me.name = "Jonathan"
print(me.name)

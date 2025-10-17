class Person :
    def __init__(self,name : str) ->None:
        self._name = name 
    
    def get_name(self)->str:
        return self._name
        
    def set_name(self,name : str) ->None:
        if isinstance(name,str) :
            self._name = name
        else :
            raise ValueError("Name must be a string")
        
        
me = Person("Jon")
print(me.get_name())
me.set_name("Jonathan")
print(me.get_name())

me._name =324324324
print(me.get_name())
me.set_name(234)


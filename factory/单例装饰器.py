

def Singleton(cls):
    instance = {}
    def _singleton(*args,**kwargs):
        if cls not in instance:
            instance[cls] = cls(*args,**kwargs)
        return instance[cls]
    return _singleton


@Singleton
class testclass():
    def __init__(self,a):
        self.a = a

tc1 = testclass(100)
tc2 = testclass(200)

print(tc1.a)
print(tc2.a)
print(id(tc1)==id(tc2))
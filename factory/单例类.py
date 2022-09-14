


class Singleton(object):

    def __new__(cls,*arg,**kwargs):
        if not hasattr(cls,'_instance'):
            cls._instance = super(Singleton,cls).__new__(cls)
        return cls._instance


class testclass(Singleton):
    def __init__(self,a):
        self.a = a

tc1 = testclass(100)
tc2 = testclass(200)

print(tc1.a)
print(tc2.a)
print(id(tc1)==id(tc2))

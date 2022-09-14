from abc import abstractclassmethod,ABCMeta


class Payment(metaclass=ABCMeta):
    @abstractclassmethod
    def pay(self,money):
        pass

class Alipay(Payment):
    def pay(self,money):
        print(f'支付宝支付{money}元！')

class Wechat(Payment):
    def pay(self,money):
        print(f'微信支付{money}元！')

class PayFactory():
    def create_pay(self,method):
        pass

class AlipayFactory(PayFactory):
    def create_pay(self,method):
        return Alipay()

class WechatFactory(PayFactory):
    def create_pay(self,method):
        return Wechat()



# pay = AlipayFactory()
pay = WechatFactory()
branch = pay.create_pay(pay)
branch.pay(100)

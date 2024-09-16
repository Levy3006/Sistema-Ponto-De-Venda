class Calculadora:
    
    def calcular(self,num1, num2,op):
        if op == '+':
            return self.__somar(num1,num2)
        elif op == '-':
            return self.__subtrair(num1,num2)
        else:
            return 'operação inválida'
    def __somar(self, a, b):
        return a+b
    def __subtrair(self, a, b):
        return a-b
    
calculadora = Calculadora()
print(calculadora.calcular(1,2,'*'))

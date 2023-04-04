# ***EASY***

# 1. Реализовать счетчик, который будет увеличиваться каждый раз, когда у нас осуществляется запуск функции суммирования.
CNT = 0

def sum_(*args, **kwargs):
    global CNT
    CNT += 1
    return sum([*args, *kwargs.values()])

print(sum_(1,2,3), CNT)
#6 1
print(sum_(1,2,3), CNT)
#6 2
print(sum_(1,2,3), CNT)
#6 3

###################################################################################################################################

# ***MEDIUM***

# 1. Написать ещё несколько произвольных функций (3-4 штуки) и решить задачу со счетчиком аналогично той,
#    котоая была решена для запуска функции суммирования.
CNT = 0


def sum_(*args, **kwargs):
    global CNT
    CNT += 1
    return sum([*args, *kwargs.values()])


def fun1():
    global CNT
    CNT += 1
    pass


def fun2():
    global CNT
    CNT += 1
    pass


def fun3():
    global CNT
    CNT += 1
    pass


print(sum_(1,2,3), CNT)
#6 1
print(fun1(), CNT)
#None 2
print(fun2(), CNT)
#None 3
print(fun2(), CNT)
#None 4

# 2. Написать функцию, внутри которой у нас будет объявляться наша функция суммирования и возвращаться в
#    качестве результата работы из объемлющей функции.
def function():

    def sum_(*args, **kwargs):
        global CNT
        CNT += 1
        return sum([*args, *kwargs.values()])

    return sum_

# 3. Попробуйте вызвать написанную функцию и сохраните результат её работы в переменную.
#    Напечатайте результат на экран. Что наблюдаете?
print(function())
#<function function.<locals>.sum_ at 0x7f9a38d9a0c0>
# Был возвращен локальный объект - функция sum_

# 4. Осуществите вызов функции суммирования из полученной переменной.
f = function()
print(f(1,2,3))
#6

###############################################################################################################################

# ***HARD***

# 1. Перенесите глобальный счетчик на уровень объемлющей функции. Будет ли работать наш код?
#    Если да, то как поменялся смысл написанного кода? Если нет, то что надо изменить, чтобы всё заработало?
CNT = 0


def function():
    global CNT
    CNT += 1

    def sum_(*args, **kwargs):
        return sum([*args, *kwargs.values()])

    return sum_

f = function()

print(f(1,2,3))
#6
# Код работает.

#  Изменения возникли в подсчете CNT. Если в случае, когда счетчик был во внутренней функции sum_,
#  то вызов наружней фунции function() возвращал только внутренний объект - функцию sum_ и значение CNT не менялось,
#  так как функция sum_ не была выполнена, а вот с выносом счетчика CNT на уровень вверх - во внешнюю функцию function,
#  счетчик возобновил работу:

CNT = 0

def function():

    def sum_(*args, **kwargs):
        global CNT
        CNT += 1
        return sum([*args, *kwargs.values()])

    return sum_


def function1():
    global CNT
    CNT += 1

    def sum_(*args, **kwargs):
        return sum([*args, *kwargs.values()])

    return sum_

print(function(), CNT)
#<function function.<locals>.sum_ at 0x7f87d4bad480> 0
print(function1(), CNT)
#<function function1.<locals>.sum_ at 0x7f87d4bad480> 1

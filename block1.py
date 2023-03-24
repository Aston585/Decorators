# ***EASY***

# 1. Написать простую функцию, которая на вход принимает строку ('test') и целое число (3), а возвращает строку вида
# 'testTESTtest' - исходную строку, умноженную на 3, в разном регистре.
def func(string, num):
    a = [string] * num
    a[1] = a[1].upper()
    return ''.join(a)

# 2. Записать эту функцию в произвольную переменную. Напечатать эту переменную на экран. Что вы видите?
f = func('test', 3)
# print(f)
# testTESTtest

# 3. Вызвать функцию суммирования через переменную, в которую вы только что её записали
#print(f)

################################################################################################################################3

# ***MEDIUM***

# 1. Написать функцию, которая на вход будет принимать произвольное количество аргументов и возвращать их сумму.
def sum_1(*args, **kwargs):
    return sum([*args, *kwargs.values()])
#print(sum_1(1, 2, 3, a=4, b=5))
#15

# 2. В сигнатуре функции объявить 4 обязательных аргумента, но оставить возможность передавать в неё сколько угодно
# дополнительных аргументов. Попробуйте вызвать функцию в следующих ситуациях и объясните результат:
# 2.1 прокинуть в функцию только 1 аргумент
def sum_2_1(a, b, c, d, *args, **kwargs):
    return sum([a, b, c, d, *args, *kwargs.values()])
# print(sum_2_1(10))
# TypeError: sum_2_1() missing 3 required positional arguments: 'b', 'c', and 'd'
# Возникает ошибка, так как в функцию обязательно нужно передать не менее четырех аргументов.

# 2.2 прокинуть аргументы таким образом, чтобы обязательный аргумент был передан одновременно позиционно и по ключу
def sum_2_2(a, b, c, d, *args, **kwargs):
    return sum([a, b, c, d, *args, *kwargs.values()])
# print(sum_2_2(1, 2, 3, 4, a=10))
# TypeError: sum_2_2() got multiple values for argument 'a'
# Возникает ошибка (TypeError: sum_2() got multiple values for argument 'a'). Так как возникает присваивание
# аргументe 'а' двух значений 1 и 10

# 2.3 создать кортеж со значениями и распаковать его при вызове функции с помощью *
args = (1, 2, 3, 4, 5, 6, 7)
def sum_2_3(a, b, c, d, *args, **kwargs):
    return sum([a, b, c, d, *args, *kwargs.values()])
# print(sum_2_3(*args))
# 28
# Произошла распаковка переменных из кортежа и переданы в функцию , в которой стали на места по порядку сначала
# позиционных аргументов (значения: 1, 2, 3, 4), а затем остальные зашли в *numbers (значения: 5, 6, 7) став кортежем,
# который далее в теле функции был распакован.

# 2.4 создать словарь со значениями и распаковать его при вызове функции с помощью * и **: что наблюдаете? Почему?
args = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
    'f': 6,
    'g': 7
    }

# args = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}

def sum_2_4(a, b, c, d, *args, **kwargs):
    return sum([a, b, c, d, *args, *kwargs.values()])

# print(sum_2_4(*args))
# TypeError: unsupported operand type(s) for +: 'int' and 'str'
# Возникает ошибка (TypeError: unsupported operand type(s) for +: 'int' and 'str'), так как при распаковке c * берутся
# ключи, и если ключи имеют тип "строка", то будет ошибка, если ключами сделать цифры, то функция выполнится.

# print(sum_2_4(**args))
# 28
# Функция вернула правильный ответ. При распаковке ** словаря функция получает все именованные аргументы(т.е. по ключу).

##########################################################################################################################################

# ***HARD***

# 1. Модифицировать функцию таким образом, чтобы для суммирования брались только обязательные
# аргументы, первые 2 аргумента из дополнительных позиционных аргументов и любой аргумент из
# дополнительных аргументов (если они есть), переданных по ключу (если они есть).

import random

def sum_3(a, b, c, d, *args, **kwargs):
    return sum([a, b, c, d, *args[:2], random.choice([*kwargs.values()])])

print(sum_3(1,2,3,4,5,6,7,8,f=100,h=200,g=300))

assert sum_3(1,2,3,4,5,6,7,8,f=100,h=200,g=300) in (121, 221, 321)

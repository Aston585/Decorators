##############################################################################

# ***БЛОК 3***

##############################################################################

# ***ЗАДАЧА 1***

# 1.1 Написать декоратор, который перед запуском произвольной функции с
# произвольным набором аргументов будет показывать в консоли сообщение
# "Покупайте наших котиков!" и возвращать результат запущенной функции.

from functools import wraps


def deco_msg(func):

    @wraps(func)
    def inner(*args, **kwargs):
        print("Buy our cats")
        return func(*args, **kwargs)

    return inner


@deco_msg
def get_sum(*args, **kwargs):
    return sum([*args, *kwargs.values()])


print(get_sum(1, 2, 3, a = 4, b = 5))
#Buy our cats
#15

#1.2 Параметризовать декоратор таким образом, чтобы сообщение, печатаемое перед
# выполнением функции можно было задавать как параметр во время декорирования

from functools import wraps


def deco_msg(message):

    def wrapper(func):

        @wraps(func)
        def inner(*args, **kwargs):
            print(message)
            return func(*args, **kwargs)

        return inner

    return wrapper


@deco_msg(message="Evil is evil, Stregobor, lesser, greater, average - "
                  "everything is one, the proportions are conditional, and "
                  "the boundaries are blurred")
def sum1(*args, **kwargs):
    return sum([*args, *kwargs.values()])


print(sum1(1, 2, 3, a = 4, b = 5))

#Evil is evil, Stregobor, lesser, greater, average - everything is one,
#the proportions are conditional, and the boundaries are blurred

#15

###############################################################################

# ***ЗАДАЧА 2***

# 2.1 Написать декоратор, который внутри себя выполнял бы функцию и возвращал
# бы результат её работы в случае успешного выполнения. В случае возникновения
# ошибки во время выполнения функции нужно сделать так, чтобы выполнение
# функции было повторено ещё раз с теми же самыми аргументами, но не более
# 10 раз. Если после последней попытки функцию так и не удастся выполнить
# успешно, то бросать исключение.

from functools import wraps


def deco_try_to_fulfill(func):
    counter = 0

    @wraps(func)
    def inner(arg1, arg2):
        result = func(arg1, arg2)
        if not result:
            nonlocal counter
            if counter > 9:
                raise Exception("Failed to complete")
            counter += 1
            inner(arg1, arg2)
        return result

    return inner


@deco_try_to_fulfill
def predicate(first_item, second_item):
    if first_item != second_item:
        return False
    return True


print(predicate(1, 1))
#True

#print(predicate(1, 2))
#Traceback (most recent call last):
#File "<string>", line 27, in <module>
#File "<string>", line 15, in inner
#File "<string>", line 15, in inner
#File "<string>", line 15, in inner
#[Previous line repeated 7 more times]
#File "<string>", line 13, in inner
#Exception: Failed to complete

# 2.2 Параметризовать декоратор таким образом, чтобы количество попыток
# выполнения функции можно было задавать как параметр во время декорирования.

from functools import wraps


def deco_try_to_fulfill(amount_tries):

    def wrapper(func):
        counter = 0

        @wraps(func)
        def inner(arg1, arg2):
            result = func(arg1, arg2)
            if not result:
                nonlocal counter
                if counter > amount_tries - 1:
                    raise Exception("Failed to complete")
                counter += 1
                inner(arg1, arg2)
            return result

        return inner

    return wrapper


@deco_try_to_fulfill(amount_tries=5)
def predicate(first_item, second_item):
    if first_item != second_item:
        return False
    return True


print(predicate(1, 1))
#True

#print(predicate(1, 2))
#Traceback (most recent call last):
#File "<string>", line 27, in <module>
#File "<string>", line 15, in inner
#File "<string>", line 15, in inner
#File "<string>", line 15, in inner
#[Previous line repeated 7 more times]
#File "<string>", line 13, in inner
#Exception: Failed to complete

###############################################################################

# ***ЗАДАЧА 3***

# 3.1 Написать кэширующий декоратор. Суть в том, что если декорируемая функция
# будет запущена с теми параметрами с которыми она уже запускалась - брать
# результат из кэша и не производить повторное выполнение функции.

# Вопрос: почему не обнуляется cache при новом вызове функции get_sum, если
# cachе = []?

from functools import wraps


def deco_cache(func):
    cache = []

    @wraps(func)
    def inner(*args, **kwargs):
        args = [*args, *kwargs.values()]
        output = func(*args, **kwargs)
        for object in cache:
            if args == object.get('args'):
                return object.get('result'), "the cache has worked"
        cache.append({'args': args, 'result': output})
        return output, "the function has worked"

    return inner


@deco_cache
def get_sum(*args, **kwargs):
    return sum([*args, *kwargs.values()])


print(get_sum(1, 2))
print(get_sum(1, 2))
print(get_sum(1, 2, 3))
print(get_sum(1, 2))
print(get_sum(1, 2, 3))
print(get_sum(1, 2, 3, 4, 5))


#(3, 'the function has worked')
#(3, 'the cache has worked')
#(6, 'the function has worked')
#(3, 'the cache has worked')
#(6, 'the cache has worked')
#(15, 'the function has worked')


# 3.2 Сделать так, чтобы информация в кэше была актуальной не более 10 секунд.
# Предусмотреть механизм автоматической очистки кэша в процессе выполнения
# функций.

from time import time, sleep
from functools import wraps


def deco_cache(func):
    cache = []

    @wraps(func)
    def inner(*args, **kwargs):
        args = [*args, *kwargs.values()]
        output = func(*args, **kwargs)
        if not cache:
            cache.append({'timestamp': time()})
        for object in cache:
            if 'timestamp' in object:
                if time() - object.get('timestamp') > 10.0:
                    cache.clear()
                    break
            if args == object.get('args'):
                return object.get('result'), "the cache has worked"
        cache.append({'args': args, 'result': output})
        return output, "the function has worked"

    return inner


@deco_cache
def get_sum(*args, **kwargs):
    return sum([*args, *kwargs.values()])


print(get_sum(1, 2))
print(get_sum(1, 2))
sleep(12)
print(get_sum(1, 2))

#(3, 'the function has worked')
#(3, 'the cache has worked')
#(3, 'the function has worked')

# 3.3 Параметризовать время кэширования в декораторе.
from time import time, sleep
from functools import wraps


def deco_cache(cache_lifetime):

    def wrapper(func):
        cache = []

        @wraps(func)
        def inner(*args, **kwargs):
            args = [*args, *kwargs.values()]
            output = func(*args, **kwargs)
            if not cache:
                cache.append({'timestamp': time()})
            for object in cache:
                if 'timestamp' in object:
                    if time() - object.get('timestamp') > cache_lifetime:
                        cache.clear()
                        break
                if args == object.get('args'):
                    return object.get('result'), "the cache has worked"
            cache.append({'args': args, 'result': output})
            return output, "the function has worked"

        return inner

    return wrapper


@deco_cache(cache_lifetime=10)
def get_sum(*args, **kwargs):
    return sum([*args, *kwargs.values()])


print(get_sum(1, 2))
print(get_sum(1, 2))
sleep(12)
print(get_sum(1, 2))

#(3, 'the function has worked')
#(3, 'the cache has worked')
#(3, 'the function has worked')

###############################################################################

# ***ЗАДАЧА 4***

# 4.1 Написать декоратор, который бы измерял время работы функции и
# печатал бы его на экран.

from time import time
from functools import wraps


def deco_work_time(func):

    @wraps(func)
    def inner(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        work_time = time() -  start_time
        print(f"Function running time: {work_time}")
        return result

    return inner


@deco_work_time
def get_sum(*args, **kwargs):
    return sum([*args, *kwargs.values()])

print(get_sum(1, 2))
#Function running time: 2.384185791015625e-06
#3

# 4.2 Доработать декоратор таким образом, чтобы в логах было название
# запускаемой функции помимо времени исполнения.

from time import time
from functools import wraps


def deco_work_time(func):

    @wraps(func)
    def inner(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        work_time = time() -  start_time
        name_func = func.__name__
        print(f"Function '{name_func}' running time: {work_time}")
        return result

    return inner


@deco_work_time
def get_sum(*args, **kwargs):
    return sum([*args, *kwargs.values()])

print(get_sum(1, 2))
#Function 'get_sum' running time: 3.814697265625e-06
#3

#4.3 Доработать декоратор так, чтобы запись лога для функции велась в файл,
# путь к которому нужно было бы задавать во время декорирования, как параметр.

from time import time
from functools import wraps


def deco_work_time(path_to_log):

    def wrapper(func):

        @wraps(func)
        def inner(*args, **kwargs):
            start_time = time()
            result = func(*args, **kwargs)
            work_time = time() -  start_time
            name_func = func.__name__
            info = f"Function '{name_func}' running time: {work_time}"
            with open('log.txt', 'a') as log:
                log.write(info)
            print(info)
            return result

        return inner

    return wrapper


@deco_work_time(path_to_log='./path/to/log')
def get_sum(*args, **kwargs):
    return sum([*args, *kwargs.values()])

print(get_sum(1, 2))

###############################################################################

# ***ЗАДАЧА 5***
# После решения задач написать функцию и задекорировать её сразу несколькими из
# созданных декораторов и посмотреть на результат и суметь объяснить его.
# Потом поменять порядок декорирования и проделать то же самое.

from time import time, sleep
from functools import wraps


def deco_msg(func):

    @wraps(func)
    def inner(*args, **kwargs):
        sleep(.3)
        result = func(*args, **kwargs)
        print("Buy our cats")
        return result

    return inner


def deco_work_time(func):

    @wraps(func)
    def inner(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        work_time = time() -  start_time
        name_func = func.__name__
        print(f"Function '{name_func}' running time: {work_time}")
        return result

    return inner


#@deco_msg
@deco_work_time
@deco_msg
def get_sum(*args, **kwargs):
    sleep(.2)
    return sum([*args, *kwargs.values()])

print(get_sum(1, 2))

# 1. Декорирую в таком порядке:
# @deco_work_time
# @deco_msg

# Результат:
#Buy our cats
#Function 'get_sum' running time: 0.5014991760253906
#3

#Объяснение:
# Так как декоратор deco_work_time является внешним, то на его вход принимается
# агрумент func - нижележащая функция deco_msg.inner. Выполнение
# кода начинается последовательно с внутренней функции deco_work_time.inner
# (строка 429): будет получено значение start_time, далее при получении значения
# переменной result будет вызвана внутренняя функция deco_msg.inner, для
# которой func = get_sum: выполнится функция sleep(0.3), далее интерпретатор
# начнет получать значение result, и вызовет функцию get_sum с аргументами 1,2,
# которые пробрасывались через все функции-декораторы как бы сверху вниз, вглубь.
# Далее отработает sleep(0.2) и в переменную result функции deco_msg.inner
# запишется значение '3' (строка 418) (то есть вернется результат работы функции
# get_sum), продолжится последовательное ввыполнение кода сверху вниз: выведется
# на экран сообщение про котиков и в функцию deco_work_time.inner в значение
# переменной result вернется значение '3' (строка 430).
# Далее последовательное выполнение: получение значения переменной
# work_time, получение значение переменной name_func, вывод на экран общее время
# работы функции get_sum (так как был использован декоратор wraps) и deco_work,
# окончание работы программы - возврат значения '3' и печать его на экран.

# По сути аргументы 1,2 прокидываются сверху вниз, до функции, где они будут
# использованы, а вызов функций происходит последовательно снизу вверх,
# как бы проваливаясь во внутрь к самой изначальной функции, которую декорируем,
# чтобы вернуть значение и протащив наверх через декораторы вернуть вычисленное
# значение (очень напоминает рекурсивный процесс) попутно выполняя принты
# сообщений (в данном примере).

# 2. Декорирю теперь так:
# @deco_msg
# @deco_work_time

# Результат:
#Function 'get_sum' running time: 0.20014667510986328
#Buy our cats
#3

#Объяснение:
# Процесс аналогичен, за тем ислючением, что принты будут выводится с той
# последовательностью, с которой будут получены значения переменных result
# внутренних функций deco_msg и deco_work_time
# В любом случае результат работы функции get_sum будет выведен последним.

###############################################################################

# ***ЗАДАЧА 6***

# 6.1 Написать декоратор, который будет запрашивать у пользователя пароль при
# попытке функции осуществить вызов. Если введён верный пароль, то функция
# будет выполнена и вернется результат её работы. Если нет - в консоли
# появляется соответствующее сообщение.

from functools import wraps


def deco_chek_user_pass(func):

    @wraps(func)
    def inner(*args, **kwargs):
        pass_user = input("Input password: ")
        correct_pass = '1234'
        if pass_user == correct_pass:
            return func(*args, **kwargs)
        return "Incorrect password"

    return inner


@deco_chek_user_pass
def get_sum(*args, **kwargs):
    return sum([*args, *kwargs.values()])

print(get_sum(1, 2))

#Input password: 1234
#3

# 6.2 Параметризовать декоратор таким образом, чтобы можно было задавать
# индивидуальный пароль для каждой декорируемой функции

from functools import wraps

def deco_chek_user_pass(correct_pass):

    def wrapper(func):

        @wraps(func)
        def inner(*args, **kwargs):
            pass_user = input("Input password: ")
            if pass_user == correct_pass:
                return func(*args, **kwargs)
            return "Incorrect password"

        return inner

    return wrapper


@deco_chek_user_pass(correct_pass='qwerty')
def get_sum(*args, **kwargs):
    return sum([*args, *kwargs.values()])


print(get_sum(1, 2))

##############################################################################

# ***ЗАДАЧА 7***

# 7.1 Написать декоратор, который после выполнения функции будет возвращать
# результат и записывать его в текстовый файл

from functools import wraps


def deco_result_to_file(func):

    @wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        with open('result.txt', 'a') as r:
            r.write(f"{result}")
        return result

    return inner


@deco_result_to_file
def get_sum(*args, **kwargs):
    return sum([*args, *kwargs.values()])

print(get_sum(1, 2))

# 7.2 Модернизировать декоратор таким образом, чтобы можно было не только
# осуществлять запись в файл, но и в целом производить любую операцию
# логирования или оповещения.

from functools import wraps


def notification_to_email(arg=None):
    print("Email notification sent")
    pass


def notification_to_telegram(arg=None):
    print("Telegram notification sent")
    pass


def notification_to_sms(arg):
    print(f"SMS notification 'result = {arg}' sent")
    pass


def deco_notificator(func):

    @wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        with open('result.txt', 'a') as r:
                r.write(f"{result}")
        notification_to_email()
        notification_to_telegram()
        notification_to_sms(result)
        return result

    return inner


@deco_notificator
def get_sum(*args, **kwargs):
    return sum([*args, *kwargs.values()])

print(get_sum(1, 2))

#Email notification sent
#Telegram notification sent
#SMS notification 'result = 3' sent
#3

# 7.3 Доработать декоратор таким образом, чтобы можно было при декорировании
# можно было передавать список нотификаторов.

from functools import wraps


def notification_to_email(arg=None):
    print("Email notification sent")
    pass


def notification_to_telegram(arg=None):
    print("Telegram notification sent")
    pass


def notification_to_sms(arg):
    print(f"SMS notification 'result = {arg}' sent")
    pass


notificators_list1 = (notification_to_email,
                      notification_to_telegram,)

notificators_list2 = (notification_to_telegram,)

notificators_list3 = (notification_to_email,
                      notification_to_telegram,
                      notification_to_sms,)


def deco_notificator(notificator):

    def wrapper(func):

        @wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            with open('result.txt', 'a') as r:
                r.write(f"{result}")
            for action in notificator:
                action(result)
            return result

        return inner

    return wrapper


@deco_notificator(notificator=notificators_list3)
def get_sum(*args, **kwargs):
    return sum([*args, *kwargs.values()])

print(get_sum(1, 2))

# Создание файла result.txt, запись в него значения result
# Вывод в консоли:
#Email notification sent
#Telegram notification sent
#3

# ***Для notificator=notificators_list2***
# Дозапись значения result в конец строки файла result.txt
# Вывод в консоли:
#Telegram notification sent
#3

# ***Для notificator=notificators_list3***
# Дозапись значения result в конец строки файла result.txt
# Вывод в консоли:
#Email notification sent
#Telegram notification sent
#SMS notification 'result = 3' sent
#3

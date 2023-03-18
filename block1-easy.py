def func(string, num):
    a = [string] * num
    a[1] = a[1].upper()
    return ''.join(a)


f = func('test', 3)


print(f)

# На экране вижу: testTESTtest

f

def S(n):
    num = 0
    for c in str(n):
        num += int(c)
    return num

def norm(n):
    return n / S(n)

k = int(input())
j = 1
order = 1
for i in range(k):
    print(j) #, norm(j))
    if norm(j + 10 ** (order - 1)) > norm(j + 10 ** (order)):
        order += 1
    j += 10 ** (order - 1)

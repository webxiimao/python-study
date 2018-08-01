#如果a+b+c = 1000,且a^2+b^2=c^2 如何求出a,b,c的所有组合
#1.枚举法
# a = 0
# b = 0
# c = 0
# for a in range(0,1001):
#     for b in range(0,1001):
#         for c in range(0,1001):
#             if a+b+c ==1000:
#                 if a*a + b*b == c*c:
#                     print(a,b,c)


for a in range(0, 1001):
    for b in range(0, 1001):
        c = 1000 - a - b
        if a**2 + b**2 == c**2:
            print(a,b,c)




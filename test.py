a = [9,8,7,6,5,4,3,2,1,0]
b = a[:5]
c = a[5:]
print a
print b
print c
c.append('a')
print a
print b
print c
for i in range(5):
    print a[0]
    a.pop(0)
print a
d = {3:'a',2:'b',1:'c'}
d.pop(1)
print d
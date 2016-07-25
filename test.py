# -*- coding=utf-8 -*-
# a = [9,8,7,6,5,4,3,2,1,0]
# b = a[:5]
# c = a[5:]
# print a
# print b
# print c
# c.append('a')
# print a
# print b
# print c
# for i in range(5):
#     print a[0]
#     a.pop(0)
# print a
# d = {3:'a',2:'b',1:'c'}
# d.pop(1)
# print d
s = '\\230\\147\\141'
print type(s)
t = ''
for e in s.split('\\')[1:]:
    print e
    t += int(e).__hex__()
print len(t)
print t
a = 230
print a.__hex__()
b = 147
print b.__hex__()
c = 141
print c.__hex__()
m = '\xe6\x93\x8d'
print t
print len(t)
print m
print len(m)
print t==m
print m.decode('utf-8')
#!/bin/python

nums = [0,0,1,1,1,2,2,3,3,4]

res = [*set(nums)]
print(res)
print (len([*set(nums)]))
res2 = f"{len(res)}, {res}"
print( res2)
#!/usr/bin/python
# -*- coding: utf-8 -*-

# AUTHOR: Renan Cakirerk <public at cakirerk.org>
# QUESTION: http://www.careercup.com/question?id=12986664 
#           Push all the zero's of a given array to the end of the array. In place only. Ex 1,2,0,4,0,0,8 becomes 1,2,4,8,0,0,0

arr = [0, 0, 1, 2, 0, 4, 0, 0 ,8 ,9]
pos = 0

for i in range(len(arr)):
    if arr[i] != 0:
        arr[pos] = arr[i]
        pos += 1

for i in reversed(range(pos, len(arr))):
    arr[i] = 0

print arr

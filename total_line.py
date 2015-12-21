#!/usr/bin/env python
#coding=utf-8
__author__ = 'reelai'
__mtime__ = '2015/7/20'
import os
import  sys
if __name__ == '__main__':
    total_line=0
    if len(sys.argv) !=2:
        print 'Usage: python ./total_line.py ROOT_PATH'
        exit(1)
    for root_path,d,files in os.walk(sys.argv[1]):
        total_line +=reduce(lambda x,y:x+y,[ len(open(os.path.join(root_path,f)).readlines()) for f in files if f.endswith(('.py','.xml'))],0)
    print total_line,"lines."


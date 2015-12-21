#!/usr/bin/python

import os
import sys


def findstr(rootpath,string_target,ext_name):
    for dirpath,dirnames,files in os.walk(rootpath):
        for f in files:
            if f.endswith(ext_name):
                fname = os.path.join(dirpath,f)
                with open(fname) as fp:
                    for index,l in enumerate(fp):
                        if string_target in l:
                            print "Find at [%s:Line%d]"%(fname,index)
                            print "-------->%s"%l

    # for dirpath,dirnames,files in os.walk(rootpath):
    #     for fname in [os.path.join(dirpath,f) for f in files if f.endswith(ext_name)]:
    #         with open(fname) as fp:
    #             for index,l in enumerate(fp):
    #                 if string_target in l:
    #                     print "%s ===>Find At %s:Line%d"%(l,fname,index)




if __name__=='__main__':
    if len(sys.argv) <3:
        print "Usage %s DIR_PATH STRING [EXT_NAME] "%sys.argv[0]
        sys.exit(1)
    elif len(sys.argv) == 3:
        dir_path = sys.argv[1]
        string_target = sys.argv[2]
        ext_name = ""
    else:
        dir_path = sys.argv[1]
        string_target = sys.argv[2]
        ext_name = sys.argv[3]
    print "Search [%s] in [%s] according [*%s]"%(string_target,dir_path,ext_name)
    print "================================="
    findstr(dir_path,string_target,ext_name)
    print "================================="




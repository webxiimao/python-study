# -*- coding: utf-8 -*
import os
import re
import chardet

def get_all_filsname():
    for root,dirs,fils in os.walk(os.getcwd()):
        for file in fils:

            if file.endswith('.py'):
                # print(chardet.detect(file))
                # print(type(file))

                start_name = re.match(r'(\w+).(\w+)*',file).group(1)
                end_name = re.match(r'(\w+).(\w+)*',file).group(2)
                print(re.match(r'(\w+).(\w+)*',file).group(1))
                # os.rename('11.py','33.html')
                os.rename(file,start_name+".html")





if __name__ == '__main__':
    get_all_filsname()
# -*- coding: utf-8 -*-

import os
import re

homepath=os.path.expanduser('~')



def clean_arenthesis(text,duplication=True):
    text=re.sub('【.+?】',"",text)
    text=re.sub('＼.+?／',"",text)
    text=re.sub('[.+?]', "", text)
    text=re.sub('＜.+?＞', "", text)
    text=re.sub('≪.+?≫', "", text)
    return text

def test():
    with open(homepath+'/_dip/data/adjust/posting_info_baitoru_text.txt','r') as fr:
        for line in fr.readlines():
            text=clean_arenthesis(line)
            print(text)


if __name__ == '__main__':
    test()
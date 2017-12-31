from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib import parse

import random
from html.parser import HTMLParser
from tqdm import *
from time import *
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import multiprocessing
from multiprocessing import Process


cpu_num = multiprocessing.cpu_count()
read = 'p5_lp0.txt'
write = 'p5_lp0_r.txt'

# text_file = open("p5_lp0.txt", "r")
txt = open('p5_lp0_r.txt', 'w')


def renew_name(read=read, write=write, core_num=cpu_num, core=0):
    read = open(read, "r")
    summoners = read.readlines()

    num_summoners = len(summoners)

    share = num_summoners // core_num + 1
    cut = []
    for i in range(core_num):
        cut.append(share * i)

    print(cut)
    cut.append(num_summoners)

    start = cut[core]
    end = cut[core + 1]
    print(start, end)

    # launch browser
    browser = webdriver.Chrome('/Users/minki/Development/boostdetect/chromedriver')

    for s in tqdm(summoners[start:end]):
        # for s in summoners:
        if s[:-1] != '취소':
            summoner = s[:-1]

            # for test
            #     if summoner == '우잉짱':
            url = 'http://lol.inven.co.kr/dataninfo/player/list.php?sname=' + summoner
            url = str(url.encode('utf-8'))
            url = url.replace('\\x', '%')[2:-1]

            browser.get(url)
            sleep(10)

            try:
                name = browser.find_elements_by_class_name("iname")[0]
                rating = browser.find_elements_by_class_name("rating")[0]

                name = name.get_attribute('innerHTML')
                rating = rating.get_attribute('innerHTML')

                if rating.find('플래티넘 5') == 1:
                    with open(write, 'a') as txt:
                        txt.write(name)
                        txt.write('\n')

            except:
                sleep(5)
                try:
                    alert = browser.switch_to_alert()
                    alert.accept()
                except:
                    pass

                sleep(30)
                pass

    browser.close()


def renew_name_tot(read=read, write=write, core_num=cpu_num):
    if core_num > multiprocessing.cpu_count():
        print('lack CPUs')
        return

    # multi-processing
    procs = []
    for i in range(core_num):
        procs.append(Process(target=renew_name, args=(read, write, core_num, i)))

    for p in procs:
        p.start()



# Execution
renew_name_tot(core_num=2)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thursday Jul 4 15:43:00 2019

@author: kevin
"""
from urllib import request

import bs4
import os
import logging

from pathlib import Path

from article_scrap.ass_article import log as ass_log
from article_scrap.ass_article import JasssArticle
from article_scrap.ass_scrap_util import doi_converter

logging.basicConfig()
log = logging.getLogger("ass.jasss_mining")
log.setLevel(logging.WARNING)
ass_log.setLevel(logging.DEBUG)

url_JASSS = "http://jasss.soc.surrey.ac.uk/index_by_issue.html"
req_text = request.urlopen(url=url_JASSS).read()

page = bs4.BeautifulSoup(req_text, "lxml")

itr: int = 0

tp = Path(os.getcwd()+"/data/")

for gen in page.findAll("p", {'class': 'item'}):
    itr += 1
    url_article = gen.find("a")['href']
    log.info(str(itr)+" => "+url_article)
    article = JasssArticle(url=url_article)

    if article.is_review():
        continue
    
    res_file = str(tp)+"/JASSS_" + doi_converter(article.doi()) + ".txt"
    log.info(res_file)
    os.makedirs(os.path.dirname(res_file), exist_ok=True)

    article.save(res_file)
    if (itr % 1) == 0:
        inp = input("Type 'c' button to continue 'e' to exit")
        exit(0) if inp == 'e' else log.info("Carry on")

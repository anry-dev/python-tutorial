#!/usr/bin/env python

from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

#assert 'Django' in browser.title
assert 'worked' in browser.title

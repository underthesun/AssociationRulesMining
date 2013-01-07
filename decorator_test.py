#/usr/bin/env python
#-*- coding: UTF-8 -*-
#__author__ = 'shuai'

def eat(fun):
    def living():
        fun()
        print 'living is to eat'
    return living

def sleep(fun):
    def living():
        fun()
        print 'living also include sleep'
    return living

@sleep
@eat
def whatIsLiving():
    print 'what the fucking is living'

whatIsLiving()
def func(*args, **kwargs):
    for arg in args:
        print arg
    for key in kwargs.keys():
        print kwargs[key]

func(1,2,3,a=5, b=6)


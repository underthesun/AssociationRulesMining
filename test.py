#!/usr/bin/env python
__author__ = 'shuai'

#import matplotlib.pyplot as plt
#import numpy as np
#
#x = np.arange(0, 5, 0.1)
#y = np.sin(x)
#plt.plot(x, y)
#plt.show()

def f():
    print 'f'

def ff():
    f()
    fff()
    print 'ff'

def fff():
    print 'fff'

ff()
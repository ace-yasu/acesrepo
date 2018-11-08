import numpy as np
x = np.array([])
y = np.array([])
"以下の作業でデータの中心化を行う　中心化はｘ－ｘの平均、ｙ－ｙの平均である"
x = x.mean()
y = y.mean()
xc = x - x.mean()
yc = y - y.mean()

xx = xc*xc
xy = xx*yc

xx.sum()
xy.sum()

a = xy.sum()/xx.sum()

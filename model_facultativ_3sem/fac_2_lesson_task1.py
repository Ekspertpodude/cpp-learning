import matplotlib.pyplot as plt
import math
import numpy as np
phi_0 = np.pi* 0
a = 1
b = 3

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(10, 4))
t = np.linspace(-100, 1 * np.pi, 1000)
print (t)
f_1 = np.sin(phi_0 + a*t)
f2 = np.cos (b*t)
print(f_1,f2)
ax[0,0].plot(f2,f_1, label = 'Синус первый')

plt.show()

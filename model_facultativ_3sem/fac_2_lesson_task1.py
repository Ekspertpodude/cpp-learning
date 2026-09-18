import matplotlib.pyplot as plt
import math
import numpy as np
a = 2
b = 3
c = 1
d = 2 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 4))
ax[0].set_aspect('equal')
ax[1].set_aspect('equal')
t = np.linspace(0, 4 * np.pi, 1000)
print (t)
f1 = np.sin( a*t)
f2 = np.sin (b*t)
f3 = np.sin( c*t)
f4 = np.sin(d*t)
print(f1,f2)
ax[0].plot(f1,f2, label = 'Фигура 1')
ax[0].set_title(rf'Фигура 1: $ \frac{{F_x}}{{F_y}} = \frac {{{a}}}{{{b}}}$', fontsize=14, pad=10) # Заголовок
ax[0].set_xlabel('F_x', fontsize=11)                 # Подпись оси X
ax[0].set_ylabel('F_y', fontsize=11)   


ax[1].plot(f3 , f4 , label = 'Фигура 2')
ax[1].set_title(rf'Фигура 2: $ \frac{{F_x}}{{F_y}} = \frac {{{c}}}{{{d}}}$', fontsize=14, pad=10) # Заголовок
ax[1].set_xlabel('F_x', fontsize=11)                 # Подпись оси X
ax[1].set_ylabel('F_y', fontsize=11)  
ax[0].grid()
ax[1].grid()


plt.show()

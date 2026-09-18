import matplotlib.pyplot as plt
import math
import numpy as np
a = 21
b = 20
c = 37
d = 38
fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))
ax[0][0].set_aspect('equal')
ax[1][0].set_aspect('equal')
t = np.linspace(0, 4 * np.pi, 100000)

print (t)
f1 = np.sin( a*t)
f2 = np.sin (b*t)
f3 = np.sin( c*t)
f4 = np.sin(d*t)

f1_round = np.round(f1 , decimals= 2)

f2_round = np.round(f2 , decimals= 2)

f3_round = np.round(f3 , decimals= 2)

f4_round = np.round(f4 , decimals= 2)

points_fig1 = np.column_stack((f1_round, f2_round))
points_fig2 = np.column_stack((f3_round , f4_round))
unique_points_fig1 , count_fig1 = np.unique(points_fig1 ,axis=0, return_counts= True)
unique_points_fig2 , count_fig2 = np.unique(points_fig2 , axis=0 , return_counts= True)

intersections_fig1 = unique_points_fig1[count_fig1 > 1]
intersections_fig2 = unique_points_fig2[count_fig2 > 1]



ax[0][0].plot(f1,f2, label = 'Фигура 1')
ax[0][0].set_title(rf'Фигура 1: $ \frac{{F_x}}{{F_y}} = \frac {{{a}}}{{{b}}}$', fontsize=14, pad=10) # Заголовок
ax[0][0].set_xlabel('F_x', fontsize=11)                 # Подпись оси X
ax[0][0].set_ylabel('F_y', fontsize=11)   



ax[0][1].hist(intersections_fig1[: , 0], bins=200, color='orange', edgecolor='black')
ax[0][1].set_title('Гистограмма распределения X-координат узлов фигуры 1')
ax[0][1].set_xlabel('X координата')
ax[0][1].set_ylabel('Количество пересечений (узлов)')

ax[1][0].plot(f3 , f4 , label = 'Фигура 2')
ax[1][0].set_title(rf'Фигура 2: $ \frac{{F_x}}{{F_y}} = \frac {{{c}}}{{{d}}}$', fontsize=14, pad=10) # Заголовок
ax[1][0].set_xlabel('F_x', fontsize=11)                 # Подпись оси X
ax[1][0].set_ylabel('F_y', fontsize=11)  
ax[0][0].grid()
ax[1][0].grid()
ax[1][1].hist(intersections_fig2[: , 0], bins=1000, color='green', edgecolor='black')
ax[1][1].set_title('Гистограмма распределения X-координат узлов фигуры 2')
ax[1][1].set_xlabel('X координата')
ax[1][1].set_ylabel('Количество пересечений (узлов)')
plt.tight_layout() 
plt.show()

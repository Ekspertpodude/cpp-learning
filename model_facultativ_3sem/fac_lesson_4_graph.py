    import matplotlib.pyplot as plt
    import math
    import numpy as np
    import os
    import subprocess

    def search_ampl (arr , args): 
        w = args[4]
        step = float(args[0])
        double_T = 4 * np.pi / float(w)
        num_of_steps = int(double_T / step + 1)
        ampl = []
        t = []
        for i in range(0 , len(arr) - num_of_steps + 1):
            Oscilation = arr[i : i + num_of_steps]
            ampl_part = max(Oscilation)
            ampl.append(ampl_part)
            t.append(step * i)
        ampl= np.array(ampl)
        return t , ampl




    cpp_file = "fac_lesson4_sem.cpp"
    executable = "C:\\Roman\\MIPT\\C_plus_plus\\model_facultativ_3sem\\fac_lesson4_sem.exe" 

    compile_command = ["g++", cpp_file, "-o", executable]
    compile_result = subprocess.run(compile_command, capture_output=True, text=True)

    #step , x_0,v_0,T , w
    args = ["0.001", "1", "0", "10", "20"]
    run_result = subprocess.run([executable]  + args , capture_output=True, text=True)

    with  open ("Data_oscilator_Eiler", "r") as data:
        lines = data.readlines()[3:]    
        t_x, x_x, v_x = np.loadtxt(lines, unpack=True)
        
    with  open ("Data_oscilator_XOINA", "r") as data:
        lines = data.readlines()[3:]    
        t, x, v = np.loadtxt(lines, unpack=True) 
        
    ampl = []
    ampl_h = []
    t_x = np.array(t_x)
    x_x = np.array(x_x)
    v_x = np.array(v_x)
    t = np.array(t)
    x = np.array(x)
    v = np.array(v)
    w = args[4]

    ampl_x_eyl = search_ampl(x_x , args)
    ampl_x_h = search_ampl(x,args)
    ampl_v_eyl = search_ampl(v_x,args)
    ampl_v_h = search_ampl(v,args)

    ln_ampl_x_eyl = np.log(ampl_x_eyl)
    ln_ampl_x_h = np.log(ampl_x_h)
    ln_ampl_v_eyl = np.log(ampl_v_eyl)
    ln_ampl_v_h = np.log(ampl_v_h)
    ln_t = np.log (t_x[1:] )
    fig, ax = plt.subplots(nrows=2, ncols=6, figsize=(10, 10))
    ax[0][0].plot (t_x , x_x ,label = 'X(t) - Method Eiler')  
    ax[0][0].set_title('X(t) - Method Eiler', fontsize=14, pad=10) # Заголовок
    ax[0][0].set_xlabel('t, c', fontsize=11)                 # Подпись оси X
    ax[0][0].set_ylabel('x , м', fontsize=11)  
    ax[1][0].plot (t_x , v_x ,label = 'X(t)')  
    ax[1][0].set_title('v (t) -  - Method Eiler', fontsize=14, pad=10) # Заголовок
    ax[1][0].set_xlabel('t, c', fontsize=11)                 # Подпись оси X
    ax[1][0].set_ylabel('v , м/c', fontsize=11)


    ax[0][1].plot (t , x ,label = 'X(t) - Method Xoina')  
    ax[0][1].set_title('X(t) - Method Xoina', fontsize=14, pad=10) # Заголовок
    ax[0][1].set_xlabel('t, c', fontsize=11)                 # Подпись оси X
    ax[0][1].set_ylabel('x , м', fontsize=11)  
    ax[1][1].plot (t , v ,label = 'X(t)')  
    ax[1][1].set_title('v (t) -  - Method Xoina', fontsize=14, pad=10) # Заголовок
    ax[1][1].set_xlabel('t, c', fontsize=11)                 # Подпись оси X
    ax[1][1].set_ylabel('v , м/c', fontsize=11)


    ax[0][2].plot (ampl_x_h[0], ampl_x_h[1] ,label = 'X(t) - Method Xoina')  
    ax[0][2].set_title('Ampl_X(t) - Method Xoina', fontsize=14, pad=10) # Заголовок
    ax[0][2].set_xlabel('t, c', fontsize=11)                 # Подпись оси X
    ax[0][2].set_ylabel('A , м', fontsize=11)  
    ax[1][2].plot (ampl_v_h[0] , ampl_v_h[1] ,label = 'X(t)')  
    ax[1][2].set_title('Ampl_v (t) -  - Method Xoina', fontsize=14, pad=10) # Заголовок
    ax[1][2].set_xlabel('t, c', fontsize=11)                 # Подпись оси X
    ax[1][2].set_ylabel('A , м/c', fontsize=11)


    ax[0][3].plot (ampl_x_eyl[0] , ampl_x_eyl[1] ,label = 'Ampl_x - Method Eiler')  
    ax[0][3].set_title('Ampl_x(t) - Method Eiler', fontsize=14, pad=10) # Заголовок
    ax[0][3].set_xlabel('t, c', fontsize=11)                 # Подпись оси X
    ax[0][3].set_ylabel('A , м', fontsize=11)  
    ax[1][3].plot (ampl_v_eyl[0] , ampl_v_eyl[1] ,label = 'Aml_v(t)')  
    ax[1][3].set_title('Ampl_v (t) -  - Method Eiler', fontsize=14, pad=10) # Заголовок
    ax[1][3].set_xlabel('t, c', fontsize=11)                 # Подпись оси X
    ax[1][3].set_ylabel('A , м/c', fontsize=11)

    ax[0][4].plot (ln_ampl_x_eyl[0] , ln_ampl_x_eyl[1] ,label = 'Ampl_x - Method Eiler')  
    ax[0][4].set_title('ln_Ampl_x(t) - Method Eiler', fontsize=14, pad=10) # Заголовок
    ax[0][4].set_xlabel('ln(t), c', fontsize=11)                 # Подпись оси X
    ax[0][4].set_ylabel('ln(A) , м', fontsize=11)  
    ax[1][4].plot (ln_ampl_v_eyl[0] , ln_ampl_v_eyl[1] ,label = 'Aml_v(t)')  
    ax[1][4].set_title('ln_Ampl_v (t) -  - Method Eiler', fontsize=14, pad=10) # Заголовок
    ax[1][4].set_xlabel('ln(t), c', fontsize=11)                 # Подпись оси X
    ax[1][4].set_ylabel('ln(A) , м/c', fontsize=11)




    ax[0][5].plot (ln_ampl_x_h[0], ln_ampl_x_h[1] ,label = 'X(t) - Method Xoina')  
    ax[0][5].set_title('ln_Ampl_X(t) - Method Xoina', fontsize=14, pad=10) # Заголовок
    ax[0][5].set_xlabel('ln(t), c', fontsize=11)                 # Подпись оси X
    ax[0][5].set_ylabel('ln(A) , м', fontsize=11)  
    ax[1][5].plot (ln_ampl_v_h[0] , ln_ampl_v_h[1] ,label = 'X(t)')  
    ax[1][5].set_title('ln_Ampl_v (t) -  - Method Xoina', fontsize=14, pad=10) # Заголовок
    ax[1][5].set_xlabel('ln(t), c', fontsize=11)                 # Подпись оси X
    ax[1][5].set_ylabel('ln(A) , м/c', fontsize=11)


    plt.tight_layout() 
    plt.show()

    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(10, 10))

    ax[0][0].plot ( x_x , v_x,label = 'Phas_diagram - Method Eiler',color = 'r')  
    ax[0][0].set_title('Phas_diagram - Method Eiler', fontsize=14, pad=10 , color = 'r') # Заголовок
    ax[0][0].set_xlabel('x, м', fontsize=11)                 # Подпись оси X
    ax[0][0].set_ylabel('v , м/c', fontsize=11)  
    ax[0][0].plot (x , v ,label = 'X(t)')  
    ax[0][0].set_title('Phas_diagram - Method Hoina ', fontsize=14, pad=10) # Заголовок
    ax[0][0].set_xlabel('x, м', fontsize=11)                 # Подпись оси X
    ax[0][0].set_ylabel('v , м/c', fontsize=11)


    ax[0][1].plot (t , x ,label = 'X(t) - Method Xoina')  
    ax[0][1].set_title('X(t) - Method Xoina', fontsize=14, pad=10) # Заголовок
    ax[0][1].set_xlabel('t, c', fontsize=11)                 # Подпись оси X
    ax[0][1].set_ylabel('x , м', fontsize=11)  
    ax[1][1].plot (t , v ,label = 'X(t)')  
    ax[1][1].set_title('v (t) -  - Method Xoina', fontsize=14, pad=10) # Заголовок
    ax[1][1].set_xlabel('t, c', fontsize=11)                 # Подпись оси X
    ax[1][1].set_ylabel('v , м/c', fontsize=11)



    plt.tight_layout() 
    plt.show()








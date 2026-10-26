#include <iostream>
#include <float.h>
#include <math.h>
#include <fstream>

double f(double w , double x){
    return -w*w*x ;
}

int main(int argc, char *argv[]) {
    if (argc < 5){
    std::cout << "Incorrect input; Please write " << std::endl;
}
    double step = std::stod(argv[1]);
    double x_0 = std::stod(argv[2]);
    double v_0 = std::stod(argv[3]);
    double T = std::stod(argv[4]);
    double w = std::stod(argv[5]);
    double x_0_copy = x_0;
    double v_0_copy = v_0;
    double x_0_1 = x_0;
    double v_0_1 = v_0;
      std::ofstream out;
      std::ofstream out1;
      std::ofstream out2;
    out.open("Data_oscilator_Eiler");
    if (out.is_open()){ 

     out << "My  Initial data:_METHOD EILER" << std::endl;
     out <<"STEP = " << step <<" X_ 0 = " << x_0 << " V_0 = " << v_0 << " W = " << w << " T =  " << T << std::endl;
     out << "t"<< " Coordinates_x " << " Velocity " << std::endl ;
     

     for (double t = 0; t < T ; t = t + step){
        std:: cout << "t = "<< t << "Coordinate_x = " << x_0 << " Velocity = " << v_0 << std::endl ;
        out << t <<'\t' << x_0 << '\t'<< v_0 << std::endl ;
        double a = f(w , x_0);
        double x = x_0 + v_0 * step;
        double v = v_0 + a * step;
        x_0 = x;
        v_0 = v;
    } 
    out.close();
    }

out1.open("Data_oscilator_XOINA");
if (out1.is_open()){
    out1 << "My  Initial data_METHOD XOINA:" << std::endl;
     out1 <<"STEP = " << step <<" X_ 0 = " << x_0_copy << " V_0 = " << v_0_copy << " W = " << w << " T =  " << T << std::endl;
     out1 << "t"<< " Coordinates_x " << " Velocity " << std::endl ;
     for (double t = 0; t < T ; t = t + step){
        std:: cout << "t = "<< t << "Coordinate_x = " << x_0_copy << " Velocity = " << v_0_copy << std::endl ;
        out1 << t <<'\t' << x_0_copy << '\t'<< v_0_copy<< std::endl ;
        double a_1 = f(w , x_0_copy);
        double x = x_0_copy + v_0_copy* step;
        double v_1 = v_0_copy + a_1 * step;
        double a_2 = f(w, x);
        double v_2 = (v_1 + v_0_copy)/2;
        x = x_0_copy + (v_1 + v_2)/2 * step;
        double v = v_0_copy + (a_1 + a_2)/2 * step;
        x_0_copy = x;
        v_0_copy = v;
    } 


}
out1.close();
out2.open("Data_Rynge_Kuta");
if (out2.is_open()){


    out2 << "My  Initial data_METHOD Runge-Kutta:" << std::endl;
     out2 <<"STEP = " << step <<" X_ 0 = " << x_0_1 << " V_0 = " << v_0_1 << " W = " << w << " T =  " << T << std::endl;
     out2 << "t"<< " Coordinates_x " << " Velocity " << std::endl ;
     for (double t = 0; t < T ; t = t + step){
        std:: cout << "t = "<< t << "Coordinate_x = " << x_0_1 << " Velocity = " << v_0_1 << std::endl ;
        out2 << t <<'\t' << x_0_1 << '\t'<< v_0_1<< std::endl ;
        double k1 = f(w , x_0_1);
        double k2_x = f(w ,x_0_1 + 1.0/2.0 * step * v_0_1 );
        double k2_v = v_0_1 + 1.0/2.0 * step * k1;
        double k3_x = f(w , x_0_1 + 0.5 * k2_v * step);
        double k3_v = v_0_1 + k2_x * step * 1.0/2.0 ;
        double k4_x = f(w , x_0_1 + step* k3_v);
        double k4_v = v_0_1 + k3_x * step;
        double v_rk = v_0_1 + step/6.0 * (k1 + 2.0 *k2_x + 2.0 * k3_x + k4_x );
        double x_rk = x_0_1 + step/6.0 * ( v_0_1 + 2.0* k2_v + 2.0 * k3_v + k4_v);
        x_0_1 = x_rk;
        v_0_1 = v_rk;




     }

}
out2.close();
return 0;
}
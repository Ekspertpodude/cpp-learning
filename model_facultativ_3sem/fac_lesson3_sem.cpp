#include <iostream>
#include <float.h>
#include <math.h>


void print_in_bit (double num){
    unsigned char * desmond = (unsigned char *) & num;
    int i;

    for (i = 0; i < sizeof (double); i++) {
     printf ("%02X ", desmond[i]);
    }
    printf ("\n");



}


double partial_sums (int  n){
    double sum = 1.0;
    double base = 2;
    for (int i = 1 ; i < n; i++){
        sum = sum + 1/(std::pow(base,i)) ;
    }
    return sum;
}

void printbits_double (double v){

double partial_sums_garm(double n){
    double sum = 1.0;
    for (int i = 1; i < n : i++ ){
        sum = sum + 1/n;

    }
    return sum;


}


int i;
 unsigned long long  *j = (unsigned long long  *) &v;
 int n = 8 * sizeof (v);

 for (i = n - 1; i >= 0; i--)
 {

 putchar (' ');
 putchar ('0' + (((*j) >> i) & 1));
 if (i % 8 == 0) {
            putchar (' ');
        }

 }
}
int main(){
    for (int i = 1; i < 200;i++){
        std::cout << std::endl;
         std::cout << i << std::endl;
         std::cout << "--------------------------------------------------------" << std::endl;
        printbits_double (partial_sums(i));
        
       
        
    }
    
    
}
#include <iostream>
#include <fstream>
#include <vector>

int fibonachi ( double index){
    if (index < 2){
        return 1;
    }
    else{
        int i = 0;
        int num_b = 1;
        int num_e = 1;
        int num_next = 2;
        while (i < index - 2 ){
            int num_next = num_b + num_e;
            num_b  = num_e;
            num_e = num_next;
            i++;
        }
        return num_e;

    }
   
    
    

}

int main( int argc, char *argv[]){

std::ofstream out;
if (argc < 2){
    std::cout << "Incorrect input; Please write  number n" << std::endl;
}
int n = 0;
out.open("Hello_text.txt");
n  = std::stoi(argv[1]);
std::vector <double> arr;
if (out.is_open()){ 

std:: cout << "Hello, World!" << std::endl;

for (double i = 1.0; i <= n; i++){
    int number = fibonachi (i);
    arr.push_back(1.0 / i);
    std::cout << std::scientific << arr[i-1] << "\t" ;
out <<' ' <<i <<  "\t"<< number << std::endl;

 }
 }
    out.close();
    std::cout << "File has been created";
}
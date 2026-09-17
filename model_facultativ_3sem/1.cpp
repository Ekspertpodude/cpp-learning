#include <iostream>
#include <fstream>
#include <array>

int fibonachi ( int index){
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
std::array <int  , 10000 > arr  ={0};
if (out.is_open()){ 

std:: cout << "Hello, World!" << std::endl;

for (int i = 1; i <= n; i++){
    int number = fibonachi (i);
    arr [i - 1] = number ;
    std::cout << arr[i-1] << "\t" ;
out <<' ' <<i <<  "\t"<< number << std::endl;

 }
 }
    out.close();
    std::cout << "File has been created";
}
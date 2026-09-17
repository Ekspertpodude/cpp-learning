#include <iostream>
#include <fstream>

  

int main( int argc, char *argv[]){

std::ofstream out;
if (argc < 2){
    std::cout << "Incorrect input; Please write  number n" << std::endl;
}
int n = 0;
out.open("Hello_text.txt");
n  = std::stoi(argv[1]);
if (out.is_open()){

std:: cout << "Hello, World!" << std::endl;

for (int i = 1; i <= n; i++){

out <<' ' <<i;

 }
 }
    out.close();
    std::cout << "File has been created";
}
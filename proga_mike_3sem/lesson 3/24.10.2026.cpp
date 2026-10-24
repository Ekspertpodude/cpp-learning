#include <iostream>
#include <chrono>
using namespace std;





void bubble( int* arr , int size){
    for (int i = 0 ; i < size; i++){
        for (int j = 0; j < size; j++){
            if  ((j+ 1 < size) and( arr[j] > arr[j+1]  )){
                int copy = arr [j +1];
                arr[j+1] = arr[j];
                arr[j] = copy;
            }
        }

    }




}

void bubble_x_2 (int* arr , int size){
    int arr1 [size /2];
    int arr2[size - size/2];
    for (int i = 0; i < sizeof(arr1)/sizeof(int); i++){
        arr1[i] = arr[i];
    }
    for (int j = 0; j < sizeof(arr2)/sizeof(int);j++){
        arr2[j] = arr[size/2 + j];
    }
    bubble(arr1 , sizeof(arr1) /sizeof(int) );
    bubble(arr2 , sizeof(arr2)/sizeof(int));
}

chrono::time_point<chrono::steady_clock> t1,t2;
auto time(){
    return chrono::steady_clock::now();
}
void make_rand_array(int* arr , int size_arr){
    for (int i = 0 ; i<size_arr ; i++){
        arr[i] = rand();
    }
}

void print_array(int* arr){

    cout << "arr: ";
    for (int i = 0; i < 5; i++ ){
        cout << arr[i] << ',';
    }
    cout << endl;
}
int main(){

 int size_arr = 100000;
 int arr[size_arr];
 make_rand_array(arr, size_arr);
 print_array(arr);
 t1 = time();
 bubble(arr,size_arr);
 t2 = time();
cout << "Time:" << (t2-t1) /1ms << "ms.\n" ;
print_array(arr);

t1 = time();
bubble_x_2(arr , size_arr);
t2 = time();
cout << "Time_ bubble_x_2:" << (t2-t1) /1ms << "ms.\n" ;
print_array(arr);



}

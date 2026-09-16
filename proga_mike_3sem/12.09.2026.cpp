#include <iostream>
#include <string>
#include <vector>
#include <deque>
#include <type_traits> 
class Vehicle {
    protected:
        std:: string make ;
        std:: string model;
        int year;
        int price;
    public:
        Vehicle( std:: string make , std:: string model,int year,int price){
            this->make = make;
            this->model = model;
            this->price = price;
            this->year = year;
        }
        virtual void print(){
            std::cout << make <<"\t" <<  model <<"\t" <<  year <<"\t" <<  price <<  std ::endl;
         }
        void print_Info (){
            std::cout << model << "\t" ;
        }
        std::string operator[](unsigned index) const{
             switch (index)
        {
        case 0 : return make;
        case 1: return model;
        case 2: return std:: to_string (year) ;
        case 3: return  std:: to_string (price);
        default: return "Bad Index";
            }   
        }



};
class Car: public virtual Vehicle {
    private:
        int num_doors;
        std::string body_style;
    public:
        Car(std:: string make , std:: string model,int year,int price , int num_doors , std::string body_style):
        Vehicle (make,model,year,price){
            this->num_doors = num_doors;
            this->body_style = body_style;
        }
        
       

        



};
class Truck: public virtual  Vehicle{
    private:
         const char* bed_length;
         const char*towing_capacity;
    public:
        Truck(std:: string make , std:: string model ,int year,int price , const char* bed_length , const char* towing_capacity):
        Vehicle (make,model,year,price){
            this->bed_length = bed_length;
            this->towing_capacity = towing_capacity;

        }
        virtual void print(){
            std::cout << make <<" \t" <<  model <<"\t" <<  year <<"\t" <<  price << "\t" << bed_length << "\t" << towing_capacity << std ::endl;
        }

};


class Garage{
    private: 
        std::deque<Vehicle> vehicles;
    public:
        Garage() {};
        void add(const Vehicle& vehicle){
            vehicles.push_back(vehicle);

        }
        void print(){
            throw "Print ERROR";
            std::cout <<  "Our garage: "<< "\t";
            for (long long unsigned int i = 0; i < vehicles.size(); i++){
                vehicles[i].print_Info() ;
            
            }
        }
        template <typename T> int find (T name ){
            for (long long unsigned int i = 0 ; i < vehicles.size();i++){
                for (long long unsigned int j = 0; j < 6; j++){
                   if constexpr ( std::is_arithmetic_v<T>){
                        if (vehicles[i][j] == std::to_string(name) ){
                        return i ;}
                   }
                    else {
                        if  (vehicles[i][j] == name ){
                        return i ;}
                    }
            }
           
        }
        return -1;
        }
 
        
};

int main(){
    try{
    Car car{"Toyota", "Camry", 2022, 2900000, 4, "Sedan"};
    auto g = Garage();
    g.add(car);
    g.print();
    }

    catch( const char* error) {
        std::cout << error << std::endl;
    }
    
    return 0;
    }
#include <iostream>
#include <string>
#include <vector>
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
        std::vector<Vehicle> vehicles;
    public:
        Garage() {};
        void add(const Vehicle& vehicle){
            vehicles.push_back(vehicle);

        }
        void print(){
            std::cout <<  "Our garage: "<< "\t";
            for (long long unsigned int i = 0; i < vehicles.size(); i++){
                vehicles[i].print_Info() ;
            }
        }
        template <typename T> int find (T name ){
            for (long long unsigned int i = 0 ; i < vehicles.size();i++){
                for (long long unsigned int j = 0; j < 4; j++){
                    if (j < 2){
                        if (vehicles[i][j] == name ){
                        return i ;}
                    }
                    else {
                        name = std::to_string(name);
                        if (vehicles[i][j] == name ){
                        return i ;}
                        }
                    }
            }
            return -1;
        }
  //template не работает. Чертовы проблемы с типами. Задание 8 как никак.    
        
};

int main(){
    Car car{"Toyota", "Camry", 2022, 2900000, 4, "Sedan"};
    Truck truck{"Ford", "F-MAX", 2023, 6000000, "6162", "13t"};
    auto g = Garage();
    g.add(car);
    g.add(truck);
    g.print();   
    std::cout << car[0] << "\n" << car[1] << "\n" << car[2] << "\n" << car[3]<< std::endl;
    std::cout << g.find("F-MAX") << std::endl;//1
    std::cout << g.find("Ferrari") << std::endl;//-1
    return 0;
    }
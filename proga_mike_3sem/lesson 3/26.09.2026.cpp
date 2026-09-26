#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <fstream>
#include <sstream>

using namespace std;

struct Student {
  string name;
  int age;
};

vector <Student> students;
vector <Student*> p_students;

string filename = "names.txt";
string delimiter = ":";
int find_age = 27;
size_t pos = 0;

void read_students(){
  ifstream file(filename);
  if (file.is_open()) {
    string line;
    while (getline(file, line)) {
      Student tmp_student;
      string age_str = line.substr(0, line.find(delimiter)); 
      int age = stoi(age_str);
      line.erase(0, line.find(delimiter) + delimiter.length());
      tmp_student.name = line;
      tmp_student.age = age;
      students.push_back(tmp_student);
      Student* address = &tmp_student;
      p_students.push_back(address);
    }
    file.close();
  }



}
  void print_students (){
    
    for (Student student : students){
      cout << "Age: " << student.age <<  " Name: " << student.name << endl ;
    }
  }

bool less_age(const Student& left, const Student& right) {
  return left.age < right.age;
}

int main() {
  read_students();
  //print_students();
  cout << students[1].name << endl;
  sort(students.begin(), students.end(), less_age);
  print_students();
  //cout << (*p_students[0]).name << endl;
  //cout << p_students[0]->name << endl;
  
}
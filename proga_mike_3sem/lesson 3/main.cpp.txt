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

vector<Student> students;
vector<Student*> p_students;

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
      tmp_student.name = line;
      cout << line << endl;
      students.push_back(tmp_student);
    }
    file.close();
  }
}

bool less_age(const Student& left, const Student& right) {
  return left.age < right.age;
}

int main() {
  read_students();
  //print_students();

  //cout << students[1].name << endl;
  //sort(students.begin(), students.end(), less_age);
  //print_students();
  //cout << (*p_students[0]).name << endl;
  //cout << p_students[0]->name << endl;
  
}
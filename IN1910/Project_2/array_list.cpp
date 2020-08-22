#include <iostream>
#include <vector>
#include <stdexcept>
#include <cmath>

using namespace std;

class ArrayList{
private:
  int *data;
  int capacity = 1000;
  int growth = 2;
  int size;

public:
  int get_capacity(){
    return capacity;
  }
  int length(){
    return size;
  }
  ArrayList(){
    size = 0;
    data = new int[capacity];
  }
  ArrayList(vector<int> numbers){
    size = 0;
    data = new int [capacity];
    for (int number: numbers){
      append(number);

    }
  }
  ~ArrayList(){
    delete data;
  }
  void print(){
    cout << "[";
    for (int i=0; i < size-1; i++){
      cout << data[i] << ", ";
    }
    cout << data[size-1] << "]" << endl;
  }
  void resize(){
    capacity *= growth;
    int *temp = new int[capacity];
    for (int i=0; i<size; i++){
      temp[i] = data[i];
    }
    delete[] data;
    data = temp;
  }
  void append(int n){
    if (size >= capacity){
      resize();
    }
    data[size] = n;
    size ++;
  }
  int& operator[](int n){
    if (0 <= n && size > n){
      return data[n];
    }
    else {
      throw range_error("Out of range");
    }
  }
  void insert(int x, int index){
    if (index < 0 || size < index){
      throw range_error("Out of range");
    }
    if (capacity <= size) {
      resize();
    }
    if (index == size){
      append(x);
    }
    else {for (int i=size; index < i; i--){
      data[i] = data[i-1];
      }
      data[index] = x;
      size++;
    }
  }
  void remove(int index){
    if (index < 0 || size <= index){
      throw range_error("Out of range");
    }
    for (int i=index; i < size; i++){
      data[i] = data[i+1];
    }
    size--;
    if (capacity*0.25 > size){
      shrink_to_fit();
    }
  }
  int pop(int index){
    int value = data[index];
    remove(index);
    return value;
  }
  int pop(){
    return pop(size-1);
  }
  void shrink_to_fit(){
    int i = 0;
    while (i < 100){
      if (size <= pow(2, i)){
        // cout << "capacity = " << capacity << endl;
        capacity = pow(2,i);
        // cout << "capacity = " <<capacity << endl;
        i = 100;
      }
      i++;
    }
  }




};

bool is_prime(int n){
  if (n <= 1){
    return false;
  }
  for (int i=2; i<n; i++){
    if (n % i == 0){
      return false;
    }
  }
  return true;
    }


int main(){
  ArrayList test;

  int i = 1;
  while (test.length() < 10){
    if (is_prime(i)){
      test.append(i);
    }
    i++;
  }
  test.print();

  cout << "Length = " << test.length() << " Capacity = " << test.get_capacity() << endl;
  test.pop();
  cout << "Length = " << test.length() << " Capacity = " << test.get_capacity() << endl;
  return 0;
}

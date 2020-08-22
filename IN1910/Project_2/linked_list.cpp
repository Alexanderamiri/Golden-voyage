#include <iostream>
#include <stdexcept>
#include <vector>

using namespace std;


struct Node{
  int value;
  Node* next;

  Node (int v){
    value = v;
    next = nullptr;
  }
  Node (int v, Node* n){
    value = v;
    next = n;
  }
};


class LinkedList{
private:
  Node* head;
  Node* tail;

  Node* get_node(int index){
    int size = length();
    if (index < 0 or index >= size){
      throw range_error("Index out of range");
    }
    Node* current = head;
    for (int i=0; i < index; i++){
      current = current->next;
    }
    return current;
  }


public:
  LinkedList(){
    head = nullptr;
    tail = nullptr;
  }
  LinkedList(vector<int> numbers){
    head = nullptr;
    tail = nullptr;
    for (int number: numbers){
      append(number);
    }
  }
  ~LinkedList(){
    Node* current = head;
    Node* next = current->next;
      while (current != nullptr){
      next = current->next;
      delete current;
      current = next;
    }
  }
  int length(){
    int len = 0;
    Node* current = head;
    while (current != nullptr){
      len++;
      current = current->next;
    }
    return len;
  }
  void append(int value){
    if (head == nullptr){
      head = new Node(value);
    }else if (tail ==nullptr){
      tail = new Node(value);
      head->next = tail;
    }else {
      Node* current = tail;
      tail = new Node(value);
      current->next = tail;
    }
  }
  void print(){
    Node* current = head;
    while (current != nullptr){
      cout << current->value << " ";
      current = current->next;
    }
    cout << endl;
  }
  int &operator[](int index){
    Node* current = get_node(index);
    return current->value;
  }
  void insert(int val, int index){
    if (index == 0){
      head = new Node(val, head);
    }
    else {
      Node* prev = get_node(index-1);
      Node* next = prev->next;
      Node* current = new Node(val, next);
      prev->next = current;
    }
  }
  void remove(int index){
    Node* current = get_node(index);
    if (index == 0){
      head = current->next;
      delete current;
    }else{
      Node* prev = get_node(index - 1);
      if (current->next == nullptr){
        delete current;
        prev->next = nullptr;
      }
      else{
        prev->next = current->next;
        delete current;
      }
    }
  }
  int pop(int index){
    Node* current = get_node(index);
    int value = current->value;
    remove(index);
    return value;
  }
  int pop(){
    int len = length();
    int value = tail->value;
    remove(len-1);
    return value;
  }

};


int main(){
  {LinkedList Test;
  cout << "Length = " << Test.length() << endl;
  cout << "Appending all numbers below 0" << endl;
  for (int i=0; i < 9; i++){
    Test.append(i);
  }
  cout << "Length = " << Test.length() << endl;
  Test.print();
  cout <<"\nTesting the [] operator for " << endl;
  for (int i=0; i < 3; i++){
    cout << "Test[" << i << "] = " << Test[i] << endl;
  }
  cout << "\nRemoving whats at index 0, 2 and 4 and inserting the number 9 there instead\n";
  for (int i=0; i<5; i+=2){
    Test.remove(i);
    Test.insert(9, i);
  }
  Test.print();
  cout << "\npop(1) = " << Test.pop(1) << endl;
  Test.print();
  cout << "pop = " << Test.pop() << endl;
  Test.print();}

  LinkedList Test2({0,1,2,3,4,5,6});
  cout << "\nTesting the LinkedList(vector<int>) constructer with the elements from 0 to 6\n";
  Test2.print();
  return 0;
}

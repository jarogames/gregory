#include <iostream>
//
// g++ -L/home/himanshu/practice/ -Wall main.cpp -o main -lCfile
//
// import C into C++
 extern "C" {
 int fso();
 }


void func1(void)
{
    std::cout<<"\n being used within C++ code\n";
}

int main(void)
{
  fso();
  func1();
  return 0;
}

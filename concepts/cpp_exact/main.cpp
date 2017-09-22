#include <iostream>

extern "C" {
void fu();
}

void func(void)
{
    std::cout<<"\n being used within C++ code\n";
}

int main(void)
{
    fu();
    func();
    return 0;
}

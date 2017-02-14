#include <iostream>
#include "Foo.h"

int main() {
    Foo<int> i;
    Foo<float> x(1.234);

    std::cout << "i = " << i.getVal() << ", " << x.getVal() << std::endl;

    i.setVal(10);
    std::cout << "i = " << i.getVal() << std::endl;

    std::cout << "mySizeof(float) = " << mySizeof<float>() << std::endl;
}

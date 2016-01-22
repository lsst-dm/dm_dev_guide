/// Implementation of templated class Foo
#include "Foo.h"

template<typename T>
Foo<T>::Foo() : _val(0) {}

template<typename T>
Foo<T>::Foo(T val) : _val(val) {}

template<typename T>
Foo<T>::~Foo() {}

#if 0
template<typename T> T Foo<T>::getVal() const; // inline in Foo.h
#endif

template<typename T>
void Foo<T>::setVal(T val) { _val = val; }
//
// And a templated function
//
template<typename T>
size_t mySizeof() { return sizeof(T); }

//
// Explicit instantiations
//
template class Foo<float>;
template class Foo<int>;

template size_t mySizeof<float>();

#if !defined(FOO_H)
#define FOO_H 1

#include <cstddef>

template <typename T>
class Foo {
public:
    explicit Foo();
    explicit Foo(T x);
    ~Foo();

    inline T getVal() const;
    void setVal(T val);

private:
    T _val;
};
//
// Inlined functions need to be in the .h file (maybe in the class definition itself)
//
template <typename T>
inline T Foo<T>::getVal() const {
    return _val;
}
//
// Declare a templated function
//
template <typename T>
size_t mySizeof(void);
//
// Provide a declaration for explicitly-instantiated version[s] of mySizeof()
// This is only needed if we provide enough information here for the compiler
// to instantiate the function/class
//
// It's non-compliant code (but see C++ standards proposal N1897), and stops
// the compiler instantiating the function in each file, and leaving it up
// to the linker to clean up the mess
//
#if 0
extern template size_t mySizeof<float>(void);
#endif

#endif

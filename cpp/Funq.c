#include <stdio.h>

/*  gcc  -c -fPIC -o Funq.o Funq.c */
/*  ll -trh */
/*  gcc -shared -o libFunq.so Funq.o */
/*  g++ -L./ -Wall usefun.C -o main  -lFunq */

// gcc  -c -fPIC -o Funq.o Funq.c;gcc -shared -o libFunq.so Funq.o
int fso(int a)
{
    printf("%s: %s %s This is a shared functio - 3asd - %f\n",__FILE__,__DATE__,__TIME__,a*1.0);
    return 16;
}

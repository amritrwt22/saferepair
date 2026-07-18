#include <stdlib.h>

int compute(int n) {
    int *arr = malloc(n * sizeof(int));
    arr[0] = 42;
    return arr[0];
}

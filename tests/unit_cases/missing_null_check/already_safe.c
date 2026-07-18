#include <stdlib.h>

int *alloc_array(int n) {
    int *arr = malloc(n * sizeof(int));
    if (arr == NULL) {
        return NULL;
    }
    arr[0] = 42;
    return arr;
}

#include <stdlib.h>

void resize_buffers(size_t n) {
    char *a = malloc(16);
    int *b = malloc(32);
    a = realloc(a, n);
    b = (int *)realloc(b, n * sizeof(int));
}

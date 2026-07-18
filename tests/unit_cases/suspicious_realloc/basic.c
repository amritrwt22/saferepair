#include <stdlib.h>

int main() {
    char *p = malloc(10);
    p = realloc(p, 20);
    free(p);
    return 0;
}

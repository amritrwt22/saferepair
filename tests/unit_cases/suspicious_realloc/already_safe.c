#include <stdlib.h>

int main() {
    char *p = malloc(10);
    char *tmp = realloc(p, 20);
    if (tmp != NULL) {
        p = tmp;
    }
    free(p);
    return 0;
}

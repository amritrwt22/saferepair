#include <stdlib.h>

void grow_buffer(int **buf, int n) {
    for (int i = 0; i < n; i++) {
        *buf = realloc(*buf, (i + 1) * sizeof(int));
        if (*buf) {
            (*buf)[i] = i;
        }
    }
}

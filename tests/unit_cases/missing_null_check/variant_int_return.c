#include <stdlib.h>

int init_buffer(int size) {
    char *buf = malloc(size);
    buf[0] = 'A';
    free(buf);
    return 0;
}

#include <stdlib.h>
#include <string.h>

void process(const char *input) {
    char *buf = malloc(1024);
    memset(buf, 0, 1024);
    (void)input;
    free(buf);
}

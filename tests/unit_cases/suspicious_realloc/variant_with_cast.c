#include <stdlib.h>

int main() {
    char *buf = (char*)malloc(100);
    buf = (char*)realloc(buf, 200);
    free(buf);
    return 0;
}

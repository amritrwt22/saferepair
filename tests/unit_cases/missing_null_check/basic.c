#include <stdlib.h>
#include <string.h>

char *duplicate(const char *s) {
    char *buf = malloc(strlen(s) + 1);
    strcpy(buf, s);
    return buf;
}

#include <string.h>

int scan(const char *buf, int len) {
    int i = 0;
    while (buf[i] != '\0' && i < len) {
        i++;
    }
    return i;
}

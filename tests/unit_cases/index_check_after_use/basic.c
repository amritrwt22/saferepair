/* V781: buf[i] accessed before i < len is checked */
#include <string.h>

int scan_buf(const char *buf, int len) {
    int i = 0;
    while (buf[i] != '\0' && i < len) {
        i++;
    }
    return i;
}

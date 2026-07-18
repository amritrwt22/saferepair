/* No V781: bound check (i < len) already appears before the array access */
int scan_safe(const char *buf, int len) {
    int i = 0;
    while (i < len && buf[i] != '\0') {
        i++;
    }
    return i;
}

/* V781: arr[k] accessed before k < size is checked (for-loop condition) */
int find_value(int *arr, int size, int target) {
    int k;
    for (k = 0; arr[k] != target && k < size; k++) {
        /* nothing */
    }
    return k;
}

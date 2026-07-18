#include <stdlib.h>

/* realloc without assignment to same pointer — should NOT be flagged
   as suspicious-realloc-usage, but if it is, handler should skip
   because there's no self-assignment pattern. */
void just_realloc(void *p, size_t n) {
    void *tmp = realloc(p, n);
    if (tmp) {
        /* use tmp */
    }
}

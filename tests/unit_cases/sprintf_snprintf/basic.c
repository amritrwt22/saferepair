/* CWE-120: sprintf to fixed-size buffer without bounds check.
 * Bug: sprintf(buf, "%s", msg) -- no length limit, potential overflow.
 * Fix: snprintf(buf, sizeof(buf), "%s", msg) -- bounded, safe.
 */
#include <stdio.h>

void format_message(const char *msg) {
    char buf[64];
    sprintf(buf, "%s", msg);
}

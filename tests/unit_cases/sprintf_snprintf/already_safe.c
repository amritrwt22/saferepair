/* Already safe: snprintf with explicit size limit.
 * Handler should produce no alert for this pattern.
 */
#include <stdio.h>

void format_message(const char *msg) {
    char buf[64];
    snprintf(buf, sizeof(buf), "%s", msg);
}

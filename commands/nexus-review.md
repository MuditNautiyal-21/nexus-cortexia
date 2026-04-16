---
description: Run the two-stage review protocol on code or a file. Spec compliance first, then code quality.
argument-hint: [file path or code to review]
---

Load the Nexus Cortexia reviewer protocol: `nexus-cortexia/skills/reviewer/SKILL.md`.

Review the target with the full two-stage protocol:

1. **Spec compliance**: walk through each acceptance criterion and mark PASS
   or FAIL. If no spec exists, infer one from the code's apparent purpose.
2. **Code quality**: check correctness, security, maintainability, and
   performance. Rate each issue as CRITICAL, WARN, or NOTE.

Output the review in the format the reviewer protocol specifies, ending with
a verdict (PASS, NEEDS FIX, or BLOCK).

Target: $ARGUMENTS

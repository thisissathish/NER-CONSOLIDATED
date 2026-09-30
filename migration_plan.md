# Migration Plan: Rename NER-based Folders to UrbanFlow

## Current Status
- Identified subfolder: `./NER-Smart-Logistics`
- Identified root folder: `E:\Mark2\NER-CONSOLIDATED`

## Migration Plan
1. Rename `./NER-Smart-Logistics` to `./urbanflow-logistics`.
2. Address root directory `E:\Mark2\NER-CONSOLIDATED`:
    - Renaming the root directory *while the session is active in it* is high-risk.
    - **Proposed Action**: I will perform the renaming of `NER-Smart-Logistics` first. For the root directory, I advise you to close the current Claude Code session, rename the root folder on the file system manually, and re-open this project in Claude Code. This ensures Git and all paths are managed correctly by your IDE.

## Verification
- Validate project integrity after renaming subdirectories.
- Re-run `backend_test.py` to ensure imports are not broken.

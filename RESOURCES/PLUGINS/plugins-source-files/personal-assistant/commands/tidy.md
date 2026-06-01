---
name: tidy
description: Scan a folder (Downloads, Desktop, Documents, Projects) and propose cleanup actions — categorise files, find duplicates, optionally suggest a better folder structure. Also triggers on "organize my [folder]", "clean up [folder]", "find duplicates", and "my [folder] is a mess".
---

# /tidy — File Cleanup & Organization Assistant

Help the user clean up a cluttered folder. Practical utility that demonstrates immediate PA value.

## Flow

1. Use AskUserQuestion to ask which folder to scan:
   - "Downloads folder"
   - "Desktop"
   - "Choose a different folder"

2. If the folder isn't already accessible, use `request_cowork_directory` to ask the user to select it.

3. Ask how aggressive to be:
   - **Conservative** — flag issues and propose moves only; never suggest deletes. Default for first-time runs.
   - **Comprehensive** — also propose deleting duplicates and stale installers, and suggest a new folder structure.

4. Scan and categorise:
   - **Large files** (>100MB) — flag with sizes
   - **Old files** (>30 days, not touched) — suggest archiving
   - **Duplicates** — detect both by name and by content hash. Pick the right command for the user's OS: macOS uses `md5`, Linux/WSL uses `md5sum` or `sha256sum`, Windows PowerShell uses `Get-FileHash`. Hash every file, group by hash, surface groups with more than one entry. For each set, show all paths, sizes, and modification dates; recommend which copy to keep (usually newest or best-located).
   - **Screenshots** — accumulated screenshots (often pile up on Desktop)
   - **Installers/DMGs** — downloaded installers that are probably stale
   - **Documents** — PDFs, docs, spreadsheets that might belong elsewhere

5. Present a summary: "I found [X] files. Here's what I'd suggest..." Group by category with clear action proposals.

6. **Comprehensive mode only** — propose a folder structure for what's there. Example for a Downloads folder:

   ```
   Downloads/
   ├── To-Sort/      (new files arrive here)
   ├── Archive/      (old files, >6 months)
   ├── Installers/   (DMGs, PKGs)
   └── Documents/    (PDFs, DOCX, XLSX)
   ```

7. Use AskUserQuestion for each proposed action:
   - "Delete these [X] old installers?"
   - "Move these screenshots to [suggested location]?"
   - "Move these duplicates to trash? Keeping [recommended version]"
   - "Create the proposed folder structure?"

8. **Never delete without explicit confirmation.** Present the list, get approval, then act. If in doubt, suggest moving to a "to-review" folder rather than deleting.

9. Apply naming conventions to any files you rename:
   - Date-prefix important files: `2026-04-22 - Description.ext`
   - Kebab-case for folders, no spaces
   - Strip download artifacts: `document-final-v2 (1).pdf` → `document.pdf`

10. Log the cleanup in the captain's log: "[time] — Tidied [folder]: removed X files, moved Y, freed Z space."

11. End with a one-line maintenance tip matched to the folder:
    - Downloads → "Run /tidy weekly to keep this under control."
    - Desktop → "Move screenshots to Pictures/Screenshots monthly."
    - Documents → "Archive projects not touched in 6+ months."
    - Projects → "Separate active from archived quarterly."

## Tone

Practical, slightly fun. "Your Downloads folder has 847 files in it. That's... ambitious. Let's sort this out." Don't be judgmental — everyone's Downloads folder is a disaster.

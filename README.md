# Colleagues

Published notes from my Obsidian vault.

## Usage

To publish notes, add `publish: true` to the frontmatter of any markdown file:

```yaml
---
publish: true
---
```

Then run the publish script:

```bash
python publish.py
```

This will copy all files with `publish: true` to the `PUBLISH/` folder.

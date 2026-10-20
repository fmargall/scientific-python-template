"""Check that the files shared with the template have not drifted from it.

Some files of this repository come from template/: CODE_OF_CONDUCT.md and
SECURITY.md are the rendering of their .jinja versions with the answers of this
repository, and the GitHub configuration (rulesets, configure-github.sh) is an
exact copy. This script renders and compares them again, and fails if any differs.

Usage: uv run --no-project --with jinja2 python scripts/check_community_files.py
"""

import difflib
import sys
from pathlib import Path

import jinja2

ROOT = Path(__file__).resolve().parent.parent
# The answers of this repository, as if it had been generated from the template
ANSWERS = {
    "project_name": "python-template",
    "repository_url": "https://github.com/fmargall/python-template",
    "author_email": "fr.margall@proton.me",
    "conduct_email": "fr.margall@proton.me",
}
# Rendered from template/<name>.jinja
RENDERED = ["CODE_OF_CONDUCT.md", "SECURITY.md"]
# Copied verbatim from template/<name>
COPIED = [
    ".github/rulesets/main.json",
    ".github/rulesets/version-tags.json",
    "scripts/configure-github.sh",
]


def main() -> int:
    """Compare each shared file with its version in the template."""
    # Same options as Copier: the final newline of the templates is kept
    environment = jinja2.Environment(keep_trailing_newline=True, undefined=jinja2.StrictUndefined)
    failed = False
    for name, source in [(name, f"{name}.jinja") for name in RENDERED] + [
        (name, name) for name in COPIED
    ]:
        expected = (ROOT / "template" / source).read_text(encoding="utf-8")
        if source.endswith(".jinja"):
            expected = environment.from_string(expected).render(ANSWERS)
        actual = (ROOT / name).read_text(encoding="utf-8")
        if actual == expected:
            print(f"{name} is in sync with template/{source}")
            continue
        failed = True
        print(f"{name} differs from template/{source}:")
        sys.stdout.writelines(
            difflib.unified_diff(
                actual.splitlines(keepends=True),
                expected.splitlines(keepends=True),
                fromfile=name,
                tofile=f"template/{source}",
            )
        )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

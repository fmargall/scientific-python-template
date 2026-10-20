"""Check that the community files of this repository match those of the template.

CODE_OF_CONDUCT.md and SECURITY.md of this repository are the rendering of their
versions in template/, with the answers of this repository: this script renders
them again and fails if they differ.

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
FILES = ["CODE_OF_CONDUCT.md", "SECURITY.md"]


def main() -> int:
    """Render the community files of the template, and compare them with the repository."""
    # Same options as Copier: the final newline of the templates is kept
    environment = jinja2.Environment(keep_trailing_newline=True, undefined=jinja2.StrictUndefined)
    failed = False
    for name in FILES:
        template = (ROOT / "template" / f"{name}.jinja").read_text(encoding="utf-8")
        expected = environment.from_string(template).render(ANSWERS)
        actual = (ROOT / name).read_text(encoding="utf-8")
        if actual == expected:
            print(f"{name} is in sync with template/{name}.jinja")
            continue
        failed = True
        print(f"{name} differs from the rendering of template/{name}.jinja:")
        sys.stdout.writelines(
            difflib.unified_diff(
                actual.splitlines(keepends=True),
                expected.splitlines(keepends=True),
                fromfile=name,
                tofile=f"template/{name}.jinja",
            )
        )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env bash
# Generate a project from the working tree of this repository, with the answers of
# tests/answers/<case>.yml, then run all its checks, as its own CI and its
# contributors would. Any failure, or any file modified by a hook, fails the test.
#
# Usage: scripts/test-template.sh <case> [<destination>]
#   <case>         name of a file of tests/answers/, without .yml (agpl, mit, ...)
#   <destination>  where to generate the project, a new temporary folder by default
set -euo pipefail

case_name=$1
template=$(cd "$(dirname "$0")/.." && pwd)
destination=${2:-$(mktemp -d)/project}

step() { printf '\n=== %s\n' "$*"; }

step "Generate the project with tests/answers/$case_name.yml in $destination"
# --vcs-ref HEAD: the working tree, uncommitted changes included, not the latest tag
uvx copier copy --defaults --vcs-ref HEAD \
    --data-file "$template/tests/answers/$case_name.yml" "$template" "$destination"
cd "$destination"
git init --quiet --initial-branch main
git add --all

step "Create the environment and the lock file"
uv sync
git add uv.lock

step "Run all the pre-commit hooks: none may fail, nor modify a file"
uv run --no-sync pre-commit run --all-files --show-diff-on-failure

step "Run the tests"
uv run --no-sync pytest --cov

step "Build and check the distributions"
uv build
uvx twine check --strict dist/*

step "Build the documentation, with a module, a class and a function in the API reference"
package=$(sed -n "s/^package_name: //p" .copier-answers.yml)
cat > "src/$package/sample.py" <<'EOF'
"""A module added by scripts/test-template.sh, to document a submodule."""


class Counter:
    """Count events.

    Parameters
    ----------
    start : int, optional
        First value of the counter.
    """

    def __init__(self, start: int = 0) -> None:
        self.value = start

    def increment(self, step: int = 1) -> int:
        """Add a step to the counter.

        Parameters
        ----------
        step : int, default 1
            Value added to the counter.

        Returns
        -------
        int
            The new value of the counter.
        """
        self.value += step
        return self.value


def double(value: float) -> float:
    """Double a value.

    Parameters
    ----------
    value : float
        Value to double.

    Returns
    -------
    float
        Twice the value.
    """
    return 2 * value
EOF
uv sync --group docs
uv run --no-sync sphinx-build -W --keep-going -b html docs docs/_build/html
for page in index api "generated/$package.sample" "generated/$package.sample.Counter"; do
    test -f "docs/_build/html/$page.html" || { echo "error: docs/_build/html/$page.html is missing" >&2; exit 1; }
done
rm "src/$package/sample.py"

step "Validate the metadata and configuration files"
uvx validate-pyproject pyproject.toml
uvx cffconvert --validate
uvx check-jsonschema --builtin-schema vendor.github-workflows .github/workflows/*.yml
uvx check-jsonschema --builtin-schema vendor.github-issue-config .github/ISSUE_TEMPLATE/config.yml
uvx check-jsonschema --builtin-schema vendor.github-issue-forms \
    .github/ISSUE_TEMPLATE/{bug_report,feature_request,question,documentation}.yml
uvx check-jsonschema --builtin-schema vendor.dependabot .github/dependabot.yml
if [[ -f .github/codecov.yml ]]; then
    uvx check-jsonschema --schemafile https://json.schemastore.org/codecov.json .github/codecov.yml
fi

step "Lint the workflows"
# actionlint does not know the self-repository syntax "$/" yet: rhysd/actionlint#732
uvx --from actionlint-py actionlint -ignore 'reusable workflow call "\$/'

step "Prepare and check a first release"
uv run --no-sync python - <<'EOF'
from pathlib import Path

changelog = Path("CHANGELOG.md")
text = changelog.read_text(encoding="utf-8")
entry = "## [Unreleased]\n\n### Added\n\n- A first feature.\n"
changelog.write_text(text.replace("## [Unreleased]\n", entry, 1), encoding="utf-8", newline="\n")
EOF
uv run --no-sync python scripts/release.py prepare 0.1.0
uv run --no-sync python scripts/release.py check v0.1.0
uv run --no-sync python scripts/release.py notes v0.1.0
# The files changed by the release must still pass the hooks
uv run --no-sync pre-commit run --files CHANGELOG.md CITATION.cff --show-diff-on-failure

step "All the checks passed for $case_name"

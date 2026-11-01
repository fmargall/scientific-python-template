# Create your first project

In this tutorial, you generate a project from the template, check it on your machine,
publish it on GitHub, and merge a first change through a pull request whose CI passes. At
the end, you have a repository that only changes through such pull requests.

It takes about half an hour. The first release, on PyPI, is the subject of the next
tutorial.

## Before you start

You need:

- [uv](https://docs.astral.sh/uv/), which also runs Copier and the other tools;
- [git](https://git-scm.com/), with your name and email configured;
- the [GitHub CLI](https://cli.github.com/), authenticated with `gh auth login`: check it
  with `gh auth status`.

:::{note}
On Windows, run the commands in PowerShell, except the `.sh` scripts: they need Git Bash,
installed with git. The `bash` command of PowerShell may be the one of WSL, which does not
see the programs installed on Windows. The steps below give the PowerShell command when it
differs.
:::

## Generate the project

Run Copier on the template:

```bash
uvx copier copy gh:fmargall/scientific-python-template my-project
```

Copier asks a few questions. Answer `My Project` to the first one, and keep the default
answer of the questions that propose one, by pressing {kbd}`Enter`. A few of them deserve a
word:

- **Package name** and **distribution name**: the first is what you `import`
  (`my_project`), the second what you `pip install` (`my-project`). Both are derived from
  the project name.
- **Oldest supported Python version**: computed from today's date, following
  [SPEC 0](https://scientific-python.org/specs/spec-0000/). The CI tests every version from
  this one to the newest release.
- **Repository URL**: the GitHub repository you create below, such as
  `https://github.com/your-name/my-project`. It does not need to exist yet.
- **Codecov**: answer `no` for this tutorial. Codecov needs its GitHub app installed,
  which is one more step outside of the template.

Copier then generates the project in `my-project/` and lists the next steps. This
tutorial follows them.

## Look around

Open the new folder. The main pieces are:

| Path | Content |
| --- | --- |
| `src/my_project/` | The package, with a `__version__` read from the git tags |
| `tests/` | The tests, run by pytest |
| `pyproject.toml` | The metadata, the dependencies and the configuration of the tools |
| `.pre-commit-config.yaml` | The checks run on every commit: ruff, pyright, spelling... |
| `.github/` | The workflows, Dependabot, the issue forms and the rulesets |
| `docs/adr/` | The architecture decision records |
| `.copier-answers.yml` | Your answers, read again by `copier update` |

Do not edit `.copier-answers.yml` by hand: it is how the project follows the template.

## Make the first commit

Create the git repository, the environment and the lock file, then install the hooks:

```bash
cd my-project
git init -b main
uv sync
uv run pre-commit install
```

`uv sync` creates `.venv/`, installs the package in it with the development tools, and
writes `uv.lock`, the exact versions that the CI uses too. Commit everything:

```bash
git add --all
git commit -m "🎉 chore: generate the project from the Scientific Python Template"
```

The hooks run before the commit is created: you see each of them pass. Their first run
takes a while, since pre-commit installs them.

## Run the checks

Run the same checks as the CI, on your machine:

```bash
uv run pytest --cov
uv run pre-commit run --all-files
```

The single test of the project passes: the package is installed, and its version is
known.

## Publish on GitHub

Create the repository on GitHub, at the URL you gave to Copier, and push to it:

```bash
gh repo create your-name/my-project --public --source . --remote origin --push
```

The CI already runs on this first push: see the **Actions** tab of the repository. Then
configure the repository. Look at what the script would change first:

```bash
bash scripts/configure-github.sh --dry-run
bash scripts/configure-github.sh
```

On Windows, in PowerShell:

```powershell
& "C:\Program Files\Git\bin\bash.exe" scripts/configure-github.sh --dry-run
& "C:\Program Files\Git\bin\bash.exe" scripts/configure-github.sh
```

The script sets the merge buttons, the security features and the permissions of the
workflows, and creates the rulesets. From now on, `main` cannot be pushed to: every
change goes through a pull request.

## Merge a first change

Add a function to the package, on a branch:

```bash
git switch -c add-kinetic-energy
```

Create `src/my_project/physics.py`:

```python
"""Formulas of classical mechanics."""


def kinetic_energy(mass: float, velocity: float) -> float:
    """Compute the kinetic energy of a moving body.

    Parameters
    ----------
    mass : float
        Mass of the body, in kilograms.
    velocity : float
        Speed of the body, in meters per second.

    Returns
    -------
    float
        Kinetic energy, in joules.
    """
    return 0.5 * mass * velocity**2
```

And its test, `tests/test_physics.py`:

```python
from my_project.physics import kinetic_energy


def test_kinetic_energy():
    assert kinetic_energy(mass=2.0, velocity=3.0) == 9.0
```

The docstring is required: ruff checks that every public function has one, in the NumPy
style, and that its signature is annotated. Users see the change, so describe it in
`CHANGELOG.md`, under `## [Unreleased]`:

```markdown
### Added

- `physics.kinetic_energy`, the kinetic energy of a moving body.
```

Commit, push, and open the pull request:

```bash
git add --all
git commit -m "✨ feat: add the kinetic energy"
git push -u origin add-kinetic-energy
gh pr create --fill
```

The title of the pull request becomes the commit message on `main`: it follows the same
convention, a [gitmoji](https://gitmoji.dev/) and a
[Conventional Commits](https://www.conventionalcommits.org/) type.

On the page of the pull request, the checks run: lint, type checking, build, and the tests
on every supported Python version. Merging stays blocked until the `ci-passed` check
succeeds. Then merge it, and come back to an up-to-date `main`:

```bash
gh pr merge --squash
git switch main
git pull
```

## What you have done

You have generated a project, checked it locally, published it on GitHub with a
protected `main` branch, and merged a first change, tested and described in the changelog.
Every next change follows the same path: a branch, a pull request, a green CI, a squash
merge.

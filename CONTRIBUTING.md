# Contributing to python-template

Thank you for your interest in python-template! Everyone taking part in the project is
expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

python-template is a [Copier](https://copier.readthedocs.io/) template: it contains no
Python package of its own, its product is the projects generated from it. Every change is
therefore judged by its effect on a freshly generated project.

## Reporting Bugs and Requesting Features

Open an [issue](https://github.com/fmargall/python-template/issues), with the answers given
to the questions of the template and the command that fails in the generated project.
Security vulnerabilities must not be reported in public issues: see the
[Security Policy](SECURITY.md) instead.

## Repository Layout

| Path | Content | Copied to generated projects |
|---|---|---|
| `copier.yml` | the questions asked by Copier, with their defaults and validators | no |
| `template/` | the files of the generated projects | yes |
| `licenses/` | the license texts, included by `template/LICENSE.txt.jinja` | through the include |
| `macros/` | the Jinja macros shared by the templates | through the imports |
| everything else | the tooling and documentation of this repository | no |

Some rules to keep in mind when editing `template/`:

- Only the files ending in `.jinja` are rendered, and lose this suffix. Every other file is
  copied verbatim, so a file containing `{{ }}` that must not be rendered, such as a GitHub
  Actions workflow, must not end in `.jinja`.
- File and directory names are rendered too: a name rendering to an empty string is not
  created, which is how optional files are made, e.g.
  `{% if license == 'AGPL-3.0-or-later' %}.license-header.txt{% endif %}.jinja`.
- A configuration file that tools discover by its name (`.editorconfig`, `.gitignore`, ...)
  is also active in this repository, for the files under `template/`. When this is not
  wanted, add the `.jinja` suffix to its name: tools no longer see it, and the generated
  project still gets it.
- `{% include %}` and `{% import %}` paths are relative to the root of this repository, not
  to `template/`.
- `licenses/` and the code of conduct are kept verbatim from their sources (SPDX and
  Contributor Covenant 3.0): only their placeholders are replaced.
- `CODE_OF_CONDUCT.md` and `SECURITY.md` of this repository are rendered from
  `template/CODE_OF_CONDUCT.md.jinja` and `template/SECURITY.md.jinja`: keep them in sync.

## Setting Up a Development Environment

The tools are run with [uv](https://docs.astral.sh/uv/). Install pre-commit as a uv tool,
then the hooks of this repository:

```bash
git clone https://github.com/fmargall/python-template.git
cd python-template
uv tool install pre-commit
pre-commit install
```

The hooks only check the hygiene of the files (YAML, TOML, whitespace, `.editorconfig`):
the generated projects carry their own checks, see below.

## Testing a Change

A change is tested on generated projects. `scripts/test-template.sh` generates one from
the working tree (uncommitted changes included) with the answers of a file of
`tests/answers/`, in a temporary folder, then runs all its checks: the pre-commit hooks,
which must neither fail nor modify a file, the tests, the build, the validation of the
metadata and workflows, and the preparation of a first release.

```bash
bash scripts/test-template.sh agpl  # AGPL, with every optional answer
bash scripts/test-template.sh mit   # MIT, without them, and with values to escape
```

The CI runs both, together with the hooks of this repository and
`scripts/check_community_files.py`, which checks that `CODE_OF_CONDUCT.md` and
`SECURITY.md` are still the rendering of their versions in `template/`.

When a change depends on an answer that no file of `tests/answers/` covers, add one.
On Windows, if a tool fails to install with the newest Python, run the script with
`UV_PYTHON=3.13`, for example.

## Submitting Changes

1. Create a branch from `main`.
2. Make your changes, and test them as described above.
3. Describe what changes in the generated projects in [`CHANGELOG.md`](CHANGELOG.md).
4. Open a pull request, listing the answers you tested the change with.

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/),
prefixed with the matching [gitmoji](https://gitmoji.dev/), for example:

```text
✨ feat: add SECURITY.md to template
🐛 fix: keep a single final newline in LICENSE.txt
📝 docs: add SECURITY.md
```

## Releasing

`copier update` relies on the git tags of this repository to know which version of the
template a project was generated from. A release is a `vX.Y.Z` tag on `main`, following
[Semantic Versioning](https://semver.org/) from the point of view of the generated projects:

- **major**: a change requiring a manual migration of the existing projects, such as a
  renamed or removed question;
- **minor**: a new file, or a new question with a default value;
- **patch**: a fix that keeps the generated files compatible.

## License

By contributing, you agree that your contributions will be licensed under the
[MIT](LICENSE.txt) license of this repository.

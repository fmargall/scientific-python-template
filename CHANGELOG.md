# Changelog

All notable changes to the Scientific Python Template are documented in this file.
They describe what changes in the projects generated from the template, to help
decide when to run `copier update`: changes to the tooling of this repository
itself are not listed.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2026-10-27

### Security

- `pypa/gh-action-pypi-publish` is updated to 1.14.3, which fixes
  [GHSA-5xjx-3w67-w9x9](https://github.com/pypa/gh-action-pypi-publish/security/advisories/GHSA-5xjx-3w67-w9x9).

### Fixed

- The lint job of the CI runs pre-commit with `uvx` instead of `pre-commit/action`,
  which calls `actions/cache` by tag: once `scripts/configure-github.sh` requires
  actions pinned to a full commit SHA, GitHub refused to run the job.

## [0.1.1] - 2026-10-26

### Changed

- The footer of the README states that the project was made with Copier, with the
  badge inline and centered.
- Pull requests are merged with "Squash and merge" only, in the main ruleset and in
  `scripts/configure-github.sh`: GitHub signs the squash commit, so every commit of
  `main` stays verified, whereas "Rebase and merge" rewrites the commits unsigned.
  Run `scripts/configure-github.sh` again after `copier update` to apply it.

## [0.1.0] - 2026-10-20

Initial release.

### Added

- Questions for the names of the project, package and distribution, its description,
  keywords and URLs, its license (MIT or AGPL-3.0-or-later), its authors with their
  ORCID, its oldest supported Python version (following SPEC 0) and the use of Codecov.
- A `pyproject.toml` built with setuptools and setuptools-scm, a typed package in `src/`,
  and the development tools in dependency groups, locked in `uv.lock`.
- ruff, pyright and pytest with coverage, and pre-commit hooks for file hygiene,
  `.editorconfig`, codespell, zizmor, ruff, pyright and, with the AGPL, SPDX headers.
- A CI on every supported Python version and on the newest versions of the
  dependencies, with a single `ci-passed` check, and a release workflow publishing to
  TestPyPI and PyPI with trusted publishing, then creating a signed GitHub release.
- `scripts/release.py`, which turns the `[Unreleased]` changes of the changelog into a
  release and sets the version of `CITATION.cff`.
- A README, a changelog, `CITATION.cff`, a license, a code of conduct, contributing and
  security guides, issue forms, a pull request template and architecture decision
  records.
- Dependabot for the actions, the dependencies and the hooks, rulesets, and
  `scripts/configure-github.sh` to configure the GitHub repository.
- `.copier-answers.yml`, so that projects can be updated with `copier update`.

[unreleased]: https://github.com/fmargall/scientific-python-template/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/fmargall/scientific-python-template/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/fmargall/scientific-python-template/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/fmargall/scientific-python-template/releases/tag/v0.1.0

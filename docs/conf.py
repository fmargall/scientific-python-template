# Configuration of the Sphinx documentation of the template
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# Built with: uv run sphinx-build -W --keep-going -b html docs docs/_build/html

project = "Scientific Python Template"
author = "François Margall"
copyright = "2026, François Margall"
language = "en"

extensions = [
    # Markdown pages, with the Sphinx directives and roles in MyST syntax
    "myst_parser",
]

# The build output must never be read back as sources
exclude_patterns = ["_build"]

# Every reference that does not resolve is a warning, so a failure with -W:
# no broken link reaches the published documentation
nitpicky = True

# -- MyST ---------------------------------------------------------------------

myst_enable_extensions = [
    # Directives written as :::{note} ... ::: are still readable on GitHub,
    # where ```{note} blocks show up as code
    "colon_fence",
]
# Anchors for the headings up to level 3, so that [text](page.md#a-heading)
# links work as they do on GitHub
myst_heading_anchors = 3

# -- HTML output --------------------------------------------------------------

html_theme = "pydata_sphinx_theme"
html_title = project
html_theme_options = {
    # Icons at the top right. The template is only used from GitHub: it is not
    # published on PyPI nor conda-forge, so it has no link to them
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/fmargall/scientific-python-template",
            "icon": "fa-brands fa-github",
        },
    ],
}

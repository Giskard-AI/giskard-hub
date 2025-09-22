# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import inspect
import os
import sys
from dataclasses import asdict
from datetime import datetime

from sphinxawesome_theme import ThemeOptions
from sphinxawesome_theme.postprocess import Icons

html_permalinks_icon = Icons.permalinks_icon

project = "Giskard"
copyright = f"{datetime.now().year}, Giskard"
author = "Giskard"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

sys.path.append(os.path.abspath("./sphinx_ext"))

extensions = [
    "myst_parser",
    "nbsphinx",
    "sphinx_design",
    "sphinx.ext.todo",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.linkcode",
    "sphinx.ext.githubpages",
    "sphinx_click",
    "fix_dataclass",
    "sphinx_tabs.tabs",
    "sphinxext.opengraph",
    "notfound.extension",
    # "sphinx_autodoc_typehints",
]

myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

# Resolve Dataset cross-reference ambiguity
autodoc_type_aliases = {
    "Dataset": "giskard.Dataset",
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "README.md"]

pygments_style = "lovelace"
# To generate the dark theme, run the following command:
# pygmentize -S one-dark -f html -a .dark > _static/pygments-dark.css

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = "sphinxawesome_theme"
# html_theme = 'alabaster'
html_static_path = ["_static"]
source_suffix = [".rst", ".md"]

html_css_files = ["pygments-dark.css", "custom.css"]
html_js_files = ["custom.js"]
html_favicon = "_static/favicon.ico"

# Do not execute the notebooks when building the docs
docs_version = os.getenv("READTHEDOCS_VERSION", "latest")
if docs_version == "latest" or docs_version == "stable":
    branch = "main"
else:
    branch = docs_version.replace("-", "/")
branch = "main"

# -- Options for nbsphinx ----------------------------------------------------
nbsphinx_execute = "never"
# fmt: off
nbsphinx_prolog = """
.. raw:: html

    <div class="open-in-colab__wrapper">
    <a href="https://colab.research.google.com/github/Giskard-AI/giskard-hub/blob/""" + branch + """/script-docs/{{ env.doc2path(env.docname, base=None) }}" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" style="display: inline; margin: 0" alt="Open In Colab"/></a>
    <a href="https://github.com/Giskard-AI/giskard-hub/tree/""" + branch + """/script-docs/{{ env.doc2path(env.docname, base=None) }}" target="_blank"><img src="https://img.shields.io/badge/github-view%20source-black.svg" style="display: inline; margin: 0" alt="View Notebook on GitHub"/></a>
    </div>
"""
# fmt: on

theme_options = ThemeOptions(
    show_prev_next=True,
    show_scrolltop=True,
    awesome_external_links=True,
    logo_light="_static/logo_light.png",
    logo_dark="_static/logo_dark.png",
    main_nav_links={
        "Getting Started": "/index",
        "Hub UI": "/hub/ui/index",
        "Hub SDK": "/hub/sdk/index",
        "Open Source": "/oss/sdk/index",
    },
)
html_theme_options = asdict(theme_options)
# -- Open Graph configuration -------------------------------------------------
# https://sphinxext-opengraph.readthedocs.io/en/latest/

# Open Graph site name
ogp_site_name = "Giskard Documentation"
ogp_site_url = "https://docs-hub.giskard.ai/"

# Open Graph image (logo for social sharing) - use relative path for local builds
ogp_image = "https://docs-hub.giskard.ai/_static/open-graph-image.png"


# make github links resolve
def linkcode_resolve(domain, info):
    if domain != "py":
        return None

    modname = info["module"]
    fullname = info["fullname"]
    print("##############")
    print(f"modname:{modname}")
    print(f"fullname:{fullname}")

    submod = sys.modules.get(modname)
    # print(submod)
    if submod is None:
        print("##############")

        return None
    obj = submod
    for part in fullname.split("."):
        try:
            obj = getattr(obj, part)
            print(f"obj:{obj}")

            # print(obj)
        except:  # noqa: E722
            print("##############")
            return None

    try:
        fn = inspect.getsourcefile(
            obj.test_fn if hasattr(obj, "test_fn") else obj
        )  # TODO: generalise for other objects!
    # print(fn)
    except:  # noqa: E722
        fn = None
    if not fn:
        print("##############")

        return None
    print(f"fn:{fn}")

    try:
        source, lineno = inspect.getsourcelines(obj)
    except:  # noqa: E722
        lineno = None

    if lineno:
        linespec = "#L%d-L%d" % (lineno, lineno + len(source) - 1)
    else:
        linespec = ""
    print(f"linespec:{linespec}")

    filename = fn.split("giskard_hub")[-1]
    print("##############")

    return f"https://github.com/Giskard-AI/giskard-hub/blob/main/src/giskard_hub{filename}{linespec}"


# Make 404 page work
notfound_urls_prefix = None

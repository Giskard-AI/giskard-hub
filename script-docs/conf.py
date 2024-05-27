# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import inspect
import sys

project = "Hub client"
copyright = "2024, Giskard"
author = "Giskard"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    "myst_parser",
    "sphinxawesome_theme.highlighting",
    # "nbsphinx",
    # "sphinx_design",
    "sphinx.ext.todo",
    "sphinx.ext.napoleon",
    "sphinx.ext.autodoc",
    "sphinx.ext.linkcode",
    "sphinx.ext.githubpages",
    "sphinx_click",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = "sphinxawesome_theme"
# html_theme = 'alabaster'
html_static_path = ["_static"]
source_suffix = [".rst", ".md", ".ipynb"]
html_theme_options = {
    "logo_light": "_static/logo_black.png",
    "logo_dark": "_static/logo_white.png",
}
html_favicon = "_static/favicon.ico"


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

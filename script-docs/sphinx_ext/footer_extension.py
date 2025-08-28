"""Sphinx extension to add footer text to all pages.

This extension adds a customizable footer text segment at the bottom of each page
in the hub documentation.
"""

from typing import Any, Dict

from sphinx.application import Sphinx


def add_footer_text(
    app: Sphinx, pagename: str, templatename: str, context: Dict[str, Any], doctree: Any
) -> None:
    """Add footer text to the page context.

    This function is called for each page during the HTML build process.
    It adds a footer_text variable to the context that will be rendered
    in the HTML template.
    """
    # Add footer text to the context
    context["footer_text"] = app.config.footer_text


def setup(app: Sphinx) -> None:
    """Set up the footer extension.

    This function is called by Sphinx to register the extension.
    """
    # Add configuration option for footer text
    app.add_config_value("footer_text", "", "html")

    # Connect the function to the html-page-context event
    app.connect("html-page-context", add_footer_text)

    return {
        "version": "1.0.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }

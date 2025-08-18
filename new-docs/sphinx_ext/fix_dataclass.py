"""Fix dataclass typing.

Source: https://github.com/sphinx-doc/sphinx/issues/10893#issuecomment-1885043306
"""

from dataclasses import is_dataclass


def process_signature(app, what, name, obj, options, signature, return_annotation):
    if what == "class" and is_dataclass(obj):
        return signature.replace("<factory>", "..."), return_annotation


def setup(app):
    app.connect("autodoc-process-signature", process_signature)

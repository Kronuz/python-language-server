# Copyright 2017 Palantir Technologies, Inc.
import logging
from pyls import hookimpl, _utils

log = logging.getLogger(__name__)


@hookimpl
def pyls_hover(document, position):
    definitions = document.jedi_script(position).goto_definitions()
    word = document.word_at_position(position)

    # Find an exact match for a completion
    definitions = [d for d in definitions if d.name == word]

    if not definitions:
        # :(
        return {'contents': ''}

    contents = definitions[0].docstring().split('\n\n') or ""
    contents[0] = {'value': contents[0], 'language': 'python'}
    contents = contents[:1] + list(map(_utils.format_docstring, contents[1:]))
    return {'contents': contents}

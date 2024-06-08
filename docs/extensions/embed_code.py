from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives import unchanged

class EmbedCodeDirective(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    option_spec = {
        'language': unchanged,
    }

    def run(self):
        language = self.options.get('language', 'python')
        code = '\n'.join(self.content)
        
        literal = nodes.literal_block(code, code)
        literal['language'] = language

        return [literal]

def setup(app):
    app.add_directive('embed_code', EmbedCodeDirective)
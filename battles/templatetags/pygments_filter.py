from django import template
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import PythonLexer

register = template.Library()


@register.filter(name='pygmentize')
def pygmentize(code):
    formatter = HtmlFormatter(style='monokai', linenos='inline')
    return highlight(code, PythonLexer(), formatter)
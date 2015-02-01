from django.template import Library
register = Library()
import markdown


@register.filter(is_safe=True)
def md(_md):
    return markdown.markdown(_md, extensions=['markdown.extensions.nl2br', 'markdown.extensions.toc', 'markdown.extensions.fenced_code', 'markdown.extensions.footnotes', 'markdown.extensions.tables', 'markdown.extensions.wikilinks'])

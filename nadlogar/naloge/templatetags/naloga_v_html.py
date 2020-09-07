from django import template
from django.utils.safestring import mark_safe
from ..generatorji.html_generator import HtmlGenerator

register = template.Library()

@register.filter(name='naloga_v_html', is_safe=True)
def naloga_v_html(generator_nalog):
    try:
        html = HtmlGenerator.generiraj_html(generator_nalog)
        if html is None:
            return mark_safe('<p>HTML generator ne zna zgenerirati naloge.</p>')
        return mark_safe(html.decode('utf-8'))
    except Exception as e:
        return mark_safe('<p><strong>Napaka pri generiranju naloge</strong>: {}.</p>'.format(e))
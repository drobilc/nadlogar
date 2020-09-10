from django import template
from django.utils.safestring import mark_safe
from ..generatorji.html_generator import HtmlGenerator
from ..generatorji.obrazec_generator import ObrazecGenerator

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

@register.filter(name='naloga_urejanje_obrazec')
def naloga_urejanje_obrazec(naloga):
    return ObrazecGenerator.generiraj_obrazec(naloga.generator_nalog())
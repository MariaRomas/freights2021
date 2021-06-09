from django import template
from freights.models import Category, Freight


register = template.Library()


@register.simple_tag()
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()

@register.inclusion_tag('freights/tags/last_freight.html')
def get_last_freights(count=5):
    freights = Freight.objects.order_by("id")[:count]
    return {"last_freights": freights}



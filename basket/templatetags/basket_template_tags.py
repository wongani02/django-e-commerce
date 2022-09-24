from django import template
from checkout.models import DeliveryOptions

register = template.Library()


@register.inclusion_tag('basket/delivery_tag.html')
def delivery_tag(count=3):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    
    return {"deliveryoptions": deliveryoptions,}



from django.shortcuts import render, get_object_or_404
from .basket import Basket
from store.models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from checkout.models import DeliveryOptions

# Create your views here.


def basket_summary(request):
    basket = Basket(request)
    context={
        'basket': basket,
    }
    return render(request, 'basket/cart.html', context)

def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action')=='post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)
        basketqty = basket.__len__()
        # print(basketqty)   
        response = JsonResponse({'quantity': basketqty})
        # print(response)
        return response

def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action')=='post':
        product_id = int(request.POST.get('productid'))
        # print(product_id)
        basket.delete(product=product_id)
        basket_total = basket.get_total_price()
        basket_qty = basket.__len__()
        response = JsonResponse({'qty': basket_qty, 'total': basket_total})
        # print(response)
        return response

def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action')=='post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        print(product_id)
        print(product_qty)
        basket.update(product=product_id, qty=product_qty)
        basket_qty = basket.__len__()
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty': basket_qty, 'total': basket_total})
        print(response)
        return response


#checkout views
@login_required
def delivery_choices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    context = {
        "deliveryoptions": deliveryoptions,
    }

    return render(request, "basket/proceed-to-checkout.html", context)

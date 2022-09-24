from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import *
from django.utils import timezone

# Create your views here.


def home(request):
    # products = Product.objects.all()
    products = Product.objects.prefetch_related("product_image").filter(is_active=True)
    context = {
        'products': products
    }
    return render(request, 'store/index.html', context)


def categories(request):

    ''' 
    This view is accesible from all pages because it is
    added to the context manager in the settings.py file
    '''

    return {'category': Category.objects.filter(level=0),}


def product_detail(request, pk):

    '''
    Single product view
    '''

    product = get_object_or_404(Product, pk=pk, is_active=True)
    context = {
        'product': product,
    }
    return render(request, 'store/product-details-affiliate.html', context)


def product_category(request, category_slug):

    '''
    View to filter products by category
    consists of mptt queries
    '''

    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(
        category__in=Category.objects.get(name=category_slug).get_descendants(include_self=True)
        )
    context = {
        'products': products,
        'category_name': category,
    }
    return render(request, 'store/shop-no-sidebar.html', context)


'''
Download degital product function
'''
def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open (file_path, 'rb')as fh:
            response = HttpResponse(fh.read(), content_type="application/digital_product")
            response['Content-Desposition']='inline;filename='+os.path.basename(file_path)
            return response
    raise http404
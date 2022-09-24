from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, UserEditForm, UserAddressForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str #force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse

from .token import account_activation_token
from .models import Customer, Address
from store.models import Product

from order.models import Order

import os
from django.conf import settings
from django.http import HttpResponse, Http404

# Create your views here.


def account_register(request):
    
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.email = register_form.cleaned_data['email']
            user.set_password(register_form.cleaned_data['password'])
            user.is_active = False
            user.save()
            
            #setup email
            current_site = get_current_site(request)
            subject = "Activate your account"
            message = render_to_string('accounts/account-activation-email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('your account has been created, please check your email to verify your account')
    
    else:
        register_form = UserRegistrationForm()
    
    return render(request, 'accounts/login-register.html', {'form': register_form})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('accounts:dashboard')
    else:
        return render(request, 'accounts/activation-invalid.html')


#dashboard section
@login_required
def user_dashboard(request):
    context = {

    }
    return render(request, 'accounts/my-account.html', context)


@login_required
def edit_details(request):
    user = request.user
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('accounts:edit-details')
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'accounts/edit-details.html', {'user_form': user_form, 'user': user})


@login_required
def orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/orders.html', context)


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open (file_path, 'rb')as fh:
            response = HttpResponse(fh.read(), content_type="application/digital_product")
            response['Content-Desposition']='inline;filename='+os.path.basename(file_path)
            return response
    raise http404


@login_required
def user_downloads(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/download.html', context)


@login_required
def settings(request):
    return render(request, 'accounts/settings.html')


@login_required
def delete_user(request):
    user = Customer.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('accounts:delete_confirmation')

def confirm_account_delete(request):
    return render(request, 'accounts/delete-confirmation.html')

#address section
@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    context = {
        'addresses': addresses,
    }
    return render(request, 'accounts/view-address.html', context)


@login_required
def add_address(request):
    if request.method=='POST':
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse('accounts:addresses'))
    else:
        address_form = UserAddressForm()
        
    return render(request, 'accounts/add-address.html', {'form': address_form})


@login_required
def edit_address(request, id):

    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("accounts:addresses"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)

    return render(request, 'accounts/edit-address.html', {"form": address_form})

@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect("account:addresses")

@login_required
def set_default(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)

    previous_url = request.META.get("HTTP_REFERER")

    if "delivery_address" in previous_url:
        return redirect("checkout:delivery_address")

    return redirect("accounts:addresses")   

#whislist section

@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, product.title + " has been removed from your WishList")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "Added " + product.title + " to your WishList")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])



@login_required
def users_wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    context = {
        'wishlist': products, 
    }
    return render(request, 'accounts/wishlist.html', context)

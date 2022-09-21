import datetime
from django.shortcuts import render,redirect,HttpResponse
from carts.models import CartItem
from .forms import OrderForm
from orders.models import Order
from django.contrib import messages
from urllib.error import URLError, HTTPError


# Create your views here.
def place_order(request,total=0,quantity=0):
    current_user = request.user

    # if the cart account is less than equal to zero redirect to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('home')
    grand_total = 0
    tax =0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = round(total * 0.06)
    grand_total = total + tax


    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            # store all the billing information inside order table
            data = Order()
            data.user           = current_user
            data.first_name     = form.cleaned_data['first_name']
            data.last_name      = form.cleaned_data['last_name']
            data.phone          = form.cleaned_data['phone']
            data.email          = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country        = form.cleaned_data['country']
            data.province       = form.cleaned_data['province']
            data.city           = form.cleaned_data['city']
            data.postal_code    = form.cleaned_data['postal_code']
            data.order_note     = form.cleaned_data['order_note']
            data.order_total    = grand_total
            data.tax            = tax
            data.ip             = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number 
            current_date = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
            order_number = current_date+str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            context={
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total
            }
            return render(request,'orders/payments.html',context)
        else:
            messages.error(request,'Invalid Email')
            return redirect('carts:checkout')


def payments(request):
    context={
        'title':'Payment | page',
    }
    return render(request,'orders/payments.html',context)
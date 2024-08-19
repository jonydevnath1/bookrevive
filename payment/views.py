from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from payment.forms import ShippingFrom, PaymentForm , ProductForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product, Profile
import datetime
from django.db.models import Sum

# Create your views here.
def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    subtotals = cart.cart_total()
    shipping_fee = 60
    totals = subtotals + shipping_fee

    if request.user.is_authenticated:
        # checkout as logged in user
        # shipping user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Shipping form
        shipping_form = ShippingFrom(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html", {"cart_products": cart_products, "quantities": quantities, "subtotals": subtotals, "shipping_fee": shipping_fee, "totals": totals, "shipping_form": shipping_form })
    else:
        # checkout as guest
        shipping_form = ShippingFrom(request.POST or None)
        return render(request, "payment/checkout.html", {"cart_products": cart_products, "quantities": quantities, "subtotals": subtotals, "shipping_fee": shipping_fee, "totals": totals, "shipping_form": shipping_form })

def payment_success(request):
    return render(request, "payment/payment_success.html", {})

# def process_order(request):
    if request.method == 'POST':
        # Create a session with shipping info
        shipping = request.POST.dict()  # Convert QueryDict to a regular dictionary
        request.session['shipping'] = shipping

        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        subtotals = cart.cart_total()
        shipping_fee = 60
        totals = subtotals + shipping_fee

        # Get shipping session data
        shipping = request.session.get('shipping')
        
        # Gather order info
        full_name = shipping.get('shipping_full_name')
        phone = shipping.get('shipping_phone')
        email = shipping.get('shipping_email')

        # Create shipping address from session info
        shipping_address = (
            f"{shipping.get('shipping_address1', '')} \n"
            f"{shipping.get('shipping_address2', '')} \n"
            f"{shipping.get('shipping_city', '')} \n"
            f"{shipping.get('shipping_state', '')} \n"
            f"{shipping.get('shipping_zipcode', '')} \n"
            f"{shipping.get('shipping_country', '')}"
        )
        amount_paid = totals

        # Get the payment method from the shipping data
        payment_method = shipping.get('payment_method')

        # Ensure payment_method is not None
        if payment_method:
            payment_method = payment_method.upper()
            payment_status = 'Unpaid' if payment_method == 'COD' else 'verifying'
        else:
            payment_status = 'Unknown'

        # Create the order
        if request.user.is_authenticated:
            user = request.user
            try:
                create_order = Order(
                    user=user,
                    phone=phone,
                    full_name=full_name,
                    email=email,
                    shipping_address=shipping_address,
                    amount_paid=amount_paid,
                    payment_method=payment_method,
                    payment_status=payment_status
                )
                create_order.save()

                # Add order items
                for product in cart_products:
                    product_id = product.id
                    price = product.sale_price if product.is_sale else product.price
                    quantity = quantities.get(str(product_id), 0)
                    
                    # Create and save the order item
                    create_order_item = OrderItem(
                        order=create_order,
                        product=product,
                        user=user,
                        quantity=quantity,
                        price=price
                    )
                    create_order_item.save()

                # delete the cart
                for key in list(request.session.keys()):
                    if key == "session_key":
                        # Delete the key
                        del request.session[key]

                # delete cart from Database (old card field)
                current_user = Profile.objects.filter()
                # delete shopping cart in database (old_cart field)
                current_user.update(old_cart="")
                messages.error(request, "Order Placed")

                return render(request, "payment/process_order.html", {})
            except TypeError as e:
                messages.error(request, f"Order creation failed: {e}")
                return redirect('home')
        else:
            try:
                create_order = Order(
                    full_name=full_name,
                    email=email,
                    shipping_address=shipping_address,
                    amount_paid=amount_paid,
                    payment_method=payment_method,
                    payment_status=payment_status
                )
                create_order.save()

                # Add order items
                for product in cart_products:
                    product_id = product.id
                    price = product.sale_price if product.is_sale else product.price
                    quantity = quantities.get(str(product_id), 0)
                    
                    create_order_item = OrderItem(
                        order=create_order,
                        product=product,
                        quantity=quantity,
                        price=price
                    )
                    create_order_item.save()
                
                # delete the cart
                for key in list(request.session.keys()):
                    if key == "session_key":
                        # Delete the key
                        del request.session[key]

                messages.error(request, "Order Placed")
                return render(request, "payment/process_order.html", {})
            except TypeError as e:
                messages.error(request, f"Order creation failed: {e}")
                return redirect('checkout')
    else:
        messages.error(request, "Access Denied")
        return redirect('home')

def process_order(request):
    if request.method == 'POST':
        # Create a session with shipping info
        shipping = request.POST.dict()  # Convert QueryDict to a regular dictionary
        request.session['shipping'] = shipping

        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        subtotals = cart.cart_total()
        shipping_fee = 60
        totals = subtotals + shipping_fee

        # Get shipping session data
        shipping = request.session.get('shipping')
        
        # Gather order info
        full_name = shipping.get('shipping_full_name')
        phone = shipping.get('shipping_phone')
        email = shipping.get('shipping_email')

        # Create shipping address from session info
        shipping_address = (
            f"{shipping.get('shipping_address1', '')} \n"
            f"{shipping.get('shipping_address2', '')} \n"
            f"{shipping.get('shipping_city', '')} \n"
            f"{shipping.get('shipping_state', '')} \n"
            f"{shipping.get('shipping_zipcode', '')} \n"
            f"{shipping.get('shipping_country', '')}"
        )
        amount_paid = totals

        # Get the payment method from the shipping data
        payment_method = shipping.get('payment_method')

        # Ensure payment_method is not None
        if payment_method:
            payment_method = payment_method.upper()
            payment_status = 'Unpaid' if payment_method == 'COD' else 'verifying'
        else:
            payment_status = 'Unknown'

        # Create the order
        if request.user.is_authenticated:
            user = request.user
            try:
                create_order = Order(
                    user=user,
                    phone=phone,
                    full_name=full_name,
                    email=email,
                    shipping_address=shipping_address,
                    amount_paid=amount_paid,
                    payment_method=payment_method,
                    payment_status=payment_status
                )
                create_order.save()

                # Add order items
                order_items = []
                for product in cart_products:
                    product_id = product.id
                    price = product.sale_price if product.is_sale else product.price
                    quantity = quantities.get(str(product_id), 0)
                    
                    # Create and save the order item
                    create_order_item = OrderItem(
                        order=create_order,
                        product=product,
                        user=user,
                        quantity=quantity,
                        price=price
                    )
                    create_order_item.save()
                    order_items.append(create_order_item)

                # Clear the cart in session and database
                for key in list(request.session.keys()):
                    if key == "session_key":
                        del request.session[key]

                current_user = Profile.objects.filter()
                current_user.update(old_cart="")
                
                
                # Pass the order data and order items to the template
                context = {
                    'order': create_order,
                    'order_items': order_items,
                    'totals': totals,
                    'shipping_fee': shipping_fee,
                    'subtotals': subtotals,
                }
                return render(request, "payment/process_order.html", context)

            except TypeError as e:
                messages.error(request, f"Order creation failed: {e}")
                return redirect('home')
        else:
            try:
                create_order = Order(
                    full_name=full_name,
                    email=email,
                    shipping_address=shipping_address,
                    amount_paid=amount_paid,
                    payment_method=payment_method,
                    payment_status=payment_status
                )
                create_order.save()

                # Add order items
                order_items = []
                for product in cart_products:
                    product_id = product.id
                    price = product.sale_price if product.is_sale else product.price
                    quantity = quantities.get(str(product_id), 0)
                    
                    create_order_item = OrderItem(
                        order=create_order,
                        product=product,
                        quantity=quantity,
                        price=price
                    )
                    create_order_item.save()
                    order_items.append(create_order_item)

                # Clear the cart in session
                for key in list(request.session.keys()):
                    if key == "session_key":
                        del request.session[key]
                
                context = {
                    'order': create_order,
                    'order_items': order_items,
                    'totals': totals,
                    'shipping_fee': shipping_fee,
                    'subtotals': subtotals,
                }
                return render(request, "payment/process_order.html", context)

            except TypeError as e:
                messages.error(request, f"Order creation failed: {e}")
                return redirect('checkout')
    else:
        messages.error(request, "Access Denied")
        return redirect('home')


def dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get counts of each type of order
        total_orders = Order.objects.count()

        # Assuming 'shipped' is a boolean field for active/completed orders
        active_orders = Order.objects.filter(shipped=False).count()
        completed_orders = Order.objects.filter(shipped=True).count()

        # Calculate the total amount paid across all orders
        total_amount_paid = Order.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0

        # Query for active orders
        orders = Order.objects.filter(shipped=False)

        # Combine all context data into a single dictionary
        context = {
            'total_orders': total_orders,
            'active_orders': active_orders,
            'completed_orders': completed_orders,
            'total_amount_paid': total_amount_paid,
            'orders': orders,  # Include the orders in the context
        }

        return render(request, "payment/dashboard.html", context)
    else:
        messages.error(request, "Access Denied")
        return redirect('home')



def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)

        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            # grab date and time
            now = datetime.datetime.now()
            # get the order
            order = Order.objects.filter(id=num)
            # update order
            order.update(shipped=True, date_shipped = now)
            return redirect('shipped_dash')

        return render(request, "payment/not_shipped_dash.html", {'orders': orders})
    else:
        messages.error(request, "Access Denied")
        return redirect('home')
    
def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)

        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            # grab date and time
            now = datetime.datetime.now()
            # get the order
            order = Order.objects.filter(id=num)
            # update order
            order.update(shipped=False, date_shipped = now)
            return redirect('not_shipped_dash')

        return render(request, "payment/shipped_dash.html", {'orders': orders})
    else:
        messages.error(request, "Access Denied")
        return redirect('home')
    
# def orders(request, pk):
#     if request.user.is_authenticated and request.user.is_superuser:
#         # get the order
#         order = Order.objects.get(id=pk)
#         # get the order items
#         items = OrderItem.objects.filter(order=pk)

#         if request.POST:
#             status = request.POST['shipping_status']
#             # Check if true or false
#             if status == "true":
#                 # get the order
#                 order = Order.objects.filter(id=pk)
#                 # Update the status
#                 now = datetime.datetime.now()
#                 order.update(shipped=True, date_shipped = now)
#                 return redirect('shipped_dash')
#             else:
#                 # get the order
#                 order = Order.objects.filter(id=pk)
#                 # Update the status
#                 now = datetime.datetime.now()
#                 order.update(shipped=False, date_shipped = now)
#                 return redirect('not_shipped_dash')

#         return render(request, "payment/orders.html", {'order': order, 'items': items})

#     else:
#         messages.error(request, "Access Denied")
#         return redirect('home')
    
def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # get the order
        order = Order.objects.get(id=pk)
        # get the order items
        items = OrderItem.objects.filter(order=pk)

        # Add a total_price attribute to each item
        for item in items:
            item.total_price = item.price * item.quantity

        if request.POST:
            status = request.POST['shipping_status']
            # Check if true or false
            if status == "true":
                # get the order
                order = Order.objects.filter(id=pk)
                # Update the status
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
                return redirect('shipped_dash')
            else:
                # get the order
                order = Order.objects.filter(id=pk)
                # Update the status
                now = datetime.datetime.now()
                order.update(shipped=False, date_shipped=now)
                return redirect('not_shipped_dash')

        return render(request, "payment/orders.html", {'order': order, 'items': items})

    else:
        messages.error(request, "Access Denied")
        return redirect('home')


def all_products(request):
    products = Product.objects.all()  # Fetch all products
    return render(request, 'payment/all_products.html', {'products': products})

def upload_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Uploaded!")
            return redirect('all_products')  # Redirect to a list of all products after upload
    else:
        form = ProductForm()
    
    return render(request, 'payment/upload_product.html', {'form': form})

# Edit product view
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Editted!")
            return redirect('all_products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'payment/product_edit.html', {'form': form})

def product_delete(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    messages.success(request, "Product Deleted!")
    return redirect('all_products')
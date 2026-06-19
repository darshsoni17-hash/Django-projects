from django.shortcuts import render, get_object_or_404, redirect
from .models import chaivarity, store, Cart, CartItem, Order, chaireview
from .forms import chaivarityForm


def all_chai(request):
    chais = chaivarity.objects.all()
    form = chaivarityForm()

    return render(
        request,
        'chai/all_chai.html',
        {
            'chais': chais,
            'form': form,
        }
    )

def chai_detail(request, chai_id):
    chai = get_object_or_404(chaivarity, pk=chai_id)
    reviews = chai.reviews.all().order_by('-date_added')

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating and comment and request.user.is_authenticated:
            chaireview.objects.create(
                chai=chai,
                user=request.user,
                rating=int(rating),
                comment=comment,
            )
            return redirect('chai_detail', chai_id=chai.id)

    return render(
        request,
        'chai/chai_detail.html',
        {
            'chai': chai,
            'reviews': reviews,
        }
    )


def chai_store_view(request):
    stores = None

    if request.method == 'POST':
        form = chaivarityForm(request.POST)

        if form.is_valid():
            chai_varity = form.cleaned_data['chai_varity']
            stores = store.objects.filter(chai_varities=chai_varity)

    else:
        form = chaivarityForm()

    return render(
        request,
        'chai/chai_store.html',
        {
            'stores': stores,
            'form': form,
        }
    )
def get_cart(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def add_to_cart(request, chai_id):
    chai = get_object_or_404(chaivarity, pk=chai_id)
    cart = get_cart(request)

    item, created = CartItem.objects.get_or_create(cart=cart, chai=chai)
    if not created:
        item.quantity += 1
        item.save()

    return redirect('view_cart')


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    item.delete()
    return redirect('view_cart')


def view_cart(request):
    cart = get_cart(request)
    return render(request, 'chai/cart.html', {'cart': cart})  


def update_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)

    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity and quantity.isdigit() and int(quantity) > 0:
            item.quantity = int(quantity)
            item.save()
        elif quantity == '0':
            item.delete()

    return redirect('view_cart')

def checkout(request):
    cart = get_cart(request)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        order = Order.objects.create(
            session_key=request.session.session_key,
            payment_method=payment_method,
            subtotal=cart.total_price(),
            gst=cart.total_gst(),
            grand_total=cart.grand_total(),
        )

        cart.items.all().delete()  # empty the cart after order placed

        return render(request, 'chai/order_success.html', {'order': order})

    return render(request, 'chai/checkout.html', {'cart': cart})
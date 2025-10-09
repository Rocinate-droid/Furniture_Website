import uuid
from .models import Room
from .models import Cart, CartItem


def room_types(request):
    rooms = Room.objects.all()
    return {'rooms': rooms}

def view_cart_common(request):
    user_id = request.session.get('user_id')
    if request.user.is_authenticated:
        cartcreated, created = Cart.objects.get_or_create(customer=request.user)
        cart_items = CartItem.objects.filter(cart=cartcreated)
    else:
        if 'user_id' in request.session:
            user_id = request.session.get('user_id')
        else:
            request.session['user_id'] = int(uuid.uuid4())
            user_id = request.session.get('user_id')
        cartcreated, created = Cart.objects.get_or_create(anonymous=user_id)
        cart_items = CartItem.objects.filter(cart=cartcreated)
    total_amount = 0
    total_original = 0
    discount = 0
    delivery = None
    grand_total = 0
    for item in cart_items:
        if item.product:
            total_original += item.product.original_price * item.quantity
            discount += (item.product.original_price - item.product.discounted_price) * item.quantity
        total_amount += item.total_cost
        grand_total += item.total_cost
    if grand_total >= 50000:
        delivery = "Free Delivery"
    else:
        delivery = 999
        grand_total += delivery
    context = {'cart_items' : cart_items, 'total_amount' : total_amount, 'total_original' : total_original, 'discount' : discount, 'delivery': delivery, 'grand_total' : grand_total }
    return context 
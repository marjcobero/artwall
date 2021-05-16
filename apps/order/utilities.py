from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from apps.cart.cart import Cart
from .models import Order, OrderItem


def checkout(request, first_name, last_name, email, address, city, zipcode, state, phone, amount):
    order = Order.objects.create(
        first_name=first_name, 
        last_name=last_name, 
        email=email, 
        address=address, 
        city=city,
        zipcode=zipcode, 
        state=state, 
        phone=phone, 
        paid_amount=amount
        )
    for item in Cart(request):
        OrderItem.objects.create(
            order=order, 
            artwork=item['artwork'], 
            artist=item['product'].artist, 
            price=item['product'].price, 
            quantity=item['quantity']
            )
        order.artists.add(item['artwork'].artist)
    return order

def notify_artist(order):
    from_email = settings.DEFAULT_EMAIL_FROM
    for artist in order.artits.all():
        to_email = artist.created_by.email
        subject = 'New order'
        text_content = 'You have a new order!'
        html_content = render_to_string('order/email_notify_artist.html', {'order': order, 'artist': artist})
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

def notify_customer(order):
    from_email = settings.DEFAULT_EMAIL_FROM
    to_email = order.email
    subject = 'Order confirmation'
    text_content = 'Thank you for the order!'
    html_content = render_to_string('order/email_notify_customer.html', {'order': order})
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
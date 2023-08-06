from django.shortcuts import redirect

from django_scopes import scope
from pretix.base.models import Order, OrderPayment, Organizer
from pretix.base.payment import PaymentException
from pretix.base.settings import GlobalSettingsObject
from pretix.multidomain.urlreverse import eventreverse

from .bambora import BamboraPayformClient


def bambora_callback(request, organizer_id=None, payment_id=None):
    gs = GlobalSettingsObject()
    api_key = gs.settings.get('payment_bambora_payform_api_key')
    private_key = gs.settings.get('payment_bambora_payform_private_key')

    client = BamboraPayformClient(api_key, private_key)

    if not client.validate_callback_request(request):
        raise PaymentException('Invalid request')

    return_code = request.GET.get('RETURN_CODE')
    settled = request.GET.get('SETTLED')
    order_number = request.GET.get('ORDER_NUMBER')
    order_code = order_number.split('_')[0]

    try:
        organizer = Organizer.objects.get(id=organizer_id)
        with scope(organizer=organizer):
            payment = OrderPayment.objects.get(id=payment_id)
            order = payment.order
            if payment.order.code != order_code:
                raise PaymentException('Invalid request')

            if return_code == '0' and settled == '1':
                payment.confirm()
                order.refresh_from_db()

            redirect_url = eventreverse(order.event, 'presale:event.order', kwargs={
                'order': order.code,
                'secret': order.secret
            }) + ('?paid=yes' if order.status == Order.STATUS_PAID else '')

            return redirect(redirect_url)
    except Order.DoesNotExist:
        raise Exception('asd')

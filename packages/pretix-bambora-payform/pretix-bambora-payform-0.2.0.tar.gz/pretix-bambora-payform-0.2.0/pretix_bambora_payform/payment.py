from secrets import token_urlsafe

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from pretix.base.payment import BasePaymentProvider
from pretix.base.settings import GlobalSettingsObject

from .bambora import BamboraPayformClient


class BamboraPayformProvider(BasePaymentProvider):
    def __init__(self, event):
        super().__init__(event)

        gs = GlobalSettingsObject()
        self.client = BamboraPayformClient(
            gs.settings.get('payment_bambora_payform_api_key'),
            gs.settings.get('payment_bambora_payform_private_key')
        )

    def checkout_confirm_render(self, request):
        return _('You will be redirected to Bambora Payform to complete the payment')

    def execute_payment(self, request, payment):
        callback_url = request.build_absolute_uri(
            reverse(
                'plugins:pretix_bambora_payform:bambora_callback',
                kwargs={
                    'payment_id': payment.id,
                    'organizer_id': payment.order.event.organizer.id,
                }
            )
        )

        order_number = '{}_{}'.format(payment.order.code, token_urlsafe(16))
        token = self.client.get_token(
            order_number=order_number,
            amount=int(payment.amount * 100),
            email=payment.order.email,
            callback_url=callback_url,
        )

        return self.client.payment_url(token)

    @property
    def identifier(self):
        return 'bambora_payform'

    def payment_is_valid_session(self, request):
        return True

    def payment_form_render(self, request, total):
        methods = self.client.get_payment_methods()['payment_methods']
        grouped_methods = {}
        for method in methods:
            normalized_name = method['name'].lower().replace(' ', '')
            method['local_img'] = 'pretix_bambora_payform/payment_methods/{}.png'.format(normalized_name)

            if not method['group'] in grouped_methods.keys():
                grouped_methods[method['group']] = []

            grouped_methods[method['group']].append(method)

        html = render_to_string(
            'pretix_bambora_payform/payment_form.html',
            {'grouped_methods': grouped_methods}
        )

        return html

    @property
    def public_name(self):
        return '{} – {}'.format(_('Bank and credit card payments'), self.verbose_name)

    @property
    def verbose_name(self):
        return 'Bambora Payform'

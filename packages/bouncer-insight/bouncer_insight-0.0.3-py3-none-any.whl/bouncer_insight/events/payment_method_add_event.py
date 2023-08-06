from bouncer_insight.events import Address
from bouncer_insight.events.base import Base

CARD = 'card'
PAYPAL = 'paypal'
PAYMENT_METHOD_TYPES = {
    CARD, PAYPAL
}


def _validate_payment_method_add_event(payment_method_add):
    if not payment_method_add.payment_method_type in PAYMENT_METHOD_TYPES:
        raise TypeError("payment_method_type '{}' not one of expected type {}".format(
            payment_method_add.payment_method_type, PAYMENT_METHOD_TYPES))

    if payment_method_add.payment_method_type == CARD and not payment_method_add.card:
        raise ValueError("payment_method_type set as CARD but no 'card' data found")

    if payment_method_add.payment_method_type == PAYPAL and not payment_method_add.paypal:
        raise ValueError("payment_method_type set as PAYPAL but no 'paypal' data found")

    if payment_method_add.paypal and payment_method_add.card:
        raise ValueError("Multiple payment method data types found")


class Card(Base):
    def __init__(self, card_brand=None, card_funding=None, card_fingerprint=None, card_last4=None,
                 card_exp_month=None, card_exp_year=None, card_name=None, card_address=None, card_cvc_check=None,
                 card_zip_check=None):
        """
        :type card_brand: str
        :type card_funding: str
        :type card_fingerprint: str
        :type card_bin: str
        :type card_last4: str
        :type card_exp_month: str
        :type card_exp_year: str
        :type card_name: str
        :type card_address: Address
        :type card_cvc_check: str
        :type card_zip_check: str
        :param card_brand: Visa, Mastercard, Discover
        :param card_funding: credit, debit, or prepaid
        :param card_cvc_check: result from the provider's CVC check
        :param card_zip_check: result from the provider's ZIP check
        """
        self.card_last4 = card_last4
        self.card_cvc_check = card_cvc_check
        self.card_exp_month = card_exp_month
        self.card_zip_check = card_zip_check
        self.card_address = card_address
        self.card_fingerprint = card_fingerprint
        self.card_name = card_name
        self.card_exp_year = card_exp_year
        self.card_brand = card_brand
        self.card_funding = card_funding


class Paypal(Base):
    def __init__(self, paypal_email=None):
        """
        :type paypal_email: str
        """
        self.paypal_email = paypal_email


class PaymentMethodAddEvent(Base):
    def __init__(self, user_id, payment_method_id, payment_method_type, payment_gateway, success,
                 paypal=None, card=None, failure_type=None, decline_code=None, failure_reason=None,
                 ip_address=None, session_id=None, metadata=None):
        """
        :type user_id: str
        :type payment_method_id: str
        :type payment_method_type: str
        :type payment_gateway: str
        :type success: bool
        :type paypal: Paypal
        :type card: Card
        :type failure_type: str
        :type decline_code: str
        :type failure_reason: str
        :type ip_address: str
        :type session_id: str
        :type metadata: dict
        """
        self.user_id = user_id
        self.payment_method_id = payment_method_id
        self.payment_method_type = payment_method_type
        self.payment_gateway = payment_gateway
        self.success = success
        self.paypal = paypal
        self.card = card
        self.failure_type = failure_type
        self.decline_code = decline_code
        self.failure_reason = failure_reason
        self.ip_address = ip_address
        self.session_id = session_id
        self.metadata = metadata

        _validate_payment_method_add_event(self)

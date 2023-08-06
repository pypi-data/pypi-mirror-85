from bouncer_insight.events import Address, Base


class UserUpdateEvent(Base):
    def __init__(self, user_id, new_username=None, new_phone_number=None, new_email=None, new_shipping_address=None,
                 new_billing_address=None, new_first_name=None, new_last_name=None, new_full_name=None,
                 changed_password=False, ip_address=None,session_id=None, metadata=None):
        """
        :type user_id: str
        :type username: str
        :type phone_number: str
        :type email: str
        :type shipping_address: Address
        :type billing_address: Address
        :type first_name: str
        :type last_name: str
        :type full_name: str
        :type changed_password: bool
        :type changed_username: bool
        :type ip_address: str
        :type session_id: str
        :type metadata: dict
        """
        self.changed_password = changed_password
        self.user_id = user_id
        self.username = new_username
        self.phone_number = new_phone_number
        self.email = new_email
        self.shipping_address = new_shipping_address
        self.billing_address = new_billing_address
        self.first_name = new_first_name
        self.last_name = new_last_name
        self.full_name = new_full_name
        self.ip_address = ip_address
        self.session_id = session_id
        self.metadata = metadata

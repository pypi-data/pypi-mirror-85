from bouncer_insight.events import Address, Base


class UserCreateEvent(Base):
    def __init__(self, user_id, username, phone_number=None, email=None, shipping_address=None,
                 billing_address=None, first_name=None, last_name=None, full_name=None, ip_address=None,
                 session_id=None, metadata=None):
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
        :type ip_address: str
        :type session_id: str
        :type metadata: dict
        """
        self.user_id = user_id
        self.username = username
        self.phone_number = phone_number
        self.email = email
        self.shipping_address = shipping_address
        self.billing_address = billing_address
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name
        self.ip_address = ip_address
        self.session_id = session_id
        self.metadata = metadata

from bouncer_insight.events.base import Base


class Address(Base):
    def __init__(self, name=None, street1=None, street2=None, city=None, state=None, zip=None,
                 country=None, phone=None):
        """
        :type name: str
        :type street1: str
        :type street2: str
        :type city: str
        :type state: str
        :type zip: str
        :type country: str
        :type phone: str
        """
        self.name = name
        self.street1 = street1
        self.street2 = street2
        self.city = city
        self.state = state
        self.zip = zip
        self.country = country
        self.phone = phone

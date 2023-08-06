from bouncer_insight.events.base import Base


class LoginEvent(Base):
    def __init__(self, user_id, username, login_success, ip_address, failure_reason=None,
                 session_id=None, metadata=None):
        """
        :type user_id: str
        :type username: str
        :type login_success: bool
        :type ip_address: str
        :type failure_reason: str
        :type session_id: str
        :type metadata: dict
        """
        self.user_id = user_id
        self.username = username
        self.login_success = login_success
        self.ip_address = ip_address
        self.failure_reason = failure_reason
        self.session_id = session_id
        self.metadata = metadata

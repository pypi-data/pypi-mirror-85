from bouncer_insight.events import Base


LABEL_TYPE_ACCOUNT_TAKEOVER = 'account_takeover'
LABEL_TYPE_PAYMENT_FRAUD = 'payment_fraud'
LABEL_TYPE_GOOD = 'good'

LABEL_SOURCE_MANUAL = 'manual_review'
LABEL_SOURCE_AUTOMATED = 'automated'


class LabelAdd(Base):
    def __init__(self, user_id, actor, source, is_bad, label, description=None, metadata=None):
        """
        :param user_id: the user_id of the user to be marked as bad
        :param actor: name of the actor that performed the label add. Examples: "agent_name@example.com", "IPVelocityRule"
        :param source: the mechanism from which the label is applied. Examples: "manual_review", "automated"
        :param is_bad: whether this user is good or bad
        :param label: the label we want to apply. Examples: "account_takeover", "payment_fraud", "good"
        :param description: freeform string around why the user is labeled the way it is
        :type user_id: str
        :type actor: str
        :type source: str
        :type is_bad: bool
        :type label: str
        :type description: str
        :type metadata: dict
        """
        self.user_id = user_id
        self.actor = actor
        self.source = source
        self.is_bad = is_bad
        self.label = label
        self.description = description
        self.metadata = metadata

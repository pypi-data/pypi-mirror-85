class Base:
    def to_dict(self):
        return {
            k: v.to_dict() if isinstance(v, Base) else v
            for k, v in self.__dict__.items() if v is not None
        }

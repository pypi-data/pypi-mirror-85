import re


class DBInstanceClass:
    aliases = {
        "db.t2.tiny": "db.cpu1.ram075",
        "db.t2.micro": "db.cpu1.ram1",
        "db.t2.small": "db.cpu1.ram2",
        "db.t2.medium": "db.cpu2.ram4",
        "db.m5.large": "db.cpu2.ram8",
        "db.m5.xlarge": "db.cpu4.ram16",
        "db.m5.2xlarge": "db.cpu8.ram32",
        "db.m5.4xlarge": "db.cpu16.ram64",
    }

    token_re = re.compile(r'(?P<name>[a-z]+)(?P<value>\d*)')

    @classmethod
    def parse(cls, raw):
        try:
            alias, raw = raw, cls.aliases[raw]
        except KeyError:
            alias = None

        db, *tokens = raw.split('.')
        if 'db' != db:
            raise ValueError("Instance class not starting with db.")

        fields = {}
        for token in tokens:
            m = cls.token_re.match(token)
            if not m:
                raise ValueError(f"Bad class token: {token}")
            value = m.group('value')
            if '' == value:
                value = True
            elif value.startswith('0'):
                value = float('0.' + value[1:])
            else:
                value = int(value)
            fields[m.group('name')] = value
        return cls(alias=alias, **fields)

    def __init__(self, alias=None, **fields):
        self.__dict__.update(fields)
        self.fields_names = fields.keys()
        self.alias = alias

    @property
    def fields(self):
        return dict(
            (name, getattr(self, name))
            for name in self.fields_names
        )

    def __repr__(self):
        return '<%s %s>' % (
            self.__class__.__name__,
            ' '.join(
                k if v is True else '%s=%s' % (k, v)
                for k, v in self.fields.items()
            )
        )

    def __str__(self):
        if self.alias:
            return self.alias

        tokens = []
        for name, value in self.fields.items():
            if value is True:
                value = ''
            elif value < 1:
                value = str(value).replace('.', '')
            tokens.append(f"{name}{value}")

        return '.'.join(['db'] + tokens)

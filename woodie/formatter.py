class BasicFormatter:
    def __init__(
            self,
            fmt: str = None,
            key_fmt: str = None,
            sep_fmt: str = None,
            datefmt: str = None,
            var: str = '%',
            prefix: str = None,
            suffix: str = None,
    ):
        self.fmt = fmt
        self.key_fmt = key_fmt or ''
        self.sep = sep_fmt or ' - '
        self.var = var or '%'
        self.prefix = prefix or ''
        self.suffix = suffix or ''

    def format(self, record):
        formatted_list = []
        record.message = record.getMessage()
        for idx, (key, value) in enumerate(record.__dict__.items()):
            formatted_list.append(self.format_key_value(key, value))

        return self.prefix + self.sep.join(formatted_list) + self.suffix

    def format_key_value(self, key, value) -> str:
        return self.key_fmt.replace(self.var, str(key)) + self.fmt.replace(self.var, str(value))

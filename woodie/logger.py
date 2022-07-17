from logging import Logger as OriginLogger, ERROR, INFO, DEBUG, WARN, CRITICAL
from typing import Dict, Any, Optional, Union, Mapping


class Logger(OriginLogger):
    def __init__(
            self,
            name: str,
            fields: Optional[Dict[str, Any]] = None,
            log_failure: bool = True,
            log_failure_level: Union[str, int] = ERROR,  # Accept int and str? check this.
    ):
        self.fields = fields or {}
        self.log_failure = log_failure
        self.log_failure_level = log_failure_level
        super().__init__(name)

    def debug(self, *args, **kwargs):
        self._log_wrapper(DEBUG, *args, **kwargs)

    def info(self, *args, **kwargs):
        self._log_wrapper(INFO, *args, **kwargs)

    def warn(self, *args, **kwargs):
        self._log_wrapper(WARN, *args, **kwargs)

    def error(self, *args, **kwargs):
        self._log_wrapper(ERROR, *args, **kwargs)

    def critical(self, *args, **kwargs):
        self._log_wrapper(CRITICAL, *args, **kwargs)

    def exception(self, *args, exc_info=True, **kwargs) -> None:
        self.error(*args, exc_info=exc_info, **kwargs)

    def _log_wrapper(self, level, *args, **kwargs):
        try:
            self.log(level, *args, **kwargs)
        except BaseException:
            if self.log_failure:
                super().log(level=self.log_failure_level, msg=f'Logger `{self.name}` failed to log.', exc_info=True)
            raise

    def log(
            self,
            level: int,
            msg: object,
            *args: object,
            exc_info: Union[None, bool, BaseException] = None,
            stack_info: bool = False,
            stacklevel: int = 1,
            extra: Optional[Mapping[str, object]] = None,
            **kwargs,
        ) -> None:
        fields = {}
        fields.update(self.fields)
        if isinstance(extra, dict):
            fields.update(extra)
        fields.update(kwargs)
        super().log(level, msg, *args, exc_info=exc_info, stack_info=stack_info, extra=fields)

    def add_fields(self, **fields: Dict[str, Any]):
        self.fields.update(fields)

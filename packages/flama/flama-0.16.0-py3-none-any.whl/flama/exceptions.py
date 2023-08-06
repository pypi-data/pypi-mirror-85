import typing

import starlette.exceptions


class DecodeError(Exception):
    """
    Raised by a Codec when `decode` fails due to malformed syntax.
    """

    def __init__(self, message, marker=None, base_format=None):
        Exception.__init__(self, message)
        self.message = message
        self.marker = marker
        self.base_format = base_format


class NoReverseMatch(Exception):
    """
    Raised by a Router when `reverse_url` is passed an invalid handler name.
    """

    ...


class NoCodecAvailable(Exception):
    ...


class ConfigurationError(Exception):
    ...


class ComponentNotFound(ConfigurationError):
    def __init__(
        self,
        parameter: str,
        component: typing.Optional[str] = None,
        function: typing.Optional[str] = None,
        *args,
        **kwargs,
    ):
        self.parameter = parameter
        self.component = component
        self.function = function
        super().__init__(*args, **kwargs)

    def __str__(self):
        msg = f'No component able to handle parameter "{self.parameter}"'
        if self.component:
            msg += f' in component "{self.component}"'
        if self.function:
            msg += f' for function "{self.function}"'

        return msg


class WebSocketException(Exception):
    def __init__(self, close_code: int):
        self.close_code = close_code


class WebSocketConnectionException(Exception):
    ...


class HTTPException(starlette.exceptions.HTTPException):
    ...


class ValidationError(HTTPException):
    def __init__(self, detail: typing.Union[str, typing.Dict[str, typing.List[str]]], status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


class SerializationError(HTTPException):
    def __init__(
        self, detail: typing.Union[None, str, typing.Dict[str, typing.List[str]]] = None, status_code: int = 500
    ):
        super().__init__(status_code=status_code, detail=detail)

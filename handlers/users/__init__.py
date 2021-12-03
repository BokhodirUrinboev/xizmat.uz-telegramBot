from .start import dp
from .language_change import dp
from .settings import dp
# should be last message in case of no handler could catch the message
from .unknown_message import dp


__all__ = ["dp"]

from .help import dp
from .start import dp
from .language_change import dp
from .back_to_main_menu import dp
from .setings import dp
from .login import dp
from .account_managment import dp
from .remove_account import dp
from .balance import dp
from .services import dp
from .payment_history_service import dp
from handlers.users.payments.payment import dp
from .sld_history import dp
from .payments import dp
# should be last message in case of no handler could catch the message
from .unknown_message import dp


__all__ = ["dp"]

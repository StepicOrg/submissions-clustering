import os

__all__ = ["telegram_send"]


def telegram_send(msg, path_to_cli="~/tg/bin/telegram-cli", user="Stanislav_Belyaev"):
    os.system("{} -W -e \"msg {} {}\" >/dev/null".format(path_to_cli, user, msg))

from telegram.ext import (
    ContextTypes,
)
from front.command import Command
from front.utils.settings import SettingMixin, setting_paths
from typing import Optional


class _StartSettings(SettingMixin):
    _return_to: str = Command.START


@setting_paths("start", "first_register")
class FirstRegisterSetting(_StartSettings):
    pass

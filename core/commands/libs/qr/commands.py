"""Команды для работы с QR кодами."""

import io

import qrcode

from core.commands.interfaces import CommandResult, TextWithPictureFileCommandResult
from core.commands.utils import register_command


@register_command(aliases=("enq",))
def encode_qr(data: str, **kwargs) -> CommandResult:
    """Закодирует данные в QR код: enq Hello world!"""
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make(fit=True)
    # Вариант кода в виде картинки.
    qr_as_image = qr.make_image(fill_color="black", back_color="white")
    # Вариант кода в виде ASCII.
    qr_as_ascii = io.StringIO()
    qr.print_ascii(qr_as_ascii)
    return TextWithPictureFileCommandResult("QR", qr_as_image.get_image().tobytes(), qr_as_ascii.getvalue())

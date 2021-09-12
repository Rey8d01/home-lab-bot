"""Команды для работы с QR кодами."""

import io

import qrcode

from core.commands.interfaces import CommandResult, TextWithPictureFileCommandResult
from core.commands.utils import register_command


@register_command(aliases=("enq",))
def encode_qr(data_for_encode: str, **kwargs) -> CommandResult:
    """Закодирует данные в QR код: enq Hello world!"""
    qr = qrcode.QRCode()
    qr.add_data(data_for_encode)
    qr.make(fit=True)
    # Вариант кода в виде картинки.
    raw_qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_as_bytes = io.BytesIO()
    raw_qr_image.save(qr_as_bytes, "JPEG")
    # Вариант кода в виде ASCII.
    qr_as_ascii = io.StringIO()
    qr.print_ascii(qr_as_ascii)
    return TextWithPictureFileCommandResult("QR", qr_as_bytes.getvalue(), qr_as_ascii.getvalue())

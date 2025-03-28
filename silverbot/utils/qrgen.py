from tempfile import NamedTemporaryFile

from qrcode.constants import ERROR_CORRECT_L
from qrcode.main import QRCode


def generate_qr_code(text: str):
    file = NamedTemporaryFile(suffix=".png", delete=False)
    qr = QRCode(
        version=1,
        error_correction=ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(file)
    file.close()
    return file

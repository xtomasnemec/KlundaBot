import qrcode
import tempfile

def generate_qr_code(text: str):
    file = tempfile.NamedTemporaryFile(suffix=".png")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(file)
    return file

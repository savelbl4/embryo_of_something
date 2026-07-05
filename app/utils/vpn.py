import qrcode
from io import BytesIO
from pathlib import Path

def send_vpn_config():
    try:
        vless_link = Path("/app/storage/link.txt").read_text(encoding="utf-8").strip()

        if not vless_link.startswith("vless://"):
            raise ValueError("Некорректная ссылка")

        img = qrcode.make(vless_link)

        bio = BytesIO()
        bio.name = "vless_qr.png"
        img.save(bio, "PNG")
        bio.seek(0)

        return bio, (
            "📱 <b>VPN-конфиг</b>\n\n"
            "Отсканируйте QR-код или скопируйте ссылку:\n\n"
            f"<code>{vless_link}</code>"
        )

    except Exception as e:
        msg = f"Не удалось отправить VLESS-конфиг: {e}"
        print(msg)
        return 0, f"❌ {msg}"


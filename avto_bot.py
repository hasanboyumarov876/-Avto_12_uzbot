import asyncio
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telethon import TelegramClient, events

# ============================================
# SOZLAMALAR
# ============================================

API_ID = 37100683
API_HASH = "13513597f58100d3232e3838d196bc60"
SIZNING_ID = 8654245295

KANALLAR = [
    "qoshkopiravto_markett",
    "Sherzodabzor",
    "nurik_avto_qarshi",
    "vodiy_avto_rasmiy",
    "Accountant_in_Logistics"
]

SOTILDI_SOZLAR = ["sotildi", "сотилди", "продано", "sold", "sotilgan", "baraka bo'ldi"]

# ============================================

logging.basicConfig(level=logging.INFO)

client = TelegramClient('avto_monitor', API_ID, API_HASH)


@client.on(events.NewMessage(chats=KANALLAR))
async def yangi_elon(event):
    matn = event.message.text or ""
    for soz in SOTILDI_SOZLAR:
        if soz.lower() in matn.lower():
            kanal = getattr(event.chat, "username", "noma'lum")
            xabar = f"✅ SOTILDI!\n\n📢 Kanal: @{kanal}\n\n{matn[:300]}"
            await client.send_message(SIZNING_ID, xabar)
            return


@client.on(events.MessageEdited(chats=KANALLAR))
async def tahrirlangan(event):
    matn = event.message.text or ""
    kanal = getattr(event.chat, "username", "noma'lum")
    for soz in SOTILDI_SOZLAR:
        if soz.lower() in matn.lower():
            xabar = f"✏️ SOTILDI (EDIT)\n\n📢 Kanal: @{kanal}\n\n{matn[:300]}"
            await client.send_message(SIZNING_ID, xabar)
            return
    xabar = f"✏️ POST EDITLANDI\n\n📢 Kanal: @{kanal}\n\n{matn[:300]}"
    await client.send_message(SIZNING_ID, xabar)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot ishlayapti!')
    def log_message(self, format, *args):
        pass


def web_server():
    server = HTTPServer(('0.0.0.0', 8080), Handler)
    server.serve_forever()


async def main():
    print("✅ Bot ishga tushdi!")
    await client.start()
    await client.run_until_disconnected()


if __name__ == "__main__":
    threading.Thread(target=web_server, daemon=True).start()
    asyncio.run(main())

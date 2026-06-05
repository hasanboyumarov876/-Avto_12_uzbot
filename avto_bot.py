import asyncio
import logging
from telethon import TelegramClient, events

# ============================================
# SOZLAMALAR
# ============================================

BOT_TOKEN = "8659725946:AAE7Narh-xlLWlT9Zd7EiIpvSFjuoVtDV1g"
API_ID = 37100683
API_HASH = "13513597f58100d3232e3838d196bc60"
SIZNING_ID = 8654245295

# Kuzatiladigan kanallar (FAQAT username)
KANALLAR = [
    "qoshkopiravto_markett",
    "Sherzodabzor",
    "nurik_avto_qarshi",
    "vodiy_avto_rasmiy",
    "Accountant_in_Logistics"
]

# Kalit so'zlar
SOTILDI_SOZLAR = ["sotildi", "сотилди", "продано", "sold", "sotilgan", "baraka bo‘ldi"]

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


async def main():
    print("✅ Bot ishga tushdi!")
    await client.start()
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())

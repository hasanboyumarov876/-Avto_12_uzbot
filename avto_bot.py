import asyncio
import logging
from telethon import TelegramClient, events
from telethon.tl.types import MessageService

# ============================================
# SOZLAMALAR — FAQAT SHUНИ O'ZGARTIRING
# ============================================

BOT_TOKEN = "8659725946:AAE7Narh-xlLWlT9Zd7EiIpvSFjuoVtDV1g"  # @BotFather dan olgan token
API_ID = 37100683               # my.telegram.org dan olasiz
API_HASH = "13513597f58100d3232e3838d196bc60"  # my.telegram.org dan olasiz
SIZNING_ID = 8654245295       # @userinfobot dan olgan ID

# Kuzatiladigan kanallar
KANALLAR = [
    "qoshkopiravto_markett",
    "Sherzodabzor", 
    "nurik_avto_qarshi",
    "vodiy_avto_rasmiy"
]

# Kalit so'zlar
SOTILDI_SOZLAR = ["sotildi", "сотилди", "продано", "sold", "sotilgan"]

# ============================================

logging.basicConfig(level=logging.INFO)

client = TelegramClient('avto_monitor', API_ID, API_HASH)

@client.on(events.NewMessage(chats=KANALLAR))
async def yangi_elon(event):
    """Yangi e'lon chiqsa xabar yuboradi"""
    matn = event.message.text or ""
    
    # Sotildi tekshirish
    for soz in SOTILDI_SOZLAR:
        if soz.lower() in matn.lower():
            kanal = event.chat.username or "Noma'lum"
            xabar = f"✅ SOTILDI!\n\n📢 Kanal: @{kanal}\n\n{matn[:300]}"
            await client.send_message(SIZNING_ID, xabar)
            return

@client.on(events.MessageEdited(chats=KANALLAR))
async def tahrirlangan(event):
    """Post tahrirlansa xabar yuboradi"""
    matn = event.message.text or ""
    kanal = event.chat.username or "Noma'lum"
    
    xabar = f"✏️ TAHRIRLANDI!\n\n📢 Kanal: @{kanal}\n\n{matn[:300]}"
    await client.send_message(SIZNING_ID, xabar)
    
    # Sotildi tekshirish
    for soz in SOTILDI_SOZLAR:
        if soz.lower() in matn.lower():
            xabar = f"✅ SOTILDI! (Tahrirlangan)\n\n📢 Kanal: @{kanal}\n\n{matn[:300]}"
            await client.send_message(SIZNING_ID, xabar)
            return

async def main():
    print("✅ Bot ishga tushdi! Kanallar kuzatilmoqda...")
    await client.start(bot_token=BOT_TOKEN)
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

# SOZLAMALAR
BOT_TOKEN = "8659725946:AAE7Narh-xlLWlT9Zd7EiIpvSFjuoVtDV1g"
SIZNING_ID = 8654245295

# Kuzatiladigan kanallar (username, @ siz)
KANALLAR = [
    "qoshkopiravto_markett",
    "Sherzodabzor",
    "nurik_avto_qarshi",
    "vodiy_avto_rasmiy",
    "Logistika_sohasidagi_buxgalter",
]

# Kalit so'zlar
SOTILDI_SOZLAR = ["sotildi", "сотилди", "продано", "sold", "sotilgan", "baraka bo'ldi"]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()


def sotildi_bormi(matn: str) -> bool:
    if not matn:
        return False
    matn_lower = matn.lower()
    return any(soz.lower() in matn_lower for soz in SOTILDI_SOZLAR)


@dp.channel_post()
async def yangi_elon(message):
    kanal = message.chat.username or "noma'lum"
    if kanal not in KANALLAR:
        return
    matn = message.text or message.caption or ""
    if sotildi_bormi(matn):
        xabar = f"✅ SOTILDI!\n\nKanal: @{kanal}\n\n{matn[:300]}"
        await bot.send_message(SIZNING_ID, xabar)


@dp.edited_channel_post()
async def tahrirlangan_elon(message):
    kanal = message.chat.username or "noma'lum"
    if kanal not in KANALLAR:
        return
    matn = message.text or message.caption or ""
    if sotildi_bormi(matn):
        xabar = f"✏️ SOTILDI (EDIT)\n\nKanal: @{kanal}\n\n{matn[:300]}"
        await bot.send_message(SIZNING_ID, xabar)


async def main():
    print("✅ Bot ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

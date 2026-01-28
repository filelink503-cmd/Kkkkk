# plugins/link_generator.py

import re
import urllib.parse
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Custom "Jaasoos Filter" jo humne banaya tha
async def not_command_filter(_, __, message: Message):
    if message.text and (message.text.startswith("/") or message.text.startswith(".")):
        return False
    return True

is_not_command = filters.create(not_command_filter)


@Client.on_message(filters.text & filters.private & is_not_command)
async def auto_link_monetizer(client, message: Message):
    """
    Yeh handler link dhoondhta hai, use monetize karta hai,
    aur naya link multi-share buttons ke saath reply karta hai.
    """
    url_pattern = r'https?://[^\s]+'
    match = re.search(url_pattern, message.text)

    if match:
        target_url = match.group(0)

        # Monetization ka logic (waisa hi hai)
        redirect_page = 'https://babubhaikundan.pages.dev/Redirect/'
        encoded_url = urllib.parse.quote(target_url, safe='')
        final_link = f"{redirect_page}?url={encoded_url}"

        # --- YEH HAIN NAYE BADLAV (MULTI-SHARE BUTTON KA LOGIC) ---

        # Text jo share karna hai
        share_text = f"Click here 👇\n\n{final_link}"
        encoded_share_text = urllib.parse.quote(share_text)

        # 1. Telegram ke liye special share URL banayein
        telegram_share_url = f"https://t.me/share/url?url={urllib.parse.quote(final_link)}"
        
        # 2. WhatsApp ke liye special share URL banayein
        whatsapp_share_url = f"https://wa.me/?text={encoded_share_text}"

        # 3. Ek Inline Keyboard banayein jismein humare dono share buttons honge
        reply_markup = InlineKeyboardMarkup(
            [
                # Ek row mein dono buttons daal dein
                [
                    InlineKeyboardButton(
                        text="☑️Share on WhatsApp",
                        url=whatsapp_share_url
                    ),
                    InlineKeyboardButton(
                        text="☑️Share on Telegram",
                        url=telegram_share_url
                    )
                ]
            ]
        )
        
        # 4. Final link user ko 'Share' buttons ke saath bhej dein
        await message.reply_text(
            f"✅ **Redirect Link Generated:**\n\n``{final_link}`",
            quote=True,
            reply_markup=reply_markup # Humne yahan naya keyboard jod diya hai
        )

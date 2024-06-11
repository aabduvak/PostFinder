import logging
import uuid
import json

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from telegram import PhotoSize, MessageEntity, Video, Document

from config import BOT_TOKEN, CHANNEL_ID, ADMIN_ID
from database import Database

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

db = Database()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    first_name = update.effective_user.first_name
    
    message = f"Привет {first_name}\n" \
        + "Чтобы отправить публикацию на утверждение, пересылайте публикации из каналов."
    
    await update.message.reply_text(text=message)

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = f"Ваш ID чата:\n{update.effective_chat.id}"

    await update.message.reply_text(text=message)


async def send_message(key: str, context: ContextTypes.DEFAULT_TYPE, chat_id) -> None:
    
    message_data = db.get_post(key)
    
    if message_data:
        bot = context.bot
        message = json.loads(message_data["message"])
    
        if message and message.get("text"):
            message_entities = [MessageEntity.de_json({"user": None, **entity}, bot) for entity in message.get("entities", [])]
            await bot.send_message(chat_id, message["text"], entities=message_entities)

        elif message and message.get("video"):
            video = Video.de_json(message["video"], bot)
            caption_entities = [MessageEntity.de_json({"user": None, **entity}, bot) for entity in message.get("caption_entities", [])]
            
            await bot.send_video(chat_id, video=video, caption=message["caption"], caption_entities=caption_entities)

        elif message and message.get("photo"):
            photo = PhotoSize.de_json(message["photo"][0], bot)
            caption_entities = [MessageEntity.de_json({"user": None, **entity}, bot) for entity in message.get("caption_entities", [])]

            await bot.send_photo(chat_id, photo=photo, caption=message["caption"], caption_entities=caption_entities)

        elif message and message.get("document"):
            document = Document.de_json(message["document"], bot)
            caption_entities = [MessageEntity.de_json({"user": None, **entity}, bot) for entity in message.get("caption_entities", [])]

            await bot.send_document(chat_id, document=document, caption=message["caption"], caption_entities=caption_entities)
        
        else:
            await bot.send_message(ADMIN_ID, "Этот тип сообщений пока не поддерживается")
    else:
        await context.bot.send_message(ADMIN_ID, "Сообщение не найдено")



async def send_post(key: str, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_message(key, context, CHANNEL_ID)

    
async def send_approve(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = context.user_data.get('message')
    bot = context.bot
    key = str(uuid.uuid4())

    db.create_post(message.to_json(), key)
    
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Одобрить", callback_data=f"approve_request:{key}")],
            [InlineKeyboardButton("Отменить", callback_data=f"cancel_request:{key}")],
            [InlineKeyboardButton("Редактировать", callback_data=f"edit_request:{key}")],
        ]
    )

    if message and message.text:
        await bot.send_message(ADMIN_ID, message.text, reply_markup=reply_markup, entities=message.entities)
    
    elif message and message.media_group_id:
        await bot.send_media_group(ADMIN_ID, media=message.photo, caption=message.caption, caption_entities=message.caption_entities)
        
    elif message and message.video:
        await bot.send_video(ADMIN_ID, video=message.video, caption=message.caption, caption_entities=message.caption_entities, reply_markup=reply_markup)
    
    elif message and message.photo:
        await bot.send_photo(ADMIN_ID, photo=message.photo[0], caption=message.caption, caption_entities=message.caption_entities, reply_markup=reply_markup)
    
    elif message and message.document:
        await bot.send_document(ADMIN_ID, document=message.document, caption=message.caption, caption_entities=message.caption_entities, reply_markup=reply_markup)
    
    else:
        await bot.forward_message(ADMIN_ID, message_id=message.id, from_chat_id=message.chat_id)

    
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['message'] = update.message
    
    await send_approve(update, context)
    await update.message.delete()


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data.split(':')
    
    if data[0] == "approve_request":
        await send_post(data[1], context)
        await query.answer("Сообщение отправлено на канал")
        await query.delete_message()
        db.delete_post(data[1])
        
    elif data[0] == "cancel_request":
        await query.answer("Сообщение удалено")
        await query.delete_message()
        db.delete_post(data[1])
        
    elif data[0] == "edit_request":
        await query.delete_message()
        await query.answer("Пожалуйста, пришлите новое содержание сообщения")
        
        await send_message(data[1], context, ADMIN_ID)
        db.delete_post(data[1])
        
        await context.bot.send_message(ADMIN_ID, "Пожалуйста, пришлите новое содержание сообщения.")


def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("chat_id", get_chat_id))
    app.add_handler(MessageHandler(~filters.FORWARDED, message_handler))
    app.add_handler(CallbackQueryHandler(button_callback))

    app.run_polling()

if __name__ == '__main__':
    main()
import asyncio
import random
from io import BytesIO
from pathlib import Path

from coolname import generate
from httpx import AsyncClient
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from bot import message_texts
from bot.hugging_face_models_client import HuggingFaceModelsClient
from bot.model_client import ModelClient
from bot.settings import BotSettings

settings = BotSettings()


model_client = ModelClient(
    model_api_url=settings.model_api_url,
    httpx_client=AsyncClient(),
)

hugging_face_client = HuggingFaceModelsClient(
    hugging_face_api_url=settings.hugging_face_api_url,
    hugging_face_token=settings.hugging_face_api_token,
    httpx_client=AsyncClient(),
    timeout=20,
)

LOGO_BYTES = (Path(__file__).parent.absolute() / "assets" / "logo.jpg").read_bytes()
MEMES = [
    file_path.read_bytes()
    for file_path in (Path(__file__).parent.absolute() / "assets" / "memes").iterdir()
]


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_photo(
        LOGO_BYTES, caption=message_texts.start(update.effective_user.first_name)
    )


async def estimate_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    file_io = BytesIO()
    await photo_file.download_to_memory(out=file_io)
    file_io.seek(0)
    file_bytes = file_io.read()
    tasks = (
        model_client.predict(file_bytes),
        hugging_face_client.generate_caption_for_image(file_bytes),
    )
    prediction_result, image_caption = await asyncio.gather(*tasks)

    response_text = message_texts.image_description(
        price=prediction_result.price, caption=image_caption
    )

    await update.message.reply_photo(
        update.message.photo[-1].file_id, caption=response_text, parse_mode="HTML"
    )

    similar_image = await hugging_face_client.generate_image_by_caption(
        f"strange {image_caption}"
    )
    similar_image_prediction_result = await model_client.predict(similar_image)

    await update.message.reply_photo(
        similar_image,
        caption=message_texts.similar_image_description(
            similar_image_prediction_result.price
        ),
        parse_mode="HTML",
    )

    await asyncio.sleep(15)
    await update.message.reply_text(
        message_texts.meme_prelude(),
        parse_mode="HTML",
    )
    await asyncio.sleep(5)
    await update.message.reply_photo(random.choice(MEMES))


def create_app() -> Application:
    app = ApplicationBuilder().token(settings.telegram_token.get_secret_value()).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(MessageHandler(filters.PHOTO, estimate_price))

    return app

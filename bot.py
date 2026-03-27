"""Telegram-бот для скачивания музыки с YouTube."""

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from src.config import config
from src.converter import convert_to_mp3
from src.downloader import download_audio

logging.basicConfig(level=logging.INFO)


class DownloadState(StatesGroup):
    waiting_for_url = State()


def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Скачать песню", callback_data="download")]
    ])


def is_allowed(user_id: int) -> bool:
    return user_id in config.allowed_users


dp = Dispatcher(storage=MemoryStorage())


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    if not is_allowed(message.from_user.id):
        await message.answer("У вас нет доступа к этому боту.")
        return
    await message.answer("Привет! Нажми кнопку, чтобы скачать песню с YouTube.", reply_markup=main_keyboard())


@dp.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    if not is_allowed(message.from_user.id):
        return
    await state.clear()
    await message.answer("Отменено.", reply_markup=main_keyboard())


@dp.callback_query(F.data == "download")
async def on_download_button(callback: CallbackQuery, state: FSMContext) -> None:
    if not is_allowed(callback.from_user.id):
        await callback.answer("У вас нет доступа.", show_alert=True)
        return
    await state.set_state(DownloadState.waiting_for_url)
    await callback.message.answer("Пришли ссылку на YouTube-видео (или /cancel для отмены):")
    await callback.answer()


@dp.message(DownloadState.waiting_for_url)
async def on_url(message: Message, state: FSMContext) -> None:
    if not is_allowed(message.from_user.id):
        await message.answer("У вас нет доступа.")
        return

    url = message.text.strip()
    await state.clear()

    status = await message.answer("Скачиваю...")

    output_file = None
    try:
        input_file, title = await asyncio.to_thread(download_audio, url)
        await status.edit_text("Конвертирую в MP3...")
        output_file = await asyncio.to_thread(convert_to_mp3, input_file)

        await status.edit_text("Отправляю файл...")
        await message.answer_audio(
            FSInputFile(output_file, filename=f"{title}.mp3"),
            title=title,
        )
        await status.delete()
    except Exception as e:
        logging.exception("Ошибка при обработке %s", url)
        await status.edit_text(f"Ошибка: {e}")
    finally:
        if output_file and os.path.exists(output_file):
            os.remove(output_file)

    await message.answer("Хочешь скачать ещё?", reply_markup=main_keyboard())


async def main() -> None:
    bot = Bot(token=config.bot_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
import requests
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
import keyBoards
import handlers
import config
import models.classes as classes
import utils
import pprint

markup_1 = ReplyKeyboardMarkup(keyBoards.reply_keyboard_1, one_time_keyboard=True)
markup_2 = ReplyKeyboardMarkup(keyBoards.reply_keyboard_2, one_time_keyboard=True)
classes_markup = ReplyKeyboardMarkup(keyBoards.reply_keyboard_classes, one_time_keyboard=True)

# Functions for the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Enter your barcode : "
    )
    return handlers.TYPING_BARCODE


async def enter_barcode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["barcode"] = text
    await update.message.reply_text(
        "This bot will help you to get your papers and marks\n"
        "Choose an option : "
        , reply_markup=markup_1
    )
    return handlers.CHOOSING


async def enter_paper_no(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["paper"] = text

    paper = context.user_data["paper"]
    clz = context.user_data["class"]
    barcode = context.user_data["barcode"]

    # pprint.pprint(context.user_data)
    if context.user_data["choice"] == "🔖  Get Marks":
        try:
            data = classes.get_marks(clz, paper, barcode).to_dict()
            # pprint.pprint(data)
            # studentData = data['student_id'].get().to_dict()
            await update.message.reply_html(utils.generate_marks_message(
                        name=barcode,
                        marks=data['marks'],
                        Drank=data['rank'],
                        Arank="-",
                        link="-",
                        year=clz,
                        paper_no=paper,
                        ptype="ONLINE"
                    ))
        except TypeError:
            await update.message.reply_text("Data not found!")
    elif context.user_data["choice"] == "🧾  Get Paper":
        await update.message.reply_html("This Feature is not available yet.")
    else:
        await update.message.reply_text("Invalid Choice")

    await update.message.reply_text(
        "Choose an option : "
        , reply_markup=markup_1
    )
    return handlers.CHOOSING


async def get_marks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(
        "Enter your paper no : "
    )
    return handlers.TYPING_PAPER


async def get_papers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(
        "Enter your paper no : "
    )
    return handlers.TYPING_PAPER


async def paper_issue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(
        "Enter Your Complaint : "
    )
    return handlers.TYPING_ISSUE


async def enter_paper_issue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["issue"] = text
    data = {
        "barcode": context.user_data['barcode'],
        "chat_id": update.message.chat_id,
        "complaint": context.user_data["issue"]
    }

    response = requests.post(config.WEBHOOK_LINK_CMP, data=data)
    response_data = response.json()
    if response_data["status"] == "success":
        await update.message.reply_text(
            "\n 👨🏼‍💻 Your Complaint has been recorded !  📥 \n"
            "\n 🎲  We will check it soon 🔰🔰 \n"
        )
    else:
        await update.message.reply_text(response_data["message"])

    await update.message.reply_text(
        "Choose an option : "
        , reply_markup=markup_1
    )
    return handlers.CHOOSING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    user_data.clear()
    await update.message.reply_html(
        "\n<b>👋🏼 Bye! </b>\n"
        "\nGood Luck for your exams. 😄😄\n"
        "\n<u>To start again</u> /start 😎\n",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def choose_class(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(
        "Choose your class : "
        , reply_markup=classes_markup
    )
    return handlers.CHOOSING_CLASS


async def choose_operation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["class"] = text
    await update.message.reply_text(
        "Choose an option : "
        , reply_markup=markup_2
    )
    return handlers.CHOOSING_OPERATION


    
    


from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
import requests
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)
import keyBoards
import handlers
import config
import utils

markup_1 = ReplyKeyboardMarkup(keyBoards.reply_keyboard_1, one_time_keyboard=True)
language_markup = ReplyKeyboardMarkup(keyBoards.reply_keyboard_lang, one_time_keyboard=True)

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
    # pprint.pprint(context.user_data)

    if context.user_data["choice"] == "🔖  Get Marks":
        params = {"barcode": context.user_data["barcode"], "paper_no": context.user_data["paper"]}
        paper_no = params["paper_no"]
        sheet_id = "Paper " + params["paper_no"]
        data = {"message": params['barcode'], "chat_id": update.message.chat_id, "paper_no": paper_no, "sheet_id": sheet_id}
        response = requests.post(config.WEBHOOK_LINK_2, data=data)
        response_data = response.json()

        if response_data["status"] == "success":
            data_record = response_data["data"][0]
            await update.message.reply_html(utils.generate_beautiful_message(
                name=data_record[1],
                marks=data_record[4],
                Drank=data_record[0],
                Arank="-",
                link="-",
                year="2023",
                paper_no=paper_no,
                ptype="ONLINE"
            ))
        elif response_data["status"] == "failed":
            await update.message.reply_text(response_data["message"])
        else:
            await update.message.reply_text("Something went wrong")

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


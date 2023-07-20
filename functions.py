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
import models.storage_functions as storage_functions
import utils
import pprint

markup_1 = ReplyKeyboardMarkup(
    keyBoards.reply_keyboard_1, one_time_keyboard=True)
markup_2 = ReplyKeyboardMarkup(
    keyBoards.reply_keyboard_2, one_time_keyboard=True)
markup_3 = ReplyKeyboardMarkup(
    keyBoards.reply_keyboard_analytics, one_time_keyboard=True)
classes_markup = ReplyKeyboardMarkup(
    keyBoards.reply_keyboard_classes, one_time_keyboard=True)
markup_close = ReplyKeyboardMarkup(
    keyBoards.reply_keyboard_close, one_time_keyboard=True)


# Functions for the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("🪪 ඔබගේ Barcode අංකය ඇතුලත් කරන්න :")
    return handlers.TYPING_BARCODE


async def enter_barcode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["barcode"] = text
    await update.message.reply_html(
        "😄<u>PAPER CLASS BOT</u> 😄\n\n"
        "💡 මෙම Bot ඔබගේ ප්‍රශ්න පත්‍ර සහ ප්‍රශ්න පත්‍ර වල ලකුණු ලබාගැනීමට, ප්‍රශ්න පත්‍ර සම්බන්ධ ගැටළු අපවෙත යොමුකිරිම පහසු කිරීම සඳහා ඔබ‍ට සහය වේ.\n\n"
        "✨️ <i>මෙම Bot ගේ සමහර යෙදුම් තවමත් සැකසුම් මට්ටමේ පවතියි.</i>\n\n"
        "🤖 BOT ගෙන් හදිසියේ ඉවත් වීමට අවශ්‍ය නම් /close භාවිත කරන්න..\n\n"
        "🔥 පහතින් ඔබ‍ට අවශ්‍ය විකල්පයක් තෝරාගන්න..\n\n",
        reply_markup=markup_1)
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
            searchingMsg = await update.message.reply_text("🔍 Searching...")
            data = classes.get_marks(clz, paper, barcode).to_dict()
            # pprint.pprint(data)
            # studentData = data['student_id'].get().to_dict()
            await update.message.reply_html(
                utils.generate_marks_message(name=barcode,
                                             marks=data['marks'],
                                             Drank=data['rank'],
                                             Arank="-",
                                             link="-",
                                             year=clz,
                                             paper_no=paper,
                                             ptype="ONLINE"))
            await searchingMsg.delete()
        except TypeError:
            await update.message.reply_text(
                "✉️ Alert -> \n\nඔබ මෙම ප්‍රශ්න පත්‍රය සඳහා පිළිතුරු ලබාදී නොමැත.\n\n ✏️ __"
            )
            await searchingMsg.delete()

    elif context.user_data["choice"] == "📝  Get Marked Paper":
        bot = context.bot
        chat_id = update.message.chat_id
        filePath = "{}/{}".format(clz, paper)
        fileName = "{}.pdf".format(barcode)
        searchingMsg = await update.message.reply_sticker(
            'assets/stickers/searching.tgs')
        # searchingMsg = await update.message.reply_text("🔍 Searching...")
        print(fileName, filePath)
        try:
            data = classes.get_marks(clz, paper, barcode).to_dict()
            storage_functions.save_file(filePath, fileName)
            caption = "Marks : {}\n\nRank : {}".format(
                data['marks'], data['rank'])
            await bot.send_document(chat_id=chat_id, document="temp/{}".format(fileName), caption=caption)
            storage_functions.delete_local_file("temp/{}".format(fileName))
        except Exception as e:
            print(e)
            await update.message.reply_text(
                "✉️ Alert -> \n\nඔබ මෙම ප්‍රශ්න පත්‍රය සඳහා පිළිතුරු ලබාදී නොමැත.\n\n ✏️ __"
            )
        await searchingMsg.delete()

    else:
        await update.message.reply_text("🛡 Invalid Choice !")

    await update.message.reply_text("🔥 පහතින් ඔබ‍ට අවශ්‍ය විකල්පයක් තෝරාගන්න.. ", reply_markup=markup_1)
    return handlers.CHOOSING


async def get_marks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text("🪪 ඔබගේ ප්‍රශ්න පත්‍ර අංකය ඇතුලත් කරන්න :")
    return handlers.TYPING_PAPER


async def get_papers(update: Update,
                     context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text("🪪 ඔබගේ ප්‍රශ්න පත්‍ර අංකය ඇතුලත් කරන්න :")
    return handlers.TYPING_PAPER


async def paper_issue(update: Update,
                      context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text("📥 \n\n ඔබගේ ගැටලුව පැහැදිලිව යොමු කරන්න..", reply_markup=markup_close)
    return handlers.TYPING_ISSUE


async def enter_paper_issue(update: Update,   context: ContextTypes.DEFAULT_TYPE) -> int:
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
            "\n 🎲  We will check it soon 🔰🔰 \n")
    else:
        await update.message.reply_text(response_data["message"])

    await update.message.reply_text("🔥 පහතින් ඔබ‍ට අවශ්‍ය විකල්පයක් තෝරාගන්න.. ", reply_markup=markup_1)
    return handlers.CHOOSING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_html(
        "\n<b>👋🏼 Bye! </b>\n"
        "\nGood Luck for your exams. 😄😄\n\n"
        "\n<u>නැවත ආරම්භ කිරීමට</u> /start 😎\n",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def choose_class(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text("🔥 පහතින් ඔබගේ පන්තිය තෝරාගන්න.. ", reply_markup=classes_markup)
    return handlers.CHOOSING_CLASS


async def choose_operation(update: Update,  context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["class"] = text
    await update.message.reply_text("🔥 පහතින් ඔබ‍ට අවශ්‍ය විකල්පයක් තෝරාගන්න.. ", reply_markup=markup_2)
    return handlers.CHOOSING_OPERATION


async def invalid_choice_1(update: Update,  context: ContextTypes.DEFAULT_TYPE) -> int:
    pprint.pprint(context)
    await update.message.reply_text("🛡 Invalid Choice !", reply_markup=markup_1)
    return handlers.CHOOSING


async def invalid_choice_2(update: Update,  context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("🛡 Invalid Choice !", reply_markup=markup_2)
    return handlers.CHOOSING_OPERATION


async def invalid_choice_3(update: Update,  context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "Back":
        await update.message.reply_text("🔥 පහතින් ඔබ‍ට අවශ්‍ය විකල්පයක් තෝරාගන්න.. ", reply_markup=markup_1)
        return handlers.CHOOSING
    await update.message.reply_text("🛡 Invalid Choice !", reply_markup=markup_3)
    return handlers.CHOOSING_ANALYTIC


async def cancel_issue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Complaint Closed \n"
                                    "Choose an option : ", reply_markup=markup_1)
    return handlers.CHOOSING


async def invalid_input_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "✉️ Alert ->\n\nඔබ ලබාදී ඇත්තේ වැරදි barcode අංකයකි.කරුණාකර නිවැරදි Barcode අංකය ලබාදෙන්න.\n\n✏️ __"
    )
    return handlers.TYPING_BARCODE


async def invalid_input_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "✉️ Alert ->\n\nඔබ ලබාදී ඇත්තේ වැරදි ප්‍රශ්න පත්‍ර අංකයකි.කරුණාකර නිවැරදි ප්‍රශ්න පත්‍රයක් ලබාදෙන්න.\n\n✏️ __"
    )
    return handlers.TYPING_PAPER


async def get_analytics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("🔥 පහතින් ඔබ‍ට අවශ්‍ය විකල්පයක් තෝරාගන්න.. ", reply_markup=markup_3)
    return handlers.CHOOSING_ANALYTIC


async def get_data_analytics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["analytic_type"] = text
    await update.message.reply_text("🔥 පහතින් ඔබගේ පන්තිය තෝරාගන්න.. ", reply_markup=classes_markup)
    return handlers.CHOOSING_CLASS_ANALYTIC


async def get_graph_analytics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["analytic_type"] = text
    await update.message.reply_text("🔥 පහතින් ඔබගේ පන්තිය තෝරාගන්න.. ", reply_markup=classes_markup)
    return handlers.CHOOSING_CLASS_ANALYTIC


async def showAnalytics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    className = update.message.text
    if context.user_data["analytic_type"] == "📊  Get Data Analysis":
        try:
            waitingMsg = await update.message.reply_text("⏳ Processing...")
            data = classes.get_student_marks(
                className, context.user_data["barcode"])
            tpl = classes.get_average(data)
            await update.message.reply_html(
                utils.generate_analytics_message(
                    tpl[1], tpl[0], data, className),
                reply_markup=markup_3
            )
            await waitingMsg.delete()
        except Exception as e:
            await update.message.reply_text(f"SOMETHING WENT WRONG ! {e}", reply_markup=markup_3)
            await waitingMsg.delete()
        return handlers.CHOOSING_ANALYTIC
    elif context.user_data["analytic_type"] == "📈  Get Graph Analysis":
        await update.message.reply_text("This feature is not available !", reply_markup=markup_3)
        return handlers.CHOOSING_ANALYTIC
    else:
        await update.message.reply_text("🛡 Invalid Choice !", reply_markup=markup_3)
        return handlers.CHOOSING_ANALYTIC

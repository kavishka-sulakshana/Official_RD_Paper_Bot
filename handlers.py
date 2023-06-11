import functions
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

# States for the bot
TYPING_BARCODE, CHOOSING, TYPING_PAPER, TYPING_ISSUE, CHOOSING_CLASS, CHOOSING_OPERATION = range(6)

conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", functions.start)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex("^🧾  Get Papers$"), functions.choose_class
                ),
                MessageHandler(
                    filters.Regex("^📍 Paper Issues$"), functions.paper_issue
                ),
            ],
            TYPING_BARCODE: [
                MessageHandler(
                    filters.Regex("^[0-9]{8,10}$"), functions.enter_barcode
                )
            ],
            TYPING_PAPER: [
                MessageHandler(
                    filters.Regex("^[0-9]{2}$"), functions.enter_paper_no
                )
            ],
            TYPING_ISSUE: [
                MessageHandler(
                    filters.TEXT, functions.enter_paper_issue
                )
            ],
            CHOOSING_CLASS: [
                MessageHandler(
                    filters.TEXT, functions.choose_operation
                )
            ],
            CHOOSING_OPERATION: [
                MessageHandler(
                    filters.Regex("^🔖  Get Marks$"), functions.get_marks
                ),
                MessageHandler(
                    filters.Regex("^📝  Get Marked Paper$"), functions.get_papers
                ),
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^❌  Close"), functions.done)],
    )
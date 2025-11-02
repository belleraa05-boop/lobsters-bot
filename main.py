from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8579121658:AAE7eYDf3b2Ia2IOKCN8Xyf6mCRAQGxyXIc"

# Храним историю состояний пользователя
user_states = {}


def get_user_state(user_id):
    if user_id not in user_states:
        user_states[user_id] = ["start"]
    return user_states[user_id]


def set_user_state(user_id, state):
    user_states[user_id] = state


async def show_main_menu(update: Update):
    user_id = update.message.from_user.id
    set_user_state(user_id, ["start", "main_menu"])

    keyboard = [
        [KeyboardButton("💬 Рабочий чат"), KeyboardButton("👥 Руководитель")],
        [KeyboardButton("📖 Путеводитель"), KeyboardButton("ℹ️ О вакансии")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🏠 Главное меню\n\nВыберите нужный раздел:",
        reply_markup=reply_markup
    )


async def show_ready_continue_menu(update: Update):
    user_id = update.message.from_user.id
    set_user_state(user_id, ["start", "ready_continue"])

    keyboard = [
        [KeyboardButton("📚 Изучить материалы")],
        [KeyboardButton("🔙 Назад"), KeyboardButton("🏠 Главное меню")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Добро пожаловать в команду Lobsters! 🦞\n\nОтлично! Мы рады, что вы готовы начать это интересное путешествие вместе с нами.",
        reply_markup=reply_markup
    )


async def show_study_materials_menu(update: Update):
    user_id = update.message.from_user.id
    set_user_state(user_id, ["start", "ready_continue", "study_materials"])

    keyboard = [
        [KeyboardButton("🎯 Начать работу")],
        [KeyboardButton("🔙 Назад"), KeyboardButton("🏠 Главное меню")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Отлично! Благодарим за готовность работать и внимательный подход к обучению.",
        reply_markup=reply_markup
    )


async def show_start_work_menu(update: Update):
    user_id = update.message.from_user.id
    set_user_state(user_id, ["start", "ready_continue", "study_materials", "start_work"])

    keyboard = [
        [KeyboardButton("💬 Рабочий чат"), KeyboardButton("👥 Руководитель")],
        [KeyboardButton("📖 Путеводитель"), KeyboardButton("🔙 Назад")],
        [KeyboardButton("🏠 Главное меню")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🎉 Поздравляем с началом работы! Выберите нужный раздел:",
        reply_markup=reply_markup
    )


async def show_not_ready_menu(update: Update):
    user_id = update.message.from_user.id
    set_user_state(user_id, ["start", "not_ready"])

    keyboard = [
        [KeyboardButton("💬 Поделиться причиной")],
        [KeyboardButton("🔙 Назад"), KeyboardButton("🏠 Главное меню")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Спасибо за вашу честность. Жаль, что наше предложение не подошло вам по каким-то параметрам.",
        reply_markup=reply_markup
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    set_user_state(user_id, ["start"])

    keyboard = [
        [KeyboardButton("✅ Готов(а) продолжить")],
        [KeyboardButton("❌ Не готов(а)")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "Здравствуйте!\n"
        "Большое спасибо за ваш отклик на вакансию «Менеджер по работе с клиентами» и готовность развиваться вместе с Lobsters! 🦞\n"
        "https://ekaterinburg.hh.ru/vacancy/127094233?hhtmFrom=main\n\n"
        "Мы рады, что вы с нами, и хотим, чтобы вы полностью понимали все детали работы. Пожалуйста, внимательно ознакомьтесь с ключевой информацией ниже.\n"
        "Сайт нашей компании: lobsters.pro",
        reply_markup=reply_markup
    )


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if text == "✅ Готов(а) продолжить":
        await show_ready_continue_menu(update)

        await update.message.reply_text(
            "Прежде чем мы перейдем к первому практическому заданию, очень важно хорошо подготовиться. Чтобы вы чувствовали себя уверенно, мы подготовили для вас подробные материалы и шпаргалки."
        )

        await update.message.reply_text(
            "Основное руководство:\n"
            "https://docs.google.com/document/d/1wg0ML8tLulT7UHZowqqB-HZo3t_hRyvpdXuMIt7p9-o/edit?tab=t.0"
        )

    elif text == "❌ Не готов(а)":
        await show_not_ready_menu(update)

    elif text == "📚 Изучить материалы":
        await show_study_materials_menu(update)

        await update.message.reply_text(
            "Теперь, когда вы ознакомились с теоретической базой, самое время перейти к практике."
        )

        await update.message.reply_text(
            "Для удобства мы добавляем вас в наш общий рабочий чат в Telegram:\n"
            "https://t.me/+HyVUA8mJRNFjN2Ni"
        )

    elif text == "🎯 Начать работу":
        await show_start_work_menu(update)

    elif text == "🏠 Главное меню":
        await show_main_menu(update)

    elif text == "🔙 Назад":
        history = get_user_state(user_id)
        if len(history) > 1:
            history.pop()
            previous_state = history[-1]

            if previous_state == "start":
                await start(update, context)
            elif previous_state == "ready_continue":
                await show_ready_continue_menu(update)
            elif previous_state == "study_materials":
                await show_study_materials_menu(update)
            elif previous_state == "not_ready":
                await show_not_ready_menu(update)
            elif previous_state == "main_menu":
                await show_main_menu(update)
        else:
            await start(update, context)

    elif text == "💬 Рабочий чат":
        await update.message.reply_text(
            "Рабочий чат команды:\n"
            "https://t.me/+HyVUA8mJRNFjN2Ni\n\n"
            "Присоединяйтесь к общему чату для общения с командой и получения актуальных материалов!"
        )

    elif text == "👥 Руководитель":
        await update.message.reply_text(
            "Руководитель отдела: @lobsters_manager\n\n"
            "Напишите для консультации по вопросам и получения доступа к материалам."
        )

    elif text == "📖 Путеводитель":
        await update.message.reply_text(
            "Основное руководство по работе:\n"
            "https://docs.google.com/document/d/1wg0ML8tLulT7UHZowqqB-HZo3t_hRyvpdXuMIt7p9-o/edit?tab=t.0"
        )

    elif text == "ℹ️ О вакансии":
        await start(update, context)

    elif text == "💬 Поделиться причиной":
        await update.message.reply_text(
            "Пожалуйста, напишите в одном предложении, что именно не устроило "
            "(например: 'условия оплаты', 'график отчетности', 'суть работы' и т.д.)"
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Ошибка: {context.error}")


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, handle_buttons))
    application.add_error_handler(error_handler)

    print("Бот запущен...")
    application.run_polling()


if __name__ == "__main__":
    main()
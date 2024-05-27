import telebot
import math

token = "7005687808:AAHmyd4kMAfE0Wh_QLfb8hlI4BwMzB9ff-A"
bot = telebot.TeleBot(token)

def calculate_remaining_balance(principal, annual_rate, years, payments_made):
    monthly_rate = annual_rate / 12 / 100
    total_payments = years * 12
    if monthly_rate == 0:
        return principal - (principal / total_payments) * payments_made

    annuity_factor = (monthly_rate * (1 + monthly_rate)**total_payments) / ((1 + monthly_rate)**total_payments - 1)
    monthly_payment = principal * annuity_factor

    remaining_balance = principal * (1 + monthly_rate)**payments_made - (monthly_payment / monthly_rate) * ((1 + monthly_rate)**payments_made - 1)
    return remaining_balance

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я помогу тебе узнать, сколько осталось выплатить по кредиту. Отправь мне данные в формате:\n\n"
                          "Сумма кредита, Годовая процентная ставка, Срок кредита (в годах), Количество выплат (месяцев)")

@bot.message_handler(func=lambda message: True)
def get_loan_info(message):
    try:
        data = message.text.split(", ")
        principal = float(data[0])
        annual_rate = float(data[1])
        years = int(data[2])
        payments_made = int(data[3])

        remaining_balance = calculate_remaining_balance(principal, annual_rate, years, payments_made)
        response = f"Остаток по кредиту: {remaining_balance:.2f} рублей"
        bot.reply_to(message, response)
    except (ValueError, IndexError):
        bot.reply_to(message, "Некорректные данные. Пожалуйста, отправьте данные в правильном формате: "
                              "Сумма кредита, Годовая процентная ставка, Срок кредита (в годах), Количество выплат (месяцев)")

bot.polling()

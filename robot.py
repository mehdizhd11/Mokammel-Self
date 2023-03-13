from main import *

TOKEN = '6254025537:AAGT8c4OYPdzGH5r2Y1y3wged0ENLIvNcc0'

from telebot import *

from persiantools import digits

schedule.every().day.at('00:30').do(clearList)

while True:
    
    schedule.run_pending()
    
    sleep(1)

    try:
        
        bot = TeleBot(TOKEN)
        
        @bot.message_handler(commands=['start' , 'help'])

        def start(message):
                            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True , row_width=2)

            item1 = types.KeyboardButton('خرید کد سلف مکمل')

            item2 = types.KeyboardButton('فروش کد سلف مکمل')

            item3 = types.KeyboardButton('درباره ما')

            markup.add(item1,item2,item3)

            bot.send_message(message.chat.id, 'یک گزینه را انتخاب کنید' , reply_markup=markup)

        @bot.message_handler(content_types=['text'])

        def handle_messages(message):
            
            if message.text == 'فروش کد سلف مکمل':
                
                studentId = bot.reply_to(message, 'شماره دانشجویی خود را وارد کنید :')

                bot.register_next_step_handler(studentId, seller_studentId)

            elif message.text == 'خرید کد سلف مکمل':
                
                if Code.codeIndex() > -1 :
                    
                    studentId = bot.reply_to(message, 'شماره دانشجویی خود را وارد کنید :')

                    bot.register_next_step_handler(studentId, buyer_studentId)

                else:

                    bot.send_message(message.chat.id, 'در حال حاضر کدی وجود ندارد')
                    
                    return

            elif message.text == 'درباره ما':
                
                about_us = 'ریات سلف مکمل راهی ساده برای خرید و فروش کد فراموشی سلف مکمل دانشگاه بهشتی است . نحوه کار این ربات به این صورت است که از فروشنده کد ، شماره دانشجویی و کد ملی را دریافت کرده و به صورت خودکار رزرو بودن غذا و استفاده نشدن کد را چک کرده و در صورت تایید در لیست فروش قرار می دهد . سپس از خریدار هم در صورت وجود کد استفاده نشده ، شماره دانشجویی  و کد ملی را دریافت کرده و به صورت خودکار مبلغ ۸۰۰۰ تومان را از حساب خریدار کم می کند و پس از چک کردن مجدد استفاده نشدن کد با حساب فروشنده ، کد را در اختیار خریدار می گذارد . سپس از مبلغ ۸۰۰۰ تومان ، ۶۰۰۰ تومان آن را به حساب فروشنده واریز می کند و باقی مبلغ هم صرف هزینه های نگهداری سرور های داخلی و خارجی ربات می شود . لطفا ما را به دوستان خود در دانشگاه معرفی کنید'

                bot.send_message(message.chat.id, about_us)
                
                return

            else:
                
                bot.send_message(message.chat.id, 'خطا ! دوباره امتحان کنید')
                
                return

        def seller_studentId(studentIdText):
            
            studentId = studentIdText.text

            studentId = digits.fa_to_en(studentId)

            if studentId.isnumeric() == False:
                
                bot.send_message(studentIdText.chat.id, 'خطا ! اطلاعات وارد شده را چک کنید و مجددا وارد شوید')

                return

            studentId = int(studentId)

            idNumber = bot.reply_to(studentIdText, 'شماره ملی خود را وارد کنید :')

            bot.register_next_step_handler(idNumber, seller_idNumber , studentId)

        def buyer_studentId(studentIdText):
            
            studentId = studentIdText.text

            studentId = digits.fa_to_en(studentId)

            if studentId.isnumeric() == False:
                
                bot.send_message(studentIdText.chat.id, 'خطا ! اطلاعات وارد شده را چک کنید و مجددا وارد شوید')

                return

            studentId = int(studentId)

            idNUmber = bot.reply_to(studentIdText, 'شماره ملی خود را وارد کنید :')

            bot.register_next_step_handler(idNUmber, buyer_idNumber , studentId)


        def seller_idNumber(idNumberText , *studentId):
            
            studentId = studentId[0]

            idNumber = idNumberText.text

            idNumber = digits.fa_to_en(idNumber)

            if idNumber.isnumeric() == False:
                
                bot.send_message(idNumberText.chat.id, 'خطا ! اطلاعات وارد شده را چک کنید و مجددا وارد شوید')

                return

            bot.send_message(idNumberText.chat.id, 'چند ثانیه صبر کنید ربات در حال پردازش اطلاعات است')

            idNumber = int(idNumber)

            newSeller = Seller(code=None, studentId=studentId, idNumber=idNumber, payedTo=False , chatId=idNumberText.chat.id)
            
            checkSeller = Seller.check(newSeller)

            if checkSeller:
                
                bot.send_message(idNumberText.chat.id , 'کد شما در لیست قرار گرفت')
                
                return

            else:
                
                bot.send_message(idNumberText.chat.id, 'خطا ! اطلاعات وارد شده و غذای رزرو شده را چک کنید و مجددا وارد ربات شوید')
                
                return

        def buyer_idNumber(idNumberText , *studentId):
            
            studentId = studentId[0]

            idNumber = idNumberText.text

            idNumber = digits.fa_to_en(idNumber)

            if idNumber.isnumeric() == False:
                
                bot.send_message(idNumberText.chat.id, 'خطا ! اطلاعات وارد شده را چک کنید و مجددا وارد شوید')

                return

            bot.send_message(idNumberText.chat.id, 'چند ثانیه صبر کنید ربات در حال تایید کد و انتقال اعتبار است')

            idNumber = int(idNumber)

            newBuyer = Buyer(code=None, studentId=studentId, idNumber=idNumber, isPayed=False)

            giveCode = Buyer.giveCode(newBuyer)

            if giveCode:
                
                bot.send_message(idNumberText.chat.id, f'{newBuyer.code.num}')

                sellerPay = Seller.payment(newBuyer.code.seller)
                
                sellerPayToFile(newBuyer.code)

                bot.send_message(newBuyer.code.seller.chatId, 'کد شما فروخته شد و مبلغ آن به حساب شما واریز شد')
                
                return

            else:
                
                bot.send_message(idNumberText.chat.id , 'خطا ! اطلاعات وارد شده و موجودی حساب خود را چک کنید و دوباره وارد شوید')
                
                return

        bot.polling(non_stop=True)

    except:

        pass

# Concurrency for 2 users
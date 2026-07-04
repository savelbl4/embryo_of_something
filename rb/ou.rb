require 'telegram/bot'

token = '200353198:AAFW8TytuD24kU-lO5cQKBXDiUAFQzPhtvY'

Telegram::Bot::Client.run(token) do |bot|

    bot.listen do |message|

        case message
            when Telegram::Bot::Types::CallbackQuery
                # Here you can handle your callbacks from inline buttons
                if message.data == 'touch'
                    bot.api.send_message(chat_id: message.from.id, text: "Don't touch me!")
                end
            when Telegram::Bot::Types::Message
                kb = [
                    [
                        Telegram::Bot::Types::KeyboardButton.new(text: '/start'),
                        Telegram::Bot::Types::KeyboardButton.new(text: '/stop')
                    ],
                    [Telegram::Bot::Types::KeyboardButton.new(text: 'запали мобилку', request_contact: true)]
                ]
                choice = Telegram::Bot::Types::ReplyKeyboardMarkup.new(keyboard: kb, one_time_keyboard: true)
                bot.api.send_message(chat_id: message.from.id, text: "чё почём, сундучата?!", reply_markup: choice)
                if message.contact
                    puts "id юзверя: #{message.contact.user_id}\nего мобилка: #{message.contact.phone_number}"
                end
                if message.text == '/start'
                    # markup = Telegram::Bot::Types::ForceReply.new(force_reply: true)
                    kb = [Telegram::Bot::Types::KeyboardButton.new(text: 'запали мобилку', request_contact: true)]
                    phone = Telegram::Bot::Types::ReplyKeyboardMarkup.new(keyboard: kb, one_time_keyboard: true)
                    bot.api.send_message(chat_id: message.from.id, text: "что-то я тебя не узнаю...", reply_markup: phone)
                    bot.api.send_message(chat_id: message.from.id, text: "приготовься охуеть")
                end
                if message.text == '/exit'
                    exit
                end
            # when Telegram::Bot::Types::Contact
                    # bot.api.send_message(chat_id: message.chat.id, text: "Give me your")
                    # puts contact.user_id
        end

    end

end
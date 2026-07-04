require 'telegram/bot'

token = '200353198:AAFW8TytuD24kU-lO5cQKBXDiUAFQzPhtvY'

Telegram::Bot::Client.run(token) do |bot|
    bot.listen do |message|
        case message.text
            when '/start@ClosedSpaceBot'
                question = 'хочешь фотку?'
                # See more: https://core.telegram.org/bots/api#replykeyboardmarkup
                answers =
                    Telegram::Bot::Types::ReplyKeyboardMarkup.new(
                        keyboard: [
                            %w(ДА),
                            %w(НЕТ)
                            ],
                        one_time_keyboard: true
                        )
                bot.api.send_message(
                    chat_id: message.chat.id,
                    text: question,
                    reply_to_message_id: message.message_id,
                    reply_markup: answers
                    )
                bot.listen do |message|
                    # hidekd = Telegram::Bot::Types::ReplyKeyboardHide.new(hide_keyboard: true)
                    hidekd = Telegram::Bot::Types::ReplyKeyboardRemove.new(hide_keyboard: true)
                    case message.text
                        when 'ДА'
                            answer = 'Ты молодец'
                            bot.api.send_message(
                                chat_id: message.chat.id,
                                text: answer,
                                reply_to_message_id: message.message_id,
                                reply_markup: hidekd
                                )
                            file_id ="https://pp.vk.me/c619728/v619728281/ee3e/XibNFhSyJsY.jpg"
                            bot.api.sendPhoto(
                                chat_id: message.chat.id,
                                photo: file_id
                                )
                        when 'НЕТ'
                            answer = 'как хочешь'
                            bot.api.send_message(
                                chat_id: message.chat.id,
                                text: answer,
                                reply_to_message_id: message.message_id,
                                reply_markup: hidekd
                                )
                    end
                    break
                end
        end
    end
end
// KeysBot.js
var TelegramBot = require('node-telegram-bot-api');
 
var token = '200353198:AAFW8TytuD24kU-lO5cQKBXDiUAFQzPhtvY';
var botOptions = {
    polling: true
};
var bot = new TelegramBot(token, botOptions);
 
bot.getMe().then(function(me)
{
    console.log('Hello! My name is %s!', me.first_name);
    console.log('My id is %s.', me.id);
    console.log('And my username is @%s.', me.username);
});
 
bot.on('text', function(msg)
{
    var messageChatId = msg.chat.id;
    var messageText = msg.text;
 
    if (messageText === '/keys') {
        var opts = {
            reply_to_message_id: msg.message_id,
            reply_markup: JSON.stringify({
                keyboard: [
                    ['Yes'],
                    ['No']
                ],
                one_time_keyboard: true
            })
        };
        var savaM = {
            text: '*Do you love me?*',
            parse_mode: Markdown
        };
        bot.sendMessage(messageChatId, savaM, opts);
    }
 
    if (messageText === 'Yes') {
        bot.sendMessage(messageChatId, 'I\'m too love you!', { caption: 'I\'m bot!' });
    }
 
    if (messageText === 'No') {
        bot.sendMessage(messageChatId, ':(', { caption: 'I\'m bot!' });
    }
});
// HelloWorldBot.js
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
    var messageDate = msg.date;
    var messageUsr = msg.from.username;
 
    if (messageText === '/say') {
        sendMessageByBot(messageChatId, 'Hello World!');
    }
    
    console.log(msg);
});
 
function sendMessageByBot(aChatId, aMessage)
{
    bot.sendMessage(aChatId, aMessage, { caption: 'I\'m a cute bot!' });
}
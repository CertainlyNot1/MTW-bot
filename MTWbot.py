import telebot
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
import base
bot = telebot.TeleBot("add your token here")

@bot.message_handler(commands=["start"])
def startup(msg):
    keybrd = InlineKeyboardMarkup()
    keybrd.add(InlineKeyboardButton("help",callback_data="help"))
    bot.send_message(msg.chat.id,"Hello! I am an movie library, so. Enjoy!",reply_markup=keybrd)

@bot.message_handler(commands=["help"])
def startup(msg):
    keybrd = InlineKeyboardMarkup()
    keybrd.add(InlineKeyboardButton("movies",callback_data="movies"))
    bot.send_message(msg.chat.id,"∇ We'll help you find movies down below ∇",reply_markup=keybrd)

@bot.message_handler(commands=["movies"])
def startup(msg):
    keybrd = InlineKeyboardMarkup()
    buttons = [InlineKeyboardButton(i,callback_data=f"movie:{i}")for i in base.library]
    keybrd.add(*buttons)
    bot.send_message(msg.chat.id, "Choose the Movie",reply_markup=keybrd)
@bot.callback_query_handler(func=lambda call:True)
def buttonclick(call):
    if call.data == "help":
        keybrd = InlineKeyboardMarkup()
        keybrd.add(InlineKeyboardButton("movies",callback_data="movies"))
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id,"∇ We'll help you find movies down below ∇",reply_markup=keybrd)
    elif call.data == "movies":
        keybrd = InlineKeyboardMarkup()
        buttons = [InlineKeyboardButton(i,callback_data=f"movie:{i}")for i in base.library]
        keybrd.add(*buttons)
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id,"Choose the movie you like",reply_markup=keybrd)
    else:
        movie_title = call.data.replace("movie:","")
        if movie_title in base.library:
            movie_details = base.library[movie_title]
            pictureurl = movie_details.get("Photo","")
            respond = f"{movie_title} ,({movie_details["Year"]})\n Director --> {movie_details["Director"]}\n Genre --> {movie_details["Genre"]}"
            if pictureurl:
                bot.send_photo(call.message.chat.id,pictureurl,caption=respond)
            else:
                bot.send_message(call.message.chat.id,respond)
        else:
            bot.send_message(call.message.chat.id,f"we're sorry but {movie_title} was not found in the library")

@bot.message_handler(commands=["addmovie"])
def add_movie(message):
    bot.reply_to(message, "Type the movie's name:")
    bot.register_next_step_handler(message, add_movie_director)

def add_movie_director(message):
    userdata = {}
    userdata["name"] = message.text
    bot.reply_to(message, "Type the movie director's name:")
    bot.register_next_step_handler(message, add_movie_year,userdata)

def add_movie_year(message,userdata):
    userdata["Director"] = message.text
    bot.reply_to(message, "Type the movie year:")
    bot.register_next_step_handler(message, add_movie_genre,userdata)

def add_movie_genre(message,userdata):
    userdata["Year"] = message.text
    bot.reply_to(message, "Type the movie genre:")
    bot.register_next_step_handler(message, add_movie_photo,userdata)

def add_movie_photo(message,userdata):
    userdata["Genre"] = message.text
    bot.reply_to(message, "Type photo's link (keep it appropriate):")
    bot.register_next_step_handler(message, save_movie,userdata)
def save_movie(message,userdata):
    base.library[userdata["name"]] = {
        "Director":userdata["Director"],
        "Year":userdata["Year"],
        "Genre":userdata["Genre"],
        "Photo":message.text
    }
    bot.reply_to(message, "Movie was succesfully added to the library")















































bot.polling()
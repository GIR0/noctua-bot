import json
import requests
import time
import urllib
import thread
import schedule
import random
from db import *


ONO = ["PYKH", "W9N7", "GYPX", "9MAG", "YYCJ", "F5PM", "X3SK", "FXN9", "BQFG", "73S9", "5W6W", "KZBJ", "3Q4E", "HDDB", "7E4R", "2NBG", "FN2R", "EA34", "MM7U"\
, "UHRY", "9F77", "RZBD", "SU9P", "EJDU", "KFFY", "Y34B", "HVJV", "2R9Z", "7E4T", "U4GT", "T6R6", "FGFH", "GXH7", "XBDD", "FRDJ", "RSJQ", "U5UG", "CCZJ", "PJKG"\
,"PZCG", "B5FV", "8MMR", "KDHT", "HFE5", "C2WT", "J62H", "E697", "J7TS", "C54U", "H5EP", "629Y", "MAK6", "BWDX", "GJPE", "VEXC", "3XK7", "CASD", "BQED", "S8EQ"\
, "2FVN"]
ONO2 = ["749P", "E2XH", "JS7F", "65HR", "MTYX", "K4DR", "FC8A", "7A9M", "ZJJB", "N24Z"]
ONO3 = ["7BPJ",  "6HXA", "5UU9", "PWPX", "VT62", "ZYGH", "EH49"]
admin =[221211693,174955135]
Ameens1 = "AgADBQAD16cxG1D9cVRAUqPXgTANtFQfzDIABOshQWnOm5M0oWgBAAEC"
Ameens2 = "AgADBQAD2KcxG1D9cVRRdymN_tg3LqEQzDIABBvz5QnkSWatPm0BAAEC"
db = feedbackdb()
USERS = userdb()
poll = polldb()
food = orderdb()
rate = ratedb()
survey = surveydb()
ono = onodb()
sample = sampledb()
photo_id = " "
blast_message = " "
blast_options = []
NoctuachatID = -1001080757384
admin_msg = "Hello there, Administrator! " + u'\U0001F916' +"\n\n/view - Displays all feedback\n/delete - Delete selected feedback\n/clearall - Erase all feedback\n\n/addevent - Add an event\n/reviewresponses - View review responses for an event\n/viewrating - View ratings for an event\n/clearevent - Delete an event and its ratings\n/closeorder - Close an ongoing food order\n\n/blast - Ultimate spam function\n/blastresults - Display blast results\n/viewusers - Display blast name list\n/removeuser - Remove user from blast list\n\n/mainmenu - Exit Admin mode"
hungerCriers = []
hungermessages = ["Someone is hungry... "+u"\U0001F914", "Start an order soon maybe? "+u"\U0001F644", "Please order some food soon. My family hasn't ate for 3 days... "+u"\U0001F925"\
, "My neighbour is starting to look juicy... "+u"\U0001F924", "McSpicy meal with coke. Now wouldn't that be lovely? If only someone started an order... "+u"\U0001F31A"\
, "I'm not telling you it's going to be easy. I'm telling you it's going to be worth it "+u"\U0001F44D"+"Okay seriously, someone start an order PLEASE! "+u"\U0001F47F"\
, "NO ONE can do everything, but EVERYONE can do something?! "+u"\U0001F60F", r"I am 700% ready to unhinge my jaw and swallow another owl whole like some owl species tend to do"+"... "+u"\U0001F643"\
, "Can I pleez has cheezburger naow "+u"\U0001F638"]

TOKEN = "358236263:AAHDIU40ArA32mfu9mPBzhyq7X9mmEUoIro"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text, chat_id, reply_markup=None):
    try:
        text = (text.encode("utf8"))
    except:
        pass
    text = urllib.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def send_photo(file_id, chat_id, caption=None):
    url = URL + "sendPhoto?chat_id={}&photo={}".format(chat_id,file_id)
    if caption:
        try:
            caption = urllib.quote_plus(caption.encode("utf8"))
        except:
            pass
        url += "&caption={}".format(caption)
    get_url(url)

def edit_message(chat_id, message_id, text, reply_markup=None):
    try:
        text = (text.encode("utf8"))
    except:
        pass
    text = urllib.quote_plus(text)
    url = URL + "editMessageText?text={}&chat_id={}&message_id={}".format(text, chat_id, message_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def answer_callback_query(call_id, text, show_alert=None):
    text = urllib.quote_plus(text.encode("utf8"))
    url = URL + "answerCallbackQuery?callback_query_id={}&text={}".format(call_id, text)
    if show_alert:
        url += "&show_alert=true"
    get_url(url)

def empty_answer(call_id):
    url = URL + "answerCallbackQuery?callback_query_id={}".format(call_id)
    get_url(url)

def build_keyboard(items):
    for a in items:
        for b in a:
            try:
                b = b.encode("utf8")
            except:
                pass
            b = urllib.quote_plus(b)
    reply_markup = {"keyboard":items, "one_time_keyboard": True, "selective": True}
    return json.dumps(reply_markup)

def inline_keyboard(items):
    for a in items:
        for b in a:
            for c in b:
                try:
                    b[c] = (b[c].encode("utf8"))
                except:
                    pass
                b[c] = urllib.quote_plus(b[c])
    reply_markup = {"inline_keyboard":items}
    return json.dumps(reply_markup)

def remove_keyboard():
    reply_markup = {"remove_keyboard": True, "selective": True}
    return json.dumps(reply_markup)

def delayed_response(blast_message, keyboard):
    print("delayed_response started")
    count = 0
    while (count != 3):
        for x in xrange(108):
            time.sleep(100)
        results = poll.get_all()
        for x in results:
            if x[1] == "Yet to reply":
                send_message(blast_message, x[2], keyboard)
        count += 1

def daily_reset():
    food.clear()
    hungerCriers = []

def daily_reset_run():
    schedule.every().day.at("20:30").do(daily_reset)
    while True:
        schedule.run_pending()
        time.sleep(1)

def orderfood_message():
    descriptions = []
    for x in food.get_all_description():
        if x[1] != "(locked)":
            descriptions.append(x[0])
    descriptions = list(set(descriptions))
    if len(descriptions) > 0:
        descriptions.reverse()
        descriptions = [str(i+1) + ") " + x for i, x in enumerate(descriptions)]
        message = u"\u23F0Ongoing Order\U0001F4DD\n"
        for x in descriptions:
                message += x + "\n"
    else:
        message = "There is currently no order ongoing"
    message += "\n" + u"\U0001F354 HungerCount \U0001F35F: " + str(len(hungerCriers)) + "\n" + u"What would you like to do? \U0001F4AD"
    return message

def orderfood_menu():
    options =[["Hunger Cry"+u'\U0001F4E2', "Start Order"+u'\U0001F4CD'], ["View Order"+u'\U0001F5D2', "Add Order"+u'\U0001F355'], ["Edit Order"+u'\U0001F4DD', u"Menus\U0001F374"], ["Manage Order"+u'\U0001F510', "back"]]
    keyboard = build_keyboard(options)
    return keyboard

class User:
    def __init__(self, id):
        self.id = id
        self.survey =["","","","",""]
        self.event = ""
        self.ordererid = [0, ""]
        self.description = ["", ""]
        self.edit = ""
        self.idx = 0
        self.orderlist = []
        self.display = ""
        self.owl = 0
        self.owlet = 0
    def MainMenu(self,text,chat,name):
        if text == "/admin":
            if chat in admin:
                self.stage = self.admin
                send_message(admin_msg, chat, remove_keyboard())
        elif text == "/start" or text == "back" or text == "/mainmenu":
            options =[[u"Owl-Owlet Anonymous Chat\U0001F4AC"], [u"OrderFood\U0001F35F"], [u"AlmaNoc\U0001F4C6", u"Feedback\U0001F5D2"], [u"Help Desk\U0001F6CE", u"About the Bot\U0001F989"]]
            keyboard = build_keyboard(options)
            send_message("Hello there, " + name + "! Nocbot at your service! " + u'\U0001F989', chat, keyboard)
        elif text == u"Feedback\U0001F5D2":
            options =[[u"General Feedback\u2601", u"Bot Suggestions\U0001F916"], [u"About House Events\U0001F3DA", "back"]]
            keyboard = build_keyboard(options)
            send_message("Is there anything particular you would like to feedback about?", chat, keyboard)
            self.stage = self.Feedback1
        elif text == u"OrderFood\U0001F35F":
            send_message(orderfood_message(), chat, orderfood_menu())
            self.stage = self.orderFood
        elif text == u"AlmaNoc\U0001F4C6":
            options = [[u"Noctua Events\U0001F4E3", u"College Calendar\U0001F5D3"], [u"Rate Our Events\U0001F4AF", "back"]]
            keyboard = build_keyboard(options)
            send_message("Hello " + name + u", welcome to the AlmaNoc! \U0001F4C6",chat, keyboard)
            self.stage = self.AlmaNoc
        elif text == u"About the Bot\U0001F989":
            send_message(u'\U0001F989' + " *About Nocbot* " + u'\U0001F989' + "\n\n" + u"\U0001F382" + " Birthday: June 2017\n\n" + u"\U0001F916" + " Bot Developers: Bai Chuan, Fiz, Youkuan\n\n" + u"\U0001F4AC" + " Language Team: Cherie, Jenn, Justin\n\n" + u"\U0001F171" + " Beta Test Team: Cheng Yong, Cherie, Ian, Jenn, Justin, Pohan, Vernon, Wesley", chat)
            options =[[u"Owl-Owlet Anonymous Chat\U0001F4AC"], [u"OrderFood\U0001F35F"], [u"AlmaNoc\U0001F4C6", u"Feedback\U0001F5D2"], [u"Help Desk\U0001F6CE", u"About the Bot\U0001F989"]]
            keyboard = build_keyboard(options)
            send_message("Hello there, " + name + "! Nocbot at your service! " + u'\U0001F989', chat, keyboard)
        elif text == u"Help Desk\U0001F6CE":
            options = [[u"Ask Me Anything\U0001F48B"], [u"Nocbot FAQ\U0001F4E1", "back"]]
            keyboard = build_keyboard(options)
            send_message(u"Welcome to Nocbot Help Desk\U0001F6CE", chat, keyboard)
            self.stage = self.helpdesk
        elif text == "/review":
            events = [x[0] for x in survey.get_all_events()]
            if len(events) > 0:
                options = [[x] for x in list(set(events))]
                options.append(["back"])
                keyboard = build_keyboard(options)
                send_message("Which event would you like to give feedback on?", chat, keyboard)
            else:
                options = [["back"]]
                keyboard = build_keyboard(options)
                send_message("There are currently no events to give feedback on " + u'\U0001F607', chat, keyboard)
            self.stage = self.survey1
        elif text == u"Owl-Owlet Anonymous Chat\U0001F4AC":
            owners = [x[2] for x in ono.get_four()]
            if chat in owners:
                send_message("Hello there, Anonymous! Click or type any of the following:\n/owl: Chat with your Owl\n/owlet: Chat with your Owlet\n/mainmenu: Exits the Chat feature, and return to the Main Menu", chat, remove_keyboard())
                self.stage = self.Anonymous
            else:
                send_message("Please enter your 4-digit UserID.\n\nor click /mainmenu to exit the registration process", chat, remove_keyboard())
                self.stage = self.register
        else:
            send_message("Did you mean: /start", chat, remove_keyboard())
    def stage(self,text,chat,name):
        self.MainMenu(text,chat,name)

    def inline(self,update):
        self.ignore(update)

    def ignore(self,update):
        pass

    def empty(self,text,chat,name):
        pass

    def register(self,text,chat,name):
        if text not in ONO and text not in ONO2 and text not in ONO3:
            send_message("You have entered the wrong 4-digit number. Please try again, or type /mainmenu to exit.", chat, remove_keyboard())
            return
        else:
            for x in ono.get_owner_from_four(text):
                test = x[2]
                break
            if test == 0:
                ono.register(text, chat, name)
                send_message("Hello there, Anonymous! Click or type any of the following:\n/owl: Chat with your Owl\n/owlet: Chat with your Owlet\n/mainmenu: Exit the Chat feature, and return to the Main Menu. You will still be able to receive any incoming messages!", chat, remove_keyboard())
                self.stage = self.Anonymous
            else:
                send_message("You have entered the wrong 4-digit number. Please try again, or type /mainmenu to exit.", chat, remove_keyboard())

    def Anonymous(self,text,chat,name):
        if text == "/owl":
            for x in ono.get_four_from_owner(chat):
                me = x[1]
                break
            if me in ONO:
                owl = ONO[(ONO.index(me) - 1)]
            elif me in ONO2:
                owl = ONO2[(ONO2.index(me) - 1)]
            else:
                owl = ONO3[(ONO3.index(me) - 1)]
            for x in ono.get_owner_from_four(owl):
                self.owl = x[2]
                break
            send_message("You have been connected with your Owl. Whatever you type here will be sent anonymously to him/her.", chat)
            self.stage = self.owlchat
        elif text == "/owlet":
            for x in ono.get_four_from_owner(chat):
                me = x[1]
                break
            if me in ONO:
                owlet = ONO[(ONO.index(me) + 1)%len(ONO)]
            elif me in ONO2:
                owlet = ONO2[(ONO2.index(me) + 1)%len(ONO2)]
            else:
                owlet = ONO3[(ONO3.index(me) + 1)%len(ONO3)]
            for x in ono.get_owner_from_four(owlet):
                self.owlet = x[2]
                break
            send_message("You have been connected with your Owlet. Whatever you type here will be sent anonymously to him/her.", chat)
            self.stage = self.owletchat

    def owlchat(self,text,chat,name):
        if text == "/owlet":
            for x in ono.get_four_from_owner(chat):
                me = x[1]
                break
            if me in ONO:
                owlet = ONO[(ONO.index(me) + 1)%len(ONO)]
            elif me in ONO2:
                owlet = ONO2[(ONO2.index(me) + 1)%len(ONO2)]
            else:
                owlet = ONO3[(ONO3.index(me) + 1)%len(ONO3)]
            for x in ono.get_owner_from_four(owlet):
                self.owlet = x[2]
                break
            send_message("You have been connected with your Owlet. Whatever you type here will be sent anonymously to him/her.", chat)
            self.stage = self.owletchat
            return
        elif text == "/owl":
            for x in ono.get_four_from_owner(chat):
                me = x[1]
                break
            if me in ONO:
                owl = ONO[(ONO.index(me) - 1)]
            elif me in ONO2:
                owl = ONO2[(ONO2.index(me) - 1)]
            else:
                owl = ONO3[(ONO3.index(me) - 1)]
            for x in ono.get_owner_from_four(owl):
                self.owl = x[2]
                break
            send_message("You have been connected with your Owl. Whatever you type here will be sent anonymously to him/her.", chat)
            return
        if self.owl != 0:
            send_message("From your Owlet:\n" + text, self.owl)
        else:
            send_message(u"Your message has failed to send, because he/she has yet to sign in to Nocbot. Please be patient and try again soon! \U0001F642", chat)

    def owletchat(self,text,chat,name):
        if text == "/owl":
            for x in ono.get_four_from_owner(chat):
                me = x[1]
                break
            if me in ONO:
                owl = ONO[(ONO.index(me) - 1)]
            elif me in ONO2:
                owl = ONO2[(ONO2.index(me) - 1)]
            else:
                owl = ONO3[(ONO3.index(me) - 1)]
            for x in ono.get_owner_from_four(owl):
                self.owl = x[2]
                break
            send_message("You have been connected with your Owl. Whatever you type here will be sent anonymously to him/her.", chat)
            self.stage = self.owlchat
            return
        elif text == "/owlet":
            for x in ono.get_four_from_owner(chat):
                me = x[1]
                break
            if me in ONO:
                owlet = ONO[(ONO.index(me) + 1)%len(ONO)]
            elif me in ONO2:
                owlet = ONO2[(ONO2.index(me) + 1)%len(ONO2)]
            else:
                owlet = ONO3[(ONO3.index(me) + 1)%len(ONO3)]
            for x in ono.get_owner_from_four(owlet):
                self.owlet = x[2]
                break
            send_message("You have been connected with your Owlet. Whatever you type here will be sent anonymously to him/her.", chat)
            return
        if self.owlet != 0:
            send_message("From your Owl:\n" + text, self.owlet)
        else:
            send_message(u"Your message has failed to send, because he/she has yet to sign in to Nocbot. Please be patient and try again soon! \U0001F642", chat)

    def Feedback1(self,text,chat,name):
        if text == u"General Feedback\u2601":
            send_message("This option is for submitting feedback about any general issues. Please submit any house-related queries and suggestions you may have here! We want to hear your voice " + u'\ud83d\udce3'\
            + "\n\nWhen you are done, hit send to submit your feedback. If you decide not to submit feedback, please enter /mainmenu to cancel.", chat, remove_keyboard())
            self.stage = self.FeedbackGF
        elif text == u"Bot Suggestions\U0001F916":
            send_message("This option is for submitting feedback about bot functions. Please submit bug reports, feature requests, and suggestions for future improvements here! We thank you for your contributions " + u'\ud83d\ude47\ud83c\udffb'\
            + "\n\nWhen you are done, hit send to submit your feedback. If you decide not to submit feedback, please enter /mainmenu to cancel.", chat, remove_keyboard())
            self.stage = self.FeedbackBI
        elif text == u"About House Events\U0001F3DA":
            send_message("This option is for submitting feedback regarding any house events. Please submit any queries and suggestions you may have here! " + u"\U0001F618" + "\n\nWhen you are done, hit send to submit your feedback. If you decide not to submit feedback, please enter /mainmenu to cancel.", chat, remove_keyboard())
            self.stage = self.FeedbackHE
        elif text == "back":
            options =[[u"Owl-Owlet Anonymous Chat\U0001F4AC"], [u"OrderFood\U0001F35F"], [u"AlmaNoc\U0001F4C6", u"Feedback\U0001F5D2"], [u"Help Desk\U0001F6CE", u"About the Bot\U0001F989"]]
            keyboard = build_keyboard(options)
            send_message("Hello there, " + name + "! Nocbot at your service! " + u'\U0001F989', chat, keyboard)
            self.stage = self.MainMenu

    def FeedbackGF(self,text,chat,name):
        db.add_item(text + " [" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "]", "General Feedback", chat, name)
        send_message("Your feedback has been received! Thank you for your submission " + u'\U0001F60A' + "\n\nAny other feedback to add? Continue typing and hit send to submit more feedback " + u'\ud83d\uddd2' + "\n\nWhen you are done, please enter /mainmenu to finish.", chat)

    def FeedbackBI(self,text,chat,name):
        db.add_item(text + " [" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "]", "Bot Suggestions", chat, name)
        send_message("Your feedback has been received! Thank you for your submission " + u'\U0001F60A' + "\n\nAny other feedback to add? Continue typing and hit send to submit more feedback " + u'\ud83d\uddd2' + "\n\nWhen you are done, please enter /mainmenu to finish.", chat)

    def FeedbackHE(self,text,chat,name):
        db.add_item(text + " [" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "]", "About House Events", chat, name)
        send_message("Your feedback has been received! Thank you for your submission " + u'\U0001F60A' + "\n\nAny other feedback to add? Continue typing and hit send to submit more feedback " + u'\ud83d\uddd2' + "\n\nWhen you are done, please enter /mainmenu to finish.", chat)

    def orderFood(self,text,chat,name):
        global hungerCriers
        global hungermessages
        if text == "Start Order"+u'\U0001F4CD':
            orderstarters = []
            for x in food.get_all():
                if x[6] != "(locked)":
                    orderstarters.append(x[1])
            orderstarters = list(set(orderstarters))
            orderstarters2 = []
            for x in food.get_all():
                    orderstarters2.append(x[1])
            orderstarters2 = list(set(orderstarters2))
            if chat in orderstarters2:
                send_message(u'Please close your current order before starting a new one via "Order Food \u27A1 Manage Order \u27A1" Close Order".', chat, remove_keyboard())
                send_message(orderfood_message(), chat, orderfood_menu())
            elif len(orderstarters) == 0:
                send_message("Where would you like to order from?\n\nIf you decide not to start an order, click /back to return to the previous menu.", chat, remove_keyboard())
                self.stage = self.StartOrder2
            else:
                options =[["Start Order"+u'\U0001F4CD'],["back"]]
                keyboard = build_keyboard(options)
                send_message("There is already an ongoing order being collated..." + u"\U0001F914" +"\nWould you like to start a separate order?", chat, keyboard)
                self.stage = self.StartOrder1
        elif text == "View Order"+u'\U0001F5D2':
            allorders = []
            for x in food.get_all():
                if x[6] != "(locked)":
                    allorders.append(x[1])
            if len(allorders) > 0:
                orderstarters = list(set([x[1] for x in food.get_all()]))
                if chat in orderstarters:
                    orders =[]
                    for x in food.get_by_orderstarter(chat):
                        if x[5] != "-":
                            orders.append(x[5] + " - " + x[3])
                    orders = [str(i+1) + ". " + x for i, x in enumerate(orders)]
                    if len(orders) > 0:
                        message = u"Order List\U0001F4DD".encode("utf8") + "\n" + "\n".join(orders)
                    else:
                        message = u"Order List\U0001F4DD".encode("utf8") + "\n" + "Your list has 0 orders added currently" + u"\U0001F52A".encode("utf8")
                    orders = ["("+x[2]+") " + x[3] for x in food.get_by_owner(chat)]
                    orders = [str(i+1) + ". " + x for i, x in enumerate(orders)]
                    message += u"\n\nMy Orders\U0001F354\n".encode("utf8")
                    if len(orders) > 0:
                        message += "\n".join(orders)
                    else:
                        message += "You have 0 orders added currently."
                else:
                    message = u"Ongoing orders\U0001F4DD\n".encode("utf8")
                    descriptions = []
                    for x in food.get_all_description():
                        if not x[0].startswith("(locked)"):
                            descriptions.append(x[0])
                    descriptions = list(set(descriptions))
                    descriptions = [str(i+1) + ") " + x for i, x in enumerate(descriptions)]
                    message += "\n".join(descriptions)
                    orders = []
                    for x in food.get_by_owner(chat):
                        if x[6] != "(locked)":
                            orders.append("("+x[2]+") "+ x[3])
                    orders = [str(i+1) + ". " + x for i, x in enumerate(orders)]
                    message += u"\n\nMy orders\U0001F354\n".encode("utf8")
                    if len(orders) > 0:
                        message += "\n".join(orders)
                    else:
                        message += "You have 0 orders added currently."
                send_message(message, chat, remove_keyboard())
            send_message(orderfood_message(), chat, orderfood_menu())
        elif text == "Manage Order"+u'\U0001F510':
            orderstarters = list(set([x[1] for x in food.get_all()]))
            if chat in orderstarters:
                orders =[]
                for x in food.get_by_orderstarter(chat):
                    if x[5] != "-":
                        orders.append(x[5] + " - " + x[3])
                if len(orders) > 0:
                    options =[[u"Lock/Unlock List\U0001F510", u"Hotlines\u260E"], [u"Settle Payments\U0001F4B0", u"Close Order\u2611"], [u"Quick Tutorial\U0001F393", "back"]]
                    keyboard = build_keyboard(options)
                    send_message(u"Hello there, Orderer! \U0001F607\nWhat would you like to do?", chat, keyboard)
                    send_message(u'First time here? Select "Quick Tutorial\U0001F393" for detailed instructions.', chat)
                else:
                    options =[[u"Close Order\u2611"],["back"]]
                    keyboard = build_keyboard(options)
                    send_message("There are 0 orders on your list. Proceed to close?", chat, keyboard)
                self.stage = self.ManageOrder
            else:
                send_message(u"\u26D4 Only the order initiator may manage the order.", chat, remove_keyboard())
                send_message(orderfood_message(), chat, orderfood_menu())
        elif text == "Add Order"+u'\U0001F355':
            allorders = []
            for x in food.get_all():
                if x[6] != "(locked)":
                    allorders.append(x[1])
            if len(allorders) > 0:
                descriptions = []
                for x in food.get_all_description():
                    if x[1] != "(locked)":
                        descriptions.append(x[0])
                descriptions = list(set(descriptions))
                options = []
                for x in descriptions:
                    options.append([x])
                options.append(["back"])
                keyboard = build_keyboard(options)
                send_message("Which order?", chat, keyboard)
                self.stage = self.AddOrder1
            else:
                send_message(orderfood_message(), chat, orderfood_menu())
        elif text == "Edit Order"+u'\U0001F4DD':
            options = [[u"Change Order\U0001F6E0"], [u"Remove Order\U0001F5D1"]]
            keyboard = build_keyboard(options)
            send_message("What would you like to do?", chat, keyboard)
            self.stage = self.EditOrder
        elif text == u"Menus\U0001F374":
            options = [[u"Ameens\U0001F958"], [u"Suggest New Menu\U0001F4A1", "back"]]
            keyboard = build_keyboard(options)
            send_message("These are the menus from places that we usually order from!", chat, keyboard)
            self.stage = self.Menus1
        elif text == "Hunger Cry"+u'\U0001F4E2':
            if chat not in hungerCriers:
                hungerCriers.append(chat)
                count = len(hungerCriers)
                if count < 3:
                    send_message(hungermessages[count-1] + "\n\n" + u"\U0001F354 HungerCount \U0001F35F: " + str(len(hungerCriers)), NoctuachatID)
                else:
                    message = hungermessages[random.randint(2,len(hungermessages)-1)]
                    send_message(message + "\n\n" + u"\U0001F354 HungerCount \U0001F35F: " + str(len(hungerCriers)), NoctuachatID, remove_keyboard())
                send_message("Hoot hoot "+u'\U0001F989'+"Your cry has been heard!\n\nThe current number of people starving is "+str(len(hungerCriers))+". When an order is started, Nocbot will PM you "+u'\U0001F609', chat, remove_keyboard())
            else:
                send_message(u"Your Cry has already been heard! \U0001F4E3", chat, remove_keyboard())
            send_message(orderfood_message(), chat, orderfood_menu())
        elif text == "back":
            options =[[u"Owl-Owlet Anonymous Chat\U0001F4AC"], [u"OrderFood\U0001F35F"], [u"AlmaNoc\U0001F4C6", u"Feedback\U0001F5D2"], [u"Help Desk\U0001F6CE", u"About the Bot\U0001F989"]]
            keyboard = build_keyboard(options)
            send_message("Hello there, " + name + "! Nocbot at your service! " + u'\U0001F989', chat, keyboard)
            self.stage = self.MainMenu

    def StartOrder1(self,text,chat,name):
        if text == "back":
            send_message(orderfood_message(), chat, orderfood_menu())
            self.stage = self.orderFood
        elif text == "Start Order"+u'\U0001F4CD':
            send_message("Where would you like to order from?\n\nIf you decide not to start an order, click /back to return to the previous menu.", chat, remove_keyboard())
            self.stage = self.StartOrder2

    def StartOrder2(self,text,chat,name):
        if text == "/back":
            send_message(orderfood_message(), chat, orderfood_menu())
            self.stage = self.orderFood
        else:
            self.description[0] = text
            send_message("What time would you like to close the order at?\n\nIf you decide not to start an order, click /back to return to the OrderFood menu.", chat, remove_keyboard())
            self.stage = self.StartOrder3

    def StartOrder3(self,text,chat,name):
        if text == "/back":
            self.description[0] = ""
            send_message(orderfood_message(), chat, orderfood_menu())
            self.stage = self.orderFood
        else:
            self.description[1] = text
            send_message(u"\U0001F374"+ name + " has started an order!\n" + u"\U0001F6F5" + "Food from: " + self.description[0] + "\n" + u"\U0001F553" + "Order closing at: " + self.description[1], NoctuachatID)
            food.add_order(chat, self.description[0] + " " + self.description[1], "-", 0, "-")
            for x in hungerCriers:
                if x != chat:
                    send_message("Hoot-ray, your knight in shining armour " + name + " has come to save you from impending starvation! " + 	u"\U0001F389\U0001F389\U0001F389" + "\n\n" + u"\U0001F6F5" + "Food from: " + self.description[0] + "\n" + u"\U0001F553" + "Order closing at: " + self.description[1] + '\n\nAdd your items via "Order Food ' + u"\u27A1" + ' Add Order"!', x)
            send_message(orderfood_message(), chat, orderfood_menu())
            self.stage = self.orderFood


    def AddOrder1(self,text,chat,name):
        descriptions = []
        for x in food.get_all_description():
            if x[1] != "(locked)":
                descriptions.append(x[0])
        if text == "back":
            send_message(orderfood_message(), chat, orderfood_menu())
            self.stage = self.orderFood
        elif text.encode("utf8") in descriptions:
            self.ordererid[1] = text
            for x in food.get_by_description(text):
                self.ordererid[0] = x[1]
                break
            send_message(u'What would you like to order?\neg. "McFlurry x 2 " \U0001F366\n\n or click /back if you are not ordering', chat, remove_keyboard())
            self.stage = self.AddOrder2

    def AddOrder2(self,text,chat,name):
        if text != "/back":
            food.add_order(self.ordererid[0],self.ordererid[1],text,chat,name)
            send_message("Order has been added", chat, remove_keyboard())
            send_message("1 order added/edited by "+ name, self.ordererid[0])
        send_message(orderfood_message(), chat, orderfood_menu())
        self.stage = self.orderFood

    def RemoveOrder(self,text,chat,name):
        if text != "back":
            descriptions = []
            for x in food.get_by_owner(chat):
                if x[6] != "(locked)":
                    descriptions.append(x[2])
            descriptions = list(set(descriptions))
            orders = []
            for x in descriptions:
                for x in food.get_by_owner_description(chat,x):
                    orders.append(x[3])
            try:
                food.clear_order(orders[int(text)-1], chat)
                send_message("Order has been deleted", chat, remove_keyboard())
            except:
                send_message("Error deleting " + x, chat)
        send_message(orderfood_message(), chat, orderfood_menu())
        self.stage = self.orderFood

    def EditOrder(self,text,chat,name):
        if text == u"Change Order\U0001F6E0":
            allorders = []
            for x in food.get_all():
                if x[6] != "(locked)":
                    allorders.append(x[1])
            if len(allorders) > 0:
                descriptions = []
                for x in food.get_by_owner(chat):
                    if x[6] != "(locked)":
                        descriptions.append(x[2])
                descriptions = list(set(descriptions))
                if len(descriptions) == 0:
                    options =[["Add Order"+u'\U0001F355'],["back"]]
                    keyboard = build_keyboard(options)
                    send_message("You have 0 orders added currently. Would you like to add an order?", chat, keyboard)
                else:
                    message = u"My Orders\U0001F354"
                    count = 0
                    for x in descriptions:
                        message += "\n\n" + x +"\n"
                        hold = [x[3] for x in food.get_by_owner_description(chat,x)]
                        orders = []
                        for x in hold:
                            count += 1
                            y = str(count) + ". " + x
                            orders.append(y)
                        message += "\n".join(orders)
                    send_message(message, chat, remove_keyboard())
                    options = []
                    i = 1
                    while i < count:
                        options.append([str(i), str(i+1)])
                        i += 2
                    if count%2:
                        options.append([str(count), "back"])
                    else:
                        options.append(["back"])
                    keyboard = build_keyboard(options)
                    send_message("Please select the respective number of the order you would like to edit", chat, keyboard)
                self.stage = self.ChangeOrder1
            else:
                send_message(orderfood_message(), chat, orderfood_menu())
                self.stage = self.orderFood
        elif text == u"Remove Order\U0001F5D1":
            descriptions = []
            for x in food.get_by_owner(chat):
                if x[6] != "(locked)":
                    descriptions.append(x[2])
            descriptions = list(set(descriptions))
            if len(descriptions) == 0:
                send_message("You have 0 orders added currently.", chat, remove_keyboard())
                send_message(orderfood_message(), chat, orderfood_menu())
            else:
                message = u"My Orders\U0001F354"
                count = 0
                for x in descriptions:
                    message += "\n\n" + x +"\n"
                    hold = [x[3] for x in food.get_by_owner_description(chat,x)]
                    orders = []
                    for x in hold:
                        count += 1
                        y = str(count) + ". " + x
                        orders.append(y)
                    message += "\n".join(orders)
                send_message(message, chat, remove_keyboard())
                options = []
                i = 1
                while i < count:
                    options.append([str(i), str(i+1)])
                    i += 2
                if count%2:
                    options.append([str(count), "back"])
                else:
                    options.append(["back"])
                keyboard = build_keyboard(options)
                send_message("Please select the respective number of the order you would like to remove", chat, keyboard)
                self.stage = self.RemoveOrder
        elif text == "back":
            send_message(orderfood_message(), chat, orderfood_menu())
            self.stage = self.orderFood


    def ChangeOrder1(self,text,chat,name):
        if text == "/back" or text == "back":
            pass
        elif text == "Add Order"+u'\U0001F355':
            allorders = []
            for x in food.get_all():
                if x[6] != "(locked)":
                    allorders.append(x[1])
            if len(allorders) > 0:
                descriptions = []
                for x in food.get_all_description():
                    if x[1] != "(locked)":
                        descriptions.append(x[0])
                options = []
                for x in list(set(descriptions)):
                        options.append([x])
                options.append(["back"])
                keyboard = build_keyboard(options)
                send_message("Which order?", chat, keyboard)
                self.stage = self.AddOrder1
                return
            else:
                send_message("There is currently no order ongoing", chat, remove_keyboard())
        else:
            descriptions = []
            for x in food.get_by_owner(chat):
                if x[6] != "(locked)":
                    descriptions.append(x[2])
            descriptions = list(set(descriptions))
            orders = []
            for x in descriptions:
                for x in food.get_by_owner_description(chat,x):
                    orders.append(x[3])
            if text > 0:
                try:
                    self.edit = orders[int(text)-1]
                    send_message(u'What would you like to order instead?eg. "McFlurry x 2 " \U0001F366\n\nor click /back to return to the Order Food menu', chat, remove_keyboard())
                    self.stage = self.ChangeOrder2
                except:
                    send_message("Invalid number. Try again\n\nWhich order would you like to edit? Please input the respective numbers.\n\nor click /back to exit", chat)
            else:
                send_message("Invalid number. Try again\n\nWhich order would you like to edit? Please input the respective numbers.\n\nor click /back to exit", chat)
            return
        send_message(orderfood_message(), chat, orderfood_menu())
        self.stage = self.orderFood

    def ChangeOrder2(self,text,chat,name):
        if text != "/back":
            for x in food.get_by_order(self.edit,chat):
                orderstarter = x[1]
                description = x[2]
                break
            food.clear_order(self.edit, chat)
            food.add_order(orderstarter,description,text,chat,name)
            send_message("Order has been edited", chat, remove_keyboard())
            send_message("1 order added/edited by " + name, orderstarter)
        send_message(orderfood_message(), chat, orderfood_menu())
        self.stage = self.orderFood

    def Menus1(self,text,chat,name):
        if text == u"Ameens\U0001F958":
            send_photo(Ameens1, chat)
            send_photo(Ameens2, chat)
            send_message(orderfood_message(), chat, orderfood_menu())
            self.stage = self.orderFood
        elif text == u"Suggest New Menu\U0001F4A1":
            send_message("What other restaurants would you like included in the menu list?\nClick /back to return to the main menu.", chat, remove_keyboard())
            self.stage = self.Menus2
        elif text == "back":
            send_message(orderfood_message(), chat, orderfood_menu())
            self.stage = self.orderFood

    def Menus2(self,text,chat,name):
        if text != "/back":
            send_message(name + " suggested a new menu:\n" + text, NoctuachatID, remove_keyboard())
            send_message(u"Thank you for your input! We'll do our best to implement it in our next update! \U0001F607", chat, remove_keyboard())
        send_message(orderfood_message(), chat, orderfood_menu())
        self.stage = self.orderFood

    def ManageOrder(self,text,chat,name):
        global hungerCriers
        if text == u"Close Order\u2611":
            options = [[u"Yes\u2714", u"No\u2716"]]
            keyboard = build_keyboard(options)
            send_message(u"Are you sure you want to close the order? \U0001F914", chat, keyboard)
            self.stage = self.CloseOrder
        elif text == "back":
            send_message(orderfood_message(), chat, orderfood_menu())
            self.stage = self.orderFood
        elif text == u"Settle Payments\U0001F4B0":
            options = [["start"],["back"]]
            keyboard = build_keyboard(options)
            send_message("Let me assist you splitting the bill!", chat, keyboard)
            self.stage = self.payments
        elif text == u"Quick Tutorial\U0001F393":
            send_message(u"Follow these steps to submit a successful order!\n\nStep 1: Lock/Unlock List\U0001F510\nClicking 'Lock' prevents anyone from adding more orders to the list. Your order list will also be compiled and sorted to assist you in making a smooth phone call later on. Clicking 'Unlock' will undo this action." +\
            u"\n\nStep 2: Hotlines\u260E (Optional)\nThis command sends you a cheatsheet containing the hotlines of all the eateries that are usually ordered from, as well as RC4's address and postal code." +\
            u"\n\nStep 3: Settle Payments\U0001F4B0\nOnce the call has been made and the food delivered, use this command to auto message everyone in the order how much they'll need to pay." +\
            u"\n\nStep 4: Close Order\u2611\nThis command should only be used when everything is settled (ie. food has been ordered, and the bill has been split via Settle Payments). This will remove your list from the master list, which then allows you to create a new list." +\
            u'\n\n\U0001F914 If you have any further questions, do send it via "Help Desk \u27A1 Ask me Anything".', chat, remove_keyboard())
            options =[[u"Lock/Unlock List\U0001F510", u"Hotlines\u260E"], [u"Settle Payments\U0001F4B0", u"Close Order\u2611"], [u"Quick Tutorial\U0001F393", "back"]]
            keyboard = build_keyboard(options)
            send_message(u"Hello there, Orderer! \U0001F607\nWhat would you like to do?", chat, keyboard)
            send_message(u'First time here? Select "Quick Tutorial\U0001F393" for detailed instructions.', chat)
        elif text == u"Hotlines\u260E":
            send_message(u"Quick access to crucial info! \U0001F60F\n\nRC4 Address:-\n\U0001F3E1Residential College 4\n\U0001F6E46 College Avenue East\n\U0001F1F8\U0001F1ECSingapore 138614", chat, remove_keyboard())
            send_message(u"Delivery Hotlines:-\n\U0001F35DAmeens: +65 6777 0555\n\U0001F355Dominos Pizza: +65 6222 6333\n\U0001F357KFC: +65 6222 6111\n\U0001F35FMcDonalds: +65 6777 6333", chat, remove_keyboard())
            options =[[u"Lock/Unlock List\U0001F510", u"Hotlines\u260E"], [u"Settle Payments\U0001F4B0", u"Close Order\u2611"], [u"Quick Tutorial\U0001F393", "back"]]
            keyboard = build_keyboard(options)
            send_message(u"Hello there, Orderer! \U0001F607\nWhat would you like to do?", chat, keyboard)
            send_message(u'First time here? Select "Quick Tutorial\U0001F393" for detailed instructions.', chat)
        elif text == u"Lock/Unlock List\U0001F510":
            for x in food.get_by_orderstarter(chat):
                description = x[2]
                status = x[6]
                break
            if status == "":
                food.lock(chat)
                orders =[]
                for x in food.get_by_orderstarter(chat):
                    if x[5] != "-":
                        orders.append(x[3] + " - (" + x[5]+ ")")
                orders = sorted(orders, key=str.lower)
                orders = [str(i+1) + ". " + x for i, x in enumerate(orders)]
                message = u"Final Order\U0001F50F" + "\n" + "\n".join(orders)
                send_message("Order is locked", chat, remove_keyboard())
                send_message(message, chat, remove_keyboard())
                send_message(description + u" - Order has been locked \U0001F512", NoctuachatID)
            else:
                food.unlock(chat)
                send_message("Order is unlocked", chat, remove_keyboard())
                send_message(description + u" - Order has been unlocked \U0001F512", NoctuachatID)
            options =[[u"Lock/Unlock List\U0001F510", u"Hotlines\u260E"], [u"Settle Payments\U0001F4B0", u"Close Order\u2611"], [u"Quick Tutorial\U0001F393", "back"]]
            keyboard = build_keyboard(options)
            send_message(u"Hello there, Orderer! \U0001F607\nWhat would you like to do?", chat, keyboard)
            send_message(u'First time here? Select "Quick Tutorial\U0001F393" for detailed instructions.', chat)

    def CloseOrder(self,text,chat,name):
        if text == u"Yes\u2714":
            food.clear_by_orderstarter(chat)
            self.description = ["",""]
            send_message("Order is closed", chat, remove_keyboard())
            send_message(orderfood_message(), chat, orderfood_menu())
            self.stage = self.orderFood
        elif text == u"No\u2716":
            orders =[]
            for x in food.get_by_orderstarter(chat):
                if x[5] != "-":
                    orders.append(x[5] + " - " + x[3])
            if len(orders) > 0:
                options =[[u"Lock/Unlock List\U0001F510", u"Hotlines\u260E"], [u"Settle Payments\U0001F4B0", u"Close Order\u2611"], [u"Quick Tutorial\U0001F393", "back"]]
                keyboard = build_keyboard(options)
                send_message(u"Hello there, Orderer! \U0001F607\nWhat would you like to do?", chat, keyboard)
                send_message(u'First time here? Select "Quick Tutorial\U0001F393" for detailed instructions.', chat)
                self.stage = self.ManageOrder
            else:
                send_message(orderfood_message(), chat, orderfood_menu())
                self.stage = self.orderFood


    def payments(self,text,chat,name):
        owners = list(set([x[4] for x in food.get_by_orderstarter(chat)]))
        if text == "back":
            options =[[u"Lock/Unlock List\U0001F510", u"Hotlines\u260E"], [u"Settle Payments\U0001F4B0", u"Close Order\u2611"], [u"Quick Tutorial\U0001F393", "back"]]
            keyboard = build_keyboard(options)
            send_message(u"Hello there, Orderer! \U0001F607\nWhat would you like to do?", chat, keyboard)
            send_message(u'First time here? Select "Quick Tutorial\U0001F393" for detailed instructions.', chat)
            self.stage = self.ManageOrder
        elif text == "start":
            self.orderlist = []
            for x in owners:
                if x > 0:
                    for y in food.get_by_owner_orderstarter(x,chat):
                        details = y[5] + "\n"
                        break
                    orders = [z[3] for z in food.get_by_owner_orderstarter(x,chat)]
                    foods = "\n".join(orders)
                    details += "\n".join(orders) + "\n\n"
                    each = [x,"",foods,details]
                    self.orderlist.append(each)
            self.idx = 0
            send_message("Please enter amount owed by:\n\n" + self.orderlist[self.idx][3] + "click /previous to go back\nclick /skip to skip this entry\nclick /exit to cancel payments", chat, remove_keyboard())
        elif text == "/skip":
            if self.idx == len(self.orderlist) - 1:
                self.idx += 1
                send_message("Done?\n\nclick /back to go back\nclick /done to continue", chat)
            elif self.idx < len(self.orderlist) - 1:
                self.idx += 1
                send_message("Please enter amount owed by:\n\n" + self.orderlist[self.idx][3] + "click /previous to go back\nclick /skip to skip this entry\nclick /exit to cancel payments", chat)
        elif text == "/exit":
            send_message(orderfood_message(), chat, orderfood_menu())
            self.stage = self.orderFood
        elif text == "/previous":
            if self.idx != 0:
                self.idx -= 1
            send_message("Please enter amount owed by:\n\n" + self.orderlist[self.idx][3] + "click /previous to go back\nclick /skip to skip this entry\nclick /exit to cancel payments", chat)
        elif text == "/done":
            message = "Here's the final order list, together with the amounts you've entered. I have forwarded this to everyone who ordered!\n\n"
            for x in self.orderlist:
                print x[3]
                message += ("$" + x[1].encode("utf8") + " - " + x[3]) #for emoji names
            send_message(message, chat)
            for x in self.orderlist:
                if x[1] != "":
                    send_message("You are required to pay $" + x[1] + " to " + name + " for your latest order:\n" + x[2], x[0])
            self.idx = 0
            self.orderlist = []
            send_message(orderfood_message(), chat, orderfood_menu())
            self.stage = self.orderFood
        else:
            if self.idx <= len(self.orderlist) - 1:
                self.orderlist[self.idx][1] = text
                if self.idx == len(self.orderlist) - 1:
                    self.idx += 1
                    send_message("Done?\n\nclick /previous to go back\nclick /done to continue", chat)
                else:
                    self.idx += 1
                    send_message("Please enter amount owed by:\n\n" + self.orderlist[self.idx][3] + "click /previous to go back\nclick /skip to skip this entry\nclick /exit to cancel payments", chat)

    def AlmaNoc(self,text,chat,name):
        if text == u"Noctua Events\U0001F4E3" or text == u"College Calendar\U0001F5D3":
            send_message("Coming Soon!", chat)
            options = [[u"Noctua Events\U0001F4E3", u"College Calendar\U0001F5D3"], [u"Rate Our Events\U0001F4AF", "back"]]
            keyboard = build_keyboard(options)
            send_message("Hello " + name + u", welcome to the AlmaNoc! \U0001F4C6",chat, keyboard)
        elif text == u"Rate Our Events\U0001F4AF":
            events = [x[0] for x in rate.get_all_events()]
            if len(events) > 0:
                options = [[x] for x in list(set(events))]
                options.append(["back"])
                keyboard = build_keyboard(options)
                send_message("Which event would you like to rate?", chat, keyboard)
            else:
                options = [["back"]]
                keyboard = build_keyboard(options)
                send_message("There are currently no events to rate " + u'\U0001F607', chat, keyboard)
            self.stage = self.rate1
        elif text == "back":
            options =[[u"Owl-Owlet Anonymous Chat\U0001F4AC"], [u"OrderFood\U0001F35F"], [u"AlmaNoc\U0001F4C6", u"Feedback\U0001F5D2"], [u"Help Desk\U0001F6CE", u"About the Bot\U0001F989"]]
            keyboard = build_keyboard(options)
            send_message("Hello there, " + name + "! Nocbot at your service! " + u'\U0001F989', chat, keyboard)
            self.stage = self.MainMenu

    def rate1(self,text,chat,name):
        events = [x[0] for x in rate.get_all_events()]
        if text == "back":
            options = [[u"Noctua Events\U0001F4E3", u"College Calendar\U0001F5D3"], [u"Rate Our Events\U0001F4AF", "back"]]
            keyboard = build_keyboard(options)
            send_message("Hello " + name + u", welcome to the AlmaNoc! \U0001F4C6",chat, keyboard)
            self.stage = self.AlmaNoc
        elif text.encode("utf8") in events:
            self.event = text
            ratings = [x[2] for x in rate.get_by_event(text)]
            ratings = list(set(ratings))
            options = []
            for x in ratings:
                if x != "NA":
                    options.append([{"text":x, "callback_data":x}])
            options.append([{"text": u'\u2764'+"New Option", "callback_data": u'\u2764'+"New Option"}])
            options.append([{"text": u'\u274C'+"Cancel", "callback_data": u'\u274C'+"Cancel"}])
            keyboard = inline_keyboard(options)
            send_message("Select one option below that best describes how you feel about this event!", chat, keyboard)
            self.inline = self.rate2
            self.stage = self.empty

    def rate2(self,update):
        call_id = update["callback_query"]["id"]
        chat = update["callback_query"]["message"]["chat"]["id"]
        data = update["callback_query"]["data"]
        message_id = update["callback_query"]["message"]["message_id"]
        name = update["callback_query"]["message"]["chat"]["first_name"]
        empty_answer(call_id)
        if data == u'\u274C'+"Cancel":
            edit_message(chat, message_id, "Cancelled")
            options =[[u"Owl-Owlet Anonymous Chat\U0001F4AC"], [u"OrderFood\U0001F35F"], [u"AlmaNoc\U0001F4C6", u"Feedback\U0001F5D2"], [u"Help Desk\U0001F6CE", u"About the Bot\U0001F989"]]
            keyboard = build_keyboard(options)
            send_message("Hello there, " + name + "! Nocbot at your service! " + u'\U0001F989', chat, keyboard)
            self.stage = self.MainMenu
            self.inline = self.ignore
        elif data == u'\u2764'+"New Option":
            options = [[{"text": "back", "callback_data": "back"}]]
            keyboard = inline_keyboard(options)
            edit_message(chat, message_id, "Please enter your option.", keyboard)
            self.stage = self.rate3
        elif data == "back":
            ratings = [x[2] for x in rate.get_by_event(self.event)]
            ratings = list(set(ratings))
            options = []
            for x in ratings:
                if x != "NA":
                    options.append([{"text":x, "callback_data":x}])
            options.append([{"text": u'\u2764'+"New Option", "callback_data": u'\u2764'+"New Option"}])
            options.append([{"text": u'\u274C'+"Cancel", "callback_data": u'\u274C'+"Cancel"}])
            keyboard = inline_keyboard(options)
            edit_message(chat, message_id, "Select one option below that best describes how you feel about this event!", keyboard)
            self.inline = self.rate2
            self.stage = self.empty
        else:
            event = self.event
            rate.add_item(event,data,chat,name)
            edit_message(chat, message_id, "Thank you for your review!"+u'\U0001F647'+"\n\nWe'll take your views into consideration, and hope to provide an even greater experience for you in our next upcoming event!")
            options =[[u"Owl-Owlet Anonymous Chat\U0001F4AC"], [u"OrderFood\U0001F35F"], [u"AlmaNoc\U0001F4C6", u"Feedback\U0001F5D2"], [u"Help Desk\U0001F6CE", u"About the Bot\U0001F989"]]
            keyboard = build_keyboard(options)
            send_message("Hello there, " + name + "! Nocbot at your service! " + u'\U0001F989', chat, keyboard)
            self.stage = self.MainMenu
            self.inline = self.ignore

    def rate3(self,text,chat,name):
        event = self.event
        rate.add_item(event,text,chat,name)
        send_message("Thank you for your review!"+u'\U0001F647'+"\n\nWe'll take your views into consideration, and hope to provide an even greater experience for you in our next upcoming event!", chat, remove_keyboard())
        options =[[u"Owl-Owlet Anonymous Chat\U0001F4AC"], [u"OrderFood\U0001F35F"], [u"AlmaNoc\U0001F4C6", u"Feedback\U0001F5D2"], [u"Help Desk\U0001F6CE", u"About the Bot\U0001F989"]]
        keyboard = build_keyboard(options)
        send_message("Hello there, " + name + "! Nocbot at your service! " + u'\U0001F989', chat, keyboard)
        self.stage = self.MainMenu
        self.inline = self.ignore

    def survey1(self,text,chat,name):
        events = [x[0] for x in survey.get_all_events()]
        if text == "back":
            options =[[u"Owl-Owlet Anonymous Chat\U0001F4AC"], [u"OrderFood\U0001F35F"], [u"AlmaNoc\U0001F4C6", u"Feedback\U0001F5D2"], [u"Help Desk\U0001F6CE", u"About the Bot\U0001F989"]]
            keyboard = build_keyboard(options)
            send_message("Hello there, " + name + "! Nocbot at your service! " + u'\U0001F989', chat, keyboard)
            self.stage = self.MainMenu
        elif text.encode("utf8") in events:
            self.survey[0] = text
            send_message("What do you think went well during the event?", chat, remove_keyboard())
            self.stage = self.survey2

    def survey2(self,text,chat,name):
        self.survey[1] = text
        send_message("What did you feel could be improved about this event?", chat, remove_keyboard())
        self.stage = self.survey3

    def survey3(self,text,chat,name):
        self.survey[2] = text
        send_message("Do you have suggestions for how we should execute this event again in the future?", chat, remove_keyboard())
        self.stage = self.survey4

    def survey4(self,text,chat,name):
        self.survey[3] = text
        send_message("Any other comments?", chat, remove_keyboard())
        self.stage = self.survey5

    def survey5(self,text,chat,name):
        self.survey[4] = text
        answer = self.survey
        survey.add_item(answer,chat,name)
        send_message("Thank you for your review!"+u'\U0001F647'+"\n\nWe'll take your views into consideration, and hope to provide an even greater experience for you in our next upcoming event!", chat, remove_keyboard())
        options =[[u"Owl-Owlet Anonymous Chat\U0001F4AC"], [u"OrderFood\U0001F35F"], [u"AlmaNoc\U0001F4C6", u"Feedback\U0001F5D2"], [u"Help Desk\U0001F6CE", u"About the Bot\U0001F989"]]
        keyboard = build_keyboard(options)
        send_message("Hello there, " + name + "! Nocbot at your service! " + u'\U0001F989', chat, keyboard)
        self.stage = self.MainMenu

    def helpdesk(self,text,chat,name):
        if text == "back":
            options =[[u"Owl-Owlet Anonymous Chat\U0001F4AC"], [u"OrderFood\U0001F35F"], [u"AlmaNoc\U0001F4C6", u"Feedback\U0001F5D2"], [u"Help Desk\U0001F6CE", u"About the Bot\U0001F989"]]
            keyboard = build_keyboard(options)
            send_message("Hello there, " + name + "! Nocbot at your service! " + u'\U0001F989', chat, keyboard)
            self.stage = self.MainMenu
        elif text == u"Nocbot FAQ\U0001F4E1":
            send_message("Coming Soon!", chat)
            options = [[u"Ask Me Anything\U0001F48B"], [u"Nocbot FAQ\U0001F4E1", "back"]]
            keyboard = build_keyboard(options)
            send_message(u"Welcome to Nocbot Help Desk\U0001F6CE", chat, keyboard)
        elif text == u"Ask Me Anything\U0001F48B":
            send_message(u"What would you like to ask me? \U0001F62C\nClick /back to return to the main menu.", chat, remove_keyboard())
            self.stage = self.ask

    def ask(self,text,chat,name):
        if text != "/back":
            send_message(name + " asked:\n" + text, NoctuachatID, remove_keyboard())
            send_message(u"Understood! I'll get back to you when I have an answer! \U0001F609", chat, remove_keyboard())
        options =[[u"Owl-Owlet Anonymous Chat\U0001F4AC"], [u"OrderFood\U0001F35F"], [u"AlmaNoc\U0001F4C6", u"Feedback\U0001F5D2"], [u"Help Desk\U0001F6CE", u"About the Bot\U0001F989"]]
        keyboard = build_keyboard(options)
        send_message("Hello there, " + name + "! Nocbot at your service! " + u'\U0001F989', chat, keyboard)
        self.stage = self.MainMenu

    def admin(self,text,chat,name):
        if text == "/view":
            items = db.get_Bot()
            items = ["("+x[2]+")"+" "+x[4]+": "+x[1] for x in items]
            items2 = db.get_General()
            items += ["("+x[2]+")"+" "+x[4]+": "+x[1] for x in items2]
            items3 = db.get_House()
            items += ["("+x[2]+")"+" "+x[4]+": "+x[1] for x in items3]
            items = [str(i+1) + ". " + x for i, x in enumerate(items)]
            message = "There are no feedbacks submitted at the moment."
            if len(items) > 0:
                message = "\n".join(items)
            send_message(message, chat, remove_keyboard())
        elif text == "/startONO":
            ono.clear()
            for x in ONO:
                ono.start(x)
        elif text == "/startONO2":
            for x in ONO2:
                ono.start(x)
        elif text == "/startONO3":
            for x in ONO3:
                ono.start(x)
        elif text == "/ONO":
            items = [x[1] + "-" + x[3] for x in ono.get_four()]
            message = "\n".join(items)
            send_message(message, chat, remove_keyboard())
        elif text == "/reset":
            send_message("Enter the code!", chat)
            self.stage = self.reset
        elif text == "/delete":
            items = db.get_Bot()
            items = ["("+x[2]+")"+" "+x[4]+": "+x[1] for x in items]
            items2 = db.get_General()
            items += ["("+x[2]+")"+" "+x[4]+": "+x[1] for x in items2]
            items3 = db.get_House()
            items += ["("+x[2]+")"+" "+x[4]+": "+x[1] for x in items3]
            items = [str(i+1) + ". " + x for i, x in enumerate(items)]
            if len(items) == 0:
                message = "There are no feedbacks submitted at the moment."
                send_message(message, chat, remove_keyboard())
            else:
                message = "\n".join(items)
                send_message(message, chat, remove_keyboard())
                send_message("Which feedback do you wish to delete? Please input the respective numbers.\n\nor click /back to exit", chat, remove_keyboard())
                self.stage = self.delete
        elif text == "/clearall":
            db.clear()
            send_message("Feedbacks cleared", chat, remove_keyboard())
        elif text == "/viewusers":
            items = USERS.get_name()
            items = [str(i+1) + ". " + x for i, x in enumerate(items)]
            message = "\n".join(items)
            send_message(message, chat, remove_keyboard())
        elif text == "/removeuser":
            items = USERS.get_name()
            items.append("back")
            items = [[x] for x in items]
            keyboard = build_keyboard(items)
            send_message("Which user do you want to remove?", chat, keyboard)
            self.stage = self.removeuser
        elif text == "/blast":
            options =[["text"],["photo"],["back"]]
            keyboard = build_keyboard(options)
            send_message("Choose the type:", chat, keyboard)
            self.stage = self.blast0
        elif text == "/blastresults":
            stats = poll.get_stats()
            message = ""
            if "Yet to reply" in stats:
                message = "Yet to reply" + ": " + str(stats["Yet to reply"]) + "\n"
                results = [x[3] for x in poll.get_results("Yet to reply")]
                results = [str(i+1) + ". " + x for i, x in enumerate(results)]
                message += "\n".join(results) + "\n\n"
            for key in stats:
                if key != "Yet to reply":
                    message += key + ": " + str(stats[key]) + "\n"
                    results = [x[3] for x in poll.get_results(key)]
                    results = [str(i+1) + ". " + x for i, x in enumerate(results)]
                    message += "\n".join(results) + "\n\n"
            send_message(message, chat, remove_keyboard())
        elif text == "/addevent":
            send_message("Add an event to be rated\n\nor click /back to exit", chat, remove_keyboard())
            self.stage = self.addevent
        elif text == "/reviewresponses":
            events = [x[0] for x in survey.get_all_events()]
            if len(events) > 0:
                options = [[x] for x in list(set(events))]
                options.append(["back"])
                keyboard = build_keyboard(options)
                send_message("Which event would you like to view results for?", chat, keyboard)
            else:
                options = [["back"]]
                keyboard = build_keyboard(options)
                send_message("There are currently no events added " + u'\U0001F607', chat, keyboard)
            self.stage = self.surveyresults
        elif text == "/clearevent":
            events = [x[0] for x in survey.get_all_events()]
            options = [[x] for x in list(set(events))]
            options.append(["back"])
            keyboard = build_keyboard(options)
            send_message("Which event would you like to remove?", chat, keyboard)
            self.stage = self.clearevent
        elif text == "/viewrating":
            events = [x[0] for x in rate.get_all_events()]
            if len(events) > 0:
                options = [[x] for x in list(set(events))]
                options.append(["back"])
                keyboard = build_keyboard(options)
                send_message("Which event would you like to view results for?", chat, keyboard)
                self.stage = self.viewrating
            else:
                send_message("There are currently no events added " + u'\U0001F607', chat)
        elif text == "/closeorder":
            descriptions = [x[0] for x in food.get_all_description()]
            descriptions = list(set(descriptions))
            if len(descriptions) > 0:
                message = "Ongoing Orders:\n\n"
                options = []
                count = 1
                for x in descriptions:
                    message += str(count) + ". " + x + "\n"
                    orders =[]
                    for y in food.get_by_description(x):
                        if y[5] != "-":
                            orders.append(y[5] + " - " + y[3])
                    message += "\n".join(orders)
                    message += "\n\n"
                    options.append([x])
                    count += 1
                send_message(message, chat, remove_keyboard())
                options.append(["back"])
                keyboard = build_keyboard(options)
                send_message("Which order would you like to close?", chat, keyboard)
            else:
                options = [["back"]]
                keyboard = build_keyboard(options)
                send_message("There are currently no ongoing orders " + u'\U0001F607', chat, keyboard)
            self.stage = self.adminclose
        elif text == "/mainmenu":
            pass
        else:
            return

    def reset(self,text,chat,name):
        ono.reset(text)
        send_message("Done!", chat)
        send_message(admin_msg, chat, remove_keyboard())
        self.stage = self.admin

    def adminclose(self,text,chat,name):
        descriptions = [x[0] for x in food.get_all_description()]
        if text == "back":
            send_message(admin_msg, chat, remove_keyboard())
            self.stage = self.admin
        elif text.encode("utf8") in descriptions:
            food.clear_by_description(text)
            send_message("Order is closed", chat, remove_keyboard())
            send_message(admin_msg, chat, remove_keyboard())
            self.stage = self.admin

    def addevent(self,text,chat,name):
        if text != "/back":
            survey.add_item([text,"-","-","-","-"],chat,name)
            rate.add_item(text,"NA",chat,name)
            send_message("Event added!", chat, remove_keyboard())
        send_message(admin_msg, chat, remove_keyboard())
        self.stage = self.admin

    def surveyresults(self,text,chat,name):
        events = [x[0] for x in survey.get_all_events()]
        if text == "back":
            send_message(admin_msg, chat, remove_keyboard())
        elif text.encode("utf8") in events:
            ratings = []
            for x in survey.get_by_event(text):
                if x[2] != "-":
                    ratings.append(x[7]+"\n"+x[2]+"\n"+x[3]+"\n"+x[4]+"\n"+x[5])
            ratings = [str(i+1) + ". " + x for i, x in enumerate(ratings)]
            message = "\n\n".join(ratings)
            send_message(message, chat, remove_keyboard())
            send_message(admin_msg, chat, remove_keyboard())
        self.stage = self.admin

    def clearevent(self,text,chat,name):
        events = [x[0] for x in survey.get_all_events()]
        if text == "back":
            send_message(admin_msg, chat, remove_keyboard())
        elif text.encode("utf8") in events:
            survey.delete_event(text)
            rate.delete_event(text)
            send_message("Event deleted", chat, remove_keyboard())
            send_message(admin_msg, chat, remove_keyboard())
        self.stage = self.admin

    def viewrating(self,text,chat,name):
        events = [x[0] for x in rate.get_all_events()]
        if text == "back":
            send_message(admin_msg, chat, remove_keyboard())
        elif text.encode("utf8") in events:
            stats = rate.get_stats(text)
            message = ""
            for key in stats:
                message += key + ": " + str(stats[key]) + "\n"
                results = [x[4] for x in rate.get_results(text,key)]
                results = [str(i+1) + ". " + x for i, x in enumerate(results)]
                message += "\n".join(results) + "\n\n"
            send_message(message, chat, remove_keyboard())
        self.stage = self.admin

    def delete(self,text,chat,name):
        if text != "/back":
            items = [x[1] for x in db.get_Bot()]
            items2 = [x[1] for x in db.get_General()]
            items3 = [x[1] for x in db.get_House()]
            count = 0
            for x in text.split():
                try:
                    if int(x) > len(items) + len(items2):
                        index = int(x) - len(items) - len(items2) - 1
                        feedback = items3[index]
                    elif int(x) > len(items):
                        index = int(x) - len(items) - 1
                        feedback = items2[index]
                    else:
                        index = int(x) - 1
                        feedback = items[index]
                    db.delete_item(feedback)
                    count += 1
                except:
                    send_message("Error deleting " + x, chat)
            if count > 0:
                send_message("Feedback(s) deleted", chat, remove_keyboard())
            send_message(admin_msg, chat, remove_keyboard())
            self.stage = self.admin
        else:
            send_message(admin_msg, chat, remove_keyboard())
            self.stage = self.admin

    def removeuser(self,text,chat,name):
        if text == "back":
            self.stage = self.admin
            send_message(admin_msg, chat, remove_keyboard())
        else:
            USERS.delete_user(text)
            send_message("User removed", chat, remove_keyboard())
            self.stage = self.admin
            send_message(admin_msg, chat, remove_keyboard())

    def blast0(self,text,chat,name):
        if text == "text":
            send_message("Type your message:", chat)
            self.stage = self.blast1
        elif text == "photo":
            send_message("Send your photo here", chat)
            self.stage = self.blastA
        elif text == "back":
            send_message(admin_msg, chat, remove_keyboard())
            self.stage = self.admin

    def blastA(self,photo,chat,name):
        global photo_id
        photo_id = photo
        print photo_id
        options =[["Yes"], ["No"]]
        keyboard = build_keyboard(options)
        send_message("Photo saved! Do you want a caption?", chat, keyboard)
        self.stage = self.blastB

    def blastB(self,text,chat,name):
        global photo_id
        print photo_id
        if text == "Yes":
            send_message("Type your caption:", chat, remove_keyboard())
            self.stage = self.blastC
        if text == "No":
            allusers = USERS.get_id_and_name()
            for x in allusers:
                send_photo(photo_id, x[1])
            send_message("Photo sent", chat, remove_keyboard())
            self.stage = self.admin

    def blastC(self,text,chat,name):
        global photo_id
        allusers = USERS.get_id_and_name()
        for x in allusers:
            send_photo(photo_id, x[1],text)
        send_message("Photo sent", chat, remove_keyboard())
        self.stage = self.admin
        send_message(admin_msg, chat, remove_keyboard())

    def blast1(self,text,chat,name):
        global blast_message
        blast_message = text
        options =[["Next Step"], ["Retype"], ["back"]]
        keyboard = build_keyboard(options)
        send_message("Message saved!", chat, keyboard)
        self.stage = self.blast2

    def blast2(self,text,chat,name):
        global blast_message
        if text == "Retype":
            send_message("Type your message:", chat, remove_keyboard())
            self.stage = self.blast
        elif text == "Next Step":
            send_message("Send the blast with your own customised reply keyboard.\n1. Type in the options separated by a single '$'.\n2. Type /no to not have a reply keyboard", chat, remove_keyboard())
            self.stage = self.blast3
        elif text == "back":
            self.stage = self.admin
            send_message(admin_msg, chat, remove_keyboard())

    def blast3(self,text,chat,name):
        global blast_message
        global blast_options
        if text == "/no":
            allusers = USERS.get_id_and_name()
            for x in allusers:
                send_message(blast_message, x[1])
            self.stage = self.admin
        else:
            blast_options = [["!" + x] for x in text.split("$")]
            keyboard = build_keyboard(blast_options)
            allusers = USERS.get_id_and_name()
            poll.clear()
            for x in allusers:
                poll.add_answer("Yet to reply",x[1],x[2])
                send_message(blast_message, x[1], keyboard)
            thread.start_new_thread(delayed_response, (blast_message, keyboard))
            self.stage = self.admin

    def blast_poll(self,text,chat,name):
        poll.add_answer(text, chat, name)
        send_message("Response recorded!\n\nType /mainmenu to return to the main menu.", chat)


users = []

def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        try:
            if len(updates["result"]) > 0:
                for update in updates["result"]:
                    if "message" in update:
                        if "text" in update["message"]: #only read text
                            text = update["message"]["text"]
                            chat = update["message"]["chat"]["id"]
                            name = update["message"]["from"]["first_name"]
                            if chat > 0:
                                for user in users:
                                    if chat == user.id:
                                        if text.startswith("!"):
                                            user.blast_poll(text,chat,name)
                                        elif text == "/mainmenu":
                                            user.stage = user.MainMenu
                                            user.stage(text,chat,name)
                                        else:
                                            user.stage(text,chat,name)
                                        break
                                    else:
                                        continue
                                if chat not in [user.id for user in users]:
                                        x = User(chat)
                                        users.append(x)
                                        USERS.add_user(chat,name)
                                        if text.startswith("!"):
                                            x.blast_poll(text,chat,name)
                                        elif text == "/mainmenu":
                                            x.stage = x.MainMenu
                                            x.stage(text,chat,name)
                                        else:
                                            x.stage(text,chat,name)
                        if "photo" in update["message"]:
                            check = False
                            photo = update["message"]["photo"][1]["file_id"]
                            chat = update["message"]["chat"]["id"]
                            name = update["message"]["from"]["first_name"]
                            if chat > 0:
                                for user in users:
                                    if chat == user.id:
                                        if user.stage == user.blastA:
                                            check = True
                                            user.stage(photo,chat,name)
                                        break
                                if not check:
                                    send_message(u"I can't understand stickers, images or GIFs. Text me, would ya? \U0001F618", chat)
                        elif "audio" in update["message"] or "video" in update["message"] or "sticker" in update["message"] or "document" in update["message"]:
                            chat = update["message"]["chat"]["id"]
                            send_message(u"I can't understand stickers, images or GIFs. Text me, would ya? \U0001F618", chat)
                    elif "callback_query" in update:
                        chat = update["callback_query"]["message"]["chat"]["id"]
                        for user in users:
                            if chat == user.id:
                                user.inline(update)
                                break
                        if chat not in [user.id for user in users]:
                                x = User(chat)
                                users.append(x)
                                x.inline(update)
                    elif "inline_query" in update:
                        chat = update["inline_query"]["from"]["id"]
                        for user in users:
                            if chat == user.id:
                                user.inline_mode(update)
                                break
                        if chat not in [user.id for user in users]:
                                x = User(chat)
                                users.append(x)
                                x.inline_mode(update)
                last_update_id = get_last_update_id(updates) + 1
        except KeyError, e:
                print('I got a KeyError - reason "%s"' % str(e))
                last_update_id = get_last_update_id(updates) + 1
                pass
        time.sleep(0.5)

if __name__ == '__main__':
    print("Initialised...")
    db.setup()
    USERS.setup()
    poll.setup()
    food.setup()
    rate.setup()
    survey.setup()
    ono.setup()
    sample.setup()
    thread.start_new_thread(daily_reset_run, ())
    main()

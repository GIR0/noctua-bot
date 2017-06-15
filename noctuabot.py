import json
import requests
import time
import urllib
import thread
from db import *

admin =[221211693,174955135]
db = feedbackdb()
USERS = userdb()
poll = polldb()
food = orderdb()
rate = ratedb()
survey = surveydb()
photo_id = " "
blast_message = " "
blast_options = []
NoctuachatID = -1001080757384
orderstarter = 0
hungerCriers = []
hungermessages = ["Someone is hungry...", "Two is better than one", "Anyone else out there?"\
, "I'm not telling you it is going to be easy, I'm telling you it's going to be worth it.\n Someone order please :)", "PLEASE SOMEONE START THE ORDER ALREADY IM STARVING"\
, "NO ONE can do everything but EVERYONE can do something.\nTime to step up!", "Still waiting for someone to volunteer as tribute..."]

TOKEN = "358236263:AAHDIU40ArA32mfu9mPBzhyq7X9mmEUoIro"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
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
        text = urllib.quote_plus(text.encode("utf8"))
    except:
        pass
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
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
    text = urllib.quote_plus(text.encode("utf8"))
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
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True, "selective": True}
    return json.dumps(reply_markup)

def inline_keyboard(items):
    for a in items:
        for b in a:
            for c in b:
                b[c] = urllib.quote_plus(b[c].encode("utf8"))
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
        results = poll.get_results()
        for x in results:
            if x[1] == "Yet to reply":
                send_message(blast_message, x[2], keyboard)
        count += 1


class User:
    def __init__(self, id):
        self.id = id
        self.survey =["","","",""]
        self.event = ""
    def MainMenu(self,text,chat,name):
        if chat in admin:
            if text == "/admin":
                self.stage = self.admin
                send_message("Hello there, Administrator! " + u'\ud83e\udd16' +"\n\n/view - Displays all feedback\n/delete - Deletes selected feedback\n/clearall - Erases all feedback\n\n/addevent - To add an event\n/surveyresults - To see survey results for an event\n/viewrating - To see ratings for an event\n/clearevent - To delete an event and its ratings\n\n/blast - Ultimate spam function\n/blastresults - Displays blast results\n/viewusers - Displays blast name list\n/removeuser - Removes user from blast list\n\n/mainmenu - Exit Admin mode", chat, remove_keyboard())
        if text == "/start" or text == "back":
            options =[("OrderFood"+u'\ud83c\udf5f'), ("Rate Events"+u'\u2764\ufe0f'), ("Feedback"+u'\ud83d\uddd2'), ("About the Bot"+u'\ud83e\udd89')]
            keyboard = build_keyboard(options)
            send_message("Hello there, " + name + "! Nocbot at your service! " + u'\ud83e\udd89', chat, keyboard)
        elif text == "Feedback"+u'\ud83d\uddd2':
            options =[("BOT Functions"), ("General Feedback"), ("back")]
            keyboard = build_keyboard(options)
            send_message("Is there anything particular you would like to feedback about?", chat, keyboard)
            self.stage = self.Feedback1
        elif text == "Order Food"+u'\ud83c\udf5f':
            options =[("startOrder"), ("viewOrder"), ("closeOrder"), ("addOrder"), ("editOrder"), ("deleteOrder"), ("hungerCry"), ("back")]
            keyboard = build_keyboard(options)
            send_message("A hungry man is an angry man.\nWhat can I do for you?", chat, keyboard)
            self.stage = self.orderFood
        elif text == "Rate Events"+u'\u2764\ufe0f':
            events = [x[0] for x in rate.get_all_events()]
            options = list(set(events))
            options.append("back")
            keyboard = build_keyboard(options)
            send_message("Which event would you like to rate?", chat, keyboard)
            self.stage = self.rate1
        elif text == "About the Bot"+u'\ud83e\udd89':
            options =[("back")]
            keyboard = build_keyboard(options)
            send_message("It's just a BOT :)", chat, keyboard)
        elif text == "/survey":
            events = [x[0] for x in survey.get_all_events()]
            options = list(set(events))
            options.append("back")
            keyboard = build_keyboard(options)
            send_message("Which event would you like to give feedback on?", chat, keyboard)
            self.stage = self.survey1
        else:
            return
    def stage(self,text,chat,name):
        self.MainMenu(text,chat,name)

    def inline(self,update):
        self.rate2(update)

    def Feedback1(self,text,chat,name):
        if text == "BOT Functions":
            send_message("This option is for submitting feedback about bot functions. Please submit bug reports, feature requests, and suggestions for future improvements here! We thank you for your contributions " + u'\ud83d\ude47\ud83c\udffb'\
            + "\n\nWhen you are done, hit send to submit your feedback. If you decide not to submit feedback, please enter /mainmenu to cancel.", chat, remove_keyboard())
            self.stage = self.FeedbackBI
        elif text == "General Feedback":
            send_message("This option is for submitting feedback about any general issues. Please submit any house-related queries and suggestions you may have here! We want to hear your voice " + u'\ud83d\udce3'\
            + "\n\nWhen you are done, hit send to submit your feedback. If you decide not to submit feedback, please enter /mainmenu to cancel.", chat, remove_keyboard())
            self.stage = self.FeedbackGF
        elif text == "back":
            options =[("OrderFood"+u'\ud83c\udf5f'), ("Rate Events"+u'\u2764\ufe0f'), ("Feedback"+u'\ud83d\uddd2'), ("About the Bot"+u'\ud83e\udd89')]
            keyboard = build_keyboard(options)
            send_message("Hello there, " + name + "! Nocbot at your service! " + u'\ud83e\udd89', chat, keyboard)
            self.stage = self.MainMenu

    def FeedbackBI(self,text,chat,name):
        db.add_item(text, "BOT Functions", chat, name)
        send_message("Your feedback has been received! Thank you for your submission " + u'\ud83d\ude0a' + "\n\nAny other feedback to add? Continue typing and hit send to submit more feedback " + u'\ud83d\uddd2' + "\n\nWhen you are done, please enter /mainmenu to finish.", chat)

    def FeedbackGF(self,text,chat,name):
        db.add_item(text, "General Feedback", chat, name)
        send_message("Your feedback has been received! Thank you for your submission " + u'\ud83d\ude0a' + "\n\nAny other feedback to add? Continue typing and hit send to submit more feedback " + u'\ud83d\uddd2' + "\n\nWhen you are done, please enter /mainmenu to finish.", chat)

    def orderFood(self,text,chat,name):
        global NoctuachatID
        global hungerCriers
        global hungermessages
        global orderstarter
        if text == "startOrder":
            if orderstarter == 0:
                send_message("Please key in the details of your order in the following format.\nSHOP <space> TIME TO CLOSE ORDER BY\nE.g.\nAmeens 11:30pm\n\n or type 'back' to return to the previous menu", chat, remove_keyboard())
                self.stage = self.startOrder
            else:
                send_message("The previous order has yet to be closed", chat, remove_keyboard())
                options =[("startOrder"), ("viewOrder"), ("closeOrder"), ("addOrder"), ("editOrder"), ("deleteOrder"), ("hungerCry"), ("back")]
                keyboard = build_keyboard(options)
                send_message("A hungry man is an angry man.\nWhat can I do for you?", chat, keyboard)
        elif text == "viewOrder":
            if chat == orderstarter:
                orders = [x[1] + " " + x[3] for x in food.get_orders()]
                orders = [str(i+1) + ". " + x for i, x in enumerate(orders)]
                message = "\n".join(orders)
                send_message(message, chat, remove_keyboard())
            else:
                send_message("Only the person who started the order can view the order", chat, remove_keyboard())
            options =[("startOrder"), ("viewOrder"), ("closeOrder"), ("addOrder"), ("editOrder"), ("deleteOrder"), ("hungerCry"), ("back")]
            keyboard = build_keyboard(options)
            send_message("A hungry man is an angry man.\nWhat can I do for you?", chat, keyboard)
        elif text == "closeOrder":
            if chat == orderstarter:
                orders = [x[1] + " " + x[3] for x in food.get_orders()]
                orders = [str(i+1) + ". " + x for i, x in enumerate(orders)]
                message = "\n".join(orders)
                options =[("close"), ("back")]
                keyboard = build_keyboard(options)
                send_message(message, chat, keyboard)
                self.stage = self.closeOrder
            else:
                send_message("Only the person who started the order can close the order", chat, remove_keyboard())
                options =[("startOrder"), ("viewOrder"), ("closeOrder"), ("addOrder"), ("editOrder"), ("deleteOrder"), ("hungerCry"), ("back")]
                keyboard = build_keyboard(options)
                send_message("A hungry man is an angry man.\nWhat can I do for you?", chat, keyboard)
        elif text == "addOrder" or text == "editOrder":
            if orderstarter == 0:
                send_message("An order needs to be started", chat, remove_keyboard())
                options =[("startOrder"), ("viewOrder"), ("closeOrder"), ("addOrder"), ("editOrder"), ("deleteOrder"), ("hungerCry"), ("back")]
                keyboard = build_keyboard(options)
                send_message("A hungry man is an angry man.\nWhat can I do for you?", chat, keyboard)
            else:
                send_message("What would you like to order?\n\n or type 'back' to return to the previous menu", chat, remove_keyboard())
                self.stage = self.addOrder
        elif text == "deleteOrder":
            food.delete_order(chat)
            send_message("Order deleted", chat, remove_keyboard())
            options =[("startOrder"), ("viewOrder"), ("closeOrder"), ("addOrder"), ("editOrder"), ("deleteOrder"), ("hungerCry"), ("back")]
            keyboard = build_keyboard(options)
            send_message("A hungry man is an angry man.\nWhat can I do for you?", chat, keyboard)
        elif text == "hungerCry":
            if chat not in hungerCriers:
                hungerCriers.append(chat)
                count = len(hungerCriers)
                if count > 7:
                    count = 7
                send_message("Your cry has been heard...", chat, remove_keyboard())
                send_message(hungermessages[count-1] + "\n\nhungerCount is " + str(len(hungerCriers)), NoctuachatID, remove_keyboard())
            else:
                send_message("You can only cry once :(", chat, remove_keyboard())
            options =[("startOrder"), ("viewOrder"), ("closeOrder"), ("addOrder"), ("editOrder"), ("deleteOrder"), ("hungerCry"), ("back")]
            keyboard = build_keyboard(options)
            send_message("A hungry man is an angry man.\nWhat can I do for you?", chat, keyboard)
        elif text == "back":
            options =[("OrderFood"+u'\ud83c\udf5f'), ("Rate Events"+u'\u2764\ufe0f'), ("Feedback"+u'\ud83d\uddd2'), ("About the Bot"+u'\ud83e\udd89')]
            keyboard = build_keyboard(options)
            send_message("Hello there, " + name + "! Nocbot at your service! " + u'\ud83e\udd89', chat, keyboard)
            self.stage = self.MainMenu

    def startOrder(self,text,chat,name):
        global NoctuachatID
        global orderstarter
        if text == "back":
            options =[("startOrder"), ("viewOrder"), ("closeOrder"), ("addOrder"), ("editOrder"), ("deleteOrder"), ("hungerCry"), ("back")]
            keyboard = build_keyboard(options)
            send_message("A hungry man is an angry man.\nWhat can I do for you?", chat, keyboard)
            self.stage = self.orderFood
        else:
            try:
                details = text.split()
                send_message(name + " has started an order!\nFood from: " + details[0] + "\nOrder closing at: " + details[1], NoctuachatID, remove_keyboard())
                orderstarter = chat
                for x in hungerCriers:
                    send_message(name + " has started an order!\nFood from: " + details[0] + "\nOrder closing at: " + details[1] + "\n\nNavigate to orderFood > addOrder to add your order!", x)
                send_message("What would you like to order?\n\n or type 'back' if you are not ordering", chat, remove_keyboard())
                self.stage = self.addOrder
            except:
                send_message("Invalid format", chat, remove_keyboard())
                options =[("startOrder"), ("viewOrder"), ("closeOrder"), ("addOrder"), ("editOrder"), ("deleteOrder"), ("hungerCry"), ("back")]
                keyboard = build_keyboard(options)
                send_message("A hungry man is an angry man.\nWhat can I do for you?", chat, keyboard)
                self.stage = self.orderFood

    def addOrder(self,text,chat,name):
        global orderstarter
        if text != "back":
            food.add_order(text,chat,name)
            send_message("Order added/edited", chat, remove_keyboard())
            send_message("1 order added/edited", orderstarter, remove_keyboard())
        options =[("startOrder"), ("viewOrder"), ("closeOrder"), ("addOrder"), ("editOrder"), ("deleteOrder"), ("hungerCry"), ("back")]
        keyboard = build_keyboard(options)
        send_message("A hungry man is an angry man.\nWhat can I do for you?", chat, keyboard)
        self.stage = self.orderFood

    def closeOrder(self,text,chat,name):
        global NoctuachatID
        global orderstarter
        global hungerCriers
        if text == "close":
            orderstarter = 0
            food.clear()
            hungerCriers = []
            send_message("Order is closed", chat, remove_keyboard())
            send_message("Order is closed", NoctuachatID, remove_keyboard())
        options =[("startOrder"), ("viewOrder"), ("closeOrder"), ("addOrder"), ("editOrder"), ("deleteOrder"), ("hungerCry"), ("back")]
        keyboard = build_keyboard(options)
        send_message("A hungry man is an angry man.\nWhat can I do for you?", chat, keyboard)
        self.stage = self.orderFood

    def rate1(self,text,chat,name):
        events = [x[0] for x in rate.get_all_events()]
        if text == "back":
            options =[("OrderFood"+u'\ud83c\udf5f'), ("Rate Events"+u'\u2764\ufe0f'), ("Feedback"+u'\ud83d\uddd2'), ("About the Bot"+u'\ud83e\udd89')]
            keyboard = build_keyboard(options)
            send_message("Hello there, " + name + "! Nocbot at your service! " + u'\ud83e\udd89', chat, keyboard)
            self.stage = self.MainMenu
        elif text in events:
            self.event = text
            ratings = [x[2] for x in rate.get_by_event(text)]
            ratings = list(set(ratings))
            options = []
            for x in ratings:
                if x != "-":
                    options.append([{"text":x, "callback_data":x}])
            options.append([{"text": "Input your own option", "callback_data": "Input your own option"}])
            options.append([{"text": "back", "callback_data": "back"}])
            keyboard = inline_keyboard(options)
            send_message("What did you like about the event?", chat, keyboard)
            self.inline = self.rate2
            self.stage = self.MainMenu

    def rate2(self,update):
        call_id = update["callback_query"]["id"]
        chat = update["callback_query"]["message"]["chat"]["id"]
        data = update["callback_query"]["data"]
        message_id = update["callback_query"]["message"]["message_id"]
        name = update["callback_query"]["message"]["from"]["first_name"]
        empty_answer(call_id)
        if data == "back":
            events = [x[0] for x in rate.get_all_events()]
            options = list(set(events))
            options.append("back")
            keyboard = build_keyboard(options)
            edit_message(chat, message_id, "What did you like about the event?")
            send_message("Which event would you like to rate?", chat, keyboard)
            self.stage = self.rate1
        elif data == "Input your own option":
            edit_message(chat, message_id, "Please give your input below")
            self.stage = self.rate3
        else:
            event = self.event
            rate.add_item(event,data,chat,name)
            edit_message(chat, message_id, "Thank you for your review! We'll take your views into consideration, and hope to provide an even greater experience for you in our next upcoming event!")
            options =[("OrderFood"+u'\ud83c\udf5f'), ("Rate Events"+u'\u2764\ufe0f'), ("Feedback"+u'\ud83d\uddd2'), ("About the Bot"+u'\ud83e\udd89')]
            keyboard = build_keyboard(options)
            send_message("Hello there, " + name + "! Nocbot at your service! " + u'\ud83e\udd89', chat, keyboard)
            self.stage = self.MainMenu

    def rate3(self,text,chat,name):
        event = self.event
        rate.add_item(event,text,chat,name)
        send_message("Thank you for your review! We'll take your views into consideration, and hope to provide an even greater experience for you in our next upcoming event!", chat, remove_keyboard())
        options =[("OrderFood"+u'\ud83c\udf5f'), ("Rate Events"+u'\u2764\ufe0f'), ("Feedback"+u'\ud83d\uddd2'), ("About the Bot"+u'\ud83e\udd89')]
        keyboard = build_keyboard(options)
        send_message("Hello there, " + name + "! Nocbot at your service! " + u'\ud83e\udd89', chat, keyboard)
        self.stage = self.MainMenu

    def survey1(self,text,chat,name):
        events = [x[0] for x in survey.get_all_events()]
        if text == "back":
            options =[("OrderFood"+u'\ud83c\udf5f'), ("Rate Events"+u'\u2764\ufe0f'), ("Feedback"+u'\ud83d\uddd2'), ("About the Bot"+u'\ud83e\udd89')]
            keyboard = build_keyboard(options)
            send_message("Hello there, " + name + "! Nocbot at your service! " + u'\ud83e\udd89', chat, keyboard)
            self.stage = self.MainMenu
        elif text in events:
            self.survey[0] = text
            send_message("What did you like about the event?", chat, remove_keyboard())
            self.stage = self.survey2

    def survey2(self,text,chat,name):
        self.survey[1] = text
        send_message("What could be improved with regards to the event?", chat, remove_keyboard())
        self.stage = self.survey3

    def survey3(self,text,chat,name):
        self.survey[2] = text
        x = u'\u2b50\ufe0f'
        options = [x*5, x*4, x*3, x*2, x]
        keyboard = build_keyboard(options)
        send_message("Please rate your overall experience with this event!", chat, keyboard)
        self.stage = self.survey4

    def survey4(self,text,chat,name):
        self.survey[3] = text
        answer = self.survey
        survey.add_item(answer,chat,name)
        send_message("Thank you for your review! We'll take your views into consideration, and hope to provide an even greater experience for you in our next upcoming event!", chat, remove_keyboard())
        options =[("OrderFood"+u'\ud83c\udf5f'), ("Rate Events"+u'\u2764\ufe0f'), ("Feedback"+u'\ud83d\uddd2'), ("About the Bot"+u'\ud83e\udd89')]
        keyboard = build_keyboard(options)
        send_message("Hello there, " + name + "! Nocbot at your service! " + u'\ud83e\udd89', chat, keyboard)
        self.stage = self.MainMenu

    def admin(self,text,chat,name):
        if text == "/view":
            items = db.get_BOT()
            items = ["("+x[2]+")"+" "+x[4]+": "+x[1] for x in items]
            items2 = db.get_General()
            items += ["("+x[2]+")"+" "+x[4]+": "+x[1] for x in items2]
            items = [str(i+1) + ". " + x for i, x in enumerate(items)]
            message = "There are no feedbacks submitted at the moment."
            if len(items) > 0:
                message = "\n".join(items)
            send_message(message, chat, remove_keyboard())
        elif text == "/delete":
            items = db.get_BOT()
            items = ["("+x[2]+")"+" "+x[4]+": "+x[1] for x in items]
            items2 = db.get_General()
            items += ["("+x[2]+")"+" "+x[4]+": "+x[1] for x in items2]
            items = [str(i+1) + ". " + x for i, x in enumerate(items)]
            if len(items) == 0:
                message = "There are no feedbacks submitted at the moment."
                send_message(message, chat, remove_keyboard())
            else:
                message = "\n".join(items)
                send_message(message, chat, remove_keyboard())
                send_message("Which feedback do you wish to delete? Please input the respective numbers.\n\n Type back to exit", chat, remove_keyboard())
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
            keyboard = build_keyboard(items)
            send_message("Which user do you want to remove?", chat, keyboard)
            self.stage = self.removeuser
        elif text == "/blast":
            options =[("text"),("photo"),("back")]
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
            send_message("Add an event to be rated\n\nor type back to exit", chat, remove_keyboard())
            self.stage = self.addevent
        elif text == "/surveyresults":
            events = [x[0] for x in survey.get_all_events()]
            options = list(set(events))
            options.append("back")
            keyboard = build_keyboard(options)
            send_message("Which event would you like to view results for?", chat, keyboard)
            self.stage = self.surveyresults
        elif text == "/clearevent":
            events = [x[0] for x in survey.get_all_events()]
            options = list(set(events))
            options.append("back")
            keyboard = build_keyboard(options)
            send_message("Which event would you like to remove?", chat, keyboard)
            self.stage = self.clearevent
        elif text == "/viewrating":
            events = [x[0] for x in rate.get_all_events()]
            options = list(set(events))
            options.append("back")
            keyboard = build_keyboard(options)
            send_message("Which event would you like to view results for?", chat, keyboard)
            self.stage = self.viewrating
        else:
            return

    def addevent(self,text,chat,name):
        if text != "back":
            survey.add_item([text,"-","-","-"],chat,name)
            rate.add_item(text,"-",chat,name)
            send_message("Event added!", chat, remove_keyboard())
        send_message("Hello there, Administrator! " + u'\ud83e\udd16' +"\n\n/view - Displays all feedback\n/delete - Deletes selected feedback\n/clearall - Erases all feedback\n\n/addevent - To add an event\n/surveyresults - To see survey results for an event\n/viewrating - To see ratings for an event\n/clearevent - To delete an event and its ratings\n\n/blast - Ultimate spam function\n/blastresults - Displays blast results\n/viewusers - Displays blast name list\n/removeuser - Removes user from blast list\n\n/mainmenu - Exit Admin mode", chat, remove_keyboard())
        self.stage = self.admin

    def surveyresults(self,text,chat,name):
        events = [x[0] for x in survey.get_all_events()]
        if text == "back":
            send_message("Hello there, Administrator! " + u'\ud83e\udd16' +"\n\n/view - Displays all feedback\n/delete - Deletes selected feedback\n/clearall - Erases all feedback\n\n/addevent - To add an event\n/surveyresults - To see survey results for an event\n/viewrating - To see ratings for an event\n/clearevent - To delete an event and its ratings\n\n/blast - Ultimate spam function\n/blastresults - Displays blast results\n/viewusers - Displays blast name list\n/removeuser - Removes user from blast list\n\n/mainmenu - Exit Admin mode", chat, remove_keyboard())
        elif text in events:
            ratings = [x[6]+"\n"+x[2]+"\n"+x[3]+"\n"+x[4]+ " " for x in survey.get_by_event(text)]
            ratings = [str(i+1) + ". " + x for i, x in enumerate(ratings)]
            message = "\n\n".join(ratings)
            send_message(message, chat, remove_keyboard())
        self.stage = self.admin

    def clearevent(self,text,chat,name):
        events = [x[0] for x in survey.get_all_events()]
        if text == "back":
            send_message("Hello there, Administrator! " + u'\ud83e\udd16' +"\n\n/view - Displays all feedback\n/delete - Deletes selected feedback\n/clearall - Erases all feedback\n\n/addevent - To add an event\n/surveyresults - To see survey results for an event\n/viewrating - To see ratings for an event\n/clearevent - To delete an event and its ratings\n\n/blast - Ultimate spam function\n/blastresults - Displays blast results\n/viewusers - Displays blast name list\n/removeuser - Removes user from blast list\n\n/mainmenu - Exit Admin mode", chat, remove_keyboard())
        elif text in events:
            survey.delete_event(text)
            rate.delete_event(text)
            send_message("Event deleted", chat, remove_keyboard())
        self.stage = self.admin

    def viewrating(self,text,chat,name):
        events = [x[0] for x in rate.get_all_events()]
        if text == "back":
            send_message("Hello there, Administrator! " + u'\ud83e\udd16' +"\n\n/view - Displays all feedback\n/delete - Deletes selected feedback\n/clearall - Erases all feedback\n\n/addevent - To add an event\n/surveyresults - To see survey results for an event\n/viewrating - To see ratings for an event\n/clearevent - To delete an event and its ratings\n\n/blast - Ultimate spam function\n/blastresults - Displays blast results\n/viewusers - Displays blast name list\n/removeuser - Removes user from blast list\n\n/mainmenu - Exit Admin mode", chat, remove_keyboard())
        elif text in events:
            stats = rate.get_stats(text)
            print stats
            message = ""
            for key in stats:
                message += key + ": " + str(stats[key]) + "\n"
                results = [x[4] for x in rate.get_results(text,key)]
                results = [str(i+1) + ". " + x for i, x in enumerate(results)]
                message += "\n".join(results) + "\n\n"
            send_message(message, chat, remove_keyboard())
        self.stage = self.admin

    def delete(self,text,chat,name):
        if text != "back":
            items = [x[1] for x in db.get_BOT()]
            items2 = [x[1] for x in db.get_General()]
            count = 0
            for x in text.split():
                try:
                    if int(x) > len(items):
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
            self.stage = self.admin
        else:
            send_message("Hello there, Administrator! " + u'\ud83e\udd16' +"\n\n/view - Displays all feedback\n/delete - Deletes selected feedback\n/clearall - Erases all feedback\n\n/addevent - To add an event\n/surveyresults - To see survey results for an event\n/viewrating - To see ratings for an event\n/clearevent - To delete an event and its ratings\n\n/blast - Ultimate spam function\n/blastresults - Displays blast results\n/viewusers - Displays blast name list\n/removeuser - Removes user from blast list\n\n/mainmenu - Exit Admin mode", chat, remove_keyboard())
            self.stage = self.admin

    def removeuser(self,text,chat,name):
        if text == "back":
            self.stage = self.admin
            send_message("Hello there, Administrator! " + u'\ud83e\udd16' +"\n\n/view - Displays all feedback\n/delete - Deletes selected feedback\n/clearall - Erases all feedback\n\n/addevent - To add an event\n/surveyresults - To see survey results for an event\n/viewrating - To see ratings for an event\n/clearevent - To delete an event and its ratings\n\n/blast - Ultimate spam function\n/blastresults - Displays blast results\n/viewusers - Displays blast name list\n/removeuser - Removes user from blast list\n\n/mainmenu - Exit Admin mode", chat, remove_keyboard())
        else:
            USERS.delete_user(text)
            send_message("User removed", chat, remove_keyboard())
            self.stage = self.admin
            send_message("Hello there, Administrator! " + u'\ud83e\udd16' +"\n\n/view - Displays all feedback\n/delete - Deletes selected feedback\n/clearall - Erases all feedback\n\n/addevent - To add an event\n/surveyresults - To see survey results for an event\n/viewrating - To see ratings for an event\n/clearevent - To delete an event and its ratings\n\n/blast - Ultimate spam function\n/blastresults - Displays blast results\n/viewusers - Displays blast name list\n/removeuser - Removes user from blast list\n\n/mainmenu - Exit Admin mode", chat, remove_keyboard())

    def blast0(self,text,chat,name):
        if text == "text":
            send_message("Type your message:", chat)
            self.stage = self.blast1
        elif text == "photo":
            send_message("Send your photo here", chat)
            self.stage = self.blastA
        elif text == "back":
            send_message("Hello there, Administrator! " + u'\ud83e\udd16' +"\n\n/view - Displays all feedback\n/delete - Deletes selected feedback\n/clearall - Erases all feedback\n\n/addevent - To add an event\n/surveyresults - To see survey results for an event\n/viewrating - To see ratings for an event\n/clearevent - To delete an event and its ratings\n\n/blast - Ultimate spam function\n/blastresults - Displays blast results\n/viewusers - Displays blast name list\n/removeuser - Removes user from blast list\n\n/mainmenu - Exit Admin mode", chat, remove_keyboard())
            self.stage = self.admin

    def blastA(self,photo,chat,name):
        global photo_id
        photo_id = photo
        print photo_id
        options =[("Yes"), ("No")]
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


    def blast1(self,text,chat,name):
        global blast_message
        blast_message = text
        options =[("Next Step"), ("Retype"), ("back")]
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
            send_message("Hello there, Administrator! " + u'\ud83e\udd16' +"\n\n/view - Displays all feedback\n/delete - Deletes selected feedback\n/clearall - Erases all feedback\n\n/addevent - To add an event\n/surveyresults - To see survey results for an event\n/viewrating - To see ratings for an event\n/clearevent - To delete an event and its ratings\n\n/blast - Ultimate spam function\n/blastresults - Displays blast results\n/viewusers - Displays blast name list\n/removeuser - Removes user from blast list\n\n/mainmenu - Exit Admin mode", chat, remove_keyboard())

    def blast3(self,text,chat,name):
        global blast_message
        global blast_options
        if text == "/no":
            allusers = USERS.get_id_and_name()
            for x in allusers:
                send_message(blast_message, x[1])
            self.stage = self.admin
        else:
            blast_options = ["!" + x for x in text.split("$")]
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
                                        options =[("OrderFood"+u'\ud83c\udf5f'), ("Rate Events"+u'\u2764\ufe0f'), ("Feedback"+u'\ud83d\uddd2'), ("About the Bot"+u'\ud83e\udd89')]
                                        keyboard = build_keyboard(options)
                                        send_message("Hello there, " + name + "! Nocbot at your service! " + u'\ud83e\udd89', chat, keyboard)
                                    else:
                                        user.stage(text,chat,name)
                                    break
                                else:
                                    continue
                            if chat not in [user.id for user in users]:
                                    x = User(chat)
                                    users.append(x)
                                    USERS.add_user(chat,name)
                                    print("new temporary user")
                                    if text.startswith("!"):
                                        x.blast_poll(text,chat,name)
                                    elif text == "/mainmenu":
                                        x.stage = x.MainMenu
                                        x.stage(text,chat,name)
                                        options =[("OrderFood"+u'\ud83c\udf5f'), ("Rate Events"+u'\u2764\ufe0f'), ("Feedback"+u'\ud83d\uddd2'), ("About the Bot"+u'\ud83e\udd89')]
                                        keyboard = build_keyboard(options)
                                        send_message("Hello there, " + name + "! Nocbot at your service! " + u'\ud83e\udd89', chat, keyboard)
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
                                send_message("Sorry, but I'm unable to process pictures, stickers or GIFs . . . Text-only please!", chat)
                    elif "audio" in update["message"] or "video" in update["message"] or "sticker" in update["message"] or "document" in update["message"]:
                        chat = update["message"]["chat"]["id"]
                        send_message("Sorry, but I'm unable to process pictures, stickers or GIFs . . . Text-only please!", chat)
                elif "callback_query" in update:
                    chat = update["callback_query"]["message"]["chat"]["id"]
                    for user in users:
                        if chat == user.id:
                            user.inline(update)
                            break
                    if chat not in [user.id for user in users]:
                            x = User(chat)
                            users.append(x)
                            print("new temporary user")
                            x.inline(update)
            last_update_id = get_last_update_id(updates) + 1
        time.sleep(0.5)

if __name__ == '__main__':
    print("Initialised...")
    db.setup()
    USERS.setup()
    poll.setup()
    food.setup()
    rate.setup()
    survey.setup()
    main()

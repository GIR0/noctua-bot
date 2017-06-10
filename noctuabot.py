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

def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True, "selective": True}
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
    def MainMenu(self,text,chat,name):
        if chat in admin:
            if text == "/admin":
                self.stage = self.admin
                send_message("Hi admin\n\n/view - To see all feedbacks\n/delete - To delete feedbacks\n/viewusers\n/removeuser\n/blast\n/blastresults\n/mainmenu - To get back to main menu", chat, remove_keyboard())
        if text == "/start" or text == "back":
            options =[("Feedback"), ("Order Food"), ("Rate Events"), ("About the Bot")]
            keyboard = build_keyboard(options)
            send_message("Hello there "+ name + "! Welcome to the BOT of Noctua!\nWhat can I help you with?", chat, keyboard)
        elif text == "Feedback":
            options =[("Suggestions for BOT"), ("General Feedback"), ("back")]
            keyboard = build_keyboard(options)
            send_message("Is there anything particular you would like to feedback about?", chat, keyboard)
            self.stage = self.Feedback1
        elif text == "Order Food":
            options =[("startOrder"), ("viewOrder"), ("closeOrder"), ("addOrder"), ("editOrder"), ("deleteOrder"), ("hungerCry"), ("back")]
            keyboard = build_keyboard(options)
            send_message("A hungry man is an angry man.\nWhat can I do for you?", chat, keyboard)
            self.stage = self.orderFood
        elif text == "Rate Events":
            options =[("back")]
            keyboard = build_keyboard(options)
            send_message("Coming soon!", chat, keyboard)
        elif text == "About the Bot":
            options =[("back")]
            keyboard = build_keyboard(options)
            send_message("It's just a BOT :)", chat, keyboard)
        else:
            return
    def stage(self,text,chat,name):
        self.MainMenu(text,chat,name)

    def Feedback1(self,text,chat,name):
        if text == "Suggestions for BOT":
            send_message("Found a bug? Are we missing essential features? Have a suggestion for improvement?\nLet us know here!", chat, remove_keyboard())
            self.stage = self.FeedbackBI
        elif text == "General Feedback":
            send_message("Feel free to tell us anything you want us to know!\n\nDo note that all responses will be kept private and confidential.", chat, remove_keyboard())
            self.stage = self.FeedbackGF
        elif text == "back":
            options =[("Feedback"), ("Order Food"), ("Rate Events"), ("About the Bot")]
            keyboard = build_keyboard(options)
            send_message("Hello there "+ name + "! Welcome to the BOT of Noctua!\nWhat can I help you with?", chat, keyboard)
            self.stage = self.MainMenu

    def FeedbackBI(self,text,chat,name):
        db.add_item(text, "Suggestions for BOT", chat, name)
        send_message("Feedback received! Would you like to submit another?\n\nWhen you're done, simply type /mainmenu to return to the main menu.", chat)

    def FeedbackGF(self,text,chat,name):
        db.add_item(text, "General Feedback", chat, name)
        send_message("Feedback received! Would you like to submit another?\n\nWhen you're done, simply type /mainmenu to return to the main menu.", chat)

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
            options =[("Feedback"), ("Order Food"), ("Rate Events"), ("About the Bot")]
            keyboard = build_keyboard(options)
            send_message("Hello there "+ name + "! Welcome to the BOT of Noctua!\nWhat can I help you with?", chat, keyboard)
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


    def admin(self,text,chat,name):
        if text == "/view":
            items = db.get_Suggestions()
            items = ["("+x[2]+")"+" "+x[4]+": "+x[1] for x in items]
            items2 = db.get_General()
            items += ["("+x[2]+")"+" "+x[4]+": "+x[1] for x in items2]
            items = [str(i+1) + ". " + x for i, x in enumerate(items)]
            message = "\n".join(items)
            send_message(message, chat, remove_keyboard())
        elif text == "/delete":
            items = db.get_Suggestions()
            items = ["("+x[2]+")"+" "+x[4]+": "+x[1] for x in items]
            items2 = db.get_General()
            items += ["("+x[2]+")"+" "+x[4]+": "+x[1] for x in items2]
            items = [str(i+1) + ". " + x for i, x in enumerate(items)]
            message = "\n".join(items)
            send_message(message, chat, remove_keyboard())
            send_message("Which feedback do you wish to delete? Please input the respective numbers.\n\n Type back to exit", chat, remove_keyboard())
            self.stage = self.delete
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
                message += "\n".join(results) +"\n\n"
            for key in stats:
                if key != "Yet to reply":
                    message += key + ": " + str(stats[key]) + "\n"
                    results = [x[3] for x in poll.get_results(key)]
                    results = [str(i+1) + ". " + x for i, x in enumerate(results)]
                    message += "\n".join(results)
            send_message(message, chat, remove_keyboard())
        else:
            return

    def delete(self,text,chat,name):
        if text != "back":
            try:
                items = [x[1] for x in db.get_Suggestions()]
                items2 = [x[1] for x in db.get_General()]
                if int(text) > len(items):
                    index = int(text) - len(items) - 1
                    feedback = items2[index]
                else:
                    index = int(text) - 1
                    feedback = items[index]
                print feedback
                db.delete_item(feedback)
                self.stage = self.admin
                send_message("Feedback deleted",chat, remove_keyboard())
            except:
                send_message("Error deleting", chat)
        send_message("Hi admin\n\n/view - To see all feedbacks\n/delete - To delete feedbacks\n/viewusers\n/removeuser\n/blast\n/blastresults\n/mainmenu - To get back to main menu", chat, remove_keyboard())
        self.stage = self.admin

    def removeuser(self,text,chat,name):
        if text == "back":
            self.stage = self.admin
            send_message("Hi admin\n\n/view - To see all feedbacks\n/delete - To delete feedbacks\n/viewusers\n/removeuser\n/blast\n/blastresults\n/mainmenu - To get back to main menu", chat, remove_keyboard())
        else:
            USERS.delete_user(text)
            send_message("User removed", chat, remove_keyboard())
            self.stage = self.admin
            send_message("Hi admin\n\n/view - To see all feedbacks\n/delete - To delete feedbacks\n/viewusers\n/removeuser\n/blast\n/blastresults\n/mainmenu - To get back to main menu", chat, remove_keyboard())

    def blast0(self,text,chat,name):
        if text == "text":
            send_message("Type your message:", chat)
            self.stage = self.blast1
        elif text == "photo":
            send_message("Send your photo here", chat)
            self.stage = self.blastA
        elif text == "back":
            send_message("Hi admin\n\n/view - To see all feedbacks\n/delete - To delete feedbacks\n/viewusers\n/removeuser\n/blast\n/blastresults\n/mainmenu - To get back to main menu", chat, remove_keyboard())
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
            send_message("Hi admin\n\n/view - To see all feedbacks\n/delete - To delete feedbacks\n/viewusers\n/removeuser\n/blast\n/blastresults\n/mainmenu - To get back to main menu", chat, remove_keyboard())

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
                                    options =[("Feedback"), ("Order Food"), ("Rate Events"), ("About the Bot")]
                                    keyboard = build_keyboard(options)
                                    send_message("Hello there "+ name + "! Welcome to the BOT of Noctua!\nWhat can I help you with?", chat, keyboard)
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
                                    options =[("Feedback"), ("Order Food"), ("Rate Events"), ("About the Bot")]
                                    keyboard = build_keyboard(options)
                                    send_message("Hello there "+ name + "! Welcome to the BOT of Noctua!\nWhat can I help you with?", chat, keyboard)
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
            last_update_id = get_last_update_id(updates) + 1
        time.sleep(0.5)

if __name__ == '__main__':
    print("Initialised...")
    db.setup()
    USERS.setup()
    poll.setup()
    food.setup()
    main()

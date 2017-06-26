
    def payments(self,update):
        call_id = update["callback_query"]["id"]
        chat = update["callback_query"]["message"]["chat"]["id"]
        data = update["callback_query"]["data"]
        message_id = update["callback_query"]["message"]["message_id"]
        name = update["callback_query"]["message"]["chat"]["first_name"]
        empty_answer(call_id)
        owners = list(set([x[4] for x in food.get_by_orderstarter(chat)]))
        if data == "start":
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
            options =[[{"text": "7", "callback_data": "7"},{"text": "8", "callback_data": "8"},{"text": "9", "callback_data": "9"}]\
            ,[{"text": "4", "callback_data": "4"},{"text": "5", "callback_data": "5"},{"text": "6", "callback_data": "6"}]\
            ,[{"text": "1", "callback_data": "1"},{"text": "2", "callback_data": "2"},{"text": "3", "callback_data": "3"}]\
            ,[{"text": ".", "callback_data": "."},{"text": "0", "callback_data": "0"},{"text": u"\u25C0", "callback_data": u"\u25C0"}]\
            ,[{"text": u"\u2B05", "callback_data": u"\u2B05"},{"text": u"\U0001F4BE"+u"\u27A1", "callback_data": u"\U0001F4BE"+u"\u27A1"},{"text": u"\u274C", "callback_data": u"\u274C"}]]
            self.idx = 0
            self.display = ""
            keyboard = inline_keyboard(options)
            edit_message(chat, message_id, "Please enter amount owed by:\n\n" + self.orderlist[self.idx][3]+self.display, keyboard)
        elif data == u"\u274C":
            edit_message(chat, message_id, "payments cancelled")
            send_message(orderfood_message(), chat, orderfood_menu())
            self.stage = self.orderFood
        elif data == u"\U0001F4BE"+u"\u27A1":
            self.orderlist[self.idx][1] = self.display
            if self.idx == len(self.orderlist) - 1:
                self.idx += 1
                options = [[{"text": u"\u2B05", "callback_data": u"\u2B05"},{"text": "done", "callback_data": "done"}]]
                keyboard = inline_keyboard(options)
                edit_message(chat, message_id, "Done?", keyboard)
            else:
                options =[[{"text": "7", "callback_data": "7"},{"text": "8", "callback_data": "8"},{"text": "9", "callback_data": "9"}]\
                ,[{"text": "4", "callback_data": "4"},{"text": "5", "callback_data": "5"},{"text": "6", "callback_data": "6"}]\
                ,[{"text": "1", "callback_data": "1"},{"text": "2", "callback_data": "2"},{"text": "3", "callback_data": "3"}]\
                ,[{"text": ".", "callback_data": "."},{"text": "0", "callback_data": "0"},{"text": u"\u25C0", "callback_data": u"\u25C0"}]\
                ,[{"text": u"\u2B05", "callback_data": u"\u2B05"},{"text": u"\U0001F4BE"+u"\u27A1", "callback_data": u"\U0001F4BE"+u"\u27A1"},{"text": u"\u274C", "callback_data": u"\u274C"}]]
                self.idx += 1
                self.display = ""
                keyboard = inline_keyboard(options)
                edit_message(chat, message_id, "Please enter amount owed by:\n\n" + self.orderlist[self.idx][3]+self.display, keyboard)
        elif data == u"\u25C0":
            self.display = self.display[:-1]
            options =[[{"text": "7", "callback_data": "7"},{"text": "8", "callback_data": "8"},{"text": "9", "callback_data": "9"}]\
            ,[{"text": "4", "callback_data": "4"},{"text": "5", "callback_data": "5"},{"text": "6", "callback_data": "6"}]\
            ,[{"text": "1", "callback_data": "1"},{"text": "2", "callback_data": "2"},{"text": "3", "callback_data": "3"}]\
            ,[{"text": ".", "callback_data": "."},{"text": "0", "callback_data": "0"},{"text": u"\u25C0", "callback_data": u"\u25C0"}]\
            ,[{"text": u"\u2B05", "callback_data": u"\u2B05"},{"text": u"\U0001F4BE"+u"\u27A1", "callback_data": u"\U0001F4BE"+u"\u27A1"},{"text": u"\u274C", "callback_data": u"\u274C"}]]
            keyboard = inline_keyboard(options)
            edit_message(chat, message_id, "Please enter amount owed by:\n\n" + self.orderlist[self.idx][3]+self.display, keyboard)
        elif data == u"\u2B05":
            if self.idx == 0:
                return
            options =[[{"text": "7", "callback_data": "7"},{"text": "8", "callback_data": "8"},{"text": "9", "callback_data": "9"}]\
            ,[{"text": "4", "callback_data": "4"},{"text": "5", "callback_data": "5"},{"text": "6", "callback_data": "6"}]\
            ,[{"text": "1", "callback_data": "1"},{"text": "2", "callback_data": "2"},{"text": "3", "callback_data": "3"}]\
            ,[{"text": ".", "callback_data": "."},{"text": "0", "callback_data": "0"},{"text": u"\u25C0", "callback_data": u"\u25C0"}]\
            ,[{"text": u"\u2B05", "callback_data": u"\u2B05"},{"text": u"\U0001F4BE"+u"\u27A1", "callback_data": u"\U0001F4BE"+u"\u27A1"},{"text": u"\u274C", "callback_data": u"\u274C"}]]
            self.idx -= 1
            self.display = ""
            keyboard = inline_keyboard(options)
            edit_message(chat, message_id, "Please enter amount owed by:\n\n" + self.orderlist[self.idx][3]+self.display, keyboard)
        elif data == "done":
            message = "Here's the final order list, together with the amounts you've entered. I have forwarded this to everyone who ordered!\n\n"
            for x in self.orderlist:
                    message += "$" + x[1] + " - " + x[3]
            edit_message(chat, message_id, message)
            for x in self.orderlist:
                if x[1] != "":
                    send_message("You are required to pay $" + x[1] + " to " + name + " for your latest order:\n" + x[2], x[0])
            self.idx = 0
            self.display = ""
            self.orderlist = []
            send_message(orderfood_message(), chat, orderfood_menu())
            self.inline = self.ignore
            self.stage = self.orderFood
        else:
            self.display += data
            options =[[{"text": "7", "callback_data": "7"},{"text": "8", "callback_data": "8"},{"text": "9", "callback_data": "9"}]\
            ,[{"text": "4", "callback_data": "4"},{"text": "5", "callback_data": "5"},{"text": "6", "callback_data": "6"}]\
            ,[{"text": "1", "callback_data": "1"},{"text": "2", "callback_data": "2"},{"text": "3", "callback_data": "3"}]\
            ,[{"text": ".", "callback_data": "."},{"text": "0", "callback_data": "0"},{"text": u"\u25C0", "callback_data": u"\u25C0"}]\
            ,[{"text": u"\u2B05", "callback_data": u"\u2B05"},{"text": u"\U0001F4BE"+u"\u27A1", "callback_data": u"\U0001F4BE"+u"\u27A1"},{"text": u"\u274C", "callback_data": u"\u274C"}]]
            keyboard = inline_keyboard(options)
            edit_message(chat, message_id, "Please enter amount owed by:\n\n" + self.orderlist[self.idx][3]+self.display, keyboard)

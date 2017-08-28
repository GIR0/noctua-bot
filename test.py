def inline_mode(self,update):
    chat = update["inline_query"]["from"]["id"]
    query_id = update["inline_query"]["id"]
    query = update["inline_query"]["query"]
    if query == "":
        query_results = []
        titles = list(set(sample.get_all_titles()))
        for x in titles:
            stats = sample.get_stats(x)
            message = ""
            options = []
            for key in stats:
                message += key + ": " + str(stats[key]) + "\n"
                options.append([{"text":key, "callback_data":key}])
            keyboard = inline_keyboard(options)
            query_results.append({"type": "article", "id": "abc", "title": x, "input_message_content": {"message_text": x + "\n\n" + message}, "reply_markup": keyboard })
        query_results = json.dumps(query_results)
        answer_inline_query(query_id, query_results)

def sampling(self,update):
    call_id = update["callback_query"]["id"]
    chat = update["callback_query"]["message"]["chat"]["id"]
    data = update["callback_query"]["data"]
    message = update["callback_query"]["message"]["text"]
    inline_message_id = update["callback_query"]["inline_message_id"]
    message_id = update["callback_query"]["message"]["message_id"]
    name = update["callback_query"]["message"]["chat"]["first_name"]
    empty_answer(call_id)
    sample.action(message,data,chat,name)
    edit_sampling(inline_message_id, "Thank you for your review!"+u'\U0001F647'+"\n\nWe'll take your views into consideration, and hope to provide an even greater experience for you in our next upcoming event!")
    options =[[u"Owl-Owlet Anonymous Chat\U0001F4AC"], [u"OrderFood\U0001F35F"], [u"AlmaNoc\U0001F4C6", u"Feedback\U0001F5D2"], [u"Help Desk\U0001F6CE", u"About the Bot\U0001F989"]]
    keyboard = build_keyboard(options)
    send_message("Hello there, " + name + "! Nocbot at your service! " + u'\U0001F989', chat, keyboard)
    self.stage = self.MainMenu
    self.inline = self.ignore

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
            keyboard = inline_keyboard(sorted(options, key=str.lower))
            query_results.append({"type": "article", "id": x[:20], "title": x, "input_message_content": {"message_text": x + "\n\n" + message}, "reply_markup": keyboard })
        query_results = json.dumps(query_results)
        answer_inline_query(query_id, query_results)

def sampling(self,update):
    call_id = update["callback_query"]["id"]
    chat = update["callback_query"]["from"]["id"]
    data = update["callback_query"]["data"]
    message = update["callback_query"]["message"]["text"]
    inline_message_id = update["callback_query"]["inline_message_id"]
    message_id = update["callback_query"]["message"]["message_id"]
    name = update["callback_query"]["from"]["first_name"]
    empty_answer(call_id)
    for x in samplerecord.get_by_id(inline_message_id):
        title = x[0]
        break
    sample.action(title,data,chat,name)
    stats = sample.get_stats(title)
    message = ""
    options = []
    for key in stats:
        message += key + ": " + str(stats[key]) + "\n"
        options.append([{"text":key, "callback_data":key}])
    keyboard = inline_keyboard(sorted(options, key=str.lower))
    edit_message2(inline_message_id, title + "\n\n" + message, keyboard)

    if text == "/countmein":
        send_message("Let's create a new poll. First, send me the title.", chat)]
        self.stage = self.create_title

def create_title(self,text,chat,name):
    self.create[0] = text
    send_message("New poll: " + text + "\n\nPlease send me the first answer option.", chat)
    self.stage = self.create_options

def create_options(self,text,chat,name):
    if text == "/done":
        for x in self.create[1]:
            sample.action(self.create[0], x, 0, "-")
        send_message("Poll created", chat)
    else:
        self.create[1].append(text)
        send_message("Good. Now send me another answer option, or /done to finish.", chat, remove_keyboard())


elif "chosen_inline_result" in update:
    inline_message_id = update["chosen_inline_result"]["inline_message_id"]
    result_id = update["chosen_inline_result"]["result_id"]
    titles = list(set(sample.get_all_titles()))
    for title in titles:
        if title.startswith(result_id):
            check = x
    samplerecord.add_id(x,inline_message_id)

        elif text == "View Order":
            descriptions = [x[0] for x in food.get_all_description()]
            options = list(set(descriptions))
            options.append("back")
            keyboard = build_keyboard(options)
            send_message("Which event would you like to rate?", chat, keyboard)
            if chat == orderstarter:
                orders = [x[1] + " " + x[3] for x in food.get_orders()]
                orders = [str(i+1) + ". " + x for i, x in enumerate(orders)]
                message = "\n".join(orders)
                send_message(message, chat, remove_keyboard())
            else:
                send_message("Only the person who started the order can view the order", chat, remove_keyboard())
            options =[["Hunger Cry"+u'\U0001F4E2', "Start Order"+u'\U0001F4CD'], ["View Order"+u'\U0001F5D2', "Add Order"+u'\U0001F355'], ["Edit Order"+u'\U0001F4DD', "Clear Order"+	u'\U0001F5D1'], ["Close Order"+	u'\U0001F510', "back"]]
            keyboard = build_keyboard(options)
            send_message("A hungry man is an angry man.\nWhat can I do for you?", chat, keyboard)

        elif text == "Add Order":
            allorders = food.get_all()
            if len(allorders) > 0:
                send_message("What would you like to order?\n\n or click /back to return to the previous menu", chat, remove_keyboard())
                self.stage = self.AddOrder
            else:
                send_message("There is currently no order ongoing", chat, remove_keyboard())
                options =[["Hunger Cry"+u'\U0001F4E2', "Start Order"+u'\U0001F4CD'], ["View Order"+u'\U0001F5D2', "Add Order"+u'\U0001F355'], ["Edit Order"+u'\U0001F4DD', "Clear Order"+	u'\U0001F5D1'], ["Close Order"+	u'\U0001F510', "back"]]
                keyboard = build_keyboard(options)
                send_message("A hungry man is an angry man.\nWhat can I do for you?", chat, keyboard)

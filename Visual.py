import dearpygui.dearpygui as dpg
from main import Chat
import urllib.request

def SendMessange():
    value = dpg.get_value("TextToMessage")
    Chat.SendMassage(value)
    AddNewMessage("You: " + value)
    dpg.set_value("TextToMessage", "")

def AddNewMessage(text):
    mes = dpg.add_text(default_value=text, parent="Chat")
    # dpg.set_item_pos(mes, pos=[300, 50])

def AddGetMessage(text):
    dpg.add_text(default_value=text, parent="Chat")
# dpg.get_viewport_width() - dpg.get_item_width(mes) - 20


def ChatVisual():
    dpg.create_context()
    dpg.create_viewport(title='Decetralizet chat', width=1100, height=700)

    with dpg.window(label="Chat",pos=[310,0], height=dpg.get_viewport_height(), no_title_bar=True, width=dpg.get_viewport_width(), tag="Chat", no_close=True, no_collapse=True):
        dpg.add_input_text(multiline=True, hint="Messange",pos=[15, 50], width=dpg.get_item_width("Chat") - 170,tag="TextToMessage", height= 50)
        dpg.add_button(label="Send", height= 50, width=120, tag="SendButton", callback=SendMessange)

    with dpg.window(label="Info", width=310, height=dpg.get_viewport_height(), tag="Info", no_close=True, no_collapse=True):
        dpg.add_text("Hello, world")

    dpg.setup_dearpygui()
    dpg.show_viewport()

    while dpg.is_dearpygui_running():
        response = urllib.request.urlopen("http://127.0.0.1:5000/")
        data = response.read()
        if str(data).replace("b'","").replace("'", "") == "":
            pass
        else:
            AddGetMessage("His: "+str(data).replace("b'","").replace("'", ""))
            urllib.request.urlopen("http://127.0.0.1:5000/Delete")

        dpg.set_item_height("Chat", dpg.get_viewport_height())   
        dpg.set_item_height("Info", dpg.get_viewport_height())
        if dpg.get_active_window() == 21:
            dpg.set_item_width("Info", dpg.get_viewport_width() - dpg.get_item_width("Chat"))

        dpg.set_item_pos("Chat", [dpg.get_item_width("Info"),0])
        dpg.set_item_width("Chat", (dpg.get_viewport_width())-dpg.get_item_width("Info"))
        dpg.set_item_width("TextToMessage", dpg.get_item_width("Chat")-170)
        dpg.set_item_pos("TextToMessage", [15, dpg.get_viewport_height() - 115])
        dpg.set_item_pos("SendButton", [dpg.get_item_pos("TextToMessage")[0] + dpg.get_item_width("TextToMessage") + 10, dpg.get_item_pos("TextToMessage")[1]])


        dpg.render_dearpygui_frame()

    dpg.start_dearpygui()
    dpg.destroy_context()

# ChatVisual()
import dearpygui.dearpygui as dpg
from main import Chat
import urllib.request

# Programm function
def SendMessange():
    value = dpg.get_value("TextToMessage")
    if value == "":
        pass
    else:
        Chat.SendMassage(value)
        AddNewMessage("You: " + "\n" + value)
        dpg.set_value("TextToMessage", "")

def AddNewMessage(text):
    with dpg.child_window(parent="MessangeField", width=200, height=100):
        dpg.add_text(default_value=text)
    # for child in range(0, len(dpg.get_item_children("MessangeField")[1])):
    #     dpg.set_item_height(dpg.get_item_children("MessangeField")[1][child], dpg.get_item_height(dpg.get_item_children(dpg.get_item_children("MessangeField")[1][child])[1][0]))
    
    dpg.focus_item("TextToMessage")
        

def AddGetMessage(text):
    with dpg.child_window(parent="MessangeField", width=200, height=100):
        dpg.add_text(default_value=text)

# Main programm
def ChatVisual():
    dpg.create_context()
    dpg.create_viewport(title='Decetralizet chat', width=1100, height=700)
    # dpg.show_item_registry()
    with dpg.window(label="Chat",pos=[310,0], height=dpg.get_viewport_height(), no_title_bar=True, width=dpg.get_viewport_width(), tag="Chat", no_close=True, no_collapse=True):
        with dpg.child_window(pos=[10,5], width=dpg.get_viewport_width() - 10, height=dpg.get_viewport_height() - 70, tag="MessangeField", border=False):
            pass
        dpg.add_input_text(multiline=True, hint="Messange",pos=[10, 50], width=dpg.get_item_width("Chat") - 170,tag="TextToMessage", height= 50)
        dpg.focus_item("TextToMessage")
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
            AddGetMessage("His: " + "\n" +str(data).replace("b'","").replace("'", "").replace("@_@", "\n").replace("@-@", " "))
            urllib.request.urlopen("http://127.0.0.1:5000/Delete")

        dpg.set_item_height("Chat", dpg.get_viewport_height())   
        dpg.set_item_height("Info", dpg.get_viewport_height())
        if dpg.get_active_window() == 21:
            dpg.set_item_width("Info", dpg.get_viewport_width() - dpg.get_item_width("Chat"))

        dpg.set_item_pos("Chat", [dpg.get_item_width("Info"),0])
        dpg.set_item_width("Chat", (dpg.get_viewport_width())-dpg.get_item_width("Info"))
        dpg.set_item_width("TextToMessage", dpg.get_item_width("Chat")-165)
        dpg.set_item_pos("TextToMessage", [10, dpg.get_viewport_height() - 115])
        dpg.set_item_pos("SendButton", [dpg.get_item_pos("TextToMessage")[0] + dpg.get_item_width("TextToMessage") + 10, dpg.get_item_pos("TextToMessage")[1]])
        dpg.set_item_width("MessangeField", dpg.get_viewport_width() - (35 + 310))
        dpg.set_item_height("MessangeField", dpg.get_viewport_height() - 130)

        for child in range(0, len(dpg.get_item_children("MessangeField")[1])):
            messangeLines = len(str(dpg.get_value((dpg.get_item_children(dpg.get_item_children("MessangeField")[1][child])[1][0]))).split("\n"))
            dpg.set_item_height(dpg.get_item_children("MessangeField")[1][child], (messangeLines * 13)+20)

            maxLine = 0
            for line in dpg.get_value((dpg.get_item_children(dpg.get_item_children("MessangeField")[1][child])[1][0])).split("\n"):
                if len(line) > maxLine:
                    maxLine = len(line)
            dpg.set_item_width(dpg.get_item_children("MessangeField")[1][child], (maxLine * 7)+20)


            # dpg.set_item_width(dpg.get_item_children("MessangeField")[1][child], dpg.get_item_width(dpg.get_item_children(dpg.get_item_children("MessangeField")[1][child]))[1][0])


        dpg.render_dearpygui_frame()

    dpg.start_dearpygui()
    dpg.destroy_context()

# ChatVisual()
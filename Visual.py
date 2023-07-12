import dearpygui.dearpygui as dpg
from main import Chat
import urllib.request

ContactIP = ["Seived Messange", "GET ","111.111.111.111:9090", "8.8.8.8:9090"]
confirmedIP = []

curentTab = "Ordinary"

# Programm function
def SendMessange():
    value = dpg.get_value("TextToMessage")
    if value == "":
        pass
    else:
        for item in dpg.get_item_children("Chat")[1]:
            if item == dpg.get_item_children("Chat")[1][0] or item == dpg.get_item_children("Chat")[1][1]:
                pass
            elif item == dpg.get_item_children("Chat")[1][2]:
                if dpg.is_item_shown(item):
                    AddNewMessage("You: " + "\n" + value)
                    dpg.set_value("TextToMessage", "")
            elif item == dpg.get_item_children("Chat")[1][3]:
                pass
            else: 
                if dpg.is_item_shown(item):
                    res = Chat(str(dpg.get_item_alias(item)).replace("messageField","").split(":")[0], int(str(dpg.get_item_alias(item)).replace("messageField","").split(":")[1])).SendMassage(value=value)
                    print(res)
                    if res == "success":
                        AddNewMessage("You: " + "\n" + value)
                        dpg.set_value("TextToMessage", "")

def resizeText():
    for item in dpg.get_item_children("Chat")[1]:
            if item == dpg.get_item_children("Chat")[1][0] or item == dpg.get_item_children("Chat")[1][1]:
                pass
            else: 
                for child in range(0, len(dpg.get_item_children(item)[1])):
                        messangeLines = len(str(dpg.get_value((dpg.get_item_children(dpg.get_item_children(item)[1][child])[1][0]))).split("\n"))
                        dpg.set_item_height(dpg.get_item_children(item)[1][child], (messangeLines * 13)+20)

                        maxLine = 0
                        for line in dpg.get_value((dpg.get_item_children(dpg.get_item_children(item)[1][child])[1][0])).split("\n"):
                            if len(line) > maxLine:
                                maxLine = len(line)
                        dpg.set_item_width(dpg.get_item_children(item)[1][child], (maxLine * 7)+20)

def AddNewMessage(text):
    parent = ""
    for item in dpg.get_item_children("Chat")[1]:
            if item == dpg.get_item_children("Chat")[1][0] or item == dpg.get_item_children("Chat")[1][1]:
                pass
            else: 
                if dpg.is_item_shown(item):
                    parent = item

    with dpg.child_window(parent=parent, width=200, height=100):
        dpg.add_text(default_value=text)
    resizeText()
    dpg.focus_item("TextToMessage")
        
def AddGetMessage(text):
    text = str(text)
    try:
        dpg.get_item_info(f"messageField{text.split('/', 1)[0]}")
    except:
        ContactIP.append(text.split('/', 1)[0])
        if confirmedIP != ContactIP:
            for ip in ContactIP:
                for i in dpg.get_item_children("ContactTab")[1]:
                    if i == dpg.get_item_children("ContactTab")[1][0]:
                        pass
                    elif curentTab == dpg.get_item_label(i):
                        for k in range(len(confirmedIP), len(ContactIP)):
                            with dpg.child_window(tag=f"messageField{ContactIP[k]}", parent="Chat", show=False, border=False):
                                pass
                            with dpg.child_window(height=80, parent=i):
                                dpg.add_text(f"{ContactIP[k]}")
                                dpg.add_button(label="-->", pos=[255, 30], callback=ShowMessangeField, tag=f"messageButton{ContactIP[k]}")
                                confirmedIP.append(ContactIP[k])

    with dpg.child_window(parent=f"messageField{text.split('/', 1)[0]}", width=200, height=100):
        dpg.add_text(default_value="His:"+ "\n" + text.split('/', 1)[1])
    resizeText()

def ShowMessangeField(sender):
    for item in dpg.get_item_children("Chat")[1]:
            if item == dpg.get_item_children("Chat")[1][0] or item == dpg.get_item_children("Chat")[1][1]:
                pass
            else: 
                dpg.hide_item(item)
    dpg.show_item(str(dpg.get_item_alias(sender)).replace("messageButton", "messageField"))

def AddNewContact():
    ip = dpg.get_value("AddContactIp")
    port = dpg.get_value("AddContactPort")
    if f"{ip}:{port}" in ContactIP:
        dpg.show_item("errorAddContact")
    else:
        ContactIP.append(f"{ip}:{port}")
        dpg.set_value("AddContactIp", "")
        dpg.set_value("AddContactPort", "")
        dpg.hide_item("errorAddContact")
        dpg.hide_item("modal_id")

def AddNewCategory():
    CatName = dpg.get_value("AddСategory")
    with dpg.tab(label=CatName, closable=True, parent="ContactTab"):
        pass
    dpg.set_value("AddСategory", "")
    dpg.hide_item("modal_id_New_Chat")

# Main programm
def ChatVisual():
    global curentTab, confirmedIP
    dpg.create_context()
    dpg.create_viewport(title='Decetralizet chat', width=1100, height=700)
    with dpg.window(label="but", tag="SpecialButton"):
        dpg.add_button()

    with dpg.window(label="Chat",pos=[310,0], height=dpg.get_viewport_height(), no_title_bar=True, width=dpg.get_viewport_width(), tag="Chat", no_close=True, no_collapse=True):
        dpg.add_input_text(multiline=True, hint="Messange",pos=[10, 50], width=dpg.get_item_width("Chat") - 170,tag="TextToMessage", height= 50)
        dpg.focus_item("TextToMessage")
        dpg.add_button(label="Send", height= 50, width=120, tag="SendButton", callback=SendMessange)
        

    with dpg.window(label="Info", width=310, height=dpg.get_viewport_height(), tag="Info", no_close=True, no_collapse=True):
        dpg.add_button(label="Add new contact")
        with dpg.tab_bar(tag="ContactTab"):
            dpg.add_tab_button(label="+", trailing=True, callback=lambda: dpg.show_item("modal_id_New_Chat"))
            with dpg.tab(label="Ordinary",closable=False):
                pass
    
    with dpg.popup(parent=dpg.get_item_children("Info")[1][0], mousebutton=dpg.mvMouseButton_Left, modal=True, tag="modal_id", min_size=[380, 160], max_size=[380, 160]):
        dpg.add_text(default_value="Add new contact", pos=[140, 25])
        dpg.add_text(default_value="Ip:", pos=[15, 70])
        dpg.add_text(default_value="Port:", pos=[15, 100])
        dpg.add_input_text(hint="192.168.0.1", pos=[40,70], width=230, tag="AddContactIp")
        dpg.add_input_text(hint="9090", pos=[55,100], width=65, tag="AddContactPort")
        dpg.add_text(default_value="This ip is already in the list", pos=[15, 125], color=(255,0,0,255), show=False, tag="errorAddContact")
        dpg.add_button(label="Add", pos=[280,70],width=90, height=50, callback=AddNewContact)

    with dpg.popup(parent=dpg.get_item_children("SpecialButton")[1][0], modal=True, tag="modal_id_New_Chat", min_size=[380, 150], max_size=[380, 150]):
        dpg.add_text(default_value="Add new category", pos=[140, 25])
        dpg.add_text(default_value="Category name:", pos=[15, 70])
        dpg.add_input_text(hint="Favorits", pos=[120,70], width=250, tag="AddСategory")
        dpg.add_button(label="Add", pos=[280,100],width=90, height=20, callback=AddNewCategory)
    
    dpg.setup_dearpygui()
    dpg.show_viewport()

    while dpg.is_dearpygui_running():
        response = urllib.request.urlopen("http://127.0.0.1:5000/")
        data = response.read()
        if str(data).replace("b'","").replace("'", "") == "":
            pass
        else:
            AddGetMessage(str(data).replace("b'","").replace("'", "").replace("@_@", "\n").replace("@-@", " ").replace("@^@","\r"))
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
        for item in dpg.get_item_children("Chat")[1]:
            if item == dpg.get_item_children("Chat")[1][0] or item == dpg.get_item_children("Chat")[1][1]:
                pass
            else: 
                dpg.set_item_width(item, dpg.get_viewport_width() - (35 + 310))
                dpg.set_item_height(item, dpg.get_viewport_height() - 130)

        for i in dpg.get_item_children("ContactTab")[1]:
            if i == dpg.get_item_children("ContactTab")[1][0]:
                pass
            else:
                if dpg.is_item_clicked(i):
                    curentTab = dpg.get_item_label(i)

        if confirmedIP != ContactIP:
            for ip in ContactIP:
                for i in dpg.get_item_children("ContactTab")[1]:
                    if i == dpg.get_item_children("ContactTab")[1][0]:
                        pass
                    elif curentTab == dpg.get_item_label(i):
                        for k in range(len(confirmedIP), len(ContactIP)):
                            with dpg.child_window(tag=f"messageField{ContactIP[k]}", parent="Chat", show=False, border=False):
                                pass
                            with dpg.child_window(height=80, parent=i):
                                dpg.add_text(f"{ContactIP[k]}")
                                dpg.add_button(label="-->", pos=[255, 30], callback=ShowMessangeField, tag=f"messageButton{ContactIP[k]}")
                                confirmedIP.append(ContactIP[k])

        for i in dpg.get_item_children("ContactTab")[1]:
            if i == dpg.get_item_children("ContactTab")[1][0]:
                pass
            elif curentTab == dpg.get_item_label(i):
                for k in dpg.get_item_children(i)[1]:
                    dpg.set_item_pos(dpg.get_item_children(k)[1][1], pos=[dpg.get_item_width("Info")-60, 30])



        dpg.render_dearpygui_frame()

    dpg.start_dearpygui()
    dpg.destroy_context()

# ChatVisual()
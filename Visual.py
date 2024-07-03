import dearpygui.dearpygui as dpg
import os
import hashlib

import tkinter as tk
from tkinter import filedialog

from main import Chat
import FileTypes


ContactIP = ["Seved Messages", "GET "]
confirmedIP = []

curentTab = "Ordinary"


# Programm function
def SendMessange():
    value:str = dpg.get_value("TextToMessage")
    newValueMessage:str = ""
    # Transform value
    for text_str in value.split("$$"):
        if text_str == "":
            pass
        elif len(text_str.split("->")) == 2:
            if os.path.exists(text_str.split("->")[1]):
                with open(text_str.split("->")[1], "rb") as file:
                    newValueMessage += f"$${text_str.split("->")[0]}->{file.read().hex()}$$"
            else:
                pass
        else:
            newValueMessage += text_str
            
    
    if newValueMessage == "":
        pass
    else:
        for item in dpg.get_item_children("Chat")[1]:
            if item == dpg.get_item_children("Chat")[1][0] or item == dpg.get_item_children("Chat")[1][1] or item == dpg.get_item_children("Chat")[1][2]:
                pass
            elif item == dpg.get_item_children("Chat")[1][3]:
                if dpg.is_item_shown(item):
                    recognizedValueMessage:str = ""
                    ip_hash = hashlib.md5("Seved Messages".encode(encoding="utf-8")).hexdigest()
                    
                    for text_str in newValueMessage.split("$$"):
                        if text_str == "":
                            pass
                        elif len(text_str.split("->")) == 2:
                            file_type = text_str.split("->")[0].split(".")[-1].lower()
                            file_name = hashlib.md5(text_str.split("->")[1].encode(encoding="utf-8")).hexdigest()
                            file_path = f"./chat/{ip_hash}/images/{file_name}.{file_type}"
                            
                            with open(file_path, "wb") as file:
                                file.write(bytes.fromhex(text_str.split("->")[1]))
                                if str(text_str.split("->")[0].split(".")[-1]) in FileTypes.images:
                                    recognizedValueMessage += f"$${file_name}.{file_type}->{file_path}$$"
                                else:
                                    pass
                        else:
                            recognizedValueMessage += text_str
                        
                    AddNewMessage(recognizedValueMessage)
                    with open(f"./chat/{ip_hash}/chat.info", "a+") as file:
                        file.write("saved/" + recognizedValueMessage + "\n")
                        file.write("-----" + "\n")
                    dpg.set_value("TextToMessage", "")
                    
            elif item == dpg.get_item_children("Chat")[1][4]:
                pass
            else: 
                if dpg.is_item_shown(item):
                    ip_client = str(dpg.get_item_alias(item)).replace("messageField","").split(":")[0]
                    port_client = int(str(dpg.get_item_alias(item)).replace("messageField","").split(":")[-1])
                    ip_hash = hashlib.md5(f"{ip_client}:{port_client}".encode(encoding="utf-8")).hexdigest()
                    
                    res = Chat(ip=ip_client, port=port_client).SendMassage(value=newValueMessage + "<!>")
                    if res == True:
                        recognizedValueMessage:str = ""
                        for text_str in newValueMessage.split("$$"):
                            if text_str == "":
                                pass
                            elif len(text_str.split("->")) == 2:
                                file_type = text_str.split("->")[0].split(".")[-1].lower()
                                file_name = hashlib.md5(text_str.split("->")[1].encode(encoding="utf-8")).hexdigest()
                                file_path = f"./chat/{ip_hash}/images/{file_name}.{file_type}"
                                
                                with open(file_path, "wb") as file:
                                    file.write(bytes.fromhex(text_str.split("->")[1]))
                                    if str(text_str.split("->")[0].split(".")[-1]) in FileTypes.images:
                                        recognizedValueMessage += f"$${file_name}.{file_type}->{file_path}$$"
                            else:
                                recognizedValueMessage += text_str
                                
                        AddNewMessage(recognizedValueMessage)
                        with open(f"./chat/{ip_hash}/chat.info", "a+") as file:
                            file.write(f"{ip_client}:{port_client}/you/" + recognizedValueMessage + "\n")
                            file.write("-----" + "\n")
                        dpg.set_value("TextToMessage", "")

def resizeMessage():
    for item in dpg.get_item_children("Chat")[1]:
        if item == dpg.get_item_children("Chat")[1][0] or item == dpg.get_item_children("Chat")[1][1] or item == dpg.get_item_children("Chat")[1][2]:
            pass
        else: 
            for child in range(0, len(dpg.get_item_children(item)[1])):
                messangeLines = 0
                maxLine = 0
                for item_index in range(0, len(dpg.get_item_children(dpg.get_item_children(item)[1][child])[1])):
                    item_type = dpg.get_item_type(dpg.get_item_children(dpg.get_item_children(item)[1][child])[1][item_index])
                    if item_type == "mvAppItemType::mvText":
                        # Text height
                        messangeLines += len(str(dpg.get_value(dpg.get_item_children(dpg.get_item_children(item)[1][child])[1][item_index])).split("\n"))
                        # Text width
                        for line in str(dpg.get_value(dpg.get_item_children(dpg.get_item_children(item)[1][child])[1][item_index])).split("\n"):
                            if len(line) > maxLine:
                                maxLine = len(line)
                    elif item_type == "mvAppItemType::mvImage":
                        image_width = dpg.get_item_width(dpg.get_item_children(dpg.get_item_children(item)[1][child])[1][item_index])
                        image_height = dpg.get_item_height(dpg.get_item_children(dpg.get_item_children(item)[1][child])[1][item_index])
                        if image_width > (maxLine * 7)+20:
                            maxLine = ((image_width - 20) / 7) + 2
                        messangeLines += ((image_height - 20) / 13) + 1
                    else:
                        pass
                    messangeLines += len(dpg.get_item_children(dpg.get_item_children(item)[1][child])[1]) / 3
                dpg.set_item_height(dpg.get_item_children(item)[1][child], (messangeLines * 13)+20)
                dpg.set_item_width(dpg.get_item_children(item)[1][child], (maxLine * 7)+20)

def AddNewMessage(text, parent=None):
    if parent is None:
        for item in dpg.get_item_children("Chat")[1]:
            if item == dpg.get_item_children("Chat")[1][0] or item == dpg.get_item_children("Chat")[1][1] or item == dpg.get_item_children("Chat")[1][2]:
                pass
            else: 
                if dpg.is_item_shown(item):
                    parent = item

    with dpg.child_window(parent=parent, width=500, height=600):
        dpg.add_text(default_value="You:")
        for text_str in text.split("$$"):
            if text_str == "":
                pass
            elif len(text_str.split("->")) == 2:
                texture_tag = text_str.split("->")[1].split("/")[-1]
                if dpg.get_alias_id(texture_tag) == 0:
                    img_width, img_height, channels, data = dpg.load_image(text_str.split("->")[1])
                    with dpg.texture_registry(show=False):
                        dpg.add_static_texture(width=img_width, height=img_height, default_value=data, tag=texture_tag)
                
                if img_width > img_height:
                        img_width_delta = img_width / 730
                        img_width = 730
                        img_height = img_height / img_width_delta
                elif img_width < img_height:
                    img_width_delta = img_width / 540
                    img_width = 540
                    img_height = img_height / img_width_delta
                else:
                    img_width = 540
                    img_height = 540
                dpg.add_image(texture_tag=texture_tag, width=img_width, height=img_height)
                    
            else:
                dpg.add_text(default_value=text_str)
    resizeMessage()
    dpg.focus_item("TextToMessage")
        
def AddGetMessage(text, is_restore=False):
    text = str(text)
    ip = text.split('/', 1)[0]
    ip_hash = hashlib.md5(ip.encode(encoding="utf-8")).hexdigest()
    if not os.path.exists(f"./chat/{ip_hash}"):
        os.mkdir(f"./chat/{ip_hash}")
        os.mkdir(f"./chat/{ip_hash}/images")

    if dpg.get_alias_id(f"messageField{ip}") == 0:
        ContactIP.append(ip)
        if confirmedIP != ContactIP:
            for counter in ContactIP:
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

    with dpg.child_window(parent=f"messageField{ip}", width=200, height=100):
        dpg.add_text(default_value="His:")
        recognizedValueMessage:str = ""
        
        # ---------------
        try:
            text = text.split('/', 1)[1] # +
        except:
            text = text.split('/', 1)[0]
        # ---------------
            
        for text_str in text.split("$$"):
            if text_str == "":
                pass
            elif len(text_str.split("->")) == 2:
                file_type = text_str.split("->")[0].split(".")[-1].lower()
                if not is_restore:
                    file_name = hashlib.md5(text_str.split("->")[1].encode(encoding="utf-8")).hexdigest()
                    file_path = f"./chat/{ip_hash}/images/{file_name}.{file_type}"
                    with open(file_path, "wb") as file:
                        file.write(bytes.fromhex(text_str.split("->")[1]))
                else:
                    file_path = text_str.split("->")[1]
                    file_name = text_str.split("->")[0].split(".")[0]
                    
                if file_type in FileTypes.images:
                    texture_tag = file_name
                    if dpg.get_alias_id(texture_tag) == 0:
                        img_width, img_height, channels, data = dpg.load_image(file_path)
                        with dpg.texture_registry(show=False):
                            dpg.add_static_texture(width=img_width, height=img_height, default_value=data, tag=texture_tag)
                    
                    if img_width > img_height:
                            img_width_delta = img_width / 730
                            img_width = 730
                            img_height = img_height / img_width_delta
                    elif img_width < img_height:
                        img_width_delta = img_width / 540
                        img_width = 540
                        img_height = img_height / img_width_delta
                    else:
                        img_width = 540
                        img_height = 540
                        
                    dpg.add_image(texture_tag=texture_tag, width=img_width, height=img_height)
                    recognizedValueMessage += f"$${file_name}.{file_type}->{file_path}$$"
            else:
                dpg.add_text(default_value=text_str)
                recognizedValueMessage += text_str
    if not is_restore:
        with open(f"./chat/{ip_hash}/chat.info", "a+") as file:
            file.write(f"{ip}/his/" + recognizedValueMessage + "\n")
            file.write("-----" + "\n")
    resizeMessage()

def ShowMessangeField(sender):
    for item in dpg.get_item_children("Chat")[1]:
        if item == dpg.get_item_children("Chat")[1][0] or item == dpg.get_item_children("Chat")[1][1] or item == dpg.get_item_children("Chat")[1][2]:
            pass
        else: 
            dpg.hide_item(item)
    dpg.set_item_label("Chat", dpg.get_item_alias(sender).lstrip("messageButton"))
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
    
def ClipboardFile():
    root = tk.Tk()
    root.withdraw()
    files = filedialog.askopenfilenames()
    root.destroy()
    if files == "":
        pass
    else:
        for file in files:
            message_file_info = f"$${file.split("/")[-1]}->{file}$$"
            dpg.set_value("TextToMessage", dpg.get_value("TextToMessage") + message_file_info)
            
def RestoreChats():
    path = "./chat"
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    for directory in dirs:
        with open(f"./chat/{directory}/chat.info") as info:
            AllFileInfo = info.read()
            for FileInfo in AllFileInfo.split("-----"):
                if FileInfo == "" or FileInfo ==  "\n":
                    pass
                else:
                    if FileInfo.split("/", 1)[0].replace("\n", "") == "saved":
                        # Add message to saved messages
                        parent = dpg.get_item_children("Chat")[1][3]
                        AddNewMessage(FileInfo.split("/", 1)[1].rstrip("\n"), parent=parent)
                    else:
                        ip = FileInfo.split("/", 1)[0].replace("\n", "")
                        parent = f"messageField{ip}"
                        if FileInfo.split("/")[1].lower() == "you":
                            # Add message to chat
                            text = FileInfo.split("/",2)[2].rstrip("\n")
                            AddNewMessage(text, parent=parent)
                        elif FileInfo.split("/", 2)[1].lower() == "his":
                            # Simulate send message
                            newMessage = FileInfo.split("/", 1)[0].lstrip("\n") + "/" + FileInfo.split("/", 2)[2].rstrip("\n")
                            AddGetMessage(newMessage, is_restore=True)
                        
    resizeMessage()
                        
        
# Main programm
def ChatVisual():
    global curentTab, confirmedIP
    dpg.create_context()
    dpg.create_viewport(title='Decetralizet chat', width=1100, height=700)
    width, height, channels, data = dpg.load_image("./images/addFileImage.png")
    with dpg.texture_registry(show=False):
        dpg.add_static_texture(width=width, height=height, default_value=data, tag="addFileImage")
        
    with dpg.window(label="but", tag="SpecialButton"):
        dpg.add_button()

    with dpg.window(label="Select chat",pos=[310,0], height=dpg.get_viewport_height(), width=dpg.get_viewport_width(), tag="Chat", no_close=True, no_collapse=True):
        dpg.add_input_text(multiline=True, hint="Messange",pos=[10, 50], width=dpg.get_item_width("Chat") - 170,tag="TextToMessage", height= 50)
        dpg.focus_item("TextToMessage")
        dpg.add_button(label="Send", height=50, width=120, tag="SendButton", callback=SendMessange)
        dpg.add_image_button(tag="addFileImageObj", texture_tag="addFileImage", width=44, height=44, callback=ClipboardFile)
        
        

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
        
    
    # dpg.show_item_registry()

    dpg.setup_dearpygui()
    dpg.show_viewport()

    one = 0
    while dpg.is_dearpygui_running():
        if not os.path.exists("./message.txt"):
            pass
        else:
            with open("./message.txt", "r") as message:
                text = message.read()
                AddGetMessage(text=text)
            os.remove("./message.txt")


        dpg.set_item_height("Chat", dpg.get_viewport_height())   
        dpg.set_item_height("Info", dpg.get_viewport_height())
        if dpg.get_active_window() == 21:
            dpg.set_item_width("Info", dpg.get_viewport_width() - dpg.get_item_width("Chat"))

        dpg.set_item_pos("Chat", [dpg.get_item_width("Info"),0])
        dpg.set_item_width("Chat", (dpg.get_viewport_width())-dpg.get_item_width("Info"))
        dpg.set_item_width("TextToMessage", dpg.get_item_width("Chat") - 215)
        dpg.set_item_pos("TextToMessage", [10, dpg.get_viewport_height() - 100])
        dpg.set_item_pos("SendButton", [dpg.get_item_pos("TextToMessage")[0] + dpg.get_item_width("TextToMessage") + 60, dpg.get_item_pos("TextToMessage")[1]])
        dpg.set_item_pos("addFileImageObj", [dpg.get_item_pos("TextToMessage")[0] + dpg.get_item_width("TextToMessage"), dpg.get_item_pos("TextToMessage")[1]])
        
        for item in dpg.get_item_children("Chat")[1]:
            if item == dpg.get_item_children("Chat")[1][0] or item == dpg.get_item_children("Chat")[1][1] or item == dpg.get_item_children("Chat")[1][2]:
                pass
            else: 
                dpg.set_item_width(item, dpg.get_viewport_width() - (35 + 310))
                dpg.set_item_height(item, dpg.get_viewport_height() - 150)

        for i in dpg.get_item_children("ContactTab")[1]:
            if i == dpg.get_item_children("ContactTab")[1][0]:
                pass
            else:
                if dpg.is_item_clicked(i):
                    curentTab = dpg.get_item_label(i)
        
        if confirmedIP != ContactIP:
                for counter in ContactIP:
                    for i in dpg.get_item_children("ContactTab")[1]:
                        if i == dpg.get_item_children("ContactTab")[1][0]:
                            pass
                        elif curentTab == dpg.get_item_label(i):
                            for k in range(len(confirmedIP), len(ContactIP)):
                                with dpg.child_window(tag=f"messageField{ContactIP[k]}", parent="Chat", show=False, border=False):
                                    pass
                                with dpg.child_window(height=80, parent=i):
                                    ip = ContactIP[k]
                                    ip_hash = hashlib.md5(ContactIP[k].encode(encoding="utf-8")).hexdigest()
                                    if not os.path.exists(f"./chat/{ip_hash}"):
                                        os.mkdir(f"./chat/{ip_hash}")
                                        os.mkdir(f"./chat/{ip_hash}/images")
                                    if not os.path.exists(f"./chat/{ip_hash}/chat.info"):
                                        with open(f"./chat/{ip_hash}/chat.info", "w") as file:
                                            file.write("")
                                    dpg.add_text(f"{ContactIP[k]}")
                                    dpg.add_button(label="-->", pos=[255, 30], callback=ShowMessangeField, tag=f"messageButton{ContactIP[k]}")
                                    confirmedIP.append(ContactIP[k])
        
        if one == 0:
            RestoreChats()
            one = 1

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
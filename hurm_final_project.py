'''
Name: hurm_final_project.py
Author: Erin Hurm
Version: 1.0
Date: 7/24/2024
Description: Ordering app for the Drone Dogs hot dog delivery service.

Hot dog image from: https://www.pngall.com/hot-dog-png/download/5007
Drone image from: https://en.wikipedia.org/wiki/File:Parrot_AR.Drone_2.JPG

'''

import tkinter as tk
from tkinter import *
from tkinter import messagebox, PhotoImage, scrolledtext, ttk
from functools import partial
from PIL import Image, ImageTk

window = tk.Tk()
window.title("Drone Dogs Ordering App")

# Menu items and their prices
dogOptions = {
    "Traditional Dog": 5,
    "Vegan Dog": 5,
    "Cheese Dog": 6,
}
bunOptions = {
    "White Bun": 0,
    "Cheese Bun": 1,
    "Gluten Free Bun": 1,
    "Corn Dog": 2,
    }
toppingOptions = {
    "Ketchup": 0,
    "Mustard": 0,
    "Relish": 0,
    "Onions": 0,
    "Chili": 0,
    "Nacho Cheese": 0,
    "Avocado": 1,
    "Bacon": 1,
}

#dictionary to hold order info
global orders, paymentdict, deliverydict
orders = {}
paymentdict = {}
deliverydict = {}
toppingsBoxes = {}
toppings = []

# create hot dog ordering window
def dogWindowMake():
    dogWindow = Toplevel(window)
    dogWindow.title("Build Your Dog")

    name_frame = tk.Frame(dogWindow)
    name_frame.grid(row=0,column=0,columnspan=3,pady=10)

    dog_frame = tk.Frame(dogWindow)
    dog_frame.grid(row=1,column=0,sticky=N,padx=15,pady=10)

    bun_frame = tk.Frame(dogWindow)
    bun_frame.grid(row=1,column=1,sticky=N,padx=15, pady=10)

    toppings_frame = tk.Frame(dogWindow)
    toppings_frame.grid(row=1,column=2,sticky=N,padx=15,pady=10)

    #name for order
    nameLabel = tk.Label(name_frame, text="Name:", font=("TkDefaultFont",12,"bold"))
    nameLabel.grid(row=0, column=0, sticky=E)
    orderNameEntry = tk.Entry(name_frame)
    orderNameEntry.grid(row=0, column=1)

    #dog column positioning
    dogLabel = tk.Label(dog_frame, text="Choose Your Dog:", font=("TkDefaultFont",12,"bold"))
    dogLabel.grid(row=0,column=0,sticky=NW)

    #make radio buttons for dog pick
    dogVar = tk.StringVar()
    radioButtons(dog_frame, dogOptions, dogVar)
    dogVar.set("Traditional Dog") #default

    bunLabel = tk.Label(bun_frame, text="Choose Your Bun:", font=("TkDefaultFont",12,"bold"))
    bunLabel.grid(row=0, column=0, sticky=NW)

    #make radio buttons for bun pick
    bunVar = tk.StringVar()
    radioButtons(bun_frame, bunOptions, bunVar)
    bunVar.set("White Bun") #default

    #make check buttons for toppings
    toppingsLabel = tk.Label(toppings_frame, text="Add Up to 3 Toppings:", font=("TkDefaultFont",12,"bold"))
    toppingsLabel.grid(row=0, column=0, columnspan= 2, sticky=NW)
    toppingsCheckboxes(toppings_frame, toppingOptions, toppingsBoxes)

    #Add to Order button
    addButtonFunc = partial(
        addToOrder,
        orderNameEntry,
        dogVar,
        bunVar,
        dogWindow
        )
    addButton = tk.Button(name_frame, text="Add to Order", command=addButtonFunc)
    addButton.grid(row=0, column=2, sticky=W, padx=10)

#create delivery info window
def deliveryWindowMake():
    deliveryWindow = Toplevel(window)
    deliveryWindow.title=("Enter Delivery Info")
    
    usStates = [
    # https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States#States.
    "AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "IA",
    "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO",
    "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI",
    "WV", "WY",
    # https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States#Federal_district.
    "DC",
    # https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States#Inhabited_territories.
    "AS", "GU", "MP", "PR", "VI",
    ]

    deliveryNameLabel = tk.Label(deliveryWindow, text="Name:")
    deliveryNameLabel.grid(row=0,sticky=E)
    deliveryNameEntry = tk.Entry(deliveryWindow)
    deliveryNameEntry.grid(row=0,column=1,padx=10,pady=10)

    addressLabel = tk.Label(deliveryWindow, text="Address:")
    addressLabel.grid(row=1,sticky=E)
    addressEntry = tk.Entry(deliveryWindow)
    addressEntry.grid(row=1,column=1,padx=10,pady=10)

    address2Label = tk.Label(deliveryWindow, text="Address 2:")
    address2Label.grid(row=2,sticky=E)
    address2Entry = tk.Entry(deliveryWindow)
    address2Entry.grid(row=2,column=1,padx=10,pady=10)

    cityLabel = tk.Label(deliveryWindow, text="City:")
    cityLabel.grid(row=3,sticky=E)
    cityEntry = tk.Entry(deliveryWindow)
    cityEntry.grid(row=3,column=1,padx=10,pady=10)

    stateLabel = tk.Label(deliveryWindow, text="State:")
    stateLabel.grid(row=4,sticky=E, padx=10)

    #allows state and zip to be on same line
    statezip_frame = tk.Frame(deliveryWindow)
    statezip_frame.grid(row=4,column=1, sticky=W)

    stateListbox = ttk.Combobox(statezip_frame, values=usStates, width=3,state="readonly")
    stateListbox.grid(row=0,column=0,sticky=W,padx=10,pady=10)
    stateListbox.set("IN")

    zipLabel = tk.Label(statezip_frame, text="ZIP:")
    zipLabel.grid(row=0,column=1,sticky=E)
    zipEntry = tk.Entry(statezip_frame, width=6)
    zipEntry.grid(row=0,column=2,sticky=E,padx=10,pady=10)

    instructionsLabel = tk.Label(deliveryWindow, text="Special Instructions:")
    instructionsLabel.grid(row=5,sticky=E, padx=10)
    instructionsEntry = tk.Text(deliveryWindow, height=2, width = 20, font="TkDefaultFont")
    instructionsEntry.grid(row=5,column=1,padx=10,pady=10)

    submitButtonFunc = partial(
        deliveryInfo,
        deliveryNameEntry,
        addressEntry,
        address2Entry,
        cityEntry,
        stateListbox,
        zipEntry,
        instructionsEntry,
        deliveryWindow
        )
    
    submitButton = tk.Button(deliveryWindow, text="Submit", command=submitButtonFunc)
    submitButton.grid(row=6,column=1,columnspan=2,padx=10,pady=10)

#what happens when you click "submit" on delivery info page
def deliveryInfo(
        deliveryNameEntry,
        addressEntry,
        address2Entry,
        cityEntry,
        stateListbox,
        zipEntry,
        instructionsEntry,
        deliveryWindow
):
    global deliverydict

    deliveryInfoList = [
        deliveryNameEntry,
        addressEntry,
        address2Entry,
        cityEntry,
        stateListbox,
        zipEntry,
        instructionsEntry
    ]

    i=0
    complete = False

    #input validation
    for i in range(0, len(deliveryInfoList)):
        if i==6:
            current = deliveryInfoList[i].get("1.0",'end-1c') #text has different syntax for get
        else:
            current = deliveryInfoList[i].get()

        if i==2 and current == "": #skips address 2 if empty
            i+=1
        elif i==5:    #checks zip for number & correct length
            if (not current.isdigit()) or (not len(current)==5):
                errorMsg()
                break
        else:
            #make sure string isn't too long
            if i==6:
                lenmin = 0
                lenmax = 140 #different max length for special instructions
            else: #2 will only go through if there is something in it
                lenmin = 1
                lenmax = 30

            if checkEntry(current,lenmin,lenmax): #will pop error & stop loop
                i+=1
                if i == len(deliveryInfoList):
                    complete=True #tell it OK to write to dict
            else:
                break

    if complete:
        deliverydict["name"] = deliveryNameEntry.get()
        deliverydict["address"] = addressEntry.get()
        deliverydict["address2"] = address2Entry.get()
        deliverydict["city"] = cityEntry.get()
        deliverydict["state"] = stateListbox.get()
        deliverydict["zip"] = zipEntry.get()
        deliverydict["instructions"] = instructionsEntry.get("1.0",'end-1c')
        
        print(deliverydict)

        paymentbutton.config(state=tk.ACTIVE)

        deliveryWindow.destroy()

#create payment info window
def paymentWindowMake():
    paymentWindow = Toplevel(window)
    paymentWindow.title=("Enter Payment Info")

    payFNLabel = tk.Label(paymentWindow, text="First Name:")
    payFNLabel.grid(row=0,sticky=E)
    payFNEntry = tk.Entry(paymentWindow)
    payFNEntry.grid(row=0,column=1,padx=10,pady=10)

    payLNLabel = tk.Label(paymentWindow, text="Last Name:")
    payLNLabel.grid(row=1,sticky=E)
    payLNEntry = tk.Entry(paymentWindow)
    payLNEntry.grid(row=1,column=1,padx=10,pady=10)

    payCardLabel = tk.Label(paymentWindow, text="Card Number:")
    payCardLabel.grid(row=2,sticky=E)
    payCardEntry = tk.Entry(paymentWindow)
    payCardEntry.grid(row=2,column=1,padx=10,pady=10)

    payDateLabel = tk.Label(paymentWindow, text="Exp. Date:")
    payDateLabel.grid(row=3,sticky=E)
    
    payDateFrame = tk.Frame(paymentWindow)
    payDateFrame.grid(row=3,column=1,padx=10,pady=10)
    
    payDateEntry1 = tk.Entry(payDateFrame, width=3)
    payDateEntry1.grid(row=0, column=0,sticky=W)

    payDateLabel2 = tk.Label(payDateFrame, text="/")
    payDateLabel2.grid(row=0, column=1,sticky=W)

    payDateEntry2 = tk.Entry(payDateFrame,width=3)
    payDateEntry2.grid(row=0,column=2,sticky=W)

    paySecLabel = tk.Label(paymentWindow, text="Security:")
    paySecLabel.grid(row=4,sticky=E)
    paySecEntry = tk.Entry(paymentWindow)
    paySecEntry.grid(row=4,column=1,padx=10,pady=10)

    payZipLabel = tk.Label(paymentWindow, text="ZIP Code:")
    payZipLabel.grid(row=5,sticky=E)
    payZipEntry = tk.Entry(paymentWindow)
    payZipEntry.grid(row=5,column=1,padx=10,pady=10)

    paySubmitFunc = partial(
        paymentInfo,
        payFNEntry,
        payLNEntry,
        payCardEntry,
        payDateEntry1,
        payDateEntry2,
        paySecEntry,
        payZipEntry,
        paymentWindow
    )

    paySubmit = tk.Button(paymentWindow, text="Submit", command=paySubmitFunc)
    paySubmit.grid(row=6,columnspan=2,padx=10,pady=10)
    
def paymentInfo(
        payFNEntry,
        payLNEntry,
        payCardEntry,
        payDateEntry1,
        payDateEntry2,
        paySecEntry,
        payZipEntry,
        paymentWindow
    ):
    
    global paymentdict

    paymentInfoList = [
        payFNEntry,     #0
        payLNEntry,     #1
        payCardEntry,   #2
        payDateEntry1,  #3
        payDateEntry2,  #4
        paySecEntry,    #5
        payZipEntry     #6
    ]

    complete = False #prevents writing to paymentdict before ready

    for i in range(0,len(paymentInfoList)):
        current = paymentInfoList[i].get()
        if i == 3 or i == 4: #date
            lenmin = 2
            lenmax = 2
        elif i == 5: #security code
            lenmin = 3
            lenmax = 4
        elif i == 6: #zip
            lenmin = 5
            lenmax = 5
        else:
            lenmin = 1
            lenmax = 20

        if checkEntry(current,lenmin,lenmax): #will pop error, break loop
            if i == 0 or i == 1: #names
                if not current.isalpha():
                    errorMsg()
                    break
            else: #everything else should be numbers
                if not current.isdigit():
                    errorMsg()
                    break
            
            i+=1
            if i == len(paymentInfoList):
                complete=True #tell it OK to write to dict if it's at the end
        else:
            break

    if complete == True:
        paymentdict["first name"] = payFNEntry.get()
        paymentdict["last name"] = payLNEntry.get()
        paymentdict["card number"] = payCardEntry.get()
        paymentdict["exp month"] = payDateEntry1.get()
        paymentdict["exp year"] = payDateEntry2.get()
        paymentdict["security code"] = paySecEntry.get()
        paymentdict["zip"] = payZipEntry.get()
        
        print(paymentdict)

        placeorderbutton.config(state=tk.ACTIVE)
        paymentWindow.destroy()

#check to make sure entry length is appropriate
def checkEntry(value,lenmin,lenmax):
    if len(value) < lenmin or len(value) > lenmax:
        errorMsg()
        return FALSE
    else:
        return TRUE

#pops up error message
def errorMsg():
    messagebox.showerror("Input Error", "Please make sure your inputs are valid.")

#DOG WINDOW STUFF
#make radio buttons for dogs and buns
def radioButtons(thisFrame, dict,var):
    i=1  #starting row
    for key in dict.keys():
        #adds cost of items to label
        if dict[key] > 0:
            buttonTxt = key+" - $"+str(dict[key])
        else:
            buttonTxt = key
        tk.Radiobutton(
            thisFrame,
            text=buttonTxt,
            value=key,
            variable=var).grid(row=i,sticky=W,pady=5)
        i += 1

#make checkboxes for toppings
def toppingsCheckboxes(thisFrame, dict,boxes):
    i=1  #starting row
    col=0 #starting col
    for key in dict.keys():
        #adds cost of items to label
        if dict[key] > 0:
            buttonTxt = key+" - $"+str(dict[key])
        else:
            buttonTxt = key

        #makes a second column to even them out
        if i == 5:
            i = 1
            col = col+1

        var = tk.BooleanVar()
        tk.Checkbutton(
            thisFrame,
            text=buttonTxt,
            variable=var).grid(row=i, column=col, sticky=W, pady=5)
        boxes[key] = var
        i += 1

#add dog to order
def addToOrder(orderNameEntry, dogVar, bunVar, dogWindow):
    global orders

    #get entries
    orderName = orderNameEntry.get()
    dogPick = dogVar.get() #NEED TO FIGURE OUT INPUT VALIDATION FOR THESE
    bunPick = bunVar.get()
    toppingsList = getChk(toppingsBoxes, toppings)

    #data validation
    if orderName.isalpha() and len(orderName) < 20 and toppingsCheck(toppingsList):
        orders[orderName] = {"dog":dogPick}
        orders[orderName]["bun"] = bunPick
        orders[orderName]["toppings"] = toppingsList

        #determine cost
        orderCostVal = dogOptions[dogPick]
        orderCostVal += bunOptions[bunPick]
        if len(toppingsList) > 0:
            i=0
            while i < len(toppingsList):
                toppingPick = toppingsList[i]
                orderCostVal += toppingOptions[toppingPick]
                i += 1

        orders[orderName]["cost"] = orderCostVal
        dogWindow.destroy()
        print(orders)

        deliverybutton.config(state=tk.ACTIVE)
        updateOrder(orderName)

    else:
       errorMsg()

    return orders

#get toppings that have checkboxes checked
def getChk(box, out):
    out = []
    for key in box.keys():
        if box[key].get():
            out.append(key)
    return out

#check that number of toppings <= 3
def toppingsCheck(x):
    if len(x) <= 3:
        return True
    else:
        return False

#adds most recent order to the main text window
def updateOrder(key):
    global orders
    orderStr = ""
    orderStr += str(key)
    orderStr += " - $" + str(orders[key]["cost"]) + "\n"
    orderStr += "  " + orders[key]["dog"] + "\n"
    orderStr += "  " + orders[key]["bun"] + "\n"
    #check if there are toppings. if so, add to list
    if len(orders[key]["toppings"]) > 0:
        for t in range(0, len(orders[key]["toppings"])):
            orderStr += "  " + orders[key]["toppings"][t] + "\n"
    orderStr += "\n"
    orderTxt.configure(state="normal")
    orderTxt.insert(tk.END, orderStr)
    orderTxt.configure(state="disabled")

#Window comes up when you hit "Place Order"
def orderPlace():
    endWindow = Toplevel(window)
    endWindow.title = "Thank You!"

    #not working for some reason
    endImage = Image.open("assets/Drone.png")
    endImage = ImageTk.PhotoImage(endImage)
    image_label = tk.Label(endWindow, image=endImage)
    image_label.grid(row=0,column=0,padx=5,pady=5)

    orderPlacedLabel = tk.Label(endWindow, text="Your order is on its way!")
    orderPlacedLabel.grid(row=1,column=0,padx=10,pady=10)

    exitButton = tk.Button(endWindow, text="OK", command=killwindow)
    exitButton.grid(row=2,column=0,padx=10,pady=10)

#closes everything when you click "OK" after order placed
def killwindow():
    window.destroy()

buttons_frame = tk.Frame(window)
buttons_frame.grid(row=0,column=0)
order_frame = tk.Frame(window)
order_frame.grid(row=0,column=2)

#build main page
dogbutton = tk.Button(buttons_frame, text = "Build Your Dog", command = dogWindowMake)
dogbutton.grid(row=0, column=0, padx=20, pady=10)

deliverybutton = tk.Button(buttons_frame, text = "Delivery Info", command = deliveryWindowMake)
deliverybutton.grid(row=1, column=0, padx=20, pady=10)
deliverybutton.config(state=tk.DISABLED)

paymentbutton = tk.Button(buttons_frame, text = "Payment Info", command = paymentWindowMake)
paymentbutton.grid(row=2, column=0, padx=20, pady=10)
paymentbutton.config(state=tk.DISABLED)

placeorderbutton = tk.Button(buttons_frame, text = "Place Order", command = orderPlace)
placeorderbutton.grid(row=3, column=0, padx=20, pady=10)
placeorderbutton.config(state=tk.DISABLED)

try:
    mainImage = Image.open("assets/Hot-Dog-Transparent.png")
    mainImage = mainImage.resize((258,201))
    mainImage = ImageTk.PhotoImage(mainImage)
    image_label = tk.Label(window, image=mainImage)
    image_label.grid(row=0, column=1, padx=5, pady=5)
except FileNotFoundError:
    raise FileNotFoundError(f"Image file not found")


orderLabel = Label(order_frame, text="Your Order", font=("TkDefaultFont",16,"bold"))
orderLabel.grid(row=0)

#"receipt"-style order info
orderTxt = scrolledtext.ScrolledText(order_frame, wrap=tk.WORD, height = 20, width = 25)
orderTxt.grid(row=1,padx=10,pady=10)
orderTxt.configure(state="disabled")

window.mainloop()
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from functools import partial

window = tk.Tk()
window.title("Drone Dogs Ordering App")


# Menu items
dogOptions = {
    "Traditional Dog": 5,
    "Vegan Dog": 5,
    "Cheese Dog": 6,
}
bunOptions = {
    "White": 0,
    "Cheese": 1,
    "Gluten Free": 1,
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

# Payment info
paymentdict = {
    "name": "",
    "card": 0,
    "expiration": 0,
    "security": 0,
    "zip": 0,
}

#Delivery info
deliverydict ={
    "address": "",
    "address2": "",
    "city": "",
    "state": "",
    "zip": 0,
    "special": "",
}

#dictionary to hold order info
global orders
orders = {}

'''
PLANNING

WINDOW: order
    BUTTON: Build Your Dog
        WINDOW: dog options
            RADIO BUTTONS: dogs
            RADIO BUTTONS: buns
            CHECK BUTTONS: toppings
            ?ENTRY: qty (default 1)?
            ENTRY: name
            BUTTON: add to order
                validate there are only 3 toppings. if not, error window
    BUTTON: Delivery
        grayed out until there is at least 1 dog in the cart
        ENTRY: address
        ENTRY: address2
        ENTRY: city
        DROPDOWN (or entry?): state
        ENTRY: zip
            validate number only
        ENTRY: special instructions
    BUTTON: Payment
        ENTRY: name on card
        ENTRY: card number
        ?DATE FIELD?: expiration date
        ENTRY: security code
        ENTRY: zip
    BUTTON: place order
        validate that everything (except address2) has something in it
'''


# create hot dog ordering window
def dogWindowMake():
    dogWindow = Toplevel(window)
    dogWindow.title("Build Your Dog")

    #name for order
    nameLabel = tk.Label(dogWindow, text="Name:", font="bold")
    nameLabel.grid(row=0, column=0, sticky=E, padx=5, pady=5)
    orderNameEntry = tk.Entry(dogWindow)
    orderNameEntry.grid(row=0, column=1, padx=10, pady=20)

    #dog column positioning
    dogCol = 0
    dogLabel = tk.Label(dogWindow, text="Choose Your Dog:", font="bold")
    dogLabel.grid(row=1, column=dogCol, sticky=W, padx=15, pady=5)

    #make radio buttons for dog pick
    dogVar = tk.StringVar()
    radioButtons(dogWindow, dogOptions, dogCol, dogVar)

    bunCol = dogCol + 1
    bunLabel = tk.Label(dogWindow, text="Choose Your Bun:", font="bold")
    bunLabel.grid(row=1, column=bunCol, sticky=W, padx=15, pady=5)

    #make radio buttons for bun pick
    bunVar = tk.StringVar()
    radioButtons(dogWindow, bunOptions, bunCol, bunVar)

    #make check buttons for toppings
    toppingsCol = bunCol + 1
    toppingsLabel = tk.Label(dogWindow, text="Add Up to 3 Toppings:", font="bold")
    toppingsLabel.grid(row=1, column=toppingsCol, columnspan= 2, sticky=W, padx=15, pady=5)

    toppingsCheckboxes(dogWindow, toppingOptions, toppingsCol)

    #Add to Order button
    addButtonFunc = partial(addToOrder,
                            orderNameEntry,
                            dogVar,
                            bunVar,
                            dogWindow)
    addButton = tk.Button(dogWindow, text="Add to Order", command=addButtonFunc)
    addButton.grid(row=0, column=toppingsCol, sticky=W, padx=5, pady=5)

#create delivery info window
def deliveryWindowMake():
    deliveryWindow = Toplevel(window)
    deliveryWindow.title=("Enter Delivery Info")
    deliveryWindow.geometry=("500x300")

#create payment info window
def paymentWindowMake():
    paymentWindow = Toplevel(window)
    paymentWindow.title=("Enter Payment Info")
    paymentWindow.geometry=("500x300")

#DOG WINDOW STUFF
#make radio buttons for dogs and buns
def radioButtons(thisWindow, dict, col, var):
    i=2
    for key in dict.keys():
        if dict[key] > 0:
            buttonTxt = key+" - $"+str(dict[key])
        else:
            buttonTxt = key
        tk.Radiobutton(
            thisWindow,
            text=buttonTxt,
            value=key,
            variable=var).grid(row=i, column=col, sticky=W, padx=15, pady=5)
        i += 1

#make checkboxes for toppings
def toppingsCheckboxes(thisWindow, dict, col):
    global toppingsBoxes
    i=2
    toppingsBoxes = {}
    for key in dict.keys():
        #adds cost of items to label
        if dict[key] > 0:
            buttonTxt = key+" - $"+str(dict[key])
        else:
            buttonTxt = key

        #makes a second column to even them out
        if i == 6:
            i = 2
            col = col+1

        var = tk.BooleanVar()
        tk.Checkbutton(
            thisWindow,
            text=buttonTxt,
            variable=var).grid(row=i, column=col, sticky=W, padx=15, pady=5)
        toppingsBoxes[key] = var
        i += 1

#add dog to order
def addToOrder(orderNameEntry, dogVar, bunVar, dogWindow):
    global orders

    #get entries
    orderName = orderNameEntry.get()
    dogPick = dogVar.get() #NEED TO FIGURE OUT INPUT VALIDATION FOR THESE
    bunPick = bunVar.get()
    toppingsList = getToppings()

    #data validation
    if textCheck(orderName) and toppingsCheck(toppingsList):
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

    else:
        messagebox.showerror("Input Error", "Please make sure your inputs are valid.")

    deliverybutton.config(state=tk.ACTIVE)
    return orders

#get toppings that have checkboxes checked
def getToppings():
    global toppingsBoxes
    toppings = []
    for key in toppingsBoxes.keys():
        if toppingsBoxes[key].get():
            toppings.append(key)
    return toppings

#check that text is valid
def textCheck(txt):
    if txt.isalpha():
        return True
    else:
        return False

#check that number of toppings <= 3
def toppingsCheck(x):
    if len(x) <= 3:
        return True
    else:
        return False

def orderPlace():
    #and this is where the rest of the process would go
    print()


#build main page
dogbutton = tk.Button(window, text = "Build Your Dog", command = dogWindowMake)
dogbutton.grid(row=0, column=0, padx=20, pady=10)

deliverybutton = tk.Button(window, text = "Delivery Info", command = deliveryWindowMake)
deliverybutton.grid(row=1, column=0, padx=20, pady=10)
deliverybutton.config(state=tk.DISABLED)

paymentbutton = tk.Button(window, text = "Payment Info", command = paymentWindowMake)
paymentbutton.grid(row=2, column=0, padx=20, pady=10)
paymentbutton.config(state=tk.DISABLED)

placeorderbutton = tk.Button(window, text = "Place Order", command = orderPlace)
placeorderbutton.grid(row=3, column=0, padx=20, pady=10)
placeorderbutton.config(state=tk.DISABLED)















window.mainloop()
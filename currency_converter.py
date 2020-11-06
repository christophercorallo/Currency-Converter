#import necessary libraries tkinter and requests
import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk

#create converter class
class CurrencyConverter():
    def __init__(self, url):
        #Load url, convert to a json file, and store in data variable
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']
    
    #method that converts 1 currency to another and returns it
    def convert(self, from_currency, to_currency, amount):
        #convert to USD if it is another currency
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency]
        #round conversion to 3 decimal places
        amount = round(amount * self.currencies[to_currency], 4)
        return amount

#create a class for the UI
class CurrencyConverterUI(tk.Tk):

    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.title = 'Currency Converter'
        self.currency_converter =  converter

        self.geometry("500x200")

        self.intro_label = Label(self, text = 'Welcome to Currency Converter!', fg='blue', relief = tk.RAISED, borderwidth = 3)
        self.intro_label.config(font = ('Courier', 15, 'bold'))

        self.date_label = Label(self, text = f"1 Canadian Dollar = {self.currency_converter.convert('CAD', 'USD', 1)} USD \n Date: {self.currency_converter.data['date']}", relief = tk.GROOVE, borderwidth = 5)

        self.intro_label.place(x = 140, y = 40)
        self.date_label.place(x = 170, y = 80)

        #Entry box
        valid = (self.register(self.RestrictNumberOnly), '%d', '%P')
        self.amount_field = Entry(self, bd = 3, relief = tk.RIDGE, justify = tk.CENTER, validate = 'key', validatecommand = valid)
        self.converted_amount_field_label = Label(self, text = '', fg = 'black', bg = 'white', relief = tk.RIDGE, justify = tk.CENTER, width = 20, borderwidth = 3)

        #Dropdown menu to select currencies
        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set('CAD')
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set('USD')

        font = ('Courier', 12, 'bold')
        self.option_add('*TCombobox*Listbox.font', font)
        self.from_currency_dropdown = ttk.Combobox(self, textvariable = self.from_currency_variable, values = list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 12, justify = tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable = self.to_currency_variable, values = list(self.currency_converter.currencies.keys()), font = font, state = 'readonly', width = 12, justify = tk.CENTER)

        #placing
        self.from_currency_dropdown.place(x = 30, y = 120)
        self.amount_field.place(x = 30, y  = 150)
        self.to_currency_dropdown.place(x = 420, y = 120)
        self.converted_amount_field_label.place(x = 346, y = 150)

        #Convert button
        self.convert_button = Button(self, text = "Convert", fg = "black", command = self.perform)
        self.convert_button.config(font=('Courier', 10, 'bold'))
        self.convert_button.place(x = 255, y = 155)

    #Define function that takes user input, converts it into other currency, and displays it
    def perform(self):
        #get amount and currency values
        amount = float(self.amount_field.get())
        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()

        #convert into desired currency
        converted_amount = self.currency_converter.convert(from_curr, to_curr, amount)
        converted_amount = round(converted_amount, 2)

        #display converted value
        self.converted_amount_field_label.config(text = str(converted_amount))

    #restrict input of entry box
    def RestrictNumberOnly(self, action, string):
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return (string == "" or  (string.count('.') <= 1 and result is not None))

if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = CurrencyConverter(url)

    CurrencyConverterUI(converter)
    mainloop()
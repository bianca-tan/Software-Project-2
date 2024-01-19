import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from RecDbSqlite import RecDbSqlite

class RecGuiCtk(customtkinter.CTk):

    def __init__(self, dataBase=RecDbSqlite('AppDb.db')):
        super().__init__()
        self.db = dataBase

        self.title("Bianca's Recipe Catalogue")
        self.geometry('1300x700') 
        self.config(bg='#FFF9EB')
        self.resizable(False, False) 

        self.font1 = ('Times New Roman', 20, 'bold') 
        self.font2 = ('Times New Roman', 12, 'bold')  
        self.font3 = ('Times New Roman', 50, 'bold', 'italic')

        ### Data Entry Form ###

        # 'Title' Label
        self.title_label = self.titleCtkLabel("Bianca's Recipe Catalogue") #
        self.title_label.place(x=380, y=30) 

        # 'Number' Label and Entry Widgets
        self.number_label = self.newCtkLabel('Recipe Number')
        self.number_label.place(x=20, y=140)
        self.number_entry = self.newCtkEntry()
        self.number_entry.place(x=180, y=140)

        #Date Attempted Label and Entry Widhet

        # 'Name' Label and Entry Widgets
        self.name_label = self.newCtkLabel('Recipe Name')
        self.name_label.place(x=20, y=200)
        self.name_entry = self.newCtkEntry()
        self.name_entry.place(x=180, y=200)

        # 'Time' Label and Combo Box Widgets
        self.time_label = self.newCtkLabel('Time Spent')
        self.time_label.place(x=20, y=260)
        self.time_cboxVar = StringVar()
        self.time_cboxOptions = ['< 1 Hour', '1 Hour', '2 Hours', '3 Hours', '4 Hours', '5 Hours', '> 5 Hours']
        self.time_cbox = self.newCtkComboBox(options=self.time_cboxOptions, 
                                    entryVariable=self.time_cboxVar)
        self.time_cbox.place(x=180, y=260)

        # 'Rating' Label and Combo Box Widgets
        self.rating_label = self.newCtkLabel('Recipe Rating')
        self.rating_label.place(x=20, y=320)
        self.rating_cboxVar = StringVar()
        self.rating_cboxOptions = ['N/A', '0/5', '1/5', '2/5', '3/5', '4/5', '5/5']
        self.rating_cbox = self.newCtkComboBox(options=self.rating_cboxOptions, 
                                    entryVariable=self.rating_cboxVar)
        self.rating_cbox.place(x=180, y=320)

        # 'Status' Label and Combo Box Widgets
        self.status_label = self.newCtkLabel('Recipe Status')
        self.status_label.place(x=20, y=380)
        self.status_cboxVar = StringVar()
        self.status_cboxOptions = ['Attempted', 'Not Attempted', 'Crowd Favorite', 'Personal Favorite', 'Did Not Enjoy']
        self.status_cbox = self.newCtkComboBox(options=self.status_cboxOptions, 
                                    entryVariable=self.status_cboxVar)
        self.status_cbox.place(x=180, y=380) 

        ### ADD / DELETE / UPDATE / REFRESH BUTTONS ###

        self.add_button = self.newCtkButton(text='Add Recipe',
                                onClickHandler=self.add_entry,
                                fgColor='#05A312', 
                                hoverColor='#00850B', 
                                borderColor='#05A312') 
        self.add_button.place(x=60,y=500)

        self.refresh_button = self.newCtkButton(text='Refresh Recipe Input',
                                onClickHandler=lambda:self.clear_form(True))
        self.refresh_button.place(x=60,y=620)

        self.update_button = self.newCtkButton(text='Update Recipe',
                                    onClickHandler=self.update_entry)
        self.update_button.place(x=60,y=580)

        self.delete_button = self.newCtkButton(text='Delete Recipe',
                                    onClickHandler=self.delete_entry,
                                    fgColor='#E40404', 
                                    hoverColor='#AE0000', 
                                    borderColor='#E40404') 
        self.delete_button.place(x=60,y=540)

        self.exportcsv_button = self.newCtkButton(text='Export Data to CSV',
                                    onClickHandler=self.export_to_csv)
        self.exportcsv_button.place(x=370,y=500)

        self.exportjson_button = self.newCtkButton(text='Export Data to JSON',
                                    onClickHandler=self.export_to_json)
        self.exportjson_button.place(x=670,y=500)

        self.import_button = self.newCtkButton(text='Import Data from CSV',
                                    onClickHandler=self.import_from_csv)
        self.import_button.place(x=980,y=500)

        # Tree View for Database Entries
        self.style = ttk.Style(self)
        self.style.theme_use('clam') 
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#C7CBA8', 
                        background='#FCF2AF', 
                        fieldlbackground='#313837') 

        self.style.map('Treeview', background=[('selected', '#1A8F2D')]) #what is this

    #change the width to how long each word is according to their methods
        self.tree = ttk.Treeview(self, height=15)
        self.tree['columns'] = ('Recipe Number', 'Recipe Name', 'Time Spent', 'Rating', 'Status')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Recipe Number', anchor=tk.CENTER, width=10)
        self.tree.column('Recipe Name', anchor=tk.CENTER, width=150)
        self.tree.column('Time Spent', anchor=tk.CENTER, width=150)
        self.tree.column('Rating', anchor=tk.CENTER, width=10)
        self.tree.column('Status', anchor=tk.CENTER, width=150)

        self.tree.heading('Recipe Number', text='Recipe Number')
        self.tree.heading('Recipe Name', text='Recipe Name')
        self.tree.heading('Time Spent', text='Time Spent')
        self.tree.heading('Rating', text='Rating')
        self.tree.heading('Status', text='Status')

        self.tree.place(x=700, y=190, width=1000, height=380)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    # new Label Widget 
        
    def titleCtkLabel(self, text = 'Title Label'):
        widget_Font=self.font3
        widget_TextColor='#BB7A72'
        widget_BgColor='#FFF9EB'

        widget = customtkinter.CTkLabel(self, 
                                    text=text,
                                    font=widget_Font, 
                                    text_color=widget_TextColor,
                                    bg_color=widget_BgColor)
        return widget

    def newCtkLabel(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#BB7A72'
        widget_BgColor='#FFF9EB'

        widget = customtkinter.CTkLabel(self, 
                                    text=text,
                                    font=widget_Font, 
                                    text_color=widget_TextColor,
                                    bg_color=widget_BgColor)
        return widget

    # new Entry Widget
    def newCtkEntry(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#BB7A72'
        widget_FgColor='#FFF'
        widget_BorderColor='#C88B90'
        widget_BorderWidth=2
        widget_Width=250

        widget = customtkinter.CTkEntry(self,
                                    font=widget_Font,
                                    text_color=widget_TextColor,
                                    fg_color=widget_FgColor,
                                    border_color=widget_BorderColor,
                                    border_width=widget_BorderWidth,
                                    width=widget_Width)
        return widget

    # new Combo Box Widget
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#BB7A72'
        widget_FgColor='#FFF'
        widget_DropdownHoverColor='#C88B90'
        widget_ButtonColor='#C88B90'
        widget_ButtonHoverColor='#C88B90'
        widget_BorderColor='#C88B90'
        widget_BorderWidth=2
        widget_Width=250
        widget_Options=options

        widget = customtkinter.CTkComboBox(self,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        border_color=widget_BorderColor,
                                        width=widget_Width,
                                        variable=entryVariable,
                                        values=options,
                                        state='readonly')
        
        # set default value to 1st option
        widget.set(options[0])

        return widget

    # new Button Widget 
    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#FFF9EB', hoverColor='#C88B90' , bgColor='#FFF9EB', borderColor='#C88B90'): 
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=15
        widget_Width=260
        widget_Function=onClickHandler

        widget = customtkinter.CTkButton(self,
                                        text=text,
                                        command=widget_Function,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        hover_color=widget_HoverColor,
                                        bg_color=widget_BackgroundColor,
                                        border_color=widget_BorderColor,
                                        border_width=widget_BorderWidth,
                                        cursor=widget_Cursor,
                                        corner_radius=widget_CornerRadius,
                                        width=widget_Width)
       
        return widget

    # Handles
    def add_to_treeview(self):
        recipes = self.db.fetch_recipes()
        self.tree.delete(*self.tree.get_children())
        for recipe in recipes:
            print(recipe)
            self.tree.insert('', END, values=recipe)

    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.number_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.time_cboxVar.set('< 1 Hour')
        self.rating_cboxVar.set('N/A')
        self.status_cboxVar.set('Attempted')

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.number_entry.insert(0, row[0])
            self.name_entry.insert(0, row[1])
            self.time_cboxVar.set(row[2])
            self.rating_cboxVar.set(row[3])
            self.status_cboxVar.set(row[4])
        else:
            pass

    def add_entry(self):
        number=self.number_entry.get()
        name=self.name_entry.get()
        time=self.time_cboxVar.get()
        rating=self.rating_cboxVar.get()
        status=self.status_cboxVar.get()

        if not (number and name and time and rating and status):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.number_exists(id):
            messagebox.showerror('Error', 'Number already exists')
        else:
            self.db.insert_recipe(number, name, time, rating, status)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')

    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a recipe to delete')
        else:
            number = self.number_entry.get()
            self.db.delete_recipe(number)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Selected Recipe has been deleted')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a Recipe to update')
        else:
            number=self.number_entry.get()
            name=self.name_entry.get()
            time=self.time_cboxVar.get()
            rating=self.rating_cboxVar.get()
            status=self.status_cboxVar.get()
            self.db.update_recipe(name, time, rating, status, number)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Selected Recipe has been updated')

    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success', f'Data exported to {self.db.RecipeCSV}')

    def export_to_json(self):
        self.db.export_json()
        messagebox.showinfo('Success', f'Data exported to {self.db.RecipeJSON}')

    def import_from_csv(self):
        self.db.import_csv()
        self.add_to_treeview()
        messagebox.showinfo('Success', f'Data has been imported from chosen CSV file.')

    






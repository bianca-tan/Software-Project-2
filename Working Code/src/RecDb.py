from RecDbEntry import RecDbEntry
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import tkinter
import json

class RecDb:
    def __init__(self, init=False, RecipeCSV='Recipe.csv', RecipeJSON='Recipe.json'):        
        self.RecipeCSV = RecipeCSV
        self.RecipeJSON = RecipeJSON
        print('TODO: __init__')
        self.entries = []

    def fetch_recipes(self):
        print('TODO: fetch_recipes')
        return [(entry.number, entry.name, entry.time, entry.rating, entry.status) for entry in self.entries]

    def insert_recipe(self, number, name, time, rating, status):
        newEntry = RecDbEntry(number=number, name=name, time=time, rating=rating, status=status)
        self.entries.append(newEntry)
        print('TODO: insert_recipe')
        print('You have successfully added a new Recipe!')

    def delete_recipe(self, number):
        for entry in self.entries:
            if entry.number == number:
                self.entries.remove(entry)
                print('TODO: delete_recipe')
                print('You have successfully deleted your selected Recipe!')

    def update_recipe(self, new_name, new_time, new_rating, new_status, number):
        entry_found = False
        for entry in self.entries:
            if entry.number == number:
                entry.name = new_name
                entry.time = new_time
                entry.rating = new_rating
                entry.status = new_status
                entry_found = True
                print('TODO: update_recipe')
                print('You have successfully updated your selected Recipe!')
        
    def import_csv(self):
        timeoptions = ['< 1 Hour', '1 Hour', '2 Hours', '3 Hours', '4 Hours', '5 Hours', '> 5 Hours']
        rankoptions = ['N/A', '0/5', '1/5', '2/5', '3/5', '4/5', '5/5']
        ratingoptions = ['Attempted', 'Not Attempted', 'Crowd Favorite', 'Personal Favorite', 'Did Not Enjoy']
        csvfile = tkinter.filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")], title="Choose a csv file to import as data.")
        with open(csvfile, "r") as f:
            readfile = f.readlines()
            for line in readfile:
                info = [value.strip() for value in line.strip().split(",")]
                if len(info) != 5:
                    continue
                if info[2] not in timeoptions or info[3] not in rankoptions or info[4] not in ratingoptions:
                    continue
                else:
                    self.insert_recipe(info[0], info[1], info[2], info[3], info[4])
                    
    def export_csv(self): 
        with open(self.RecipeCSV, mode='w') as file:
            for entry in self.entries:
                file.write(f"{entry.number},{entry.name},{entry.time},{entry.rating},{entry.status}\n")
        print('TODO: export_csv')
        print('You have successfully exported to CSV file!')

    def export_json(self): 
        recipeentries = {}
        x = 0
        with open(self.RecipeJSON, 'w') as file:
            for entry in self.entries:
                entry = [entry.number, entry.name, entry.time, entry.rating, entry.status]
                x += 1
                recipeentries[f"entry" + str(x)] = entry
            jsonentries = json.dumps(recipeentries)
            file.write(jsonentries)

    def number_exists(self, number):
        return any(entry.number == number for entry in self.entries)

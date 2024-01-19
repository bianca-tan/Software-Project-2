'''
This is the interface to an SQLite Database
'''

import sqlite3
import tkinter
import json
from tkinter import filedialog

class RecDbSqlite:
    def __init__(self, Recipe='Recipes.db'):
        super().__init__()
        self.Recipe = Recipe
        self.csvFile = self.Recipe.replace('.db', '.csv')
        self.conn = sqlite3.connect(self.Recipe)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Employees (
                id TEXT PRIMARY KEY,
                name TEXT,
                role TEXT,
                gender TEXT,
                status TEXT)''')
        self.conn.commit()
        self.conn.close()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.Recipe)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()        

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Employees (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    role TEXT,
                    gender TEXT,
                    status TEXT)''')
        self.commit_close()

    def fetch_recipes(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM Recipes')
        recipes =self.cursor.fetchall()
        self.conn.close()
        return recipes

    def insert_recipe(self, number, name, time, rating, status):
        self.connect_cursor()
        self.cursor.execute('INSERT INTO Recipes (number, name, time, rating, status) VALUES (?, ?, ?, ?, ?)',
                    (number, name, time, rating, status))
        self.commit_close()

    def delete_recipe(self, number):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM Recipes WHERE number = ?', (number,))
        self.commit_close()

    def update_recipe(self, new_name, new_time, new_rating, new_status, number):
        self.connect_cursor()
        self.cursor.execute('UPDATE Recipes SET name = ?, time = ?, rating = ?, status = ? WHERE number = ?',
                    (new_name, new_time, new_rating, new_status, number))
        self.commit_close()

    def number_exists(self, number):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM Recipes WHERE number = ?', (number,))
        result =self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0
    
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
        with open(self.csvFile, "w") as filehandle:
            RecipeEntries = self.fetch_recipes()
            for entry in RecipeEntries:
                print(entry)
                filehandle.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]},{entry[4]}\n")

    def export_json(self): 
        recipeentries = {}
        x = 0
        with open(self.RecipeJSON, mode='w') as file:
            for entry in self.entries:
                entry = [entry.number, entry.name, entry.time, entry.rating, entry.status]
                x += 1
            recipeentries[f"entry" + str(x)] = entry
        jsonentries = json.dumps(recipeentries)
        file.write(jsonentries)
        print('TODO: export_json')
        print('You have successfully exported to JSON file!')

def test_Recipe():
    iRecipe = RecDbSqlite(Recipe='RecDbSql.db')

    for entry in range(30):
        iRecipe.insert_recipe(entry, f'Recipe Name{entry}', f'< 1 Hour {entry}', 'N/A', 'Attempted')
        assert iRecipe.number_exists(entry)

    all_entries = iRecipe.fetch_()
    assert len(all_entries) == 30

    for entry in range(10, 20):
        iRecipe.update_recipe(f'Recipe Name{entry}', f'< 1 Hour {entry}', 'N/A', 'Attempted', entry)
        assert iRecipe.number_exists(entry)

    all_entries = iRecipe.fetch_recipes()
    assert len(all_entries) == 30

    for entry in range(10):
        iRecipe.delete_recipe(entry)
        assert not iRecipe.number_exists(entry) 

    all_entries = iRecipe.fetch_recipes()
    assert len(all_entries) == 20
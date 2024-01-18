from RecDb import RecDb
from RecGuiCtk import RecGuiCtk

def main():
    db = RecDb(init=False, RecipeCSV='RecDb.csv', RecipeJSON='RecDb.json')
    app = RecGuiCtk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()
from RecDb import RecDb
from RecGuiCtk import RecGuiCtk

def main():
    db = RecDb(init=False, dbNameCSV='RecDb.csv', dbNameJSON='RecDb.json')
    app = RecGuiCtk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()
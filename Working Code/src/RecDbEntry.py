class RecDbEntry:
    def __init__(self,
                 number=1,
                 name='Recipe Name',
                 time='< 1 Hour',
                 rating='N/A',
                 status='Attempted'):
        self.number = number
        self.name = name
        self.time = time
        self.rating = rating
        self.status = status

import sqlite3

class Database:
    def __init__(self, semester: str):
        try:
            self.connection = sqlite3.connect(f'Data_{semester}.sqlite')
        except(Exception, sqlite3.Error) as error:
            print(error)
        finally:
            try:
                self.cursor = self.connection.cursor()
                self.cursor.executescript('''
                    CREATE TABLE Course (
                    "ID_Course" TEXT,
                    "Name"	TEXT NOT NULL,
                    PRIMARY KEY("ID_Course")
                    );

                    CREATE TABLE Calendar (
                    "ID"	TEXT,
                    "Date"	TEXT NOT NULL,
                    "Time_Start" TEXT NOT NULL,
                    "Time_End" TEXT NOT NULL,
                    "ID_Course"	TEXT NOT NULL,
                    "ID_Event" TEXT,
                    PRIMARY KEY("ID")
                    FOREIGN KEY("ID_Course") REFERENCES "Course"("ID_Course")
                    )
                ''')
                self.connection.commit()
            except (Exception, sqlite3.Error) as error:
                print(error)



    def addValue_Course(self, Course_ID: str, Name: str):
        try:
            self.cursor.execute('INSERT INTO Course(ID_Course,Name)VALUES(?,?)', (Course_ID, Name,))
            self.connection.commit()
        except(Exception, sqlite3.Error) as error:
            print(error)

    def addValue_Calendar(self,Date: str, Time: str, Course_ID: str):
        try:
            # Slot_Dict = {'1': '7:00-8:30', '2': '8:45-10:15', '3': '12:30-14:45', '4': '15:00-17:30', '7': '17:45-19h15'}

            Dates = Date.split("/")
            Date = '-'.join(i for i in Dates[::-1])
            ID = str(Course_ID.lower() + ''.join(i for i in Dates[::-1]) + Time)
            Time_Start = Time.split('-')[0]
            Time_End = Time.split('-')[1]

            self.cursor.execute("SELECT Calendar.ID FROM Calendar")
            ls_calendar_id =  [id[0] for id in self.cursor.fetchall()]
            if ID not in ls_calendar_id:
                self.cursor.execute("INSERT INTO Calendar(ID,Date,Time_Start,Time_End,ID_Course)VALUES(?,?,?,?,?)", (ID, Date, Time_Start, Time_End, Course_ID,))
                self.connection.commit()
                print(f'\nInsert {ID} - calendar successfull')
            elif ID in ls_calendar_id:
                print(f'\nthis {ID} have already, prepare updating, ...')
                self.cursor.execute("UPDATE Calendar SET Date=?, Time_Start=?, Time_End=? WHERE ID=?", (Date, Time_Start, Time_End, ID,))
                self.connection.commit()
                print(f'Update {ID} - calendar successfull')

        except(Exception, sqlite3.Error) as error:
            print(error)

    def addID_even_Calendar(self, ID: str, ID_event: str):
        try:
            self.cursor.execute("UPDATE Calendar SET ID_event = ? WHERE ID = ?", (str(ID_event), str(ID),))
            self.connection.commit()
            print(f'Add ID of event to database calendar')
        except(Exception, sqlite3.Error) as error:
            print(error)

    def retrive_Calendar(self):
        try:
            self.cursor.execute("""SELECT Course.Name, Calendar.Date, Calendar.Time_Start, Calendar.Time_End, Calendar.ID, Calendar.ID_Event
                 FROM Calendar JOIN Course on Course.ID_Course = Calendar.ID_Course""")
            result = self.cursor.fetchall()
            return result
        except (Exception, sqlite3.Error) as error:
            print(error)
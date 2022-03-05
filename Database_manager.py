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
                    "ID"	INTEGER,
                    "Date"	TEXT NOT NULL,
                    "Time_Start" TEXT NOT NULL,
                    "Time_End" TEXT NOT NULL,
                    "ID_Course"	TEXT NOT NULL,
                    PRIMARY KEY("ID" AUTOINCREMENT)
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

    def addValue_Calendar(self,Date: str, Slot: str, Course_ID: int):
        try:
            #Month_Dict = {'01': 'January', '02': 'Ferbuary', '03': 'March', '04': 'April', '05': 'May', '06': 'June',
            #             '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November',
            #              '12': 'December'}
            Slot_Dict = {'1': '7:00-8:30', '2': '8:45-10:15', '3': '10:30-12:00', '4': '12:30-14:00',
                         '5': '14:15-15:30','6': '15:45-17:00', '7': '17:15-18:45pm', '8': '18h45-20:00'}

            Dates = Date.split("/")
            Date = '-'.join(i for i in Dates[::-1])
            Time = Slot_Dict[Slot].split('-')
            Time_Start = Time[0]
            Time_End = Time[1]

            self.cursor.execute("INSERT INTO Calendar(Date,Time_Start,Time_End,ID_Course)VALUES(?,?,?,?)", (Date, Time_Start, Time_End, Course_ID,))
            self.connection.commit()

        except(Exception, sqlite3.Error) as error:
            print(error)

    def retrive_Calendar(self):
        try:
            self.cursor.execute("SELECT Course.Name, Calendar.Date, Calendar.Time_Start, Calendar.Time_End FROM Calendar JOIN Course on Course.ID_Course = Calendar.ID_Course")
            result = self.cursor.fetchall()
            return result
        except (Exception, sqlite3.Error) as error:
            print(error)
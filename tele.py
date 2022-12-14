from datetime import datetime

import connectserver
import mysql.connector

def getSessionID(db:mysql.connector.MySQLConnection):
    cursor = db.cursor()

    while True:
        date = input("session date until (format YYYY-MM-DD HH:MM:SS)\n(leave blank to use current time): ")
        queryNum = input("Number of session: ")
        try:
            if date == "":
                date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            
            timestamp = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            queryNum = int(queryNum)
            break

        except ValueError as e:
            if str(e).find("does not match format '%Y-%m-%d %H:%M:%S'") != -1:
                input("date format error, press enter to retry......\n")
            elif str(e).find("") != -1:
                test = input("Press enter to retry, Enter \"q\" to quit......")
                if test == 'q' or test == "q":
                    return -1
                print()
            
    
    f = open("bin/get_sessionID.sql", "r")
    query = f.read().replace("DATETIME", timestamp.strftime("%Y-%m-%d %H:%M:%S")) \
                    .replace("queryNUM", str(queryNum))
    print(f'Fetching session data until {timestamp.strftime("%Y-%m-%d %H:%M:%S")}, number: {queryNum}.')
    cursor.execute(query)
    result = cursor.fetchall()

    print(f'Session data from previous query')
    print(f'{"Session ID":<15}{"Session time":25}{"Tele Ver.":<15}{"Game Ver.":<10}')
    for i in range(len(result)-1, -1, -1):
        session = result[i]
        print(f'{session[0]:<15}{session[1].strftime("%Y-%m-%d %H:%M:%S"):<25}{session[2]:<15}{session[3]}.{session[4]}')







def main():
    db = connectserver.connectserver("server.json", "db")

    while True:
        print("Welcome to AFR telemetry data center")
        print()
        print("1. recent session id")
        print("2. qualiying lapdata")
        print("3. race lapdata")
        print("4. telemetry data")
        print("5. final classification")
        print("6. delete data")
        print("7. fetch all data (by event)")
        print("0. exit")
        print()
        choice = input("your choice: ")

        if choice == "1":
            getSessionID(db)
            input("press eneter back to main menu......")
            print()
        
        elif choice == "2":
            
            input("press eneter back to main menu......")
            print()

        elif choice == "3":
            
            input("press eneter back to main menu......")
            print()

        elif choice == "4":
            
            input("press eneter back to main menu......")
            print()

        elif choice == "5":
            
            input("press eneter back to main menu......")
            print()
        
        elif choice == "6":

            input("press eneter back to main menu......")
            print()

        elif choice == "0":
            input("press enter to exit......")
            break

        else:
            input("please enter a correct option......")
            print()



if __name__ == "__main__":
    main()
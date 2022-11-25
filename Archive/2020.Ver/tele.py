from datetime import datetime

import connectserver
import qualiLapdata
import raceLapdata
import telemetry
import finalclassification
import delData

db = connectserver.connectserver()
cursor = db.cursor()


def getSessionid():
    query = f"SELECT fake_id, curTime, packetFormat, gameMajorVersion, gameMinorVersion \
              FROM session_id ORDER BY fake_id DESC LIMIT 30;"
    cursor.execute(query)
    result = cursor.fetchall()

    print(f'{"sessionID":<15}|{"session time":<30}|{"packet format":<20}|{"game version"}')
    for session in result:
        print(f'{session[0]:<15}|{session[1].strftime("%Y-%m-%d %H:%M:%S"):<30}|{session[2]:<20}|{session[3]}.{session[4]}')


def menu():
    
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
            getSessionid()
            input("press eneter back to main menu......")
            print()
        
        elif choice == "2":
            qualiLapdata.getQualiLapdata()
            input("press eneter back to main menu......")
            print()

        elif choice == "3":
            raceLapdata.getRaceLapdata()
            input("press eneter back to main menu......")
            print()

        elif choice == "4":
            telemetry.getTelemetryData()
            input("press eneter back to main menu......")
            print()

        elif choice == "5":
            finalclassification.getFinalClassification()
            input("press eneter back to main menu......")
            print()
        
        elif choice == "6":
            delData.deleteSession()

        elif choice == "0":
            input("press enter to exit......")
            break

        else:
            input("please enter a correct option......")
            print()


if __name__ == "__main__":
    menu()
import os
import csv
import xlsxwriter

import connectserver

def getFinalClassification():
    db = connectserver.connectserver()
    cursor = db.cursor()

    while True:
        #"""
        sessionid1 = input("please enter session id 1: ")
        if sessionid1 == "q" or sessionid1 == "Q":
            break
        sessionid2 = input("please enter session id 2: ")
        if sessionid2 == "q" or sessionid2 == "Q":
            break
        elif sessionid2 == "":
            sessionid2 = sessionid1
        #"""
        #sessionid1 = 956
        #sessionid2 = 956

        try:
            sessionid1 = int(sessionid1)
            sessionid2 = int(sessionid2)

            # query final classification of the session
            query = f'SELECT sessionUID, driverName, teamName, position, numLaps, \
                            gridPosition, numPitStops, resultStatusStr, \
                            bestLapTimeStr, totalRaceTimeStr, penaltiesTime, tyreStintsVisual \
                    FROM FinalClassification \
                    WHERE sessionUID >= {sessionid1} AND sessionUID <= {sessionid2} \
                    ORDER BY position ASC;'
            cursor.execute(query)
            result = cursor.fetchall()

            os.system('mkdir "final classification"')
            # writing final classification data to csv file
            filepath = f'final classification/FinalClassification_{sessionid2}.csv'
            with open(filepath, "w", newline="") as classification:
                header = ["name", "team", "position", "Laps", "grid", "pits", "status",
                          "bestLapTime", "totalTime", "penalties", "tyreStints"]
                writer = csv.DictWriter(classification, header)

                writer.writeheader()

                for driver in result:
                    driverdict = {
                        #"sessionID": driver[0],
                        "name": driver[1],
                        "team": driver[2],
                        "position": driver[3],
                        "Laps": driver[4],
                        "grid": driver[5],
                        "pits": driver[6],
                        "status": driver[7],
                        "bestLapTime": driver[8],
                        "totalTime": driver[9],
                        "penalties": driver[10],
                        "tyreStints": driver[11]
                    }
                    writer.writerow(driverdict)

            # writing final classification data to excel file
            filepath = f'final classification/FinalClassification_{sessionid2}.xlsx'
            workbook = xlsxwriter.Workbook(filepath)
            classification = workbook.add_worksheet(f'classification {sessionid2}')
            default = workbook.add_format({"font_size":11})
            default.set_font_name("Dengxian")
            default.set_align("vcenter")
            default.set_text_wrap()

            for i in range(0,25):
                classification.set_row(i, 15)
            classification.set_column(0,0, 15)
            classification.set_column(1,1, 17)
            classification.set_column(2,2, 8)
            classification.set_column(3,3, 5)
            classification.set_column(4,4, 5)
            classification.set_column(5,5, 4)
            classification.set_column(6,6, 13)
            classification.set_column(7,7, 12)
            classification.set_column(8,8, 12)
            classification.set_column(9,9, 9)
            classification.set_column(10,10, 8)

            # writing the header
            for i in range(0, len(header)):
                classification.write(0, i, header[i], default)
            
            row = 1
            for driver in result:
                for i in range(1, len(driver)):
                    classification.write(row, i-1, driver[i], default)
                
                row += 1

            workbook.close()

            print(f'Final Classification data of session {sessionid2} fetched and saved!')





            # querying race director of the session
            query = f'SELECT sessionUID, penaltyID, code, driverName, otherDriverName, penaltyDescription, \
                            infringementDescription, timeGained, LapNum, placesGained \
                    FROM penalty_update \
                    WHERE sessionUID >= {sessionid1} AND sessionUID <= {sessionid2} \
                    ORDER BY LapNum ASC, penaltyID ASC;'
            cursor.execute(query)
            result = cursor.fetchall()


            # writing final classification data to csv file
            filepath = f'final classification/RaceDirector_{sessionid2}.csv'
            with open(filepath, "w", newline="") as racedirectoer:
                header = ["penaltyID", "code", "LapNum", "name", "involved driver",
                          "description", "detailed description", "time penalty", "placesGained"]
                writer = csv.DictWriter(racedirectoer, header)

                for record in result:
                    record_dict = {
                        #"sessionID": record[0],
                        "penaltyID": record[1],
                        "code": record[2],
                        "LapNum": record[8],
                        "name": record[3],
                        "involved driver": record[4],
                        "description": record[5],
                        "detailed description": record[6],
                        "time penalty": record[7],
                        "placesGained": record[9]
                    }
                    writer.writerow(record_dict)

            
            # writing race director data to excel file
            filepath = f'final classification/RaceDirector_{sessionid2}.xlsx'
            workbook = xlsxwriter.Workbook(filepath)
            rd = workbook.add_worksheet(f'RaceDirector {sessionid2}')
            default = workbook.add_format({"font_size":11})
            default.set_font_name("Dengxian")
            default.set_align("vcenter")
            default.set_text_wrap()

            for i in range(0, len(result)+2):
                rd.set_row(i, 15)
            rd.set_column(0,0, 9)
            rd.set_column(1,1, 9)
            rd.set_column(2,2, 8)
            rd.set_column(3,3, 30)
            rd.set_column(4,4, 30)
            rd.set_column(5,5, 17)
            rd.set_column(6,6, 40)
            rd.set_column(7,7, 10)
            rd.set_column(8,8, 12)

            # writing the header
            for i in range(0, len(header)):
                rd.write(0, i ,header[i], default)

            row = 1
            for record in result:
                rd.write(row, 0, record[1], default)
                rd.write(row, 1, record[2], default)
                rd.write(row, 2, record[8], default)
                rd.write(row, 3, record[3], default)
                rd.write(row, 4, record[4], default)
                rd.write(row, 5, record[5], default)
                rd.write(row, 6, record[6], default)
                rd.write(row, 7, record[7], default)
                rd.write(row, 8, record[9], default)

                row += 1

            workbook.close()

            print(f'Race Director data of session {sessionid2} fetched and saved!')


            break

        except ValueError:
            input("session id error, please re-enter session id...")
            print()



if __name__ == "__main__":
    getFinalClassification()
import os
import csv
import xlsxwriter

import connectserver

def getTelemetryData():
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

            # find all the driver in the session
            query = f'SELECT DISTINCT(name) FROM LapOverview \
                    WHERE sessionUID >= {sessionid1} AND sessionUID <= {sessionid2};'
            print(f'fetching driverlist from session {sessionid2}')
            cursor.execute(query)
            result = cursor.fetchall()
            print(f'driver list from session {sessionid2} acquired......\n')

            driverlist = []
            for driver in result:
                driverlist.append(driver[0])
            
            """
            # pre-create an excel file
            filepath = f'telemetry data/telemetry.xlsx'
            workbook = xlsxwriter.Workbook(filepath)
            default = workbook.add_format({"font_size":11})
            default.set_font_name("Dengxian")
            default.set_align("vcenter")
            default.set_text_wrap()
            """

            # query telemetry data for every driver
            for driver in driverlist:
                query = f'SELECT sessionUID, frameIdentifier, carIndex, curTime, name, \
                                carPosition, currentLapNum, currentLapTime, LapDistance, sector, \
                                speed, steer, throttle, brake, gear, engineRPM, currentLapInvalid, \
                                tractionControl, antiLockBrakes, aiControlled, \
                                worldPositionX, worldPositionY, worldPositionZ, \
                                gForceLateral, gForceLongitudinal, gForceVertical \
                        FROM LapOverview \
                        WHERE sessionUID >= {sessionid1} AND sessionUID <= {sessionid2} \
                            AND name = "{driver}" \
                        ORDER BY sessionUID ASC, frameIdentifier ASC;'
                print(f'fetching telemetry data of {driver}......')
                cursor.execute(query)
                result = cursor.fetchall()
                print("telemetry data fetched, preparing writing to csv file......")

                os.system(f'mkdir "telemetry data ({sessionid2})"')
                # writing telemetry data to csv file
                filepath = f'telemetry data ({sessionid2})/{driver.replace(":","")}_telemetry.csv'
                with open(filepath, "w", newline="") as teledata:
                    header = ["frame", "curTime", "name", "Position", "curLapNum", "curLapTime", 
                              "LapDistance", "sector", "speed", "steer", "throttle", "brake", "gear",
                              "engineRPM", "LapInvalid", "TC", "ABS", "AI",
                              "worldPositionX", "worldPositionY", "worldPositionZ",
                              "gForceLateral", "gForceLongitudinal", "gForceVertical"]
                    writer = csv.DictWriter(teledata, header)

                    writer.writeheader()
                    for lap in result:
                        lapdict = {
                            #"sessionID": lap[0],
                            "frame": lap[1],
                            #"carInx": lap[2],
                            "curTime": lap[3],
                            "name": lap[4],
                            "Position": lap[5],
                            "curLapNum": lap[6],
                            "curLapTime": lap[7],
                            "LapDistance": lap[8],
                            "sector": lap[9],
                            "speed": lap[10],
                            "steer": lap[11],
                            "throttle": lap[12],
                            "brake": lap[13],
                            "gear": lap[14],
                            "engineRPM": lap[15],
                            "LapInvalid": lap[16],
                            "TC": lap[17],
                            "ABS": lap[18],
                            "AI": lap[19],
                            "worldPositionX": lap[20],
                            "worldPositionY": lap[21],
                            "worldPositionZ": lap[22],
                            "gForceLateral": lap[23],
                            "gForceLongitudinal": lap[24],
                            "gForceVertical": lap[25]
                        }
                        writer.writerow(lapdict)

                """
                # writing telemetry data to excel file
                telemetry = workbook.add_worksheet(f'{driver.replace(":","")}')
                for i in range(0, len(result)):
                    telemetry.set_row(i, 15)
                telemetry.set_column(0,0, 6)
                telemetry.set_column(1,1, 16)
                telemetry.set_column(2,2, 20)
                telemetry.set_column(3,3, 8)
                telemetry.set_column(4,5, 10)
                telemetry.set_column(6,6, 6)
                telemetry.set_column(7,7, 10)
                telemetry.set_column(8,9, 9)
                telemetry.set_column(10,10, 5)
                telemetry.set_column(11,11, 10)
                telemetry.set_column(12,12, 9)
                telemetry.set_column(13,13, 3)
                telemetry.set_column(14,14, 4)
                telemetry.set_column(15,15, 3)

                # writing the header
                for i in range(0, len(header)):
                    telemetry.write(0, i, header[i], default)

                row = 1
                for lap in result:
                    telemetry.write(row, 0, lap[1], default)
                    telemetry.write(row, 1, lap[3], default)
                    telemetry.write(row, 2, lap[4], default)
                    telemetry.write(row, 3, lap[5], default)
                    telemetry.write(row, 4, lap[6], default)
                    telemetry.write(row, 5, lap[7], default)
                    telemetry.write(row, 6, lap[8], default)
                    telemetry.write(row, 7, lap[9], default)
                    telemetry.write(row, 8, lap[10], default)
                    telemetry.write(row, 9, lap[11], default)
                    telemetry.write(row, 10, lap[12], default)
                    telemetry.write(row, 11, lap[13], default)
                    telemetry.write(row, 12, lap[14], default)
                    telemetry.write(row, 13, lap[15], default)
                    telemetry.write(row, 14, lap[16], default)
                    telemetry.write(row, 15, lap[17], default)
                    row += 1
                """

                print(f'telemetry data of {driver} saved complete!\n')

            print(f'All driver telemetry data from session {sessionid2} fetched and saved!')
            break

        except ValueError:
            input("session id error, please re-enter session id...")
            print()

if __name__ == "__main__":
    getTelemetryData()
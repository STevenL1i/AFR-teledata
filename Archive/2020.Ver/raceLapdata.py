import os
import csv
import xlsxwriter

import connectserver

def getRaceLapdata():
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
            query = f'SELECT DISTINCT(LapOverview.name) \
                    FROM LapDetail JOIN LapOverview ON \
                            LapDetail.sessionUID = LapOverview.sessionUID \
                        AND LapDetail.carIndex = LapOverview.carIndex \
                        AND LapDetail.lapNum = LapOverview.currentLapNum \
                    WHERE LapDetail.sessionUID >= {sessionid1} AND LapDetail.sessionUID <= {sessionid2};'
            print(f'fetching driverlist from session {sessionid2}......')
            cursor.execute(query)
            result = cursor.fetchall()
            print(f'driver list from session {sessionid2} acquired......\n')
            
            driverlist = []
            for driver in result:
                driverlist.append(driver[0])
            
            # driverlist = ["PSG.LGD.STeven L2i"]     # testing usage

            os.system('mkdir "lap data"')
            # pre-create an excel file
            filepath = f'lap data/race lapdata.xlsx'
            workbook = xlsxwriter.Workbook(filepath)
            default = workbook.add_format({"font_size":11})
            default.set_font_name("Dengxian")
            default.set_align("vcenter")
            default.set_text_wrap()

            # query lap data for every driver in the session
            for driver in driverlist:
                query = f'SELECT DISTINCT(lapNum), LapDetail.sessionUID, LapOverview.name, LapDetail.carIndex, LapDetail.carPosition, \
                        sector1TimeInStr, sector2TimeInStr, sector3TimeInStr, totalTimeInStr \
                        FROM LapDetail JOIN LapOverview ON \
                                LapDetail.sessionUID = LapOverview.sessionUID \
                            AND LapDetail.carIndex = LapOverview.carIndex \
                            AND LapDetail.lapNum = LapOverview.currentLapNum \
                        WHERE LapDetail.sessionUID >= {sessionid1} AND LapDetail.sessionUID <= {sessionid2} \
                            AND LapOverview.name = "{driver}";'
                print(f'fetching race lapdata of {driver}......')
                cursor.execute(query)
                result = cursor.fetchall()
                print("lapdata fetched, preparing writing to csv file......")

                
                # writing race lap data to csv file
                filepath = f'lap data/{driver.replace(":","")}.csv'
                with open(filepath, "w", newline="") as lapdata:
                    header = ["LapNum", "driverName", "Position",
                              "sector1", "sector2", "sector3", "Laptime"]
                    writer = csv.DictWriter(lapdata, header)
                    writer.writeheader()

                    for lap in result:
                        lapdict = {
                            "LapNum": lap[0],
                            #"sessionID": lap[1],
                            "driverName": lap[2],
                            #"carIndex": lap[3],
                            "Position": lap[4],
                            "sector1": lap[5],
                            "sector2": lap[6],
                            "sector3": lap[7],
                            "Laptime": lap[8]
                        }
                        writer.writerow(lapdict)
                

                # writing race lap data to excel file
                lapdata = workbook.add_worksheet(f'{driver.replace(":","")}')
                for i in range(0,50):
                    lapdata.set_row(i, 15)
                lapdata.set_column(0,0, 8)
                lapdata.set_column(1,1, 20)
                lapdata.set_column(2,2, 8)
                lapdata.set_column(3,5, 9)
                lapdata.set_column(6,6, 11)

                # writing the header
                for i in range(0, len(header)):
                    lapdata.write(0, i, header[i], default)

                row = 1
                for lap in result:
                    lapdata.write(row, 0, lap[0], default)
                    lapdata.write(row, 1, lap[2], default)
                    lapdata.write(row, 2, lap[4], default)
                    lapdata.write(row, 3, lap[5], default)
                    lapdata.write(row, 4, lap[6], default)
                    lapdata.write(row, 5, lap[7], default)
                    lapdata.write(row, 6, lap[8], default)
                    row += 1

                print(f'race lapdata of {driver} saved complete!\n')

            workbook.close()
            print(f'All driver race lapdata fetched and saved!')
            break

        except ValueError:
            input("session id error, please re-enter session id...")
            print()



if __name__ == "__main__":
    getRaceLapdata()
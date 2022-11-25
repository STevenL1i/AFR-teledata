import connectserver

def deleteSession():
    db = connectserver.connectserver()
    cursor = db.cursor()

    while True:
        
        sessionid1 = input("please enter session id 1: ")
        if sessionid1 == "q" or sessionid1 == "Q":
            break
        sessionid2 = input("please enter session id 2: ")
        if sessionid2 == "q" or sessionid2 == "Q":
            break

        try:
            sessionid1 = int(sessionid1)
            sessionid2 = int(sessionid2)

            query = "show tables;"
            cursor.execute(query)
            result = cursor.fetchall()

            tablelist = []
            for table in result:
                table = table[0]
                if table.find("_frame") == -1:
                    tablelist.append(table)

            for table in tablelist:
                query = ""
                if table != "session_id":
                    query = f'DELETE FROM {table} WHERE sessionUID >= {sessionid1} AND sessionUID <= {sessionid2};'
                else:
                    query = f'DELETE FROM {table} WHERE fake_id >= {sessionid1} AND fake_id <= {sessionid2};'
                print(f'deleting data from table {table} of session {sessionid1} to {sessionid2}......')
                cursor.execute(query)
                db.commit()
                print(f'data from table {table} of session {sessionid1} to {sessionid2} deleted!')
                print()

            break
            

        except ValueError:
            input("session id error, please re-enter session id...")
            print()


if __name__ == "__main__":
    deleteSession()
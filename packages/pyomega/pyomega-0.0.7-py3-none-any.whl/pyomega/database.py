import json
import pg8000


def query(db_client, query_string):

    print("QUERY: " + query_string)

    try:
        with db_client.cursor() as cursor:

            cursor.execute(query_string)

            return True

    except (Exception, pg8000.DatabaseError) as error:
        print(error)
        return False
    finally:
        db_client.commit()
        db_client.close()



def get_many(db_client, query_string):

    print("GET MANY QUERY: " + query_string)

    try:
        with db_client.cursor() as cursor:
            cursor.execute(query_string)

        result = cursor.fetchall()

        if result is None:
            return None

        else:
            print("GET MANY RESULT: " + json.dumps(result))
            return result

    except (Exception, pg8000.DatabaseError) as error:
        print(error)
        return False
    finally:
        db_client.commit()
        db_client.close()


def get_one(db_client, query_string):

    print("GET ONE QUERY: " + query_string)

    try:
        with db_client.cursor() as cursor:
            cursor.execute(query_string)

        result = cursor.fetchone()

        if result is None:
            return None

        else:
            print("GET ONE RESULT: " + json.dumps(result))
            return result

    except (Exception, pg8000.DatabaseError) as error:
        print(error)
        return False
    finally:
        db_client.commit()
        db_client.close()
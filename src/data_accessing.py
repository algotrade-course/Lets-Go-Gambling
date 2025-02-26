import psycopg
import json

def get_db_connection():
    try:
        with open('database.json', 'rb') as fb:
            db_info = json.load(fb)

        return psycopg.connect(
            host=db_info['host'],
            port=db_info['port'],
            dbname=db_info['database'],
            user=db_info['user'],
            password=db_info['password']
        )
    except Exception as e:
        print(f" Error connecting to database: {e}")
        return None


def get_futurecontract_tickersymbol(future_contract_code, date=None):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT m.tickersymbol
                    FROM "quote"."futurecontractcode" AS m
                    WHERE m.futurecode = %s
                    AND m.datetime = %s
                    """,
                    (future_contract_code, date)
                )
                result = cur.fetchone()
                
                if result:
                    print(f" Current Futures Contract tickersymbol: {result[0]}")
                    return result[0]
                else:
                    print(f" No symbol found for {future_contract_code}.")
                    return None
    except Exception as e:
        print(f" Database Error: {e}")
        return None

def get_current_price(symbol):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT m.price
                    FROM "quote"."matched" AS m
                    WHERE m.tickersymbol = %s
                    ORDER BY m.datetime 
                    DESC LIMIT 1
                    """,
                    (symbol,)
                )
                result = cur.fetchone()
                
                if result:
                    print(f" Current Price for {symbol}: {result[0]}")
                    return float(result[0])
                else:
                    print(f" No price data found for {symbol}.")
                    return None
    except Exception as e:
        print(f" Database Error: {e}")
        return None
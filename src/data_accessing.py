import psycopg
from dotenv import load_dotenv
import os
import csv
from datetime import datetime

load_dotenv()

def get_db_connection():
    try:
        return psycopg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None


def fetch_data(future_code, start_date, end_date):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT DISTINCT m.datetime, m.price, f.tickersymbol, f.futurecontractcode 
                    FROM "quote"."matched" AS m
                    JOIN (
                        SELECT DISTINCT tickersymbol, futurecontractcode
                        FROM "quote"."futurecontractcode"
                        WHERE futurecode = %s
                        AND datetime BETWEEN %s AND %s
                    ) AS f
                    ON m.tickersymbol = f.tickersymbol
                    WHERE m.datetime BETWEEN %s AND %s
                    ORDER BY m.datetime ASC;
                    """, 
                    (future_code, start_date, end_date, start_date, end_date)
                )
                return cur.fetchall()
    except Exception as e:
        print(f" Error loading historical data: {e}")
        return None
    
def collect_data_from_csv(start_date, end_date, filename="data.csv"):
    datetime_price_data = []

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        print(f"Invalid date format: {e}")
        return datetime_price_data

    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        
        if 'datetime' not in csv_reader.fieldnames or 'price' not in csv_reader.fieldnames:
            print("CSV file does not contain required columns.")
            return datetime_price_data

        for row in csv_reader:
            try:
                row_datetime = datetime.strptime(row['datetime'], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                print(f"Invalid datetime format in row: {row['datetime']}")
                continue

            if start_date <= row_datetime <= end_date:
                try:
                    price = float(row['price'])
                    datetime_price_data.append((row['datetime'], price))
                except ValueError:
                    print(f"Invalid price value in row: {row['price']}")
                    continue

    return datetime_price_data
    
if __name__ == "__main__":
    print("### Fetching Data... ###")
    data = fetch_data("VN30F1M", "2022-01-01", "2024-01-03")
    if data:
        with open("data.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["datetime", "price", "tickersymbol", "futurecontractcode"])
            for row in data:
                writer.writerow(row)
        print("Data saved to data.csv")
    else:
        print("No data fetched.")
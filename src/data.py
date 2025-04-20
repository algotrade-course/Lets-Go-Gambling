import sys
import psycopg
from dotenv import load_dotenv
import os
import csv
from datetime import datetime
from src.settings import data_params, in_sample_params, out_sample_params, DATA_PATH_ROOT
from src.path import data_path, in_sample_data_path, out_sample_data_path

load_dotenv()

def get_db_connection():
    try:
        print("Connecting to database...")
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
            print("Connected to database.")
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
    
def collect_data_from_csv(start_date, end_date, filename=data_path):
    datetime_price_data = []

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
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
                row_datetime = datetime.strptime(row['datetime'], "%Y-%m-%d %H:%M:%S.%f")
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

def data_processing(params):
    data = collect_data_from_csv(params["START_DATE"], params["END_DATE"])
    if not data:
        print("No data found in the specified date range.")
        return
    return data

def save_to_csv(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["datetime", "price"])
        for row in data:
            writer.writerow(row)
    print(f"Saved {len(data)} rows to {path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please specify a mode: 'get' (need .env) or 'process'")
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "get":
        print("### Fetching Data... ###")
        data = fetch_data("VN30F1M", data_params["START_DATE"], data_params["END_DATE"])
        if data:
            print(f"writing to data.csv")
            with open(data_path, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["datetime", "price", "tickersymbol", "futurecontractcode"])
                for row in data:
                    writer.writerow(row)
            print("Data saved to data.csv")
        else:
            print("No data fetched.")

    elif mode == "process":
        print("### Processing Data... ###")
        print("In-sample data:")
        in_sample_data = data_processing(in_sample_params)
        save_to_csv(in_sample_data, in_sample_data_path)

        print("Out-of-sample data:")
        out_sample_data = data_processing(out_sample_params)
        save_to_csv(out_sample_data, out_sample_data_path)

    else:
        print("Invalid mode. Use 'get' or 'process'.")
        sys.exit(1)

from data_accessing import get_db_connection 
import sys
import csv
def main(start_date, end_date):
    # start_date = '2022-03-01'
    # end_date = '2022-03-05'
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        SELECT
                        m.datetime::DATE AS date,
                        m.datetime::TIME AS time,
                        m.tickersymbol,
                        m.price,
                        tb_open.price AS open_price,
                        tb_close.price AS close_price,
                        tb_max.price AS high_price,
                        tb_min.price AS low_price,
                        tb.quantity AS total_quantity
                    FROM "quote"."matched" m
                    INNER JOIN "quote"."open" tb_open
                        ON m.tickersymbol = tb_open.tickersymbol
                        AND m.datetime::DATE = tb_open.datetime::DATE
                    INNER JOIN "quote"."close" tb_close
                        ON m.tickersymbol = tb_close.tickersymbol
                        AND m.datetime::DATE = tb_close.datetime::DATE
                    INNER JOIN "quote"."max" tb_max
                        ON m.tickersymbol = tb_max.tickersymbol
                        AND m.datetime::DATE = tb_max.datetime::DATE
                    INNER JOIN "quote"."min" tb_min
                        ON m.tickersymbol = tb_min.tickersymbol
                        AND m.datetime::DATE = tb_min.datetime::DATE
                    INNER JOIN "quote"."matchedvolume" tb
                        ON m.tickersymbol = tb.tickersymbol
                        AND m.datetime = tb.datetime
                    WHERE m.datetime BETWEEN  %s AND  %s
                    AND m.tickersymbol LIKE %s
                    ORDER BY m.datetime, m.tickersymbol;
                    """, 
                    (start_date, end_date, 'VN30F%')
                        )
                data =  cur.fetchall()
                fieldnames = [
                    "date", "time", "tickersymbol", "price", 
                    "open_price", "close_price", "high_price", 
                    "low_price", "total_quantity"
                ]
                csv_filename = "ticker_data" + start_date + "_" + end_date + ".csv"

                # Write data to CSV
                with open(csv_filename, mode="w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(fieldnames)
                    # Write rows
                    writer.writerows(data)

                print(f"Data saved to {csv_filename}")
    except Exception as e:
        print(f" Error loading historical data: {e}")
        return None

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
import psycopg2
from concurrent.futures import ThreadPoolExecutor
import time

# Налаштування підключення до бази даних
DB_CONFIG = {
    "dbname": "test_db_name",
    "user": "dari",
    "password": "dariismyname",
    "host": "localhost",
    "port": 5432
}

def lost_update():
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1")
            counter = cursor.fetchone()[0]
            counter += 1
            cursor.execute("UPDATE user_counter SET counter = %s WHERE user_id = 1", (counter,))
            conn.commit()

def in_place_update():
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE user_counter SET counter = counter + 1 WHERE user_id = 1")
            conn.commit()

def row_level_locking():
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT counter FROM user_counter WHERE user_id = 1 FOR UPDATE")
            counter = cursor.fetchone()[0]
            counter += 1
            cursor.execute("UPDATE user_counter SET counter = %s WHERE user_id = 1", (counter,))
            conn.commit()

def optimistic_concurrency():
    while True:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT counter, version FROM user_counter WHERE user_id = 1")
                counter, version = cursor.fetchone()
                counter += 1
                cursor.execute("""
                    UPDATE user_counter
                    SET counter = %s, version = %s
                    WHERE user_id = 1 AND version = %s
                """, (counter, version + 1, version))
                conn.commit()
                if cursor.rowcount > 0:
                    break

def measure_time(func, threads=10, iterations=10000):
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for _ in range(threads):
            executor.submit(lambda: [func() for _ in range(iterations)])
    end_time = time.time()
    print(f"{func.__name__}: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    print("Testing different approaches...")
    measure_time(lost_update)
    measure_time(in_place_update)
    measure_time(row_level_locking)
    measure_time(optimistic_concurrency)

import psycopg2
import time
import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "transactions")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

# Sample data — kasnije može da čita iz CSV fajla
TRANSACTIONS = [
    (1, 1, 120.00, "Food",      "2024-03-01"),
    (2, 1,  45.00, "Transport", "2024-03-02"),
    (3, 2,  60.00, "Transport", "2024-03-01"),
    (4, 2, 150.00, "Shopping",  "2024-03-02"),
    (5, 3, 500.00, "Shopping",  "2024-03-01"),
    (6, 3,  80.00, "Food",      "2024-03-03"),
    (7, 1, 200.00, "Shopping",  "2024-03-04"),
    (8, 2,  30.00, "Food",      "2024-03-04"),
]

def wait_for_db():
    """Čeka da PostgreSQL bude spreman (Docker timing problem)."""
    print("Čekam na bazu...")
    for i in range(10):
        try:
            conn = psycopg2.connect(
                host=DB_HOST, dbname=DB_NAME,
                user=DB_USER, password=DB_PASSWORD
            )
            conn.close()
            print("Baza je spremna!")
            return
        except psycopg2.OperationalError:
            print(f"  Pokušaj {i+1}/10 — čekam 3s...")
            time.sleep(3)
    raise Exception("Baza nije dostupna nakon 10 pokušaja.")

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id  SERIAL PRIMARY KEY,
                user_id         INTEGER NOT NULL,
                amount          NUMERIC(10, 2) NOT NULL,
                category        VARCHAR(50),
                tx_date         DATE NOT NULL
            );
        """)
        conn.commit()
    print("Tabela 'transactions' je kreirana (ili već postoji).")

def ingest_data(conn):
    with conn.cursor() as cur:
        # Briše stare podatke da ne duplicira pri ponovnom pokretanju
        cur.execute("TRUNCATE TABLE transactions RESTART IDENTITY;")
        cur.executemany("""
            INSERT INTO transactions (transaction_id, user_id, amount, category, tx_date)
            VALUES (%s, %s, %s, %s, %s)
        """, TRANSACTIONS)
        conn.commit()
    print(f"Uneseno {len(TRANSACTIONS)} transakcija.")

def main():
    wait_for_db()
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
    )
    create_table(conn)
    ingest_data(conn)
    conn.close()
    print("Ingest završen!")

if __name__ == "__main__":
    main()
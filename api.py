from fastapi import FastAPI, HTTPException
import psycopg2
import psycopg2.extras
import os

app = FastAPI(title="Transactions API")

def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        dbname=os.getenv("DB_NAME", "transactions"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )

@app.get("/transactions")
def get_transactions():
    conn = get_conn()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT * FROM transactions ORDER BY tx_date;")
        data = cur.fetchall()
    conn.close()
    return {"data": data, "count": len(data)}

@app.get("/transactions/{user_id}")
def get_user_transactions(user_id: int):
    conn = get_conn()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            "SELECT * FROM transactions WHERE user_id = %s ORDER BY tx_date;",
            (user_id,)
        )
        data = cur.fetchall()
    conn.close()
    if not data:
        raise HTTPException(status_code=404, detail="Korisnik nema transakcija.")
    return {"data": data, "count": len(data)}

@app.get("/summary")
def get_summary():
    conn = get_conn()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("""
            SELECT user_id, COUNT(*) AS broj, SUM(amount) AS ukupno
            FROM transactions GROUP BY user_id ORDER BY ukupno DESC;
        """)
        data = cur.fetchall()
    conn.close()
    return {"data": data}

@app.get("/health")
def health():
    return {"status": "ok"}
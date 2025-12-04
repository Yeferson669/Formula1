import psycopg2

# Datos de conexión (los mismos que usas en tu app)
DB_HOST = "b9snz55bmuviqhb7nkhv-postgresql.services.clever-cloud.com"
DB_NAME = "b9snz55bmuviqhb7nkhv"
DB_USER = "uyfwrbo579r56bazkvpe"
DB_PASS = "fY4dymWS8N1bOKhpMQCdshFUVIfb81"
DB_PORT = 50013

def kill_idle_connections():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Termina todas las conexiones "idle" de tu usuario
        cur.execute("""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE usename = %s
              AND state = 'idle'
              AND pid <> pg_backend_pid();
        """, (DB_USER,))

        print("✅ Conexiones viejas cerradas correctamente.")
        cur.close()
        conn.close()
    except Exception as e:
        print("❌ Error cerrando conexiones:", e)

if __name__ == "__main__":
    kill_idle_connections()

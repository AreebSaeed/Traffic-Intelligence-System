import socket

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

DATABASE_URL = (
    "postgresql://postgres.qxgoagigfcnhawsuthvs:ktis_proj_1234"
    "@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
)

HOST = "aws-1-ap-south-1.pooler.supabase.com"
PORT = 6543


def check_dns():
    try:
        results = socket.getaddrinfo(HOST, PORT)
        families = {family.name for family, *_ in results}
        print(f"DNS OK for {HOST}: {', '.join(sorted(families))}")
        return True
    except socket.gaierror:
        print(f"DNS failed for {HOST}.")
        return False


print("Checking DNS...")
if not check_dns():
    raise SystemExit(1)

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("Connected successfully!")
except OperationalError as e:
    print("Connection failed:", e)
    raise SystemExit(1)

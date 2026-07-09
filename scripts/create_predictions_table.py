from sqlalchemy import create_engine, text

DATABASE_URL = (
    "postgresql://postgres.qxgoagigfcnhawsuthvs:ktis_proj_1234"
    "@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
)

engine = create_engine(DATABASE_URL)

CREATE_SQL = """
create table if not exists predictions (
    id bigint generated always as identity primary key,
    road_id bigint,
    road_name text,
    prediction text,
    confidence float,
    temperature float,
    humidity float,
    rain float,
    datetime timestamp default now()
);
"""

with engine.begin() as conn:
    conn.execute(text(CREATE_SQL))

print("predictions table created (or already exists).")

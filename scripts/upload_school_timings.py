import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql://postgres.qxgoagigfcnhawsuthvs:ktis_proj_1234"
    "@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
)

engine = create_engine(DATABASE_URL)

df = pd.read_csv("data/external/school_timings.csv")

df.to_sql(
    "school_timings",
    engine,
    if_exists="append",
    index=False,
    method="multi"
)

print("School timings uploaded successfully!")
import pandas as pd
from sqlalchemy import text
from config import BASE_DIR, get_engine

def load_data():
    print("⏳ Loading clean data from CSV...")
    
    df = pd.read_csv(BASE_DIR / "data" / "processed" / "clean_retail_data.csv")
    
    # --- Remove duplicates to ensure clean data ---
    initial_rows = len(df)
    df.drop_duplicates(inplace=True)
    print(f"🧹 Removed {initial_rows - len(df)} duplicate rows.")
    # ----------------------------------------------
    
    # Convert InvoiceDate to datetime
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    print(f"✅ Loaded {len(df)} rows after cleaning.")
    
    # Connect to Neon database
    engine = get_engine()
    
    print("⏳ Dropping old table if it exists...")
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS retail_transactions;"))
        conn.commit()

    print("⏳ Pushing data to Neon PostgreSQL (this may take 1-2 minutes)...")
    
    # Push to database in chunks to prevent memory issues
    df.to_sql(
        name='retail_transactions', 
        con=engine, 
        if_exists='replace', 
        index=False,
        chunksize=10000 
    )
    
    print("🎉 Data successfully loaded into PostgreSQL!")

if __name__ == "__main__":
    load_data()
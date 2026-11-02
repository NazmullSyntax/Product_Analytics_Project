import pytest
import pandas as pd
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

def test_database_connection():
    """Test that we can connect to the Neon database."""
    from src.config import get_engine
    from sqlalchemy import text
    
    engine = get_engine()
    assert engine is not None
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar()
        assert result == 1

def test_data_loaded():
    """Test that the main table has data."""
    from src.config import get_engine
    engine = get_engine()
    df = pd.read_sql("SELECT COUNT(*) as count FROM retail_transactions", engine)
    assert df['count'].iloc[0] > 700000  # Should be ~779k

def test_no_negative_quantities():
    """Test that data cleaning removed negative quantities."""
    from src.config import get_engine
    engine = get_engine()
    df = pd.read_sql('SELECT COUNT(*) as count FROM retail_transactions WHERE "Quantity" < 0', engine)
    assert df['count'].iloc[0] == 0

def test_no_missing_customer_ids():
    """Test that all records have a CustomerID (no nulls)."""
    from src.config import get_engine
    engine = get_engine()
    df = pd.read_sql('SELECT COUNT(*) as count FROM retail_transactions WHERE "CustomerID" IS NULL', engine)
    assert df['count'].iloc[0] == 0

def test_revenue_calculation():
    """Test that TotalAmount is correctly calculated."""
    from src.config import get_engine
    engine = get_engine()
    df = pd.read_sql('''
        SELECT "Quantity", "Price", "TotalAmount" 
        FROM retail_transactions 
        LIMIT 100
    ''', engine)
    
    # Manually calculate TotalAmount
    df['expected'] = (df['Quantity'] * df['Price']).round(2)
    df['actual'] = df['TotalAmount'].round(2)
    
    assert (df['expected'] == df['actual']).all(), "TotalAmount is not correctly calculated!"
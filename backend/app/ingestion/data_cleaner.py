import pandas as pd
import numpy as np
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DataCleaner:
    def __init__(self):
        self.cleaning_stats = {}
    
    async def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Starting data cleaning process...")
        original_rows = len(df)
        
        df_clean = df.copy()
        
        df_clean = self._handle_missing_values(df_clean)
        df_clean = self._remove_duplicates(df_clean)
        df_clean = self._normalize_text(df_clean)
        df_clean = self._handle_data_types(df_clean)
        
        cleaned_rows = len(df_clean)
        self.cleaning_stats = {
            "original_rows": original_rows,
            "cleaned_rows": cleaned_rows,
            "rows_removed": original_rows - cleaned_rows
        }
        
        logger.info(f"Data cleaning complete. Removed {original_rows - cleaned_rows} rows")
        return df_clean
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in df.columns:
            if df[col].dtype in ['float64', 'int64']:
                df[col].fillna(df[col].median(), inplace=True)
            else:
                df[col].fillna('', inplace=True)
        return df
    
    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.drop_duplicates()
    
    def _normalize_text(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.strip()
        return df
    
    def _handle_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in df.columns:
            try:
                if df[col].dtype == 'object':
                    try:
                        df[col] = pd.to_numeric(df[col])
                    except:
                        pass
            except:
                pass
        return df
    
    def get_cleaning_stats(self) -> Dict[str, Any]:
        return self.cleaning_stats
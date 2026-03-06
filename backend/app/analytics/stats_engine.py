import pandas as pd
import numpy as np
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class StatsEngine:
    def __init__(self):
        self.stats = {}
    
    async def compute_dataset_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        logger.info("Computing dataset statistics")
        
        stats = {
            "basic": {
                "num_rows": len(df),
                "num_columns": len(df.columns),
                "total_cells": len(df) * len(df.columns),
                "missing_cells": int(df.isnull().sum().sum())
            },
            "columns": {}
        }
        
        for col in df.columns:
            col_stats = {
                "dtype": str(df[col].dtype),
                "missing": int(df[col].isnull().sum()),
                "unique": int(df[col].nunique())
            }
            
            if df[col].dtype in ['int64', 'float64']:
                col_stats.update({
                    "mean": float(df[col].mean()) if not df[col].isnull().all() else 0,
                    "median": float(df[col].median()) if not df[col].isnull().all() else 0,
                    "std": float(df[col].std()) if not df[col].isnull().all() else 0,
                    "min": float(df[col].min()) if not df[col].isnull().all() else 0,
                    "max": float(df[col].max()) if not df[col].isnull().all() else 0
                })
            
            stats["columns"][col] = col_stats
        
        self.stats = stats
        return stats
    
    def get_stats(self) -> Dict[str, Any]:
        return self.stats
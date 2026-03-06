import pandas as pd
import openpyxl
from pathlib import Path
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class ExcelLoader:
    def __init__(self):
        self.supported_formats = ['.xlsx', '.xls', '.xlsm']
    
    async def load_excel(self, file_path: Path) -> pd.DataFrame:
        try:
            if file_path.suffix not in self.supported_formats:
                raise ValueError(f"Unsupported file format: {file_path.suffix}")
            
            logger.info(f"Loading Excel file: {file_path}")
            df = pd.read_excel(file_path, engine='openpyxl')
            
            logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
            return df
            
        except Exception as e:
            logger.error(f"Error loading Excel file: {str(e)}")
            raise
    
    async def get_dataset_info(self, df: pd.DataFrame) -> Dict[str, Any]:
        return {
            "num_rows": len(df),
            "num_columns": len(df.columns),
            "columns": df.columns.tolist(),
            "data_types": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "memory_usage": df.memory_usage(deep=True).sum()
        }
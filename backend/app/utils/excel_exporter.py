import pandas as pd
from io import BytesIO
from typing import Dict, Any, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ExcelExporter:
    @staticmethod
    def export_query_results(query: str, answer: str, supporting_rows: List[Dict[str, Any]], 
                            confidence_score: float, latency_ms: float) -> BytesIO:
        """Export query results to Excel format"""
        
        # Create Excel writer
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Sheet 1: Query Summary
            summary_data = {
                'Field': ['Query', 'Answer', 'Confidence Score', 'Latency (ms)', 'Number of Sources', 'Generated At'],
                'Value': [query, answer, f"{confidence_score*100:.1f}%", f"{latency_ms:.0f}", 
                         len(supporting_rows), datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Sheet 2: Supporting Data
            if supporting_rows:
                # Extract metadata from supporting rows
                data_rows = []
                for i, row in enumerate(supporting_rows, 1):
                    row_data = {'Source #': i}
                    row_data.update(row.get('data', {}))
                    data_rows.append(row_data)
                
                supporting_df = pd.DataFrame(data_rows)
                supporting_df.to_excel(writer, sheet_name='Supporting Data', index=False)
            
            # Sheet 3: Raw Context
            context_data = []
            for i, row in enumerate(supporting_rows, 1):
                context_data.append({
                    'Source #': i,
                    'Row ID': row.get('row_id', ''),
                    'Full Text': row.get('text', '')
                })
            
            if context_data:
                context_df = pd.DataFrame(context_data)
                context_df.to_excel(writer, sheet_name='Context', index=False)
        
        output.seek(0)
        return output

import pandas as pd
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class SuggestionGenerator:
    @staticmethod
    def generate_suggestions(dataset_info: Dict[str, Any]) -> List[str]:
        """Generate smart query suggestions based on dataset columns"""
        suggestions = []
        columns = dataset_info.get('columns', [])
        
        if not columns:
            return suggestions
        
        # Generic suggestions
        suggestions.append(f"How many rows are in the dataset?")
        suggestions.append(f"What columns are available in this dataset?")
        suggestions.append(f"Show me a summary of the data")
        
        # Column-specific suggestions
        for col in columns[:5]:  # Limit to first 5 columns
            col_lower = col.lower()
            
            # Numerical columns
            if any(word in col_lower for word in ['price', 'cost', 'revenue', 'sales', 'amount', 'quantity', 'total']):
                suggestions.append(f"What is the average {col}?")
                suggestions.append(f"What is the highest {col}?")
                suggestions.append(f"What is the total {col}?")
            
            # Name/ID columns
            elif any(word in col_lower for word in ['name', 'product', 'customer', 'employee', 'id']):
                suggestions.append(f"List all unique {col}")
                suggestions.append(f"How many different {col} are there?")
            
            # Date columns
            elif any(word in col_lower for word in ['date', 'time', 'year', 'month']):
                suggestions.append(f"What is the date range in {col}?")
            
            # Category columns
            elif any(word in col_lower for word in ['category', 'type', 'status', 'department']):
                suggestions.append(f"What are the different {col}?")
                suggestions.append(f"Count by {col}")
        
        # Relationship queries
        if len(columns) >= 2:
            suggestions.append(f"What is the relationship between {columns[0]} and {columns[1]}?")
        
        return suggestions[:10]  # Return top 10 suggestions

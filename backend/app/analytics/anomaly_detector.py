import numpy as np
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class AnomalyDetector:
    def __init__(self):
        self.anomalies = []
    
    async def detect_anomalies(self, data: List[float]) -> Dict[str, Any]:
        logger.info("Running anomaly detection")
        
        if not data or len(data) < 3:
            return {
                "anomalies_detected": 0,
                "anomaly_indices": [],
                "method": "IQR"
            }
        
        data_array = np.array(data)
        
        q1 = np.percentile(data_array, 25)
        q3 = np.percentile(data_array, 75)
        iqr = q3 - q1
        
        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)
        
        anomaly_indices = np.where((data_array < lower_bound) | (data_array > upper_bound))[0].tolist()
        
        result = {
            "anomalies_detected": len(anomaly_indices),
            "anomaly_indices": anomaly_indices,
            "method": "IQR",
            "bounds": {
                "lower": float(lower_bound),
                "upper": float(upper_bound)
            }
        }
        
        logger.info(f"Detected {len(anomaly_indices)} anomalies")
        return result
"""
Machine Learning Model Predictor
Handles loading and using the fraud detection model
"""

import pickle
import os
import numpy as np
from typing import Union

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'best_model.pkl')


class FraudPredictor:
    """Handles fraud detection predictions using the trained model"""
    
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the pickled machine learning model"""
        try:
            if os.path.exists(MODEL_PATH):
                with open(MODEL_PATH, 'rb') as f:
                    self.model = pickle.load(f)
                print(f"✓ ML model loaded successfully from {MODEL_PATH}")
            else:
                print(f"✗ Model file not found at {MODEL_PATH}")
                raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            raise
    
    def predict(self, transaction_data: dict) -> Union[int, None]:
        """
        Predict if a transaction is fraudulent (1) or not (0)
        
        Args:
            transaction_data: Dictionary containing transaction features
            
        Returns:
            Prediction (0 or 1), or None if prediction fails
        """
        try:
            if self.model is None:
                raise ValueError("Model not loaded")
            
            # Convert transaction data to the format expected by the model
            # This assumes the model expects features in a specific order
            # Adjust the feature extraction based on your model's requirements
            features = self._extract_features(transaction_data)
            
            # Make prediction
            prediction = self.model.predict([features])[0]
            
            # Ensure prediction is 0 or 1
            return int(prediction)
        except Exception as e:
            print(f"✗ Prediction error: {e}")
            raise
    
    def predict_proba(self, transaction_data: dict) -> Union[dict, None]:
        """
        Get prediction probabilities if the model supports it
        
        Args:
            transaction_data: Dictionary containing transaction features
            
        Returns:
            Dictionary with probabilities for each class
        """
        try:
            if self.model is None:
                raise ValueError("Model not loaded")
            
            # Check if model has predict_proba method
            if not hasattr(self.model, 'predict_proba'):
                return None
            
            features = self._extract_features(transaction_data)
            probabilities = self.model.predict_proba([features])[0]
            
            return {
                "fraud_probability": float(probabilities[1]) if len(probabilities) > 1 else 0.0,
                "legitimate_probability": float(probabilities[0]) if len(probabilities) > 0 else 0.0
            }
        except Exception as e:
            print(f"✗ Probability prediction error: {e}")
            return None
    
    def _extract_features(self, transaction_data: dict) -> np.ndarray:
        """
        Extract features from transaction data in the order expected by the model
        
        The model expects 35 features. This extracts available transaction and pattern data.
        Adjust based on your actual model's training features.
        """
        # Extract available features and pad with zeros for missing ones
        features = [
            transaction_data.get('amount', 0),
            transaction_data.get('cst_dim_id', 0),
            transaction_data.get('docno', 0),
            transaction_data.get('direction', 0),
            transaction_data.get('transdate', 0),
            transaction_data.get('transdatetime', 0)
        ]
        
        # Pad with zeros to reach 35 features expected by the model
        while len(features) < 35:
            features.append(0)
        
        # Ensure we have exactly 35 features
        features = features[:35]
        
        return np.array(features, dtype=np.float32)


# Global predictor instance
predictor = FraudPredictor()

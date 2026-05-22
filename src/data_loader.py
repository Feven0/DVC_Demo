import pandas as pd
import numpy as np
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InsuranceDataLoader:
    """
    A class for loading and preprocessing the insurance dataset.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

    def load_data(self) -> pd.DataFrame:
        """
        Loads the pipe-separated insurance dataset.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Data file not found at: {self.file_path}")
        
        logger.info(f"Loading data from {self.file_path}...")
        
        # Load pipe-separated file
        self.df = pd.read_csv(self.file_path, sep='|', low_memory=False)
        
        # Strip whitespaces from column names
        self.df.columns = [col.strip() for col in self.df.columns]
        
        logger.info(f"Successfully loaded dataset with shape: {self.df.shape}")
        return self.df

    def preprocess_data(self) -> pd.DataFrame:
        """
        Performs basic preprocessing:
        - Parses datetime columns
        - Ensures numerical columns are properly typed
        - Computes derived metrics (Loss Ratio and Margin)
        """
        if self.df is None:
            self.load_data()

        logger.info("Starting preprocessing...")

        # Parse dates
        if 'TransactionMonth' in self.df.columns:
            self.df['TransactionMonth'] = pd.to_datetime(self.df['TransactionMonth'])
        
        # Parse numeric columns
        numeric_cols = [
            'TotalPremium', 'TotalClaims', 'SumInsured', 'CalculatedPremiumPerTerm',
            'CustomValueEstimate', 'CapitalOutstanding', 'Cylinders', 
            'cubiccapacity', 'kilowatts', 'RegistrationYear', 'NumberOfDoors'
        ]
        
        for col in numeric_cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
        
        # Fill missing values for core analysis columns
        # In a production pipeline, we want to keep track of missing values or impute them carefully.
        self.df['TotalPremium'] = self.df['TotalPremium'].fillna(0.0)
        self.df['TotalClaims'] = self.df['TotalClaims'].fillna(0.0)

        # Compute derived metrics
        logger.info("Computing derived metrics: LossRatio and Margin...")
        
        # LossRatio = TotalClaims / TotalPremium. Set to 0 if TotalPremium is 0 or negative
        self.df['LossRatio'] = np.where(
            self.df['TotalPremium'] > 0,
            self.df['TotalClaims'] / self.df['TotalPremium'],
            0.0
        )
        
        # Margin = TotalPremium - TotalClaims
        self.df['Margin'] = self.df['TotalPremium'] - self.df['TotalClaims']

        logger.info("Preprocessing complete.")
        return self.df

    def get_summary_statistics(self) -> pd.DataFrame:
        """
        Generates summary statistics for the dataset.
        """
        if self.df is None:
            self.preprocess_data()
        
        return self.df.describe(include='all', datetime_is_numeric=True)

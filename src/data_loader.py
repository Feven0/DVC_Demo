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

    def load_data(self, chunksize: int = 100000) -> pd.DataFrame:
        """
        Loads the pipe-separated insurance dataset in chunks to optimize memory.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Data file not found at: {self.file_path}")
        
        logger.info(f"Loading data from {self.file_path} in chunks of {chunksize}...")
        
        chunks = []
        for chunk in pd.read_csv(self.file_path, sep='|', chunksize=chunksize, low_memory=False):
            # Clean whitespaces in column names for the chunk
            chunk.columns = [col.strip() for col in chunk.columns]
            chunks.append(chunk)
            
        self.df = pd.concat(chunks, ignore_index=True)
        
        logger.info(f"Successfully loaded dataset with shape: {self.df.shape}")
        return self.df

    def preprocess_chunk(self, chunk: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocesses a single chunk of data: standardizes numeric types and calculates metrics.
        """
        # Parse dates
        if 'TransactionMonth' in chunk.columns:
            chunk['TransactionMonth'] = pd.to_datetime(chunk['TransactionMonth'])
        
        # Parse numeric columns
        numeric_cols = [
            'TotalPremium', 'TotalClaims', 'SumInsured', 'CalculatedPremiumPerTerm',
            'CustomValueEstimate', 'CapitalOutstanding', 'Cylinders', 
            'cubiccapacity', 'kilowatts', 'RegistrationYear', 'NumberOfDoors'
        ]
        
        for col in numeric_cols:
            if col in chunk.columns:
                chunk[col] = pd.to_numeric(chunk[col], errors='coerce')
        
        # Fill missing values for core analysis columns
        chunk['TotalPremium'] = chunk['TotalPremium'].fillna(0.0)
        chunk['TotalClaims'] = chunk['TotalClaims'].fillna(0.0)

        # Compute derived metrics
        chunk['LossRatio'] = np.where(
            chunk['TotalPremium'] > 0,
            chunk['TotalClaims'] / chunk['TotalPremium'],
            0.0
        )
        chunk['Margin'] = chunk['TotalPremium'] - chunk['TotalClaims']
        
        return chunk

    def preprocess_data(self) -> pd.DataFrame:
        """
        Performs in-memory preprocessing on self.df.
        """
        if self.df is None:
            self.load_data()

        logger.info("Starting preprocessing...")
        self.df = self.preprocess_chunk(self.df)
        logger.info("Preprocessing complete.")
        return self.df

    @staticmethod
    def preprocess_large_file(input_path: str, output_path: str, chunksize: int = 100000):
        """
        Streams, cleans, and writes a large file chunk-by-chunk to save memory.
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found at: {input_path}")
            
        logger.info(f"Streaming and preprocessing {input_path} -> {output_path}...")
        
        # Handle in-place preprocessing safely by writing to a temporary file first
        in_place = (os.path.abspath(input_path) == os.path.abspath(output_path))
        target_path = output_path + ".tmp" if in_place else output_path
        
        first_chunk = True
        
        for chunk in pd.read_csv(input_path, sep='|', chunksize=chunksize, low_memory=False):
            # Clean whitespaces in column names
            chunk.columns = [col.strip() for col in chunk.columns]
            
            # Preprocess the chunk
            processed = InsuranceDataLoader.static_preprocess_chunk(chunk)
            
            # Write to output file using pipe delimiter to remain consistent
            mode = 'w' if first_chunk else 'a'
            header = True if first_chunk else False
            
            processed.to_csv(target_path, sep='|', index=False, mode=mode, header=header)
            first_chunk = False
            
        if in_place:
            if os.path.exists(output_path):
                os.remove(output_path)
            os.rename(target_path, output_path)
            
        logger.info("Preprocessed stream write successful.")

    @staticmethod
    def static_preprocess_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
        """
        Helper to preprocess a chunk without an instance.
        """
        # Parse dates
        if 'TransactionMonth' in chunk.columns:
            chunk['TransactionMonth'] = pd.to_datetime(chunk['TransactionMonth'])
        
        # Parse numeric columns
        numeric_cols = [
            'TotalPremium', 'TotalClaims', 'SumInsured', 'CalculatedPremiumPerTerm',
            'CustomValueEstimate', 'CapitalOutstanding', 'Cylinders', 
            'cubiccapacity', 'kilowatts', 'RegistrationYear', 'NumberOfDoors'
        ]
        
        for col in numeric_cols:
            if col in chunk.columns:
                chunk[col] = pd.to_numeric(chunk[col], errors='coerce')
        
        # Fill missing values for core analysis columns
        chunk['TotalPremium'] = chunk['TotalPremium'].fillna(0.0)
        chunk['TotalClaims'] = chunk['TotalClaims'].fillna(0.0)

        # Compute derived metrics
        chunk['LossRatio'] = np.where(
            chunk['TotalPremium'] > 0,
            chunk['TotalClaims'] / chunk['TotalPremium'],
            0.0
        )
        chunk['Margin'] = chunk['TotalPremium'] - chunk['TotalClaims']
        
        return chunk

    def get_summary_statistics(self) -> pd.DataFrame:
        """
        Generates summary statistics for the dataset.
        """
        if self.df is None:
            self.preprocess_data()
        
        return self.df.describe(include='all', datetime_is_numeric=True)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Load and preprocess insurance data.")
    parser.add_argument("--input", default="data/insurance_data.csv", help="Input raw data file path")
    parser.add_argument("--output", default="data/insurance_data.csv", help="Output preprocessed CSV path")
    args = parser.parse_args()
    
    # Run the streaming stream preprocessing
    InsuranceDataLoader.preprocess_large_file(args.input, args.output)

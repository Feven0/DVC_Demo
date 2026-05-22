import pytest
import pandas as pd
import numpy as np
import os
from src.data_loader import InsuranceDataLoader

@pytest.fixture
def sample_data_file(tmp_path):
    """
    Creates a temporary pipe-separated mock data file.
    """
    data = (
        "UnderwrittenCoverID|PolicyID|TransactionMonth|IsVATRegistered|TotalPremium|TotalClaims\n"
        "1|100|2015-01-01|True|100.0|20.0\n"
        "2|200|2015-02-01|False|0.0|0.0\n"
        "3|300|2015-03-01|True|50.0|100.0\n"
    )
    file_path = os.path.join(tmp_path, "mock_data.txt")
    with open(file_path, "w") as f:
        f.write(data)
    return file_path

def test_data_loader_initialization(sample_data_file):
    loader = InsuranceDataLoader(sample_data_file)
    assert loader.file_path == sample_data_file
    assert loader.df is None

def test_load_and_preprocess(sample_data_file):
    loader = InsuranceDataLoader(sample_data_file)
    df = loader.preprocess_data()
    
    # Check shape
    assert df.shape == (3, 8)  # 6 raw columns + 2 derived columns
    
    # Check column names are stripped
    assert "TotalPremium" in df.columns
    assert "TotalClaims" in df.columns
    
    # Check derived metrics
    # Row 1: LR = 20 / 100 = 0.2, Margin = 100 - 20 = 80
    assert df.loc[0, 'LossRatio'] == 0.2
    assert df.loc[0, 'Margin'] == 80.0
    
    # Row 2: Premium is 0, so LR should be 0.0, Margin = 0.0
    assert df.loc[1, 'LossRatio'] == 0.0
    assert df.loc[1, 'Margin'] == 0.0
    
    # Row 3: LR = 100 / 50 = 2.0, Margin = 50 - 100 = -50
    assert df.loc[2, 'LossRatio'] == 2.0
    assert df.loc[2, 'Margin'] == -50.0

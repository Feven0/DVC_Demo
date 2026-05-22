# Insurance Risk & Profitability Analytics

This repository is dedicated to analyzing historical insurance claim data to optimize risk and profitability for an insurance portfolio. The project implements a structured, reproducible development environment with versioned data tracking using DVC (Data Version Control) and continuous integration (CI) via GitHub Actions.

## Project Structure

```text
insurance-risk-analytics/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI pipeline (linting and testing)
├── data/                     # Tracked by DVC (not in Git)
│   ├── .gitignore             # DVC auto-generated ignore for data
│   └── MachineLearningRating_v3.txt.dvc  # DVC pointer file
├── notebooks/
│   ├── 01_eda.ipynb           # Task 1: Exploratory Data Analysis
│   ├── 02_hypothesis_testing.ipynb  # Task 2: Hypothesis Testing
│   └── 03_modeling.ipynb      # Task 3: Modeling & Evaluation
├── src/
│   ├── __init__.py
│   ├── data_loader.py         # Modular utility for data loading and preprocessing
│   ├── eda_utils.py           # Modular helper functions for plotting and analysis
│   ├── hypothesis_tests.py    # Modular helper functions for statistical testing
│   └── modeling.py            # Modular modeling pipelines
├── reports/
│   └── final_report.md        # Comprehensive findings and business insights
├── tests/                     # Unit tests for source code modules
├── .dvc/                      # DVC configuration
├── .gitignore                 # Git ignore file
├── dvc.yaml                   # DVC pipeline stages
├── requirements.txt           # Python dependency specifications
└── README.md                  # Project overview
```

## Logical Data Groups

The raw dataset contains 50+ variables organized into the following logical groups:

| Group | Key Fields |
| :--- | :--- |
| **Policy** | `UnderwrittenCoverID`, `PolicyID` |
| **Transaction** | `TransactionMonth` |
| **Client** | `IsVATRegistered`, `Citizenship`, `LegalType`, `Title`, `Language`, `Bank`, `AccountType`, `MaritalStatus`, `Gender` |
| **Location** | `Country`, `Province`, `PostalCode`, `MainCrestaZone`, `SubCrestaZone` |
| **Vehicle** | `ItemType`, `Mmcode`, `VehicleType`, `RegistrationYear`, `Make`, `Model`, `Cylinders`, `Cubiccapacity`, `Kilowatts`, `Bodytype`, `NumberOfDoors`, `VehicleIntroDate`, `CustomValueEstimate`, `AlarmImmobiliser`, `TrackingDevice`, `CapitalOutstanding`, `NewVehicle`, `WrittenOff`, `Rebuilt`, `Converted`, `CrossBorder`, `NumberOfVehiclesInFleet` |
| **Plan** | `SumInsured`, `TermFrequency`, `CalculatedPremiumPerTerm`, `ExcessSelected`, `CoverCategory`, `CoverType`, `CoverGroup`, `Section`, `Product`, `StatutoryClass`, `StatutoryRiskType` |
| **Payment & Claim** | `TotalPremium`, `TotalClaims` |

## Core Metrics

Two derived metrics are implemented to anchor the entire analysis:
*   **Loss Ratio (LR)**: `TotalClaims / TotalPremium` — The primary measure of portfolio profitability.
*   **Margin**: `TotalPremium - TotalClaims` — The net per-policy profit contribution.

## Getting Started

### Prerequisites

*   Python 3.10+
*   Git
*   DVC

### Setup Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/Feven0/DVC_Demo.git
   cd DVC_Demo
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

4. Pull data from DVC local/remote cache:
   ```bash
   dvc pull
   ```

## Data Version Control (DVC) Pipeline

This project uses **DVC** to version-control datasets and ensure full reproducibility of the data pipeline.

### How It Works

The data goes through two tracked versions:

| Version | Description | Git Commit Tag |
| :--- | :--- | :--- |
| **v1 (Raw)** | Original pipe-separated dataset as received | `v1: track raw insurance dataset with DVC` |
| **v2 (Cleaned)** | Preprocessed with standardized types, derived `LossRatio` and `Margin` columns | `v2: track cleaned/preprocessed insurance dataset` |

### Reproducing the Data Pipeline

1.  **Pull the raw data** from the DVC remote:
    ```bash
    dvc pull
    ```

2.  **Run the preprocessing pipeline** to regenerate the cleaned dataset:
    ```bash
    dvc repro
    ```
    This executes the `preprocess` stage defined in `dvc.yaml`, which reads the raw `MachineLearningRating_v3.txt` and outputs the cleaned `insurance_data.csv` with derived metrics.

3.  **Switch between data versions** using Git + DVC:
    ```bash
    # Check out the raw data version
    git log --oneline  # find the v1 commit hash
    git checkout <v1-commit-hash> -- data/insurance_data.csv.dvc
    dvc checkout

    # Check out the cleaned data version
    git checkout <v2-commit-hash> -- data/insurance_data.csv.dvc
    dvc checkout
    ```

4.  **Push new data versions** after modifications:
    ```bash
    dvc add data/insurance_data.csv
    git add data/insurance_data.csv.dvc
    git commit -m "v3: description of changes"
    dvc push
    git push
    ```

### DVC Remote Storage

The DVC remote is configured as a local directory outside the project:
```
Remote name: localstorage
Path: C:\Users\mesfi\OneDrive\Documents\KAIM\Week 3\dvc-storage
```

## Development and Testing

*   **Linting**: Run `flake8 src/` to check code style.
*   **Unit Tests**: Run `pytest tests/` to execute unit tests.

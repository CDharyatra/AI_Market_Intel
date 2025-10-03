#!/usr/bin/env python3
"""
Abstract Data Loader Classes
Provides a unified interface for loading data from different sources.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import pandas as pd
import json
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from config import (
    KAGGLE_CSV_PATH, KAGGLE_PARQUET_PATH, RAPIDAPI_JSONL_PATH,
    FALLBACK_ENCODINGS, DEFAULT_ENCODING
)


class DataLoader(ABC):
    """Abstract base class for data loaders."""
    
    def __init__(self, source_name: str):
        """
        Initialize the data loader.
        
        Args:
            source_name: Name of the data source
        """
        self.source_name = source_name
        self.data = None
    
    @abstractmethod
    def load(self) -> pd.DataFrame:
        """
        Load data from the source.
        
        Returns:
            DataFrame containing the loaded data
        """
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """
        Validate the loaded data.
        
        Returns:
            True if data is valid, False otherwise
        """
        pass
    
    def get_data(self) -> Optional[pd.DataFrame]:
        """
        Get the loaded data.
        
        Returns:
            DataFrame if data is loaded, None otherwise
        """
        return self.data
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of the loaded data.
        
        Returns:
            Dictionary with summary statistics
        """
        if self.data is None:
            return {"error": "No data loaded"}
        
        return {
            "source": self.source_name,
            "rows": len(self.data),
            "columns": len(self.data.columns),
            "column_names": list(self.data.columns),
            "memory_usage": f"{self.data.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB"
        }


class CSVDataLoader(DataLoader):
    """Data loader for CSV files."""
    
    def __init__(self, source_name: str, file_path: Path, required_columns: Optional[List[str]] = None):
        """
        Initialize CSV data loader.
        
        Args:
            source_name: Name of the data source
            file_path: Path to the CSV file
            required_columns: List of required columns (optional)
        """
        super().__init__(source_name)
        self.file_path = file_path
        self.required_columns = required_columns or []
    
    def load(self) -> pd.DataFrame:
        """Load data from CSV file with encoding fallback."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.file_path}")
        
        print(f"Loading {self.source_name} from CSV: {self.file_path}")
        
        # Try different encodings
        for encoding in FALLBACK_ENCODINGS:
            try:
                self.data = pd.read_csv(self.file_path, encoding=encoding)
                print(f"Successfully loaded with {encoding} encoding")
                print(f"Loaded {len(self.data)} rows, {len(self.data.columns)} columns")
                return self.data
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"Error with {encoding} encoding: {e}")
                continue
        
        # Final fallback with error handling
        print("Using error handling for encoding")
        self.data = pd.read_csv(self.file_path, encoding=DEFAULT_ENCODING, errors='replace')
        return self.data
    
    def validate(self) -> bool:
        """Validate the loaded CSV data."""
        if self.data is None or self.data.empty:
            print(f"Validation failed: No data loaded for {self.source_name}")
            return False
        
        # Check for required columns
        if self.required_columns:
            missing_columns = set(self.required_columns) - set(self.data.columns)
            if missing_columns:
                print(f"Validation failed: Missing columns: {missing_columns}")
                return False
        
        print(f"Validation passed for {self.source_name}")
        return True


class ParquetDataLoader(DataLoader):
    """Data loader for Parquet files."""
    
    def __init__(self, source_name: str, file_path: Path, required_columns: Optional[List[str]] = None):
        """
        Initialize Parquet data loader.
        
        Args:
            source_name: Name of the data source
            file_path: Path to the Parquet file
            required_columns: List of required columns (optional)
        """
        super().__init__(source_name)
        self.file_path = file_path
        self.required_columns = required_columns or []
    
    def load(self) -> pd.DataFrame:
        """Load data from Parquet file."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"Parquet file not found: {self.file_path}")
        
        print(f"Loading {self.source_name} from Parquet: {self.file_path}")
        self.data = pd.read_parquet(self.file_path)
        print(f"Loaded {len(self.data)} rows, {len(self.data.columns)} columns")
        return self.data
    
    def validate(self) -> bool:
        """Validate the loaded Parquet data."""
        if self.data is None or self.data.empty:
            print(f"Validation failed: No data loaded for {self.source_name}")
            return False
        
        # Check for required columns
        if self.required_columns:
            missing_columns = set(self.required_columns) - set(self.data.columns)
            if missing_columns:
                print(f"Validation failed: Missing columns: {missing_columns}")
                return False
        
        print(f"Validation passed for {self.source_name}")
        return True


class JSONLDataLoader(DataLoader):
    """Data loader for JSONL (JSON Lines) files."""
    
    def __init__(self, source_name: str, file_path: Path, required_fields: Optional[List[str]] = None):
        """
        Initialize JSONL data loader.
        
        Args:
            source_name: Name of the data source
            file_path: Path to the JSONL file
            required_fields: List of required fields (optional)
        """
        super().__init__(source_name)
        self.file_path = file_path
        self.required_fields = required_fields or []
        self.raw_data = []
    
    def load(self) -> pd.DataFrame:
        """Load data from JSONL file."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"JSONL file not found: {self.file_path}")
        
        print(f"Loading {self.source_name} from JSONL: {self.file_path}")
        
        self.raw_data = []
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    self.raw_data.append(json.loads(line.strip()))
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON at line {line_num}: {e}")
                    continue
        
        self.data = pd.DataFrame(self.raw_data)
        print(f"Loaded {len(self.data)} rows, {len(self.data.columns)} columns")
        return self.data
    
    def validate(self) -> bool:
        """Validate the loaded JSONL data."""
        if self.data is None or self.data.empty:
            print(f"Validation failed: No data loaded for {self.source_name}")
            return False
        
        # Check for required fields
        if self.required_fields:
            missing_fields = set(self.required_fields) - set(self.data.columns)
            if missing_fields:
                print(f"Validation failed: Missing fields: {missing_fields}")
                return False
        
        print(f"Validation passed for {self.source_name}")
        return True
    
    def get_raw_data(self) -> List[Dict[str, Any]]:
        """Get the raw JSON data (before DataFrame conversion)."""
        return self.raw_data


class ExcelDataLoader(DataLoader):
    """Data loader for Excel files."""
    
    def __init__(self, source_name: str, file_path: Path, sheet_name: str = 0, 
                 required_columns: Optional[List[str]] = None):
        """
        Initialize Excel data loader.
        
        Args:
            source_name: Name of the data source
            file_path: Path to the Excel file
            sheet_name: Sheet name or index (default: 0)
            required_columns: List of required columns (optional)
        """
        super().__init__(source_name)
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.required_columns = required_columns or []
    
    def load(self) -> pd.DataFrame:
        """Load data from Excel file."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"Excel file not found: {self.file_path}")
        
        print(f"Loading {self.source_name} from Excel: {self.file_path}")
        self.data = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        print(f"Loaded {len(self.data)} rows, {len(self.data.columns)} columns")
        return self.data
    
    def validate(self) -> bool:
        """Validate the loaded Excel data."""
        if self.data is None or self.data.empty:
            print(f"Validation failed: No data loaded for {self.source_name}")
            return False
        
        # Check for required columns
        if self.required_columns:
            missing_columns = set(self.required_columns) - set(self.data.columns)
            if missing_columns:
                print(f"Validation failed: Missing columns: {missing_columns}")
                return False
        
        print(f"Validation passed for {self.source_name}")
        return True


class DataLoaderFactory:
    """Factory class for creating data loaders based on file type."""
    
    @staticmethod
    def create_loader(source_type: str, source_name: str, file_path: Path, 
                     **kwargs) -> DataLoader:
        """
        Create a data loader based on the source type.
        
        Args:
            source_type: Type of data source ('csv', 'parquet', 'jsonl', 'excel')
            source_name: Name of the data source
            file_path: Path to the data file
            **kwargs: Additional arguments for specific loaders
            
        Returns:
            DataLoader instance
            
        Raises:
            ValueError: If source_type is not supported
        """
        loaders = {
            'csv': CSVDataLoader,
            'parquet': ParquetDataLoader,
            'jsonl': JSONLDataLoader,
            'excel': ExcelDataLoader
        }
        
        loader_class = loaders.get(source_type.lower())
        if loader_class is None:
            raise ValueError(f"Unsupported source type: {source_type}")
        
        return loader_class(source_name, file_path, **kwargs)


# Convenience functions for common data sources
def load_kaggle_data(use_parquet: bool = True) -> pd.DataFrame:
    """
    Load Kaggle Google Play Store data.
    
    Args:
        use_parquet: If True, load from parquet file, else from CSV
        
    Returns:
        DataFrame with Kaggle data
    """
    if use_parquet and KAGGLE_PARQUET_PATH.exists():
        loader = ParquetDataLoader(
            source_name="Kaggle Google Play Store",
            file_path=KAGGLE_PARQUET_PATH
        )
    else:
        loader = CSVDataLoader(
            source_name="Kaggle Google Play Store",
            file_path=KAGGLE_CSV_PATH
        )
    
    data = loader.load()
    if loader.validate():
        return data
    else:
        raise ValueError("Data validation failed")


def load_ios_data() -> pd.DataFrame:
    """
    Load iOS App Store data from RapidAPI.
    
    Returns:
        DataFrame with iOS data
    """
    loader = JSONLDataLoader(
        source_name="RapidAPI iOS App Store",
        file_path=RAPIDAPI_JSONL_PATH
    )
    
    data = loader.load()
    if loader.validate():
        return data
    else:
        raise ValueError("Data validation failed")


def load_combined_data() -> pd.DataFrame:
    """
    Load combined app store data.
    
    Returns:
        DataFrame with combined data
    """
    from config import COMBINED_APPS_PATH
    
    loader = ParquetDataLoader(
        source_name="Combined App Store Data",
        file_path=COMBINED_APPS_PATH
    )
    
    data = loader.load()
    if loader.validate():
        return data
    else:
        raise ValueError("Data validation failed")


if __name__ == "__main__":
    # Test the data loaders
    print("Testing Data Loaders...")
    print("=" * 50)
    
    # Test Kaggle loader
    try:
        print("\n1. Testing Kaggle Data Loader:")
        kaggle_data = load_kaggle_data()
        print(f"Successfully loaded Kaggle data: {len(kaggle_data)} rows")
    except Exception as e:
        print(f"Kaggle loader failed: {e}")
    
    # Test iOS loader
    try:
        print("\n2. Testing iOS Data Loader:")
        ios_data = load_ios_data()
        print(f"Successfully loaded iOS data: {len(ios_data)} rows")
    except Exception as e:
        print(f"iOS loader failed: {e}")
    
    # Test Combined loader
    try:
        print("\n3. Testing Combined Data Loader:")
        combined_data = load_combined_data()
        print(f"Successfully loaded combined data: {len(combined_data)} rows")
    except Exception as e:
        print(f"Combined loader failed: {e}")
    
    print("\n" + "=" * 50)
    print("Data loader tests completed!")

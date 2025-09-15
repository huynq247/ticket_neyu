import pandas as pd
import numpy as np
from typing import List, Dict, Any, Union, Optional
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from scipy import stats
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataNormalizer:
    """
    Data normalization component for analytics
    Provides various methods to normalize, standardize, and transform data
    """
    
    def __init__(self):
        self.scalers = {}
    
    def normalize_minmax(
        self, 
        df: pd.DataFrame, 
        columns: List[str] = None, 
        feature_range: tuple = (0, 1),
        persist_scaler: bool = False,
        scaler_id: str = None
    ) -> pd.DataFrame:
        """
        Normalize data using Min-Max scaling
        
        Args:
            df: Input DataFrame
            columns: Columns to normalize (if None, all numeric columns)
            feature_range: Output range for normalized values
            persist_scaler: Whether to store the scaler for future use
            scaler_id: ID to store the scaler (required if persist_scaler=True)
            
        Returns:
            DataFrame with normalized columns
        """
        # Create a copy of the DataFrame to avoid modifying the original
        result_df = df.copy()
        
        # If no columns specified, use all numeric columns
        if columns is None:
            columns = result_df.select_dtypes(include=['number']).columns.tolist()
        
        # Create a scaler
        scaler = MinMaxScaler(feature_range=feature_range)
        
        # Normalize the specified columns
        if columns:
            result_df[columns] = scaler.fit_transform(result_df[columns])
            
            # Store the scaler if requested
            if persist_scaler and scaler_id:
                self.scalers[scaler_id] = scaler
        
        return result_df
    
    def standardize(
        self, 
        df: pd.DataFrame, 
        columns: List[str] = None,
        robust: bool = False,
        persist_scaler: bool = False,
        scaler_id: str = None
    ) -> pd.DataFrame:
        """
        Standardize data (zero mean, unit variance)
        
        Args:
            df: Input DataFrame
            columns: Columns to standardize (if None, all numeric columns)
            robust: Whether to use robust scaling (median/IQR instead of mean/std)
            persist_scaler: Whether to store the scaler for future use
            scaler_id: ID to store the scaler (required if persist_scaler=True)
            
        Returns:
            DataFrame with standardized columns
        """
        # Create a copy of the DataFrame to avoid modifying the original
        result_df = df.copy()
        
        # If no columns specified, use all numeric columns
        if columns is None:
            columns = result_df.select_dtypes(include=['number']).columns.tolist()
        
        # Create a scaler
        if robust:
            scaler = RobustScaler()
        else:
            scaler = StandardScaler()
        
        # Standardize the specified columns
        if columns:
            result_df[columns] = scaler.fit_transform(result_df[columns])
            
            # Store the scaler if requested
            if persist_scaler and scaler_id:
                self.scalers[scaler_id] = scaler
        
        return result_df
    
    def transform_with_stored_scaler(
        self,
        df: pd.DataFrame,
        scaler_id: str,
        columns: List[str] = None
    ) -> pd.DataFrame:
        """
        Transform data using a previously stored scaler
        
        Args:
            df: Input DataFrame
            scaler_id: ID of the stored scaler
            columns: Columns to transform (if None, all numeric columns)
            
        Returns:
            DataFrame with transformed columns
        """
        # Check if scaler exists
        if scaler_id not in self.scalers:
            raise ValueError(f"No scaler found with ID: {scaler_id}")
        
        # Create a copy of the DataFrame to avoid modifying the original
        result_df = df.copy()
        
        # If no columns specified, use all numeric columns
        if columns is None:
            columns = result_df.select_dtypes(include=['number']).columns.tolist()
        
        # Get the scaler
        scaler = self.scalers[scaler_id]
        
        # Transform the specified columns
        if columns:
            result_df[columns] = scaler.transform(result_df[columns])
        
        return result_df
    
    def remove_outliers(
        self,
        df: pd.DataFrame,
        columns: List[str] = None,
        method: str = 'zscore',
        threshold: float = 3.0,
        replace_with: Optional[Union[str, float]] = None
    ) -> pd.DataFrame:
        """
        Remove or replace outliers in the data
        
        Args:
            df: Input DataFrame
            columns: Columns to process (if None, all numeric columns)
            method: Outlier detection method ('zscore', 'iqr', 'percentile')
            threshold: Threshold for outlier detection
            replace_with: Value to replace outliers with (None to remove rows)
            
        Returns:
            DataFrame with outliers removed or replaced
        """
        # Create a copy of the DataFrame to avoid modifying the original
        result_df = df.copy()
        
        # If no columns specified, use all numeric columns
        if columns is None:
            columns = result_df.select_dtypes(include=['number']).columns.tolist()
        
        # Process each column
        for column in columns:
            if method == 'zscore':
                # Z-score method
                z_scores = np.abs(stats.zscore(result_df[column], nan_policy='omit'))
                outliers = z_scores > threshold
                
            elif method == 'iqr':
                # IQR method
                q1 = result_df[column].quantile(0.25)
                q3 = result_df[column].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - threshold * iqr
                upper_bound = q3 + threshold * iqr
                outliers = (result_df[column] < lower_bound) | (result_df[column] > upper_bound)
                
            elif method == 'percentile':
                # Percentile method
                lower_bound = result_df[column].quantile(threshold / 100)
                upper_bound = result_df[column].quantile(1 - threshold / 100)
                outliers = (result_df[column] < lower_bound) | (result_df[column] > upper_bound)
            
            else:
                raise ValueError(f"Unknown outlier detection method: {method}")
            
            # Replace or remove outliers
            if replace_with is not None:
                if replace_with == 'mean':
                    result_df.loc[outliers, column] = result_df[column].mean()
                elif replace_with == 'median':
                    result_df.loc[outliers, column] = result_df[column].median()
                elif replace_with == 'mode':
                    result_df.loc[outliers, column] = result_df[column].mode()[0]
                else:
                    result_df.loc[outliers, column] = replace_with
            else:
                # Remove rows with outliers
                result_df = result_df[~outliers]
        
        return result_df
    
    def fill_missing_values(
        self,
        df: pd.DataFrame,
        columns: List[str] = None,
        method: str = 'mean'
    ) -> pd.DataFrame:
        """
        Fill missing values in the data
        
        Args:
            df: Input DataFrame
            columns: Columns to process (if None, all columns)
            method: Method to fill missing values ('mean', 'median', 'mode', 'ffill', 'bfill', 'interpolate')
            
        Returns:
            DataFrame with missing values filled
        """
        # Create a copy of the DataFrame to avoid modifying the original
        result_df = df.copy()
        
        # If no columns specified, use all columns
        if columns is None:
            columns = result_df.columns.tolist()
        
        # Process each column
        for column in columns:
            if result_df[column].isna().any():
                if method == 'mean' and pd.api.types.is_numeric_dtype(result_df[column]):
                    result_df[column] = result_df[column].fillna(result_df[column].mean())
                    
                elif method == 'median' and pd.api.types.is_numeric_dtype(result_df[column]):
                    result_df[column] = result_df[column].fillna(result_df[column].median())
                    
                elif method == 'mode':
                    result_df[column] = result_df[column].fillna(result_df[column].mode()[0])
                    
                elif method == 'ffill':
                    result_df[column] = result_df[column].fillna(method='ffill')
                    
                elif method == 'bfill':
                    result_df[column] = result_df[column].fillna(method='bfill')
                    
                elif method == 'interpolate' and pd.api.types.is_numeric_dtype(result_df[column]):
                    result_df[column] = result_df[column].interpolate()
                    
                else:
                    logger.warning(f"Cannot apply method '{method}' to column '{column}'")
        
        return result_df
    
    def normalize_categorical(
        self,
        df: pd.DataFrame,
        columns: List[str],
        method: str = 'one-hot'
    ) -> pd.DataFrame:
        """
        Normalize categorical variables
        
        Args:
            df: Input DataFrame
            columns: Categorical columns to normalize
            method: Normalization method ('one-hot', 'label')
            
        Returns:
            DataFrame with normalized categorical variables
        """
        # Create a copy of the DataFrame to avoid modifying the original
        result_df = df.copy()
        
        if method == 'one-hot':
            # One-hot encoding
            for column in columns:
                one_hot = pd.get_dummies(result_df[column], prefix=column)
                result_df = pd.concat([result_df, one_hot], axis=1)
                result_df = result_df.drop(column, axis=1)
                
        elif method == 'label':
            # Label encoding
            for column in columns:
                unique_values = result_df[column].unique()
                value_map = {value: i for i, value in enumerate(unique_values)}
                result_df[column] = result_df[column].map(value_map)
                
        else:
            raise ValueError(f"Unknown categorical normalization method: {method}")
        
        return result_df
    
    def normalize_time_series(
        self,
        df: pd.DataFrame,
        date_column: str,
        value_column: str,
        method: str = 'diff',
        period: int = 1
    ) -> pd.DataFrame:
        """
        Normalize time series data
        
        Args:
            df: Input DataFrame
            date_column: Column containing dates
            value_column: Column containing values
            method: Normalization method ('diff', 'pct_change', 'rolling')
            period: Period for differencing or rolling window
            
        Returns:
            DataFrame with normalized time series
        """
        # Create a copy of the DataFrame to avoid modifying the original
        result_df = df.copy()
        
        # Sort by date
        result_df = result_df.sort_values(by=date_column)
        
        if method == 'diff':
            # Differencing
            result_df[f'{value_column}_norm'] = result_df[value_column].diff(period)
            
        elif method == 'pct_change':
            # Percentage change
            result_df[f'{value_column}_norm'] = result_df[value_column].pct_change(period)
            
        elif method == 'rolling':
            # Rolling normalization
            result_df[f'{value_column}_norm'] = result_df[value_column] / result_df[value_column].rolling(window=period).mean()
            
        else:
            raise ValueError(f"Unknown time series normalization method: {method}")
        
        return result_df
    
    def normalize_across_groups(
        self,
        df: pd.DataFrame,
        group_column: str,
        value_column: str,
        method: str = 'zscore'
    ) -> pd.DataFrame:
        """
        Normalize values within groups
        
        Args:
            df: Input DataFrame
            group_column: Column to group by
            value_column: Column to normalize
            method: Normalization method ('zscore', 'minmax', 'robust')
            
        Returns:
            DataFrame with values normalized within groups
        """
        # Create a copy of the DataFrame to avoid modifying the original
        result_df = df.copy()
        
        # Group by the specified column
        groups = result_df.groupby(group_column)
        
        if method == 'zscore':
            # Z-score normalization within groups
            result_df[f'{value_column}_norm'] = groups[value_column].transform(lambda x: (x - x.mean()) / x.std())
            
        elif method == 'minmax':
            # Min-max normalization within groups
            result_df[f'{value_column}_norm'] = groups[value_column].transform(lambda x: (x - x.min()) / (x.max() - x.min()))
            
        elif method == 'robust':
            # Robust normalization within groups
            result_df[f'{value_column}_norm'] = groups[value_column].transform(
                lambda x: (x - x.median()) / (x.quantile(0.75) - x.quantile(0.25))
            )
            
        else:
            raise ValueError(f"Unknown group normalization method: {method}")
        
        return result_df
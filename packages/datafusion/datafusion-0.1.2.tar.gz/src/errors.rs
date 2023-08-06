use core::fmt;

use arrow::error::ArrowError;
use datafusion::error::ExecutionError;
use pyo3::{exceptions, PyErr};

#[derive(Debug)]
pub enum DataFusionError {
    ExecutionError(ExecutionError),
    ArrowError(ArrowError),
    Common(String),
}

impl fmt::Display for DataFusionError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            DataFusionError::ExecutionError(e) => write!(f, "DataFusion error: {:?}", e),
            DataFusionError::ArrowError(e) => write!(f, "Arrow error: {:?}", e),
            DataFusionError::Common(e) => write!(f, "{}", e),
        }
    }
}

impl From<DataFusionError> for PyErr {
    fn from(err: DataFusionError) -> PyErr {
        exceptions::PyException::new_err(err.to_string())
    }
}

impl From<ExecutionError> for DataFusionError {
    fn from(err: ExecutionError) -> DataFusionError {
        DataFusionError::ExecutionError(err)
    }
}

impl From<ArrowError> for DataFusionError {
    fn from(err: ArrowError) -> DataFusionError {
        DataFusionError::ArrowError(err)
    }
}

pub(crate) fn wrap<T>(a: Result<T, ExecutionError>) -> Result<T, DataFusionError> {
    Ok(a?)
}

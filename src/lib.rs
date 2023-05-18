mod api;
mod plot;
use pyo3::prelude::*;

#[pymodule]
fn stonks(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(api::get_symbols, m)?)?;
    m.add_function(wrap_pyfunction!(api::get_daily_historical_data, m)?)?;
    m.add_function(wrap_pyfunction!(plot::graph, m)?)?;

    Ok(())
}
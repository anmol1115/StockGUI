use reqwest::{self, Error};
use pyo3::{pyfunction, exceptions::PyOSError, PyErr};

#[derive(Debug)]
pub struct MyError(Error);

impl ToString for MyError {
    fn to_string(&self) -> String {
        self.0.to_string()
    }
}

impl std::convert::From<MyError> for PyErr {
    fn from(err: MyError) -> PyErr {
        PyOSError::new_err(err.to_string())
    }
}

impl std::convert::From<Error> for MyError {
    fn from(err: Error) -> Self {
        MyError(err)
    }
}

#[pyfunction]
pub fn get_symbols(partial_symbol: &str, api_key: &str) -> Result<Vec<Vec<String>>, MyError> {
    let url = format!("https://alpha-vantage.p.rapidapi.com/query?keywords={}&function=SYMBOL_SEARCH&datatype=csv", partial_symbol);

    let client = reqwest::blocking::Client::new();
    let response = client.get(url)
    .header("X-RapidAPI-Host", "alpha-vantage.p.rapidapi.com")
    .header("X-RapidAPI-Key", api_key)
    .send()?
    .text()?;

    let mut symbols = Vec::new();
    response.split("\r\n")
    .enumerate()
    .filter(|&(i, resp)| i != 0 && resp != "")
    .for_each(|(_, resp)| {
        let values: Vec<&str> = resp.split(",").collect();
        symbols.push(vec![values[0].to_string(), values[1].to_string()])
    });

    Ok(symbols)
}

#[pyfunction]
pub fn get_daily_historical_data(symbol: &str, api_key: &str) -> Result<(Vec<String>, Vec<Vec<String>>), MyError> {
    let url = format!("https://alpha-vantage.p.rapidapi.com/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&outputsize=compact&datatype=csv", symbol);

    let client = reqwest::blocking::Client::new();
    let response = client.get(url)
    .header("X-RapidAPI-Host", "alpha-vantage.p.rapidapi.com")
    .header("X-RapidAPI-Key", api_key)
    .send()?
    .text()?;

    let mut dates = Vec::new();
    let mut data = Vec::new();
    response.split("\r\n")
    .enumerate()
    .filter(|&(i, resp)| i != 0 && resp != "")
    .for_each(|(_, resp)| {
        let values: Vec<&str> = resp.split(",").collect();
        dates.push(values[0].to_string());
        data.push(vec![values[1].to_string(), values[2].to_string(), values[3].to_string(), values[4].to_string(), values[5].to_string(), values[6].to_string()])
    });

    Ok((dates, data))
}
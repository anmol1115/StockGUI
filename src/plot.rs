use plotters::prelude::*;
use std::num::ParseFloatError;
use pyo3::{pyfunction, exceptions::PyOSError, PyErr};
use chrono::DateTime;
use chrono::format::{ParseResult, ParseError};
use chrono::offset::{Local, TimeZone};

pub enum MyError {
    ChronoParseError(ParseError),
    RustParseFloatError(ParseFloatError),
    PlotterError(String)
}

impl ToString for MyError {
    fn to_string(&self) -> String {
        match self {
            MyError::ChronoParseError(err) => err.to_string(),
            MyError::RustParseFloatError(err) => err.to_string(),
            MyError::PlotterError(err) => err.to_string()
        }
    }
}

impl std::convert::From<MyError> for PyErr {
    fn from(err: MyError) -> PyErr {
        PyOSError::new_err(err.to_string())
    }
}

impl std::convert::From<ParseError> for MyError {
    fn from(err: ParseError) -> Self {
        MyError::ChronoParseError(err)
    }
}

impl std::convert::From<ParseFloatError> for MyError {
    fn from(err: ParseFloatError) -> Self {
        MyError::RustParseFloatError(err)
    }
}

fn parse_time(date_str: &str) -> ParseResult<DateTime<Local>> {
    Local
    .datetime_from_str(&format!("{} 0:0", date_str), "%Y-%m-%d %H:%M")
}

fn process(data: Vec<Vec<String>>) -> Result<(f32, f32, Vec<Vec<f32>>), ParseFloatError> {
    let mut min = 1000.00;
    let mut max = 0.0;

    let mut out = vec![];
    for row in data {
        let mut new_row = vec![];
        for (i, element) in row.iter().enumerate() {
            if i == 4 {
                continue;
            }
            new_row.push(element.parse::<f32>()?);
        }
        if new_row[0] < min {
            min = new_row[0];
        }
        if new_row[0] > max {
            max = new_row[0];
        }
        out.push(new_row);
    }

    Ok((min-0.05*min, max+0.05*max, out))
}

#[pyfunction]
pub fn graph(dates: Vec<String>, data: Vec<Vec<String>>) -> Result<(), MyError> {
    let end_date = parse_time(&dates[0])?.date();
    let start_date = parse_time(dates.last().unwrap())?.date();
    
    let (min_y, max_y, data) = process(data)?;
    
    let root = BitMapBackend::new("plotters-doc-data/0.png", (640, 480)).into_drawing_area();
    if let Err(e) = root.fill(&WHITE) {
        return Err(MyError::PlotterError(e.to_string()))
    };
    let mut chart = match ChartBuilder::on(&root)
    .caption("Stonk", ("sans-serif", 50).into_font())
    .margin(5)
    .x_label_area_size(30)
    .y_label_area_size(30)
    .build_cartesian_2d(start_date..end_date, min_y..max_y) {
        Ok(context) => context,
        Err(e) => return Err(MyError::PlotterError(e.to_string()))
    };
    
    if let Err(e) = chart.configure_mesh().x_labels(6).draw() {
        return Err(MyError::PlotterError(e.to_string()))
    };
    
    chart.draw_series(
        dates.iter().enumerate().map(|(i, date)| {
            CandleStick::new(parse_time(date).expect("This should not fail :(.").date(), data[i][0], data[i][1], data[i][2], data[i][3], GREEN.filled(), RED, 15)
        })
    );
    
    if let Err(e) = root.present() {
        return Err(MyError::PlotterError(e.to_string()))
    };
    Ok(())
}
# GovEase Property Research & Tax Analysis

A Python automation tool designed to streamline property research and tax-sale analysis. The application collects parcel information from GovEase, organizes property records, estimates acreage from legal descriptions, generates PDF reports, and assists with property lookups across county and state systems.

## Features

- **Automated Data Collection:** Uses Selenium to collect property and parcel information from GovEase.
- **Acreage Estimation:** Analyzes legal descriptions using multiple parsing methods to estimate property size and identify parcels of at least half an acre.
- **CSV Data Management:** Exports parcel records into organized CSV files, including separate reports for records with unknown acreage results.
- **PDF Report Generation:** Creates formatted property reports with parcel numbers, owner information, property values, legal descriptions, and page numbering.
- **Custom PDF Filtering:** Filters property records based on owner location and generates customized PDF reports.
- **County Property Lookup:** Automates parcel searches through county property assessment websites.
- **State Property Lookup:** Automates parcel searches through Alabama property tax systems.
- **Tax Information Collection:** Checks property tax amounts and exports the results to CSV.
- **Interactive CLI:** Provides a menu-driven terminal interface for accessing the application's features.
- **Environment-Based Credentials:** Loads login credentials from environment variables.

## Technologies

- Python
- Selenium
- Pandas
- ReportLab
- python-dotenv
- Regular Expressions
- CSV Data Processing
- Chrome WebDriver

## Project Structure

```text
GovEase-Program/
├── main.py
├── .env
├── property_data/
└── __gov/
    ├── __init__.py
    ├── acerage_solver.py
    ├── county_lookup.py
    ├── goveease.py
    ├── helpers.py
    ├── pdf_filter.py
    ├── pdf_generator.py
    └── state_lookup.py
```

## Installation

1. Install Python 3.10 or newer.
2. Clone the repository.
3. Install the required dependencies:

```bash
pip install selenium webdriver-manager pandas reportlab python-dotenv
```

4. Install Google Chrome.
5. Create a `.env` file in the project root and configure your credentials:

```env
USER=your_username
PASSWORD=your_password
```

6. Run the application:

```bash
python main.py
```

## Usage

Launch the application and select an option from the main menu.

### PDF Generator

Generate formatted PDF reports for qualifying properties or create custom reports using owner-location filters.

### Acreage Solver

Process collected parcel records and identify properties that meet the half-acre threshold based on their legal descriptions.

### Lookup Systems

Navigate county and state property lookup systems to review parcel information and check taxes due.

### GovEase Data Collector

Log in to GovEase, select counties, collect parcel information, estimate acreage, and export the results for further analysis.

## Output Files

The application generates several types of output:

- **`property_data/`** — Collected parcel data in CSV format.
- **`property_data/unknown/`** — Records where acreage could not be determined.
- **`tax_info/`** — Generated property PDF reports.
- **`Customed Filter PDFs/`** — Custom-filtered PDF reports.
- **`moneys.csv`** — Exported property tax lookup results.

## Security

- Store credentials in environment variables rather than hardcoding them into source files.
- Keep `.env` out of version control by adding it to `.gitignore`.
- Do not publish account credentials, private property records, or other sensitive data in the repository.

## Important Notes

- Website layouts and element selectors can change, requiring updates to the Selenium automation.
- Acreage estimates derived from legal descriptions are heuristic calculations and should be verified against authoritative property records.
- Confirm tax amounts and parcel details with the appropriate county or state authority before making financial or legal decisions.

## License

No license is specified. Add a license file if you intend to grant others permission to use, modify, or distribute this project.

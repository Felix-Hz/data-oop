# Imports Analysis from Customs Data

This project provides a refactorization of an Imports Analysis from Customs Data in Argentina, Brazil, Uruguay, Paraguay, and other countries for specific tariff codes project done in the past. In here, I selected only Peru and refactorized old functions in an OOP approach and implementing Type Hints as stated in PEP 484. The original analysis focused on the tariff codes `283525`, `283526`, `310430`, and `230990` and involved over 150 cleaned and standardized databases.

## Project Overview
The main goal of this project is to perform a comprehensive analysis of import data using Jupyter Notebooks and Python. The project utilizes a modularized codebase and follows an object-oriented programming (OOP) approach. The code has been refactored from older functions to improve readability, organization, and maintainability. Additionally, type hints have been implemented to enhance code documentation and readability.

## Key Features
- **Data Cleaning and Standardization:** The project involves cleaning and standardizing over 150 databases, ensuring consistency and accuracy in the analysis.
- **Statistical Analysis:** Various statistical techniques are applied to analyze the price behavior, total volume per country and per origin, and other relevant factors.
- **Top Importers Analysis:** The code identifies the top 3 importers for each country on each year, providing valuable insights into import trends.
- **Automated Report Generation:** Using the `export_API.py` module from the `utils` package, the project generates automated reports in Google Sheets, facilitating easy visualization and sharing of analysis results.

## Getting Started
To use this codebase, follow these steps:
1. Clone the repository from GitHub.
2. Install the required dependencies specified in the `requirements.txt` file.
3. Prepare the import databases and ensure they are in the appropriate format.
4. Modify the code or scripts as needed to suit your specific analysis requirements.
5. Execute the desired scripts or use the provided functions to perform the imports analysis.
6. Utilize the `export_API.py` module to generate automated reports in Google Sheets.

## Documentation
Detailed documentation for each module, including function descriptions, arguments, and return types, can be found within the codebase. Refer to the relevant modules and functions for in-depth information.

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

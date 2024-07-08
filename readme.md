
# Construction P069 Phase 3 and Phase 4 EDA

This repository contains the Exploratory Data Analysis (EDA) for the Liverpool Queens Day Care project. The EDA is divided into Phase 3 and Phase 4, conducted for an engineering company to assist in project management and decision-making. The data was sourced from Odoo, exported as Excel and PDF files. A Python script was created to process these files, enabling the analysis within Jupyter Notebooks. Additionally, a Streamlit app was developed to host the dashboard for stakeholders, engineers, and the YMCA.

## Table of Contents
- [Project Overview](#project-overview)
- [Data Sources](#data-sources)
- [Phase 3 Analysis](#phase-3-analysis)
- [Phase 4 Analysis](#phase-4-analysis)
- [Streamlit Dashboard](#streamlit-dashboard)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
The Liverpool Queens Day Care project involves a detailed analysis of construction data to monitor overtime and regular hours, project length, task overlaps, expenses, and purchases. This repository provides insights into these aspects through visualizations and tables.

## Data Sources
- **Odoo Exports**: Data was exported from Odoo in Excel and PDF formats.
- **Python Scripts**: Custom scripts were created to parse and clean the data for analysis.

## Phase 3 Analysis
### 1. Overtime and Regular Hour Analysis
- **Metrics**: Per employee, per week, per task.
- **Tasks**: Groundwork, Foundation, Framing, Roofing, Siding.
- **Visualizations**: Plots and tables showing time allocation and overlaps between tasks.

### 2. Expenses and Purchase Analysis
- **Metrics**: Monthly expenses, expenses per task, purchases per subcontract, purchases per month.
- **Visualizations**: Plots and tables illustrating expense distribution and purchase trends.

## Phase 4 Analysis
### 1. Overtime and Regular Hour Analysis
- **Metrics**: Per employee, per week, per task.
- **Tasks**: Interior Framing, Insulation, Drywall, Paint.
- **Visualizations**: Plots and tables showing time allocation and overlaps between tasks.

### 2. Expenses and Purchase Analysis
- **Metrics**: Monthly expenses, expenses per task, purchases per subcontract, purchases per month.
- **Visualizations**: Plots and tables illustrating expense distribution and purchase trends.

## Streamlit Dashboard
A Streamlit app was developed to host an interactive dashboard for stakeholders, engineers, and the YMCA. This dashboard provides easy access to the analyses and visualizations from both phases.

## Installation
To run the analyses and the Streamlit app locally, follow these steps:
1. Clone this repository:
   \`\`\`bash
   git clone https://github.com/yourusername/Construction-P069-Phase3-Phase4-EDA.git
   \`\`\`
2. Install the required dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

## Usage
1. Run the Jupyter Notebooks to perform the EDA:
   \`\`\`bash
   jupyter notebook
   \`\`\`
2. Launch the Streamlit app:
   \`\`\`bash
   streamlit run app.py
   \`\`\`

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

# WAGRIMS | World Affairs & Geopolitical Risk Intelligence Monitoring System

### Interactive Data Analytics & Geopolitical Conflict Monitoring Platform

<p align="center">
  <strong>Exploring global conflict patterns, event frequency, regional instability, and human impact through interactive data visualization.</strong>
</p>

---

## 🌍 Project Overview

**WAGRIMS** is an interactive data analytics and visualization project designed to explore global conflict events and understand their impact across different countries and regions.

The project uses historical conflict data to identify patterns in event frequency, fatalities, event categories, and regional distributions.

Built using Python, Pandas, Plotly, and Dash, WAGRIMS transforms raw conflict records into meaningful visual insights through an interactive analytical dashboard with dynamic filters and professional visualizations.

The dashboard allows users to explore conflict trends across countries, regions, event categories, and years through a unified interface.

## 🎯 Project Objectives

- Analyze historical conflict patterns across different countries and regions.
- Identify countries experiencing the highest numbers of conflict events and fatalities.
- Examine the relationship between conflict events and human impact.
- Identify event categories associated with the highest fatalities.
- Explore yearly changes in conflict intensity.
- Compare regional conflict patterns.
- Present complex datasets through interactive and understandable visualizations.

## ✨ Key Features

### 1. Interactive Dashboard
- Professional dark-themed dashboard interface.
- Dynamic filtering by region and country.
- Event category selection.
- Interactive year-range filtering.
- Automatically updated KPIs and visualizations.

### 2. Conflict Analysis
- Yearly conflict event trends.
- Yearly fatality trends.
- Country-wise event distribution.
- Country-wise fatality comparison.
- High-impact event category analysis.
- Sub-event category exploration.

### 3. Key Performance Indicators (KPIs)

The dashboard provides important analytical indicators, including:

- Total recorded events.
- Total recorded fatalities.
- Number of countries analyzed.
- Number of event categories.
- Average fatalities per recorded event.

### 4. Interactive Visualizations

Visualizations are powered by Plotly and support interactive exploration, hover information, zooming, and filtering.

## 📊 Analytical Insights

The project focuses on answering important questions:

| Analytical Question | Purpose |
|---|---|
| Which countries experience the most conflict events? | Identify highly affected countries. |
| Which countries record the highest fatalities? | Understand the distribution of human impact. |
| Which event categories cause the most fatalities? | Identify high-impact event types. |
| How do conflict events change over time? | Understand yearly trends. |
| Which regions experience greater conflict intensity? | Compare regional instability. |
| How do sub-event categories contribute to fatalities? | Explore detailed conflict patterns. |

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data cleaning and manipulation |
| NumPy | Numerical operations |
| Plotly | Interactive data visualization |
| Dash | Interactive web dashboard |
| HTML & CSS | Dashboard layout and styling |
| Jupyter Notebook | Exploratory Data Analysis |
| Git & GitHub | Version control and project hosting |

## 📁 Project Structure

```text
WAGRIMS/
│
├── dashboard/
│   ├── app.py
│   └── assets/
│       └── wagirms_dark.css
│
├── data/
│   ├── raw/
│   │   └── middle_east.csv
│   │
│   └── processed/
│       └── cleaned_conflict_data.csv
│
├── notebooks/
│   ├── Data_cleaning.ipynb
│   └── Eda.ipynb
│
├── reports/
│   ├── country_event_heatmap.html
│   ├── event_type_fatalities.html
│   ├── population_vs_fatalities.html
│   ├── sub_event_treemap.html
│   ├── top5_countries_fatalities.html
│   ├── yearly_fatalities.html
│   └── other analytical reports
│
├── .gitignore
├── README.md
└── requirements.txt
```

## ⚙️ Installation & Setup

Follow these steps to run WAGRIMS locally.

### Prerequisites

- Python 3.10 or later
- Git
- Visual Studio Code (recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/amulyasrivastava1408-cell/WAGRIMS.git
```

### 2. Navigate to the Project Directory

```bash
cd WAGRIMS
```

### 3. Create a Virtual Environment

**Windows:**

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the Dashboard

```bash
python dashboard/app.py
```

### 6. Open in Your Browser

Visit:

```text
http://127.0.0.1:8050/
```

The interactive WAGRIMS dashboard should now be available locally.

## 📈 Data Analysis Workflow

The project follows a structured data analytics workflow:

1. **Data Collection:** Load the available historical conflict dataset.
2. **Data Cleaning:** Handle data types, missing values, and inconsistencies.
3. **Exploratory Data Analysis:** Examine countries, regions, events, sub-events, and fatalities.
4. **Data Aggregation:** Calculate yearly, country-wise, regional, and event-wise statistics.
5. **Data Visualization:** Build interactive charts using Plotly.
6. **Dashboard Development:** Integrate analytical outputs into a Dash application.
7. **Insight Generation:** Interpret patterns and communicate findings through visual analytics.

## 🎨 Dashboard Design

WAGRIMS uses a professional dark interface designed for analytical exploration.

Design elements include:

- Dark navy background.
- High-contrast typography.
- Blue, purple, green, and red analytical accents.
- Interactive filters and charts.
- Consistent KPI cards.
- Responsive dashboard layout.

## 🔍 Future Enhancements

Potential future improvements include:

- Live or regularly updated conflict datasets.
- Geographic conflict intensity maps.
- Advanced statistical analysis.
- Predictive conflict trend modelling.
- Population-normalized fatality comparisons.
- Regional comparison reports.
- Downloadable analytical reports.
- Cloud-hosted dashboard deployment.

## ⚠️ Data & Interpretation Notes

- The dashboard analyzes historical records available in the project's dataset.
- Recorded fatalities represent the values contained in the source data.
- Historical patterns should not automatically be interpreted as predictions of future conflicts.
- Data completeness, reporting practices, and source definitions may influence comparisons.
- Population-based comparisons should account for the population reference year and coverage of the dataset.

## 👨‍💻 Author

**Amulya Srivastava**

Data Analytics | Python | Data Visualization | Exploratory Data Analysis

GitHub: [@amulyasrivastava1408-cell](https://github.com/amulyasrivastava1408-cell)

## ⭐ Support

If you find this project interesting or useful, consider giving the repository a ⭐ on GitHub.

Your support is appreciated!

---

<p align="center">
  <strong>WAGRIMS — Turning Conflict Data into Meaningful Insights.</strong>
</p>

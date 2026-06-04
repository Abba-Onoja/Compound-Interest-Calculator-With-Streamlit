# Compound-Interest-Calculator-With-Streamlit

---

## Project Overview

This project is a simple streamlit web application built to compare two different investment scenarios. I developed this tool as a practical exercise to get comfortable with the **Streamlit** framework, specifically focusing on reactive state management, custom CSS injection, and integrating interactive **Plotly** visualizations within a data dashboard.

The application allows users to input various financial parameters such as initial deposits, recurring contributions, and varying rates of return to visualize how small changes in interest or frequency can drastically alter long-term wealth accumulation.

---

## Key Features

* **Dual Scenario Comparison:** View two financial trajectories simultaneously to see the impact of a 1% or 2% difference in annual returns.
* **Flexible Compounding Logic:** Handles daily, monthly, and annual compounding frequencies, even when contribution schedules (e.g., monthly deposits) do not match the compounding periods.
* **Interactive Visualizations:**
* **Growth Line Chart:** Tracks the total portfolio balance over the selected timeframe.
* **Annual Interest Histogram:** Breaks down exactly how much interest is earned each specific year, highlighting the "snowball effect" of compound interest.
* **Data Portability:** Includes a data table and a CSV export feature for further analysis in Excel or other BI tools.

---

## The Technical Stack

* **Python:** The core language.
* **Streamlit:** Used for the front-end.
* **Pandas:** Handles data processing and creates the dataframes for the yearly breakdowns.
* **Plotly Express:** Used for the interactive charts.

---

## Calculation Logic

The backend uses a standard future value formula for both the initial principal and a series of periodic contributions (annuity). To handle cases where compounding and contributions happen at different intervals, the app calculates an effective interest rate per payment period ($r_p$).

The core formula used for the growth of recurring contributions is:

$$FV = C \times \frac{(1 + r_p)^n - 1}{r_p}$$

Where:

* $C$ = Contribution amount
* $r_p$ = Effective interest rate per period
* $n$ = Total number of contribution periods

---

## How to Run the Project

To run this application locally, ensure you have Python installed, then follow these steps:

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/Compound-Interest-Calculator-With-Streamlit.git
cd Compound-Interest-Calculator-With-Streamlit

```


2. **Install dependencies:**
```bash
pip install streamlit pandas plotly

```


3. **Launch the app:**
```bash
streamlit run app.py

```
---
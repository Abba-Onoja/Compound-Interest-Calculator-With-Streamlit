import streamlit as st
import pandas as pd
import plotly.express as px


def inject_custom_css():
    """
    Injects custom CSS to enforce a minimalist, black-background aesthetic.
    Overrides default Streamlit component styles to maintain the dark theme.
    """
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #000000;
            color: #FFFFFF;
        }
        
        /* Typography */
        h1, h2, h3, h4, h5, h6, p, label {
            color: #FFFFFF !important;
        }

        /* Warren Buffett Quote Styling */
        .buffett-quote {
            font-size: 1.25rem;
            font-style: italic;
            font-weight: 300;
            color: #E0E0E0;
            padding-left: 20px;
            margin-top: 10px;
            margin-bottom: 30px;
            padding-top: 15px;
            padding-bottom: 15px;
            border-radius: 4px;
        }

        /* Input Widget Overrides */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            background-color: #1A1A1A;
            color: #FFFFFF;
            border: 1px solid #333333;
        }
        
        /* Selectbox Styling */
        [data-baseweb="select"] > div {
            background-color: #1A1A1A;
            color: #FFFFFF;
            border: 1px solid #333333;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0A0A0A;
            border-right: 1px solid #222222;
        }

        /* KPI Card Styling (Metric values and deltas) */
        [data-testid="stMetricValue"] {
            color: #FFFFFF !important;
            font-size: 2rem !important;
        }
        [data-testid="stMetricDelta"] > div {
            color: #AAAAAA !important; /* Neutral color for interest earned */
        }
        
        /* Dataframe background transparency override */
        [data-testid="stDataFrame"] {
            background-color: #000000;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def calculate_compound_interest(principal, rate, years, comp_freq, cont_amt, cont_freq):
    """
    Calculates the compound interest step-by-year, accounting for 
    mismatched compounding and contribution frequencies.
    
    Uses standard future value annuity formulas based on effective rates.
    """
    # Mapping frequency strings to numerical periods per year
    n_map = {'Daily': 365, 'Monthly': 12, 'Annually': 1}
    p_map = {'Monthly': 12, 'Annually': 1}
    
    n = n_map[comp_freq]
    p = p_map[cont_freq]
    r = rate / 100.0
    
    data = []
    
    for t in range(int(years) + 1):
        if t == 0:
            data.append({
                'Year': 0, 
                'Balance': principal, 
                'Total Contributions': principal, 
                'Interest Earned': 0
            })
            continue

        # 1. Calculate growth of the initial principal
        if r > 0:
            fv_principal = principal * (1 + r / n)**(n * t)
        else:
            fv_principal = principal

        # 2. Calculate growth of ongoing contributions
        if cont_amt > 0:
            total_payments = p * t
            if r > 0:
                # Calculate the effective interest rate per payment period
                r_p = (1 + r / n)**(n / p) - 1
                # Future Value of an Ordinary Annuity
                fv_contributions = cont_amt * (((1 + r_p)**total_payments - 1) / r_p)
            else:
                fv_contributions = cont_amt * total_payments
        else:
            fv_contributions = 0.0

        # 3. Aggregate totals for the current year
        total_balance = fv_principal + fv_contributions
        total_contributions = principal + (cont_amt * p * t)
        interest = total_balance - total_contributions

        data.append({
            'Year': t,
            'Balance': round(total_balance, 2),
            'Total Contributions': round(total_contributions, 2),
            'Interest Earned': round(interest, 2)
        })

    return pd.DataFrame(data)



def main():
    st.set_page_config(
        page_title="Compound Interest Calculator", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    inject_custom_css()

    st.title("Compound Interest Comparison")
    st.markdown(
        """
        <div class="buffett-quote">
        "My wealth has come from a combination of living in America, some lucky genes, and compound interest." — Warren Buffett
        </div>
        """, 
        unsafe_allow_html=True
    )

    #SIDEBAR INPUTS
    st.sidebar.header("Investment Parameters")
    
    initial_deposit = st.sidebar.number_input(
        "Initial Deposit ($)", 
        min_value=0.0, 
        value=10000.0, 
        step=500.0
    )
    
    years = st.sidebar.slider(
        "Years of Growth", 
        min_value=1, 
        max_value=50, 
        value=20, 
        step=1
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Scenarios")
    rate_1 = st.sidebar.number_input("Est. Rate of Return - Scenario 1 (%)", value=7.0, step=0.5)
    rate_2 = st.sidebar.number_input("Est. Rate of Return - Scenario 2 (%)", value=10.0, step=0.5)
    
    comp_freq = st.sidebar.selectbox(
        "Compound Frequency", 
        options=["Annually", "Monthly", "Daily"],
        index=1
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Regular Contributions")
    cont_amt = st.sidebar.number_input("Contribution Amount ($)", min_value=0.0, value=500.0, step=50.0)
    cont_freq = st.sidebar.selectbox("Contribution Frequency", options=["Monthly", "Annually"], index=0)

    df_scen1 = calculate_compound_interest(initial_deposit, rate_1, years, comp_freq, cont_amt, cont_freq)
    df_scen1['Scenario'] = 'Scenario 1'
    df_scen1['Yearly Interest'] = df_scen1['Interest Earned'].diff().fillna(0)
    
    df_scen2 = calculate_compound_interest(initial_deposit, rate_2, years, comp_freq, cont_amt, cont_freq)
    df_scen2['Scenario'] = 'Scenario 2'
    df_scen2['Yearly Interest'] = df_scen2['Interest Earned'].diff().fillna(0)
    
    df_combined = pd.concat([df_scen1, df_scen2])

    final_balance_1 = df_scen1['Balance'].iloc[-1]
    final_interest_1 = df_scen1['Interest Earned'].iloc[-1]
    
    final_balance_2 = df_scen2['Balance'].iloc[-1]
    final_interest_2 = df_scen2['Interest Earned'].iloc[-1]

    #KPI CARDS
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Scenario 1 Final Balance (Emerald Green)", 
            value=f"${final_balance_1:,.2f}", 
            delta=f"${final_interest_1:,.2f} Total Interest"
        )
    with col2:
        st.metric(
            label="Scenario 2 Final Balance (Slate Blue)", 
            value=f"${final_balance_2:,.2f}", 
            delta=f"${final_interest_2:,.2f} Total Interest"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    #LINE CHART
    st.subheader("Growth Trajectory Comparison")
    
    fig = px.line(
        df_combined, 
        x='Year', 
        y='Balance', 
        color='Scenario',
        color_discrete_map={
            'Scenario 1': '#50C878', # Emerald Green
            'Scenario 2': '#6A5ACD'  # Slate Blue
        },
        labels={"Balance": "Portfolio Balance ($)", "Year": "Years Elapsed"}
    )
    
    
    fig.update_layout(
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        font_color='#FFFFFF',
        xaxis=dict(showgrid=True, gridcolor='#333333'),
        yaxis=dict(showgrid=True, gridcolor='#333333'),
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)

    #ANNUAL RETURNS HISTOGRAM
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Annual Interest Earned")
    
    # Filter out Year 0 since no interest is earned at the exact moment of initial deposit
    df_filtered = df_combined[df_combined['Year'] > 0]
    
    fig_hist = px.histogram(
        df_filtered,
        x="Year",
        y="Yearly Interest",
        color="Scenario",
        barmode="group",
        color_discrete_map={
            'Scenario 1': '#50C878', # Emerald Green
            'Scenario 2': '#6A5ACD'  # Slate Blue
        },
        labels={"Yearly Interest": "Annual Interest ($)", "Year": "Years Elapsed"}
    )
   
    fig_hist.update_layout(
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        font_color='#FFFFFF',
        xaxis=dict(showgrid=True, gridcolor='#333333'),
        yaxis=dict(showgrid=True, gridcolor='#333333'),
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    #TABLE
    st.subheader("Year-by-Year Breakdown")
    
    df_table = pd.merge(
        df_scen1[['Year', 'Total Contributions', 'Balance', 'Yearly Interest', 'Interest Earned']],
        df_scen2[['Year', 'Balance', 'Yearly Interest', 'Interest Earned']],
        on='Year',
        suffixes=(' (Scen 1)', ' (Scen 2)')
    )
    
    format_mapping = {col: "${:,.2f}" for col in df_table.columns if col != 'Year'}
    st.dataframe(df_table.style.format(format_mapping), use_container_width=True)
    
    # Convert dataframe to CSV for download
    csv = df_table.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="Download Breakdown as CSV",
        data=csv,
        file_name='compound_interest_comparison.csv',
        mime='text/csv'
    )

if __name__ == "__main__":
    main()
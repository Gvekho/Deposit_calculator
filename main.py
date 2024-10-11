import streamlit as st
import pandas as pd
from datetime import datetime

# Function to calculate future value with interest
def calculate_future_value(df, interest_rate, current_date):
    df['date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df['future_value'] = df.apply(lambda row: row['Amount'] * (1 + interest_rate) ** ((current_date - row['date']).days / 365), axis=1)
    total_future_value = df['future_value'].sum()
    return df, total_future_value

# Streamlit app
def main():
    st.title("Deposit Growth Calculator")
    
    # Upload file
    st.write("Upload your file (CSV/Excel) with 'Date' and 'Amount' columns.")
    uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'])
    
    if uploaded_file is not None:
        # Load file based on type
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                st.error("Unsupported file format.")
                return
        except Exception as e:
            st.error(f"Error loading file: {e}")
            return
        
        # Show preview of the uploaded data
        st.write("Preview of uploaded data:")
        st.dataframe(df.head())
        
        # Interest rate input
        interest_rate = st.number_input("Interest Rate (as percentage)", min_value=0.0, max_value=100.0, value=11.0) / 100
        
        # Current date for calculation
        current_date = datetime.now()
        
        if 'Date' in df.columns and 'Amount' in df.columns:
            df, total_future_value = calculate_future_value(df, interest_rate, current_date)
            
            # Display the results
            st.write("Calculated Future Values:")
            st.dataframe(df)
            
            st.write(f"**Total Future Value as of {current_date.strftime('%Y-%m-%d')}:** ${total_future_value:.2f}")
        else:
            st.error("Make sure your file has 'Date' and 'Amount' columns.")

if __name__ == "__main__":
    main()

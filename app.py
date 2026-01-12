import streamlit as st
import pandas as pd
from data_loader import get_clean_data
from ep_algorithm import EP_Optimizer

st.set_page_config(page_title="Diet Optimizer - EP", layout="wide")
st.title("🥗 Evolutionary Diet Meal Planner")

# Load Data
menu_df = get_clean_data('Food_and_Nutrition_with_Price.csv')

# Sidebar
st.sidebar.header("🎯 Health Targets")
t_cal = st.sidebar.slider("Target Calories", 1200, 3500, 1900)
t_prot = st.sidebar.slider("Min Protein (g)", 40, 200, 120)
t_fat = st.sidebar.slider("Max Fat (g)", 20, 150, 70)

if st.button("🚀 Run Optimization"):
    optimizer = EP_Optimizer(menu_df, t_cal, t_prot, t_fat)
    best_idx, history = optimizer.run()
    
    # Get the chosen set (the row)
    best_set = menu_df.iloc[int(best_idx[0])]

    st.success("Optimization Successful!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 Selected Meal Set")
        # Display the names of the 4 meals in that set
        st.write(f"**Breakfast**: {best_set['Breakfast Suggestion']}")
        st.write(f"**Lunch**: {best_set['Lunch Suggestion']}")
        st.write(f"**Dinner**: {best_set['Dinner Suggestion']}")
        st.write(f"**Snack**: {best_set['Snack Suggestion']}")
        
        st.divider()
        # Single Price for the whole set
        st.metric("Total Set Price", f"RM {best_set['Price_RM']:.2f}")
        st.metric("Total Protein", f"{best_set['Protein']:.1f}g")

    with col2:
        st.subheader("📈 Convergence")
        st.line_chart(history)

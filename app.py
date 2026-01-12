import streamlit as st
import pandas as pd
from data_loader import get_clean_data
from ep_algorithm import EP_Optimizer

st.set_page_config(page_title="Diet Optimizer - EP", layout="wide")
st.title("🥗 Evolutionary Diet Meal Planner")

# Load Data
menu_df = get_clean_data('Food_and_Nutrition_with_Price.csv')

# Sidebar for targets
st.sidebar.header("🎯 Health Targets")
t_cal = st.sidebar.slider("Target Calories", 1200, 3500, 1550)
t_prot = st.sidebar.slider("Min Protein (g)", 40, 200, 120)
t_fat = st.sidebar.slider("Max Fat (g)", 20, 150, 70)

# --- RESTORED ALGORITHM SETTINGS ---
st.sidebar.header("⚙️ Algorithm Settings")
pop_size = st.sidebar.slider("Population Size", 10, 200, 50)
gens = st.sidebar.slider("Generations", 10, 500, 100)
mut_rate = st.sidebar.slider("Mutation Probability", 0.1, 1.0, 0.3)

if st.button("🚀 Run Optimization"):
    # Pass the new settings to the run method
    optimizer = EP_Optimizer(menu_df, t_cal, t_prot, t_fat)
    best_idx, history = optimizer.run(generations=gens, pop_size=pop_size, mut_rate=mut_rate)
    
    best_set = menu_df.iloc[int(best_idx[0])]

    st.success("Optimization Successful!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 Selected Meal Set")
        st.write(f"**Breakfast**: {best_set['Breakfast Suggestion']}")
        st.write(f"**Lunch**: {best_set['Lunch Suggestion']}")
        st.write(f"**Dinner**: {best_set['Dinner Suggestion']}")
        st.write(f"**Snack**: {best_set['Snack Suggestion']}")
        
        st.divider()
        st.subheader("💰 Summary Results")
        m1, m2 = st.columns(2)
        m1.metric("Total Set Price", f"RM {best_set['Price_RM']:.2f}")
        # --- RESTORED TOTAL CALORIES ---
        m2.metric("Total Calories", f"{best_set['Calories']:.0f} kcal")
        
        m3, m4 = st.columns(2)
        m3.metric("Total Protein", f"{best_set['Protein']:.1f}g")
        # --- RESTORED TOTAL FAT ---
        m4.metric("Total Fat", f"{best_set['Fat']:.1f}g")

    with col2:
        st.subheader("📈 Convergence")
        st.line_chart(history)

import streamlit as st
import pandas as pd
from data_loader import get_clean_data
from ep_algorithm import EP_Optimizer

st.set_page_config(page_title="Diet Optimizer - EP", layout="wide")
st.title("🥗 Evolutionary Diet Meal Planner")
st.markdown("Optimize your meal plan for the **lowest price** while meeting nutritional goals.")

# Load Data
menu_df = get_clean_data('Food_and_Nutrition_with_Price.csv')

# Sidebar for targets and parameters
st.sidebar.header("🎯 Health Targets")
t_cal = st.sidebar.slider("Target Calories", 1200, 3500, 2000)
t_prot = st.sidebar.slider("Min Protein (g)", 40, 200, 80)
t_fat = st.sidebar.slider("Max Fat (g)", 20, 150, 70)

st.sidebar.header("⚙️ Algorithm Settings")
pop = st.sidebar.slider("Population Size", 10, 200, 50)
gens = st.sidebar.slider("Generations", 10, 500, 100)
mut = st.sidebar.slider("Mutation Probability", 0.1, 1.0, 0.3)

if st.button("🚀 Run Optimization"):
    optimizer = EP_Optimizer(menu_df, t_cal, t_prot, t_fat)
    best_plan, history = optimizer.run(generations=gens, pop_size=pop, mut_rate=mut)
    
    st.success("Optimization Successful!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📋 Your Personalized Plan")
        p, c, pr, f = 0, 0, 0, 0
        for i, cat in enumerate(['Breakfast', 'Lunch', 'Dinner', 'Snack']):
            items = menu_df[menu_df['Category'] == cat]
            meal = items.iloc[best_plan[i] % len(items)]
            
            st.write(f"**{cat}**: {meal['Item']}")
            st.caption(f"Price: RM {meal['Price_RM']:.2f} | Prot: {meal['Protein']:.1f}g | Fat: {meal['Fat']:.1f}g")
            
            p += meal['Price_RM']
            c += meal['Calories']
            pr += meal['Protein']
            f += meal['Fat']
        
        st.divider()
        st.subheader("💰 Summary Results")
        m1, m2 = st.columns(2)
        m1.metric("Total Cost", f"RM {p:.2f}")
        m2.metric("Total Calories", f"{c:.0f} kcal")
        m3, m4 = st.columns(2)
        m3.metric("Total Protein", f"{pr:.1f}g")
        m4.metric("Total Fat", f"{f:.1f}g")

    with col2:
        st.subheader("📈 Convergence Analysis")
        # Use Streamlit's built-in chart to avoid Matplotlib errors
        st.line_chart(history)

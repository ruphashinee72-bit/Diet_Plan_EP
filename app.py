import streamlit as st
import pandas as pd
from data_loader import get_clean_data
from ep_algorithm import EP_Optimizer

st.set_page_config(page_title="Diet Optimizer - EP", layout="wide")
st.title("🥗 Evolutionary Diet Meal Planner")

menu_df = get_clean_data('Food_and_Nutrition_with_Price.csv')

st.sidebar.header("🎯 Health Targets")
t_cal = st.sidebar.slider("Target Calories", 1200, 3500, 2000)
t_prot = st.sidebar.slider("Min Protein (g)", 40, 200, 120)
t_fat = st.sidebar.slider("Max Fat (g)", 20, 150, 70)

if st.button("🚀 Run Optimization"):
    if menu_df is not None:
        optimizer = EP_Optimizer(menu_df, t_cal, t_prot, t_fat)
        best_plan, history = optimizer.run()
        
        st.success("Optimization Successful!")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📋 Plan")
            tp, tc, tpr, tf = 0, 0, 0, 0
            for i, cat in enumerate(['Breakfast', 'Lunch', 'Dinner', 'Snack']):
                items = menu_df[menu_df['Category'] == cat]
                meal = items.iloc[int(best_plan[i]) % len(items)]
                st.write(f"**{cat}**: {meal['Item']}")
                st.caption(f"Price: RM {meal['Price_RM']:.2f}")
                tp += meal['Price_RM']; tc += meal['Calories']; tpr += meal['Protein']; tf += meal['Fat']
            
            st.divider()
            st.metric("Total Cost", f"RM {tp:.2f}")
            st.metric("Total Protein", f"{tpr:.1f}g")
        with col2:
            st.subheader("📈 Convergence")
            st.line_chart(history)

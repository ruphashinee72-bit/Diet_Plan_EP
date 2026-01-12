import streamlit as st
import pandas as pd
# Removed matplotlib to fix the ModuleNotFoundError
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
t_prot = st.sidebar.slider("Min Protein (g)", 40, 200, 120) # Set to 120 to match friends
t_fat = st.sidebar.slider("Max Fat (g)", 20, 150, 70)

st.sidebar.header("⚙️ Algorithm Settings")
pop_size = st.sidebar.slider("Population Size", 10, 200, 50)
gens = st.sidebar.slider("Generations", 10, 500, 100)
mut_rate = st.sidebar.slider("Mutation Probability", 0.1, 1.0, 0.3)

if st.button("🚀 Run Optimization"):
    if menu_df is not None:
        optimizer = EP_Optimizer(menu_df, t_cal, t_prot, t_fat)
        # Ensure your ep_algorithm.py returns (best_plan, history)
        best_plan, history = optimizer.run(generations=gens, pop_size=pop_size, mut_rate=mut_rate)
        
        st.success("Optimization Successful!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📋 Your Personalized Plan")
            total_p, total_c, total_pr, total_f = 0, 0, 0, 0
            
            categories = ['Breakfast', 'Lunch', 'Dinner', 'Snack']
            
            for i, cat in enumerate(categories):
                items = menu_df[menu_df['Category'] == cat]
                if not items.empty:
                    # Logic to pick the individual meal from the 4-gene list
                    meal_idx = int(best_plan[i]) % len(items)
                    meal = items.iloc[meal_idx]
                    
                    st.write(f"**{cat}**: {meal['Item']}")
                    st.caption(f"Price: RM {meal['Price_RM']:.2f} | Prot: {meal['Protein']:.1f}g")
                    
                    total_p += meal['Price_RM']
                    total_c += meal['Calories']
                    total_pr += meal['Protein']
                    total_f += meal['Fat']
            
            st.divider()
            st.subheader("💰 Summary Results")
            m1, m2 = st.columns(2)
            m1.metric("Total Cost", f"RM {total_p:.2f}")
            m2.metric("Total Calories", f"{total_c:.0f} kcal")
            
            m3, m4 = st.columns(2)
            m3.metric("Total Protein", f"{total_pr:.1f}g")
            m4.metric("Total Fat", f"{total_f:.1f}g")

        with col2:
            st.subheader("📈 Convergence Analysis")
            # Using built-in chart to avoid Matplotlib dependency errors
            st.line_chart(history)
    else:
        st.error("Data could not be loaded. Check your CSV file.")

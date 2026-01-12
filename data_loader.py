import pandas as pd

def get_clean_data(file_path):
    df = pd.read_csv(file_path)
    menu = []
    
    categories = {
        'Breakfast Suggestion': 'Breakfast',
        'Lunch Suggestion': 'Lunch',
        'Dinner Suggestion': 'Dinner',
        'Snack Suggestion': 'Snack'
    }
    
    for col, cat_name in categories.items():
        unique_meals = df[col].unique()
        for meal in unique_meals:
            subset = df[df[col] == meal].iloc[0]
            # NO DIVISION - Using full values for logical RM 20+ pricing
            menu.append({
                'Item': meal,
                'Category': cat_name,
                'Calories': subset['Calories'],
                'Protein': subset['Protein'],
                'Fat': subset['Fat'],
                'Price_RM': subset['Price_RM']
            })
            
    return pd.DataFrame(menu)

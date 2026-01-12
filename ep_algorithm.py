import numpy as np

class EP_Optimizer:
    def __init__(self, menu_df, target_cal, target_prot, target_fat):
        self.df = menu_df
        self.target_cal = target_cal
        self.target_prot = target_prot
        self.target_fat = target_fat
        self.cats = ['Breakfast', 'Lunch', 'Dinner', 'Snack']

    def fitness(self, individual):
        t_price, t_cal, t_prot, t_fat = 0, 0, 0, 0
        
        # This loop picks 4 items based on the 4 numbers in the individual list
        for i, cat in enumerate(self.cats):
            items = self.df[self.df['Category'] == cat]
            if not items.empty:
                idx = int(individual[i]) % len(items)
                meal = items.iloc[idx]
                
                t_price += meal['Price_RM']
                t_cal += meal['Calories']
                t_prot += meal['Protein']
                t_fat += meal['Fat']
        
        # Penalties: Adjusting weights to prioritize Protein and Calories
        cal_penalty = abs(t_cal - self.target_cal) * 2
        prot_penalty = max(0, self.target_prot - t_prot) * 10
        fat_penalty = max(0, t_fat - self.target_fat) * 5
        
        return t_price + cal_penalty + prot_penalty + fat_penalty

    def run(self, generations=100, pop_size=50, mut_rate=0.3):
        # Initialize population with 4 random genes (one for each meal)
        pop = [[np.random.randint(0, 100) for _ in range(4)] for _ in range(pop_size)]
        history = []
        
        for g in range(generations):
            offspring = []
            for parent in pop:
                child = parent.copy()
                # Mutation: Randomly changing one or more of the 4 meals
                for i in range(4):
                    if np.random.rand() < mut_rate:
                        child[i] = np.random.randint(0, 100)
                offspring.append(child)
            
            # Survival of the fittest selection
            combined = pop + offspring
            combined.sort(key=lambda x: self.fitness(x))
            pop = combined[:pop_size]
            history.append(self.fitness(pop[0]))
            
        return pop[0], history

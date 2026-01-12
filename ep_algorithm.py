import numpy as np

class EP_Optimizer:
    def __init__(self, menu_df, target_cal, target_prot, target_fat):
        self.df = menu_df
        self.target_cal = target_cal
        self.target_prot = target_prot
        self.target_fat = target_fat

    def fitness(self, individual):
        # Pick the row index from the individual
        idx = int(individual[0]) % len(self.df)
        row = self.df.iloc[idx]
        
        # Use the total price/nutrients for that whole set (one row)
        t_price = row['Price_RM']
        t_cal = row['Calories']
        t_prot = row['Protein']
        t_fat = row['Fat']
        
        # Penalties (matching your targets)
        cal_diff = abs(t_cal - self.target_cal) * 5
        prot_diff = max(0, self.target_prot - t_prot) * 10
        fat_diff = max(0, t_fat - self.target_fat) * 10
        
        return t_price + cal_diff + prot_diff + fat_diff

    def run(self, generations=100, pop_size=50, mut_rate=0.3):
        # Initial population: random row indices
        pop = [[np.random.randint(0, len(self.df))] for _ in range(pop_size)]
        history = []
        
        for g in range(generations):
            offspring = []
            for parent in pop:
                child = parent.copy()
                # Mutation: Randomly pick a different set/row
                if np.random.rand() < mut_rate:
                    child[0] = np.random.randint(0, len(self.df))
                offspring.append(child)
            
            # Selection
            combined = pop + offspring
            combined.sort(key=lambda x: self.fitness(x))
            pop = combined[:pop_size]
            history.append(self.fitness(pop[0]))
            
        return pop[0], history

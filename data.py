import pandas as pd
import numpy as np

# Parameters
n_samples = 1000  # Number of synthetic samples

# Synthetic data generation
data = {
    'Device': np.random.choice(
        ['Mobile', 'Laptop', 'Refrigerator', 'Television', 'Accessories', 'Other'], 
        n_samples
    ),
    'Phase Reward': np.random.uniform(20, 100, n_samples),  # Reward between $20 and $100
    'Recyclable Score': np.random.randint(0, 2, n_samples),  # Binary recyclable score (0 or 1)
    'CO2 Emission Saved': np.random.uniform(0, 10, n_samples),  # CO2 emission saved in kg
    'Other Savings': np.random.uniform(0, 15, n_samples),  # Other savings in arbitrary units (could be dollars)
    'CPU': np.random.randint(0, 51, n_samples),  # CPU score on a scale of 0-50
    'Memory': np.random.randint(0, 51, n_samples),  # Memory score on a scale of 0-50
    'Battery': np.random.randint(0, 51, n_samples),  # Battery score on a scale of 0-50
    'Display': np.random.randint(0, 51, n_samples),  # Display score on a scale of 0-50
    'Keyboard': np.random.randint(0, 51, n_samples),  # Keyboard score on a scale of 0-50
    'Plastics': np.random.randint(0, 51, n_samples),  # Plastics score on a scale of 0-50
    'Metals': np.random.randint(0, 51, n_samples),  # Metals score on a scale of 0-50
    'Copper': np.random.uniform(0, 5, n_samples),  # Amount of copper in kg
    'Aluminum': np.random.uniform(0, 5, n_samples),  # Amount of aluminum in kg
    'Gold': np.random.uniform(0, 1, n_samples),  # Amount of gold in kg
    'Silver': np.random.uniform(0, 1, n_samples),  # Amount of silver in kg
    'Lead': np.random.uniform(0, 1, n_samples),  # Amount of lead in kg
    'Tin': np.random.uniform(0, 1, n_samples),  # Amount of tin in kg
    'Nickel': np.random.uniform(0, 1, n_samples),  # Amount of nickel in kg
    'Zinc': np.random.uniform(0, 1, n_samples)  # Amount of zinc in kg
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("synthetic_e_waste_data_with_all_columns.csv", index=False)

print("Synthetic data with all columns generated and saved to 'synthetic_e_waste_data_with_all_columns.csv'.")

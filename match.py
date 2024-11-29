import pandas as pd

# Load the dataset
data = pd.read_csv('C:\Users\Eashwar\OneDrive\Desktop\plant.csv')  # Replace with the path to your CSV file

def check_soil_type(plant_name, user_soil_type):
    # Convert user inputs to lowercase for case-insensitive comparison
    plant_name = plant_name.lower()
    user_soil_type = user_soil_type.lower()
    
    # Filter the dataset for the entered plant name
    plant_data = data[data['Plant Name'].str.lower() == plant_name]
    
    if plant_data.empty:
        return f"Error: Plant '{plant_name}' not found in the database."
    
    # Retrieve the correct soil type
    correct_soil_type = plant_data.iloc[0]['Best Soil Type'].lower()
    
    # Check if the soil type matches
    if user_soil_type == correct_soil_type:
        match_status = "Match: The soil type is correct!"
    else:
        match_status = f"Warning: The soil type is incorrect! Recommended soil type is '{correct_soil_type}'."
    
    # Print other details of the plant
    other_details = plant_data.iloc[0].drop(['Plant Name', 'Best Soil Type', 'Worst Soil Type']).to_dict()
    
    # Return the results
    return {
        "Match Status": match_status,
        "Plant Details": other_details
    }

# Example user input
plant_name = input("Enter the name of the plant: ").strip()
soil_type = input("Enter the soil type: ").strip()

# Call the function and display results
result = check_soil_type(plant_name, soil_type)

if isinstance(result, str):
    print(result)  # Error message if plant not found
else:
    print(result["Match Status"])
    print("Additional Details:")
    for key, value in result["Plant Details"].items():
        print(f"{key}: {value}")

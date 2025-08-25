# import pandas as pd 
# import requests
# data_path = "C:/Users/KATALA JEETHENDER/OneDrive/Desktop/college project modification/historical data/supply_chain_data.csv" 

# def load_supply_chain_data():
#     return pd.read_csv(data_path)

# def simulate_demand_change(df, percentage_change):
#     df = df.copy()
#     df['Simulated_Sales'] = df['Number of products sold'] * (1 + percentage_change / 100)
#     df['Simulated_Revenue'] = df['Simulated_Sales'] * df['Price']
#     return df

# def simulate_lead_time_change(df, new_lead_time):
#     df = df.copy()
#     df['Simulated_Lead_Time'] = new_lead_time
#     return df

# def simulate_shipping_cost_increase(df, percent_increase):
#     df = df.copy()
#     df['Simulated_Shipping_Cost'] = df['Shipping costs'] * (1 + percent_increase / 100)
#     return df

# def summarize_impact(df, scenario):
#     print(f"\n📊 Scenario Analysis: {scenario}")
#     print("🔍 Impact Summary:")
    
#     if 'Simulated_Revenue' in df.columns:
#         print(f"- Avg Revenue Impact: ${df['Simulated_Revenue'].sum():,.2f}")
#     elif 'Revenue generated' in df.columns:
#         print(f"- Avg Revenue (Base): ${df['Revenue generated'].sum():,.2f}")
#     else:
#         print("- Revenue data not available")
        
#     if 'Lead time' in df.columns:
#         print(f"- Avg Lead Time: {df['Lead time'].mean():.2f} days")
#     elif 'Lead times' in df.columns:
#         print(f"- Avg Lead Time: {df['Lead times'].mean():.2f} days")
        
#     if 'Shipping costs' in df.columns:
#         print(f"- Avg Shipping Cost: ${df['Shipping costs'].mean():.2f}") 
# def generate_prompt_from_data(scenario_name, df):
#     total_revenue = df['Simulated_Revenue'].sum() if 'Simulated_Revenue' in df.columns else df['Revenue generated'].sum()
#     avg_lead_time = df['Lead time'].mean() if 'Lead time' in df.columns else df['Lead times'].mean()
#     avg_shipping = df['Shipping costs'].mean()

#     prompt = f"""
# You are a supply chain analyst. The following scenario has been simulated: "{scenario_name}"

# 📊 Numerical Summary:
# - Total Revenue: ${total_revenue:,.2f}
# - Avg Lead Time: {avg_lead_time:.2f} days
# - Avg Shipping Cost: ${avg_shipping:.2f}

# Please analyze:
# 1. What is the likely business impact of this scenario?
# 2. What actionable steps should a supply chain manager take?
# 3. Are there any risks or opportunities this scenario uncovers?

# Respond with practical, business-savvy suggestions.
# """
#     return prompt     
# def get_llm_insight(prompt):
#     response = requests.post(
#         'http://localhost:11434/api/generate',
#         json={
#             "model": "tinyllama",
#             "prompt": prompt,
#             "stream": False
#         }
#     )
#     return response.json()['response'].strip()


# if __name__ == "__main__":
#     df = load_supply_chain_data()

#     # # Example Scenario: Demand Drop
#     # demand_scenario = simulate_demand_change(df, -30)
#     # summarize_impact(demand_scenario, "30% Demand Drop")

#     # # Example Scenario: Supply Lead Time Spike
#     # lead_time_scenario = simulate_lead_time_change(df, new_lead_time=20)
#     # summarize_impact(lead_time_scenario, "Lead Time Increased to 20 Days")

#     # # Example Scenario: Shipping Cost Increase
#     # shipping_cost_scenario = simulate_shipping_cost_increase(df, 40)
#     # summarize_impact(shipping_cost_scenario, "Shipping Costs Increase by 40%") 
#     df = load_supply_chain_data()
#     demand_scenario = simulate_demand_change(df, -15)
#     prompt = generate_prompt_from_data("15% Demand Drop", demand_scenario)
#     insight = get_llm_insight(prompt)
#     print("\n🤖 LLM Recommendation:\n", insight) 
import pandas as pd 
import requests

data_path = "C:/Users/KATALA JEETHENDER/OneDrive/Desktop/college project modification/historical data/supply_chain_data.csv" 

def load_supply_chain_data():
    return pd.read_csv(data_path)

def simulate_demand_change(df, percentage_change):
    df = df.copy()
    df['Simulated_Sales'] = df['Number of products sold'] * (1 + percentage_change / 100)
    df['Simulated_Revenue'] = df['Simulated_Sales'] * df['Price']
    return df

def simulate_lead_time_change(df, new_lead_time):
    df = df.copy()
    df['Simulated_Lead_Time'] = new_lead_time
    return df

def simulate_shipping_cost_increase(df, percent_increase):
    df = df.copy()
    df['Simulated_Shipping_Cost'] = df['Shipping costs'] * (1 + percent_increase / 100)
    return df

def summarize_impact(df, scenario):
    print(f"\n📊 Scenario Analysis: {scenario}")
    print("🔍 Impact Summary:")
    
    if 'Simulated_Revenue' in df.columns:
        print(f"- Avg Revenue Impact: ${df['Simulated_Revenue'].sum():,.2f}")
    elif 'Revenue generated' in df.columns:
        print(f"- Avg Revenue (Base): ${df['Revenue generated'].sum():,.2f}")
    else:
        print("- Revenue data not available")
        
    if 'Lead time' in df.columns:
        print(f"- Avg Lead Time: {df['Lead time'].mean():.2f} days")
    elif 'Lead times' in df.columns:
        print(f"- Avg Lead Time: {df['Lead times'].mean():.2f} days")
        
    if 'Shipping costs' in df.columns:
        print(f"- Avg Shipping Cost: ${df['Shipping costs'].mean():.2f}") 

def generate_prompt_from_data(scenario_name, df):
    total_revenue = df['Simulated_Revenue'].sum() if 'Simulated_Revenue' in df.columns else df['Revenue generated'].sum()
    avg_lead_time = df['Lead time'].mean() if 'Lead time' in df.columns else df['Lead times'].mean()
    avg_shipping = df['Shipping costs'].mean()

    prompt = f"""
You are a supply chain analyst. The following scenario has been simulated: "{scenario_name}"

📊 Numerical Summary:
- Total Revenue: ${total_revenue:,.2f}
- Avg Lead Time: {avg_lead_time:.2f} days
- Avg Shipping Cost: ${avg_shipping:.2f}

Please analyze:
1. What is the likely business impact of this scenario?
2. What actionable steps should a supply chain manager take?
3. Are there any risks or opportunities this scenario uncovers?

Respond with practical, business-savvy suggestions.
"""
    return prompt     

def get_llm_insight(prompt):
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            "model": "tinyllama",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()['response'].strip()

# ✅ Function callable from agent_flow.py
def get_scenario_summary(percentage_change: float):
    df = load_supply_chain_data()
    scenario_df = simulate_demand_change(df, percentage_change)

    # Label: e.g., "-10% Demand Drop" or "15% Demand Increase"
    if percentage_change < 0:
        label = f"{abs(percentage_change)}% Demand Drop"
    else:
        label = f"{percentage_change}% Demand Increase"

    prompt = generate_prompt_from_data(label, scenario_df)
    insight = get_llm_insight(prompt)
    return insight

# === Optional testing block ===
if __name__ == "__main__":
    summary = get_scenario_summary(-15)  # You can change to any float
    print("\n🤖 LLM Recommendation:\n", summary)




   

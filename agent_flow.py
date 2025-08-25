from langgraph.graph import StateGraph, END
from langgraph.pregel import Pregel
from typing import TypedDict, Optional
from load_contracts import get_procurement_summary
from scenario_planning import get_scenario_summary
from sku_rationalization import get_sku_summary
# import pprint

# === Define Shared State ===
class AgentState(TypedDict):
    scenario_summary: Optional[str]
    sku_summary: Optional[str]
    procurement_summary: Optional[str]
    # final_dashboard: Optional[str]  
# === Node 1: Procurement Analysis ===
def procurement_node(state: AgentState) -> AgentState:
    summary = get_procurement_summary()
    return {**state, "procurement_summary": "📑 Procurement Summary:\n" + summary}   
# === Node 2: Scenario Planning Analysis ===
def scenario_node(state: AgentState) -> AgentState:
    summary = get_scenario_summary(-15)  # You can change this to any % dynamically later
    return {**state, "scenario_summary": "📈 Scenario Planning Summary:\n" + summary}  
# === Node 3: SKU Rationalization ===
def sku_node(state: AgentState) -> AgentState:
    summary = get_sku_summary()
    return {**state, "sku_summary": "📦 SKU Rationalization Summary:\n" + summary} 
# === Node 4: Final Dashboard Aggregation ===
def dashboard_node(state: AgentState) -> AgentState:
    dashboard = (
        "\n🧾 FINAL SUPPLY CHAIN DASHBOARD\n"
        "=====================================\n"
        f"{state.get('procurement_summary', '❗ No procurement summary available.')}\n\n"
        f"{state.get('scenario_summary', '❗ No scenario summary available.')}\n\n"
        f"{state.get('sku_summary', '❗ No SKU summary available.')}\n"
        "=====================================\n"
    )
    return {**state, "final_dashboard": dashboard}

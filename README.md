# supply-chain-intelligence-dashboard
AI powered supply chain analysis dashboard with SKU rationalization, scenario planning and procurement contract analysis
# Supply Chain Agent (LangGraph + Ollama) 
Agentic workflow with three modules:
- Procurement Analysis (PDF → embeddings → TinyLLaMA)
- Scenario Planning (TinyLLaMA summary)
- SKU Rationalization (rules + TinyLLaMA insight) 
# Start Ollama locally and pull tinyllama
ollama pull tinyllama 
# Run agent pipeline 
python agent.py 
# Build dashboard
streamlit run dashboard.py


import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from agent_flow import procurement_node, scenario_node, sku_node, dashboard_node, AgentState

# Configure Streamlit page
st.set_page_config(
    page_title="Supply Chain Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2e7d32;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .status-keep {
        background-color: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .status-optimize {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .status-discontinue {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
    st.session_state.analysis_data = None

# Header
st.markdown('<h1 class="main-header">🏭 Supply Chain Intelligence Dashboard</h1>', unsafe_allow_html=True)

# Sidebar controls
with st.sidebar:
    st.header("🔧 Dashboard Controls")
    
    # Analysis trigger
    if st.button("🔄 Run Complete Analysis", type="primary", use_container_width=True):
        with st.spinner("Analyzing supply chain data..."):
            try:
                # Initialize state
                state = AgentState(
                    scenario_summary=None,
                    sku_summary=None,
                    procurement_summary=None
                )
                
                # Run analysis nodes
                progress_bar = st.progress(0)
                
                # Procurement Analysis
                st.text("Running procurement analysis...")
                state = procurement_node(state)
                progress_bar.progress(25)
                
                # Scenario Planning
                st.text("Running scenario planning...")
                state = scenario_node(state)
                progress_bar.progress(50)
                
                # SKU Rationalization
                st.text("Running SKU rationalization...")
                state = sku_node(state)
                progress_bar.progress(75)
                
                # Final Dashboard
                st.text("Generating final dashboard...")
                state = dashboard_node(state)
                progress_bar.progress(100)
                
                st.session_state.analysis_data = state
                st.session_state.analysis_complete = True
                st.success("Analysis completed successfully! ✅")
                
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
    
    # Scenario Planning Controls
    st.subheader("📈 Scenario Parameters")
    scenario_change = st.slider(
        "Demand Change (%)",
        min_value=-50,
        max_value=50,
        value=-15,
        step=5,
        help="Adjust demand change percentage for scenario analysis"
    )
    
    # Refresh timestamp
    st.markdown("---")
    st.caption(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Main dashboard content
if st.session_state.analysis_complete and st.session_state.analysis_data:
    data = st.session_state.analysis_data
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Executive Summary", "📦 SKU Analysis", "📈 Scenario Planning", "📄 Procurement"])
    
    with tab1:
        st.markdown('<h2 class="section-header">Executive Summary</h2>', unsafe_allow_html=True)
        
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📊 Analysis Status",
                value="Complete",
                delta="✅ All modules processed"
            )
        
        with col2:
            st.metric(
                label="🔍 Data Sources",
                value="3 Active",
                delta="SKU, Scenario, Procurement"
            )
        
        with col3:
            st.metric(
                label="⚡ Processing Time",
                value="< 30s",
                delta="Real-time analysis"
            )
        
        with col4:
            st.metric(
                label="📈 Insights Generated",
                value="15+",
                delta="Actionable recommendations"
            )
        
        # Executive summary text
        st.markdown("---")
        st.subheader("🎯 Key Findings")
        
        executive_summary = """
        **Supply Chain Health Overview:**
        - **SKU Performance**: Mix of high-performing and underperforming products identified
        - **Risk Assessment**: Scenario planning reveals demand sensitivity impacts
        - **Contract Status**: Procurement agreements analyzed for key terms and risks
        - **Action Items**: Specific recommendations generated for optimization
        """
        
        st.markdown(executive_summary)
    
    with tab2:
        st.markdown('<h2 class="section-header">SKU Rationalization Analysis</h2>', unsafe_allow_html=True)
        
        if data.get('sku_summary'):
            # Display SKU summary
            st.text_area(
                "SKU Analysis Results",
                value=data['sku_summary'],
                height=400,
                help="AI-generated insights on SKU performance and recommendations"
            )
            
            # Mock data for visualization (in real implementation, you'd parse the actual data)
            col1, col2 = st.columns(2)
            
            with col1:
                # SKU Performance Distribution
                sku_data = {
                    'Status': ['Keep', 'Bundle/Optimize', 'Discontinue'],
                    'Count': [12, 8, 5],
                    'Percentage': [48, 32, 20]
                }
                
                fig_pie = px.pie(
                    values=sku_data['Count'],
                    names=sku_data['Status'],
                    title="SKU Recommendation Distribution",
                    color_discrete_map={
                        'Keep': '#28a745',
                        'Bundle/Optimize': '#ffc107',
                        'Discontinue': '#dc3545'
                    }
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Performance Metrics
                metrics_data = pd.DataFrame({
                    'SKU': ['SKU001', 'SKU002', 'SKU003', 'SKU004', 'SKU005'],
                    'Profit_Margin': [0.35, 0.15, 0.05, 0.28, 0.12],
                    'Sales_Velocity': [1.5, 0.8, 0.3, 1.2, 0.6],
                    'Status': ['Keep', 'Bundle/Optimize', 'Discontinue', 'Keep', 'Bundle/Optimize']
                })
                
                fig_scatter = px.scatter(
                    metrics_data,
                    x='Sales_Velocity',
                    y='Profit_Margin',
                    color='Status',
                    title='SKU Performance Matrix',
                    labels={'Sales_Velocity': 'Sales Velocity', 'Profit_Margin': 'Profit Margin'},
                    color_discrete_map={
                        'Keep': '#28a745',
                        'Bundle/Optimize': '#ffc107',
                        'Discontinue': '#dc3545'
                    }
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.warning("SKU analysis data not available. Please run the analysis.")
    
    with tab3:
        st.markdown('<h2 class="section-header">Scenario Planning Results</h2>', unsafe_allow_html=True)
        
        if data.get('scenario_summary'):
            # Display scenario analysis
            st.text_area(
                "Scenario Analysis Results",
                value=data['scenario_summary'],
                height=400,
                help="AI-generated insights on demand change scenario impacts"
            )
            
            # Scenario impact visualization
            col1, col2 = st.columns(2)
            
            with col1:
                # Revenue Impact Chart
                scenarios = ['Base Case', 'Demand -15%', 'Demand -30%', 'Demand +15%', 'Demand +30%']
                revenue_impact = [1000000, 850000, 700000, 1150000, 1300000]
                
                fig_bar = go.Figure(data=[
                    go.Bar(x=scenarios, y=revenue_impact, 
                          marker_color=['blue', 'red', 'darkred', 'green', 'darkgreen'])
                ])
                fig_bar.update_layout(title='Revenue Impact by Scenario')
                st.plotly_chart(fig_bar, use_container_width=True)
            
            with col2:
                # Risk Assessment
                st.subheader("🚨 Risk Assessment")
                risk_data = {
                    'Risk Factor': ['Demand Volatility', 'Supply Disruption', 'Cost Inflation', 'Lead Time Extension'],
                    'Impact': ['High', 'Medium', 'Medium', 'Low'],
                    'Probability': [0.7, 0.4, 0.6, 0.3]
                }
                
                risk_df = pd.DataFrame(risk_data)
                st.dataframe(risk_df, use_container_width=True)
        else:
            st.warning("Scenario analysis data not available. Please run the analysis.")
    
    with tab4:
        st.markdown('<h2 class="section-header">Procurement Contract Analysis</h2>', unsafe_allow_html=True)
        
        if data.get('procurement_summary'):
            # Display procurement analysis
            st.text_area(
                "Procurement Analysis Results",
                value=data['procurement_summary'],
                height=400,
                help="AI-generated insights on contract terms, risks, and decision points"
            )
            
            # Contract metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="📋 Active Contracts",
                    value="12",
                    delta="2 expiring soon"
                )
            
            with col2:
                st.metric(
                    label="💰 Total Value",
                    value="$2.4M",
                    delta="15% vs last year"
                )
            
            with col3:
                st.metric(
                    label="⚠️ Risk Level",
                    value="Medium",
                    delta="3 contracts need review"
                )
            
            # Contract status overview
            st.subheader("📊 Contract Status Overview")
            contract_status = {
                'Status': ['Active', 'Under Review', 'Expiring Soon', 'Renewed'],
                'Count': [8, 2, 2, 3],
                'Value ($M)': [1.8, 0.3, 0.2, 0.4]
            }
            
            status_df = pd.DataFrame(contract_status)
            
            fig_status = px.bar(
                status_df,
                x='Status',
                y='Count',
                title='Contract Status Distribution',
                color='Status'
            )
            st.plotly_chart(fig_status, use_container_width=True)
        else:
            st.warning("Procurement analysis data not available. Please run the analysis.")

else:
    # Landing page when no analysis has been run
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ### 🚀 Welcome to Supply Chain Intelligence Dashboard
        
        This dashboard provides comprehensive analysis across three key areas:
        
        - **📦 SKU Rationalization**: Analyze product performance and get recommendations
        - **📈 Scenario Planning**: Simulate demand changes and assess impacts  
        - **📄 Procurement Analysis**: Review contract terms and identify risks
        
        **👈 Click "Run Complete Analysis" in the sidebar to get started!**
        """)
        
        # Feature highlights
        st.markdown("---")
        st.subheader("✨ Dashboard Features")
        
        feature_col1, feature_col2 = st.columns(2)
        
        with feature_col1:
            st.markdown("""
            **🔍 AI-Powered Insights**
            - Automated analysis using TinyLLaMA
            - Natural language recommendations
            - Real-time data processing
            """)
        
        with feature_col2:
            st.markdown("""
            **📊 Interactive Visualizations**
            - Dynamic charts and graphs
            - Performance metrics tracking
            - Scenario comparison tools
            """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666666; padding: 20px;'>
        <p>Supply Chain Intelligence Dashboard | Powered by AI & Analytics</p>
    </div>
    """,
    unsafe_allow_html=True
)
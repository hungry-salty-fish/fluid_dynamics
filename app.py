"""
核电凝汽器热力特性场预测系统 - 主入口
"""

import streamlit as st

# 页面配置
st.set_page_config(
    page_title="核电凝汽器热力特性场预测",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式
st.markdown("""
<style>
    /* 隐藏默认元素 */
    [data-testid="stSidebarNav"] {display: none !important;}
    [data-testid="stSidebarNavItems"] {display: none !important;}
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header[data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    .stPageLink {display: none !important;}
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D47A1 0%, #1565C0 100%);
        min-width: 220px;
    }
    [data-testid="stSidebar"] > div:first-child {padding-top: 0 !important;}
    [data-testid="stSidebarUserContent"] {padding-top: 0 !important;}
    
    /* 导航按钮 */
    [data-testid="stSidebar"] .stRadio > div > label {
        background: rgba(255,255,255,0.1);
        padding: 10px 14px;
        border-radius: 8px;
        margin: 3px 0;
        color: white !important;
        transition: all 0.3s;
    }
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(255,255,255,0.2);
    }
    [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {
        background: #4CAF50 !important;
        font-weight: bold;
    }
    
    /* 页面布局 */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0.5rem !important;
        max-width: 100% !important;
    }
    
    /* 区块标题 */
    .section-header {
        font-size: 1rem;
        font-weight: bold;
        color: #1565C0;
        background: linear-gradient(90deg, #E3F2FD, transparent);
        padding: 6px 10px;
        border-left: 4px solid #1565C0;
        margin: 8px 0;
        border-radius: 0 6px 6px 0;
    }
    
    /* 紧凑布局 */
    .stNumberInput {margin-bottom: 8px !important;}
    .stSelectbox {margin-bottom: 8px !important;}
    .stButton > button {padding: 8px 16px !important; border-radius: 20px;}
    [data-testid="stMetricValue"] {font-size: 1.1rem !important; color: #1565C0;}
    [data-testid="stMetricLabel"] {font-size: 0.8rem !important;}
</style>
""", unsafe_allow_html=True)

# 初始化 session state
if 'calculated' not in st.session_state:
    st.session_state.calculated = False
if 'synthesized_img' not in st.session_state:
    st.session_state.synthesized_img = None
if 'flow_data' not in st.session_state:
    st.session_state.flow_data = None

# ========== 侧边栏导航 ==========
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 15px 8px; border-bottom: 1px solid rgba(255,255,255,0.2); margin-bottom: 12px;">
            <div style="font-size: 2rem;">⚛️</div>
            <div style="color: white; font-size: 1rem; font-weight: bold; margin-top: 5px;">
                核电凝汽器
            </div>
            <div style="color: rgba(255,255,255,0.7); font-size: 0.8rem;">
                热力特性场预测
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    page = st.radio(
        "导航",
        [
            "🏠 系统首页",
            "⚛️ 热力场预测",
            "📈 趋势分析",
            "📊 结果对比",
            "📁 数据管理",
            "⚙️ 系统设置"
        ],
        index=1,
        label_visibility="collapsed"
    )
    
    st.markdown("""
        <div style="position: fixed; bottom: 10px; left: 10px; color: rgba(255,255,255,0.4); font-size: 0.7rem;">
            v1.0.0 © 2024
        </div>
    """, unsafe_allow_html=True)

# ========== 路由 ==========
if page == "🏠 系统首页":
    from pages import home
    home.show()
elif page == "⚛️ 热力场预测":
    from pages import fluid_dynamics
    fluid_dynamics.show()
elif page == "📈 趋势分析":
    from pages import heat_transfer
    heat_transfer.show()
elif page == "📊 结果对比":
    from pages import result_compare
    result_compare.show()
elif page == "📁 数据管理":
    from pages import data_manage
    data_manage.show()
elif page == "⚙️ 系统设置":
    from pages import settings
    settings.show()

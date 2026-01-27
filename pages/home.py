"""首页"""
import streamlit as st

def show():
    st.markdown("""
        <div style="
            font-size: 1.6rem; font-weight: bold; color: #1565C0;
            text-align: center; padding: 12px;
            border-bottom: 3px solid #1565C0; margin-bottom: 15px;
            background: linear-gradient(90deg, #E3F2FD, white, #E3F2FD);
            border-radius: 8px;
        ">🏠 核电凝汽器热力特性场预测系统</div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#1565C0,#0D47A1);padding:25px;border-radius:12px;text-align:center;color:white;">
            <div style="font-size:2.5rem;">⚛️</div>
            <div style="font-weight:bold;margin:8px 0;">热力场预测</div>
            <div style="font-size:0.85rem;opacity:0.9;">温度场分布预测</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#2196F3,#1976D2);padding:25px;border-radius:12px;text-align:center;color:white;">
            <div style="font-size:2.5rem;">📈</div>
            <div style="font-weight:bold;margin:8px 0;">趋势分析</div>
            <div style="font-size:0.85rem;opacity:0.9;">参数变化趋势</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#42A5F5,#2196F3);padding:25px;border-radius:12px;text-align:center;color:white;">
            <div style="font-size:2.5rem;">📊</div>
            <div style="font-weight:bold;margin:8px 0;">结果对比</div>
            <div style="font-size:0.85rem;opacity:0.9;">多工况对比</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📖 使用说明</div>', unsafe_allow_html=True)
    st.info("""
    **操作步骤：**
    1. 选择左侧【热力场预测】
    2. 输入凝汽器运行参数
    3. 选择图表类型（热力图/等值线图/矢量图/流线图/组合图）
    4. 点击【运行】按钮
    5. 查看预测结果并保存
    """)

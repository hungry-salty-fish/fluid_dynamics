"""
电磁场分析模块
"""

import streamlit as st
import numpy as np
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from components.header import render_header, render_section_header
from components.charts import create_electromagnetic_field
from utils.calculations import run_em_simulation

def show():
    """渲染电磁场分析页面"""
    render_header("电磁场分析系统", "⚡")
    
    col1, col2 = st.columns([1, 2])
    
    # 输入参数
    with col1:
        params = render_em_params()
        
        if st.button("⚡ 开始电磁分析", type="primary", use_container_width=True):
            run_em_calculation(params)
    
    # 可视化
    with col2:
        render_em_visualization(params)
    
    # 结果展示
    if st.session_state.get('em_results'):
        render_em_results()


def render_em_params() -> dict:
    """渲染电磁参数"""
    render_section_header("📥 电磁参数")
    
    voltage = st.slider(
        "⚡ 电压 (V)",
        min_value=0,
        max_value=1000,
        value=220,
        step=10
    )
    
    frequency = st.slider(
        "🔄 频率 (Hz)",
        min_value=1,
        max_value=10000,
        value=50,
        step=1
    )
    
    current = st.slider(
        "🔌 电流 (A)",
        min_value=0.1,
        max_value=100.0,
        value=10.0,
        step=0.5
    )
    
    conductivity = st.select_slider(
        "📊 电导率 (S/m)",
        options=[1e3, 1e4, 1e5, 1e6, 1e7],
        value=1e6,
        format_func=lambda x: f"{x:.0e}"
    )
    
    st.markdown("---")
    
    render_section_header("🧲 磁性材料")
    
    material = st.selectbox(
        "材料类型",
        ["空气", "铁", "镍", "钴", "铁氧体", "自定义"]
    )
    
    permeability = st.number_input(
        "相对磁导率 μr",
        min_value=1.0,
        max_value=10000.0,
        value=1.0 if material == "空气" else 5000.0,
        step=10.0
    )
    
    permittivity = st.number_input(
        "相对介电常数 εr",
        min_value=1.0,
        max_value=1000.0,
        value=1.0,
        step=1.0
    )
    
    return {
        'voltage': voltage,
        'frequency': frequency,
        'current': current,
        'conductivity': conductivity,
        'material': material,
        'permeability': permeability,
        'permittivity': permittivity
    }


def run_em_calculation(params: dict):
    """执行电磁分析计算"""
    with st.spinner("正在进行电磁分析..."):
        time.sleep(1.5)
        
        results = run_em_simulation(params)
        st.session_state.em_results = results
    
    st.success("✅ 电磁分析完成！")
    st.rerun()


def render_em_visualization(params: dict):
    """渲染电磁场可视化"""
    render_section_header("🧲 电磁场分布")
    
    # 创建子图
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("电场强度分布", "磁场强度分布"),
        horizontal_spacing=0.15
    )
    
    # 生成数据
    x = np.linspace(-5, 5, 40)
    y = np.linspace(-5, 5, 40)
    X, Y = np.meshgrid(x, y)
    
    # 电场
    E = params['voltage'] * np.exp(-(X**2 + Y**2) / 5) * \
        np.cos(2 * np.pi * params['frequency'] * X / 1000)
    
    # 磁场
    B = params['current'] * params['permeability'] / (2 * np.pi) * \
        np.exp(-(X**2 + Y**2) / 8)
    
    # 添加电场热图
    fig.add_trace(
        go.Heatmap(x=x, y=y, z=E, colorscale='RdBu', 
                   colorbar=dict(title="E [V/m]", x=0.45)),
        row=1, col=1
    )
    
    # 添加磁场热图
    fig.add_trace(
        go.Heatmap(x=x, y=y, z=B, colorscale='Viridis',
                   colorbar=dict(title="B [T]", x=1.0)),
        row=1, col=2
    )
    
    fig.update_layout(height=400)
    fig.update_xaxes(title_text="X [m]")
    fig.update_yaxes(title_text="Y [m]")
    
    st.plotly_chart(fig, use_container_width=True)


def render_em_results():
    """渲染电磁分析结果"""
    results = st.session_state.em_results
    
    render_section_header("📊 分析结果")
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric(
        "最大电场强度",
        f"{results['max_e_field']:.2f} V/m"
    )
    
    col2.metric(
        "最大磁场强度",
        f"{results['max_b_field']:.4f} T"
    )
    
    col3.metric(
        "趋肤深度",
        f"{results['skin_depth']*1000:.2f} mm"
    )
    
    col4.metric(
        "计算状态",
        "✅ 成功"
    )
    
    # 频率响应曲线
    st.markdown("---")
    render_section_header("📈 频率响应")
    
    frequencies = np.logspace(1, 4, 50)
    impedance = np.sqrt(1 + (frequencies / 100)**2) * 50
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=frequencies,
        y=impedance,
        mode='lines',
        name='阻抗',
        line=dict(color='blue', width=2)
    ))
    
    fig.update_layout(
        title="阻抗-频率曲线",
        xaxis_title="频率 (Hz)",
        yaxis_title="阻抗 (Ω)",
        xaxis_type="log",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

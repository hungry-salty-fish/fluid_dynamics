"""
热传导分析模块
"""

import streamlit as st
import numpy as np
import time
from components.header import render_header, render_section_header
from components.charts import create_temperature_field
from utils.calculations import run_heat_simulation

def show():
    """渲染热传导分析页面"""
    render_header("热传导分析系统", "🔥")
    
    col1, col2 = st.columns([1, 2])
    
    # 输入参数
    with col1:
        params = render_heat_params()
        
        if st.button("🔥 开始热分析", type="primary", use_container_width=True):
            run_heat_calculation(params)
    
    # 可视化
    with col2:
        render_heat_visualization(params)
    
    # 结果展示
    if st.session_state.get('heat_results'):
        render_heat_results()


def render_heat_params() -> dict:
    """渲染热分析参数"""
    render_section_header("📥 热源参数")
    
    heat_source = st.slider(
        "🔥 热源功率 (W)",
        min_value=100,
        max_value=5000,
        value=1000,
        step=100
    )
    
    thermal_conductivity = st.slider(
        "🧊 热导率 (W/m·K)",
        min_value=0.1,
        max_value=500.0,
        value=50.0,
        step=1.0
    )
    
    ambient_temp = st.slider(
        "🌡️ 环境温度 (°C)",
        min_value=-20,
        max_value=50,
        value=25,
        step=1
    )
    
    convection_coeff = st.slider(
        "💨 对流换热系数 (W/m²·K)",
        min_value=1.0,
        max_value=100.0,
        value=25.0,
        step=1.0
    )
    
    st.markdown("---")
    
    render_section_header("⚙️ 材料属性")
    
    material = st.selectbox(
        "材料类型",
        ["铝合金", "铜", "钢", "不锈钢", "陶瓷", "自定义"]
    )
    
    density = st.number_input(
        "密度 (kg/m³)",
        min_value=100.0,
        max_value=20000.0,
        value=2700.0,
        step=100.0
    )
    
    specific_heat = st.number_input(
        "比热容 (J/kg·K)",
        min_value=100.0,
        max_value=5000.0,
        value=900.0,
        step=50.0
    )
    
    return {
        'heat_source': heat_source,
        'thermal_conductivity': thermal_conductivity,
        'ambient_temp': ambient_temp,
        'convection_coeff': convection_coeff,
        'material': material,
        'density': density,
        'specific_heat': specific_heat
    }


def run_heat_calculation(params: dict):
    """执行热分析计算"""
    with st.spinner("正在进行热分析..."):
        time.sleep(1.5)
        
        results = run_heat_simulation(params)
        st.session_state.heat_results = results
    
    st.success("✅ 热分析完成！")
    st.rerun()


def render_heat_visualization(params: dict):
    """渲染热场可视化"""
    render_section_header("🌡️ 温度场分布")
    
    fig = create_temperature_field(
        heat_source=params['heat_source'],
        thermal_conductivity=params['thermal_conductivity'],
        ambient_temp=params['ambient_temp'],
        convection_coeff=params['convection_coeff']
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_heat_results():
    """渲染热分析结果"""
    results = st.session_state.heat_results
    
    render_section_header("📊 分析结果")
    
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric(
        "最高温度",
        f"{results['max_temp']:.1f} °C",
        f"+{results['max_temp'] - results['avg_temp']:.1f}"
    )
    
    col2.metric(
        "最低温度",
        f"{results['min_temp']:.1f} °C",
        f"{results['min_temp'] - results['avg_temp']:.1f}"
    )
    
    col3.metric(
        "平均温度",
        f"{results['avg_temp']:.1f} °C"
    )
    
    col4.metric(
        "热流密度",
        f"{results['heat_flux']:.2f} W/m²"
    )
    
    # 温度曲线
    st.markdown("---")
    render_section_header("📈 温度分布曲线")
    
    import plotly.graph_objects as go
    
    x = results['x']
    T_center = results['temperature_field'][25, :]  # 中心线温度
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=T_center,
        mode='lines',
        name='中心线温度',
        line=dict(color='red', width=2)
    ))
    
    fig.update_layout(
        title="中心线温度分布",
        xaxis_title="位置 (mm)",
        yaxis_title="温度 (°C)",
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)

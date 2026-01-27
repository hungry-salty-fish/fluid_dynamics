"""
结果对比模块
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from components.header import render_header, render_section_header

def show():
    """渲染结果对比页面"""
    render_header("结果对比分析", "📊")
    
    # 对比模式选择
    compare_mode = st.radio(
        "对比模式",
        ["多工况对比", "历史对比", "参数敏感性分析"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if compare_mode == "多工况对比":
        render_multi_case_compare()
    elif compare_mode == "历史对比":
        render_history_compare()
    else:
        render_sensitivity_analysis()


def render_multi_case_compare():
    """渲染多工况对比"""
    render_section_header("📈 多工况对比")
    
    # 模拟数据
    cases = ["工况1", "工况2", "工况3", "工况4"]
    velocities = [125.3, 142.8, 156.2, 138.9]
    pressures = [198.5, 210.3, 225.1, 205.8]
    temperatures = [45.2, 48.6, 52.1, 47.3]
    efficiencies = [85.2, 87.5, 89.1, 86.3]
    
    # 图表
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = go.Figure(data=[
            go.Bar(x=cases, y=velocities, marker_color='steelblue')
        ])
        fig1.update_layout(
            title="各工况流速对比",
            yaxis_title="流速 (m/s)",
            height=300
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = go.Figure(data=[
            go.Bar(x=cases, y=pressures, marker_color='coral')
        ])
        fig2.update_layout(
            title="各工况压力对比",
            yaxis_title="压力 (kPa)",
            height=300
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        fig3 = go.Figure(data=[
            go.Bar(x=cases, y=temperatures, marker_color='green')
        ])
        fig3.update_layout(
            title="各工况温度对比",
            yaxis_title="温度 (°C)",
            height=300
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        fig4 = go.Figure(data=[
            go.Bar(x=cases, y=efficiencies, marker_color='purple')
        ])
        fig4.update_layout(
            title="各工况效率对比",
            yaxis_title="效率 (%)",
            height=300
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # 数据表格
    render_section_header("📋 详细数据")
    
    df = pd.DataFrame({
        "工况": cases,
        "流速 (m/s)": velocities,
        "压力 (kPa)": pressures,
        "温度 (°C)": temperatures,
        "效率 (%)": efficiencies
    })
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # 导出按钮
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 导出数据",
            csv,
            "comparison_data.csv",
            "text/csv",
            use_container_width=True
        )


def render_history_compare():
    """渲染历史对比"""
    render_section_header("📜 历史数据对比")
    
    # 选择对比的历史记录
    col1, col2 = st.columns(2)
    
    with col1:
        record1 = st.selectbox(
            "选择记录 1",
            ["2024-01-15 流体分析", "2024-01-14 热分析", "2024-01-13 流体分析"]
        )
    
    with col2:
        record2 = st.selectbox(
            "选择记录 2",
            ["2024-01-14 热分析", "2024-01-15 流体分析", "2024-01-13 流体分析"]
        )
    
    # 对比结果
    st.markdown("---")
    
    # 模拟历史数据
    x = np.linspace(0, 100, 50)
    y1 = 100 + 50 * np.sin(x / 10) + np.random.normal(0, 5, 50)
    y2 = 110 + 45 * np.sin(x / 10 + 0.5) + np.random.normal(0, 5, 50)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name=record1))
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name=record2))
    
    fig.update_layout(
        title="历史数据对比曲线",
        xaxis_title="位置",
        yaxis_title="数值",
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 差异统计
    col1, col2, col3, col4 = st.columns(4)
    
    diff = y2 - y1
    col1.metric("平均差异", f"{np.mean(diff):.2f}")
    col2.metric("最大差异", f"{np.max(np.abs(diff)):.2f}")
    col3.metric("标准差", f"{np.std(diff):.2f}")
    col4.metric("相关系数", f"{np.corrcoef(y1, y2)[0,1]:.4f}")


def render_sensitivity_analysis():
    """渲染参数敏感性分析"""
    render_section_header("🔍 参数敏感性分析")
    
    # 选择分析参数
    param = st.selectbox(
        "选择分析参数",
        ["进气量", "入口压力", "循环水温度", "运行模式"]
    )
    
    output = st.selectbox(
        "选择输出变量",
        ["出口流速", "压力损失", "温度变化", "效率"]
    )
    
    st.markdown("---")
    
    # 生成敏感性数据
    if param == "进气量":
        x = np.linspace(0.5, 5, 20)
        xlabel = "进气量 (m³/s)"
    elif param == "入口压力":
        x = np.linspace(100, 400, 20)
        xlabel = "入口压力 (kPa)"
    elif param == "循环水温度":
        x = np.linspace(10, 80, 20)
        xlabel = "循环水温度 (°C)"
    else:
        x = np.array([1, 2, 3])
        xlabel = "运行模式"
    
    y = 50 + 20 * np.log(x + 1) + np.random.normal(0, 2, len(x))
    
    # 敏感性曲线
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines+markers',
        name=output,
        line=dict(color='blue', width=2)
    ))
    
    # 添加趋势线
    z = np.polyfit(x, y, 2)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=x, y=p(x),
        mode='lines',
        name='趋势线',
        line=dict(color='red', dash='dash')
    ))
    
    fig.update_layout(
        title=f"{param} 对 {output} 的影响",
        xaxis_title=xlabel,
        yaxis_title=output,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 敏感性指标
    sensitivity = np.gradient(y, x).mean()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("敏感性系数", f"{sensitivity:.4f}")
    col2.metric("影响程度", "高" if abs(sensitivity) > 1 else "中" if abs(sensitivity) > 0.5 else "低")
    col3.metric("建议", "需要精确控制" if abs(sensitivity) > 1 else "正常控制")

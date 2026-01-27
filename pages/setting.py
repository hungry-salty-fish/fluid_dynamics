"""
系统设置模块
"""

import streamlit as st
from components.header import render_header, render_section_header
from utils.constants import THEMES, LANGUAGES

def show():
    """渲染系统设置页面"""
    render_header("系统设置", "⚙️")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎨 显示设置",
        "⚡ 计算设置",
        "🔧 高级设置",
        "ℹ️ 关于系统"
    ])
    
    with tab1:
        render_display_settings()
    
    with tab2:
        render_calculation_settings()
    
    with tab3:
        render_advanced_settings()
    
    with tab4:
        render_about()


def render_display_settings():
    """渲染显示设置"""
    render_section_header("🎨 主题与外观")
    
    col1, col2 = st.columns(2)
    
    with col1:
        theme = st.selectbox(
            "主题",
            THEMES,
            index=0
        )
        
        language = st.selectbox(
            "语言",
            LANGUAGES,
            index=0
        )
        
        font_size = st.slider(
            "字体大小",
            min_value=12,
            max_value=24,
            value=16,
            step=1
        )
    
    with col2:
        chart_style = st.selectbox(
            "图表样式",
            ["默认", "科技风", "简约", "彩色"]
        )
        
        animation = st.toggle(
            "启用动画效果",
            value=True
        )
        
        show_grid = st.toggle(
            "显示网格线",
            value=True
        )
    
    st.markdown("---")
    
    render_section_header("📊 图表设置")
    
    col1, col2 = st.columns(2)
    
    with col1:
        default_colormap = st.selectbox(
            "默认颜色映射",
            ["Jet", "Rainbow", "Viridis", "Plasma", "Hot"]
        )
        
        chart_height = st.slider(
            "默认图表高度",
            min_value=200,
            max_value=800,
            value=400,
            step=50
        )
    
    with col2:
        dpi = st.slider(
            "图像分辨率 (DPI)",
            min_value=72,
            max_value=300,
            value=150,
            step=10
        )
        
        auto_refresh = st.toggle(
            "自动刷新图表",
            value=False
        )
    
    # 保存按钮
    st.markdown("---")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("💾 保存设置", type="primary", use_container_width=True):
            st.session_state['display_settings'] = {
                'theme': theme,
                'language': language,
                'font_size': font_size,
                'chart_style': chart_style,
                'animation': animation,
                'show_grid': show_grid,
                'default_colormap': default_colormap,
                'chart_height': chart_height,
                'dpi': dpi,
                'auto_refresh': auto_refresh
            }
            st.success("✅ 显示设置已保存！")


def render_calculation_settings():
    """渲染计算设置"""
    render_section_header("⚡ 求解器设置")
    
    col1, col2 = st.columns(2)
    
    with col1:
        solver_type = st.selectbox(
            "求解器类型",
            ["SIMPLE", "SIMPLEC", "PISO", "耦合求解器"]
        )
        
        max_iterations = st.number_input(
            "最大迭代次数",
            min_value=100,
            max_value=100000,
            value=1000,
            step=100
        )
        
        convergence_criteria = st.select_slider(
            "收敛标准",
            options=[1e-3, 1e-4, 1e-5, 1e-6, 1e-7],
            value=1e-5,
            format_func=lambda x: f"{x:.0e}"
        )
    
    with col2:
        time_scheme = st.selectbox(
            "时间离散格式",
            ["一阶隐式", "二阶隐式", "Crank-Nicolson"]
        )
        
        spatial_scheme = st.selectbox(
            "空间离散格式",
            ["一阶迎风", "二阶迎风", "QUICK", "中心差分"]
        )
        
        under_relaxation = st.slider(
            "欠松弛因子",
            min_value=0.1,
            max_value=1.0,
            value=0.7,
            step=0.05
        )
    
    st.markdown("---")
    
    render_section_header("🔢 网格设置")
    
    col1, col2 = st.columns(2)
    
    with col1:
        mesh_type = st.selectbox(
            "网格类型",
            ["结构化网格", "非结构化网格", "混合网格"]
        )
        
        mesh_quality = st.selectbox(
            "网格质量",
            ["粗糙 (快速)", "中等 (平衡)", "精细 (精确)", "超精细 (研究级)"]
        )
    
    with col2:
        min_cell_size = st.number_input(
            "最小网格尺寸 (mm)",
            min_value=0.1,
            max_value=100.0,
            value=1.0,
            step=0.1
        )
        
        growth_rate = st.slider(
            "网格增长率",
            min_value=1.0,
            max_value=2.0,
            value=1.2,
            step=0.05
        )
    
    st.markdown("---")
    
    render_section_header("💻 并行计算")
    
    col1, col2 = st.columns(2)
    
    with col1:
        enable_parallel = st.toggle(
            "启用并行计算",
            value=True
        )
        
        if enable_parallel:
            num_cores = st.slider(
                "CPU核心数",
                min_value=1,
                max_value=32,
                value=4
            )
    
    with col2:
        enable_gpu = st.toggle(
            "启用GPU加速",
            value=False
        )
        
        if enable_gpu:
            gpu_device = st.selectbox(
                "GPU设备",
                ["GPU 0: NVIDIA RTX 3080", "GPU 1: NVIDIA RTX 3070"]
            )
    
    # 保存按钮
    st.markdown("---")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("💾 保存设置", type="primary", use_container_width=True, key="save_calc"):
            st.success("✅ 计算设置已保存！")


def render_advanced_settings():
    """渲染高级设置"""
    render_section_header("🔧 高级选项")
    
    st.warning("⚠️ 以下设置仅供高级用户使用，修改不当可能影响系统稳定性。")
    
    col1, col2 = st.columns(2)
    
    with col1:
        debug_mode = st.toggle(
            "调试模式",
            value=False,
            help="启用后会显示详细的调试信息"
        )
        
        log_level = st.selectbox(
            "日志级别",
            ["ERROR", "WARNING", "INFO", "DEBUG"]
        )
        
        cache_size = st.slider(
            "缓存大小 (MB)",
            min_value=100,
            max_value=4096,
            value=512,
            step=100
        )
    
    with col2:
        auto_save = st.toggle(
            "自动保存",
            value=True
        )
        
        if auto_save:
            save_interval = st.number_input(
                "保存间隔 (分钟)",
                min_value=1,
                max_value=60,
                value=5
            )
        
        backup_enabled = st.toggle(
            "启用备份",
            value=True
        )
    
    st.markdown("---")
    
    render_section_header("📁 文件路径")
    
    work_dir = st.text_input(
        "工作目录",
        value="/home/user/cfd_projects"
    )
    
    output_dir = st.text_input(
        "输出目录",
        value="/home/user/cfd_results"
    )
    
    temp_dir = st.text_input(
        "临时文件目录",
        value="/tmp/cfd_temp"
    )
    
    st.markdown("---")
    
    render_section_header("🔄 系统维护")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧹 清理缓存", use_container_width=True):
            with st.spinner("正在清理..."):
                import time
                time.sleep(1)
            st.success("✅ 缓存已清理！")
    
    with col2:
        if st.button("🔄 重置设置", use_container_width=True):
            st.warning("确定要重置所有设置吗？")
    
    with col3:
        if st.button("📤 导出配置", use_container_width=True):
            config = {
                "debug_mode": debug_mode,
                "log_level": log_level,
                "cache_size": cache_size,
                "work_dir": work_dir,
                "output_dir": output_dir
            }
            import json
            st.download_button(
                "📥 下载配置文件",
                json.dumps(config, indent=2),
                "cfd_config.json",
                "application/json"
            )


def render_about():
    """渲染关于页面"""
    render_section_header("ℹ️ 关于系统")
    
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <div style="font-size: 4rem;">🌊</div>
        <h2>CFD 分析系统</h2>
        <p style="color: gray;">Computational Fluid Dynamics Analysis System</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **版本信息**
        - 当前版本：v2.0.1
        - 发布日期：2024-01-15
        - 更新通道：稳定版
        """)
    
    with col2:
        st.markdown("""
        **系统要求**
        - Python：3.8+
        - 内存：8GB+
        - 存储：10GB+
        """)
    
    with col3:
        st.markdown("""
        **技术支持**
        - 邮箱：support@cfdlab.com
        - 文档：docs.cfdlab.com
        - 社区：forum.cfdlab.com
        """)
    
    st.markdown("---")
    
    render_section_header("📦 依赖组件")
    
    dependencies = {
        "Streamlit": "1.29.0",
        "NumPy": "1.24.0",
        "Pandas": "2.0.0",
        "Plotly": "5.18.0",
        "SciPy": "1.11.0"
    }
    
    dep_df = pd.DataFrame([
        {"组件": k, "版本": v, "状态": "✅ 正常"} 
        for k, v in dependencies.items()
    ])
    
    st.dataframe(dep_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    render_section_header("📜 更新日志")
    
    with st.expander("v2.0.1 (2024-01-15)", expanded=True):
        st.markdown("""
        - 🆕 新增电磁场分析模块
        - 🔧 优化流体计算性能
        - 🐛 修复热分析边界条件问题
        - 📊 改进结果可视化界面
        """)
    
    with st.expander("v2.0.0 (2024-01-01)"):
        st.markdown("""
        - 🎉 全新UI设计
        - 🆕 新增热传导分析
        - 🆕 新增结果对比功能
        - 🔧 重构代码架构
        """)
    
    with st.expander("v1.5.0 (2023-12-01)"):
        st.markdown("""
        - 🆕 新增参数敏感性分析
        - 🔧 优化数据导出功能
        - 🐛 修复多个已知问题
        """)
    
    st.markdown("---")
    
    render_section_header("📄 许可证")
    
    st.info("""
    **MIT License**
    
    Copyright (c) 2024 CFD Lab
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software.
    """)

"""
数据管理模块
"""

import streamlit as st
import pandas as pd
import numpy as np
from components.header import render_header, render_section_header
from utils.data_io import import_data, export_data, get_history_data, generate_report

def show():
    """渲染数据管理页面"""
    render_header("数据管理中心", "📁")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📤 数据导入", 
        "📥 数据导出", 
        "🗄️ 历史记录",
        "📋 报告生成"
    ])
    
    with tab1:
        render_import_tab()
    
    with tab2:
        render_export_tab()
    
    with tab3:
        render_history_tab()
    
    with tab4:
        render_report_tab()


def render_import_tab():
    """渲染数据导入标签页"""
    render_section_header("📤 上传数据文件")
    
    uploaded_file = st.file_uploader(
        "选择文件",
        type=['csv', 'xlsx', 'xls', 'json'],
        help="支持 CSV、Excel、JSON 格式"
    )
    
    if uploaded_file is not None:
        try:
            df = import_data(uploaded_file)
            
            st.success(f"✅ 成功导入 {len(df)} 行数据")
            
            # 数据预览
            render_section_header("📊 数据预览")
            st.dataframe(df.head(20), use_container_width=True)
            
            # 数据统计
            render_section_header("📈 数据统计")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("总行数", len(df))
            col2.metric("总列数", len(df.columns))
            col3.metric("数值列", len(df.select_dtypes(include=[np.number]).columns))
            col4.metric("缺失值", df.isnull().sum().sum())
            
            # 保存到session
            if st.button("💾 保存到工作区", type="primary"):
                st.session_state['imported_data'] = df
                st.success("数据已保存到工作区！")
                
        except Exception as e:
            st.error(f"❌ 导入失败: {str(e)}")
    
    st.markdown("---")
    
    render_section_header("📝 手动输入数据")
    
    data_text = st.text_area(
        "粘贴数据 (CSV格式)",
        height=150,
        placeholder="列1,列2,列3\n值1,值2,值3\n..."
    )
    
    if data_text and st.button("📥 解析数据"):
        try:
            from io import StringIO
            df = pd.read_csv(StringIO(data_text))
            st.success(f"✅ 成功解析 {len(df)} 行数据")
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"❌ 解析失败: {str(e)}")


def render_export_tab():
    """渲染数据导出标签页"""
    render_section_header("📥 导出设置")
    
    # 选择导出格式
    export_format = st.selectbox(
        "导出格式",
        ["CSV", "Excel", "JSON"]
    )
    
    # 选择导出内容
    export_content = st.multiselect(
        "导出内容",
        ["流场数据", "温度场数据", "压力场数据", "统计结果", "输入参数"],
        default=["流场数据", "统计结果"]
    )
    
    # 文件名
    filename = st.text_input(
        "文件名",
        value="cfd_export_data"
    )
    
    st.markdown("---")
    
    # 生成导出数据
    if st.button("🔄 生成导出数据", type="primary"):
        # 模拟数据
        export_df = pd.DataFrame({
            "位置_X": np.linspace(0, 100, 50),
            "位置_Y": np.linspace(0, 50, 50),
            "流速": np.random.uniform(100, 200, 50),
            "压力": np.random.uniform(100, 300, 50),
            "温度": np.random.uniform(20, 80, 50)
        })
        
        st.session_state['export_data'] = export_df
        st.success("✅ 导出数据已生成")
        
        st.dataframe(export_df.head(10), use_container_width=True)
    
    # 下载按钮
    if 'export_data' in st.session_state:
        df = st.session_state['export_data']
        
        if export_format == "CSV":
            data = df.to_csv(index=False).encode('utf-8')
            mime = "text/csv"
            ext = ".csv"
        elif export_format == "Excel":
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            data = output.getvalue()
            mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ext = ".xlsx"
        else:  # JSON
            data = df.to_json(orient='records', force_ascii=False).encode('utf-8')
            mime = "application/json"
            ext = ".json"
        
        st.download_button(
            f"📥 下载 {export_format} 文件",
            data,
            f"{filename}{ext}",
            mime,
            use_container_width=True
        )


def render_history_tab():
    """渲染历史记录标签页"""
    render_section_header("🗄️ 计算历史")
    
    # 获取历史数据
    history_df = get_history_data()
    
    # 筛选选项
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_type = st.selectbox(
            "分析类型",
            ["全部", "流体分析", "热分析", "电磁分析"]
        )
    
    with col2:
        filter_status = st.selectbox(
            "状态",
            ["全部", "完成", "失败"]
        )
    
    with col3:
        sort_by = st.selectbox(
            "排序",
            ["时间 (新→旧)", "时间 (旧→新)", "文件大小"]
        )
    
    # 应用筛选
    filtered_df = history_df.copy()
    
    if filter_type != "全部":
        filtered_df = filtered_df[filtered_df['type'] == filter_type]
    
    if filter_status == "完成":
        filtered_df = filtered_df[filtered_df['status'].str.contains("完成")]
    elif filter_status == "失败":
        filtered_df = filtered_df[filtered_df['status'].str.contains("失败")]
    
    # 应用排序
    if sort_by == "时间 (新→旧)":
        filtered_df = filtered_df.sort_values('time', ascending=False)
    elif sort_by == "时间 (旧→新)":
        filtered_df = filtered_df.sort_values('time', ascending=True)
    
    st.markdown("---")
    
    # 显示历史记录
    st.dataframe(
        filtered_df[['time', 'type', 'status', 'file_size', 'params']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "time": st.column_config.TextColumn("时间", width="medium"),
            "type": st.column_config.TextColumn("类型", width="small"),
            "status": st.column_config.TextColumn("状态", width="small"),
            "file_size": st.column_config.TextColumn("文件大小", width="small"),
            "params": st.column_config.TextColumn("参数", width="large")
        }
    )
    
    # 批量操作
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 刷新", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("📥 导出选中", use_container_width=True):
            st.info("请先选择要导出的记录")
    
    with col3:
        if st.button("🗑️ 删除选中", use_container_width=True):
            st.warning("请先选择要删除的记录")
    
    with col4:
        if st.button("🧹 清空历史", use_container_width=True):
            st.warning("确定要清空所有历史记录吗？")


def render_report_tab():
    """渲染报告生成标签页"""
    render_section_header("📋 报告生成")
    
    # 报告类型
    report_type = st.selectbox(
        "报告类型",
        ["完整分析报告", "简要摘要", "数据报表", "图表报告"]
    )
    
    # 报告内容选择
    st.markdown("**包含内容：**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        include_params = st.checkbox("输入参数", value=True)
        include_results = st.checkbox("计算结果", value=True)
        include_charts = st.checkbox("图表", value=True)
    
    with col2:
        include_stats = st.checkbox("统计分析", value=True)
        include_conclusions = st.checkbox("结论建议", value=False)
        include_raw_data = st.checkbox("原始数据", value=False)
    
    # 报告格式
    report_format = st.radio(
        "输出格式",
        ["PDF", "Word", "HTML", "Markdown"],
        horizontal=True
    )
    
    # 报告标题
    report_title = st.text_input(
        "报告标题",
        value="CFD分析报告"
    )
    
    # 作者信息
    author = st.text_input(
        "作者",
        value="CFD Lab"
    )
    
    st.markdown("---")
    
    # 生成报告
    if st.button("📝 生成报告", type="primary", use_container_width=True):
        with st.spinner("正在生成报告..."):
            import time
            time.sleep(2)
            
            # 模拟生成报告
            report_content = f"""
# {report_title}

**作者：** {author}
**生成时间：** {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")}
**报告类型：** {report_type}

---

## 1. 概述

本报告由CFD分析系统自动生成，包含流体动力学分析的完整结果。

## 2. 输入参数

| 参数 | 数值 | 单位 |
|------|------|------|
| 循环水温度 | 25.0 | °C |
| 进气量 | 2.5 | m³/s |
| 入口压力 | 200.0 | kPa |
| 出口压力 | 101.3 | kPa |

## 3. 计算结果

| 输出 | 数值 | 单位 |
|------|------|------|
| 平均流速 | 156.8 | m/s |
| 最大流速 | 232.5 | m/s |
| 压力损失 | 98.7 | kPa |
| 雷诺数 | 1.2×10⁶ | - |

## 4. 结论

分析结果表明系统运行正常，各项指标在预期范围内。

---

*本报告由 CFD 分析系统 v2.0.1 自动生成*
"""
            
            st.session_state['generated_report'] = report_content
        
        st.success("✅ 报告生成完成！")
    
    # 显示和下载报告
    if 'generated_report' in st.session_state:
        render_section_header("📄 报告预览")
        
        st.markdown(st.session_state['generated_report'])
        
        st.download_button(
            "📥 下载报告",
            st.session_state['generated_report'],
            f"{report_title}.md",
            "text/markdown",
            use_container_width=True
        )

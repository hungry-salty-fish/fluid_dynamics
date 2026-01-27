"""
核电凝汽器热力特性场预测模块
- 前台：4个输入参数 + 图表类型选择
- 后台：Excel文件 + 8个计算系数（用户不可见）
- 支持5种图表类型：热力图、等值线图、矢量图、流线图、组合图
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os

# ==================== 后台固定配置 ====================
EXCEL_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "8张图.xlsx")
# 或使用绝对路径
# EXCEL_FILE_PATH = r"C:\Users\admin\Nutstore\1\同步文件夹\项目程序\data\8张图.xlsx"

IMG_HEIGHT = 190
IMG_WIDTH = 87

# 图表类型选项
CHART_TYPES = {
    "热力图": "heatmap",
    "等值线图": "contour",
    "流场矢量图": "vector",
    "流线图": "streamline",
    "组合图（等值线+矢量）": "combined"
}


def calculate_coefficients(p1: float, p2: float, p3: float, p4: float) -> list:
    """根据4个前台参数计算8个后台系数"""
    c1 = p1 * 0.10 + 0.05
    c2 = -p2 * 0.15 - 0.10
    c3 = p3 * 0.20 + 0.15
    c4 = p1 * p2 * 0.05
    c5 = -p3 * 0.10 - 0.10
    c6 = p4 * 0.20 + 0.10
    c7 = -(p1 + p2) * 0.05 - 0.05
    c8 = (p3 + p4) * 0.10
    return [c1, c2, c3, c4, c5, c6, c7, c8]


def show():
    """渲染页面"""
    # 主标题
    st.markdown("""
        <div style="
            font-size: 1.6rem;
            font-weight: bold;
            color: #1565C0;
            text-align: center;
            padding: 12px;
            border-bottom: 3px solid #1565C0;
            margin-bottom: 15px;
            background: linear-gradient(90deg, #E3F2FD, white, #E3F2FD);
            border-radius: 8px;
        ">
            ⚛️ 核电凝汽器热力特性场预测
        </div>
    """, unsafe_allow_html=True)
    
    # 三列布局
    col_input, col_image, col_stats = st.columns([1.2, 2.5, 1])
    
    # ===== 左侧：输入参数 =====
    with col_input:
        st.markdown('<div class="section-header">🔧 输入参数</div>', unsafe_allow_html=True)
        
        p1 = st.number_input("循环水温度 (°C)", 0.0, 50.0, 25.0, 0.5, format="%.1f")
        p2 = st.number_input("循环水流量 (m³/s)", 0.0, 100.0, 45.0, 1.0, format="%.1f")
        p3 = st.number_input("蒸汽压力 (kPa)", 0.0, 20.0, 5.0, 0.1, format="%.2f")
        p4 = st.number_input("热负荷 (MW)", 0.0, 2000.0, 800.0, 10.0, format="%.0f")
        
        st.markdown("---")
        st.markdown('<div class="section-header">📊 图表类型</div>', unsafe_allow_html=True)
        chart_type = st.selectbox(
            "选择图表类型", 
            list(CHART_TYPES.keys()), 
            index=0,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown('<div class="section-header">🎮 操作</div>', unsafe_allow_html=True)
        
        b1, b2 = st.columns(2)
        with b1:
            run_clicked = st.button("🚀 运行", type="primary", use_container_width=True)
        with b2:
            reset_clicked = st.button("🔄 重置", use_container_width=True)
        
        if st.session_state.get('synthesized_img') is not None:
            csv_data = pd.DataFrame(st.session_state.synthesized_img).to_csv(index=False, header=False)
            st.download_button("💾 保存结果", csv_data, "result.csv", "text/csv", use_container_width=True)
        
        if run_clicked:
            run_synthesis(p1, p2, p3, p4)
        if reset_clicked:
            st.session_state.calculated = False
            st.session_state.synthesized_img = None
            st.session_state.flow_data = None
            st.rerun()
    
    # ===== 中间：图像 =====
    with col_image:
        chart_titles = {
            "热力图": "🌡️ 温度场热力分布",
            "等值线图": "📈 温度场等值线分布",
            "流场矢量图": "🌀 流场矢量分布",
            "流线图": "💨 流线分布图",
            "组合图（等值线+矢量）": "🔥 等值线+矢量组合图"
        }
        st.markdown(f'<div class="section-header">{chart_titles.get(chart_type, "🌡️ 热力特性场分布")}</div>', unsafe_allow_html=True)
        
        if st.session_state.get('calculated') and st.session_state.get('synthesized_img') is not None:
            fig = create_chart(st.session_state.synthesized_img, st.session_state.flow_data, CHART_TYPES[chart_type])
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig = create_empty_chart()
            st.plotly_chart(fig, use_container_width=True)
            st.info("👈 请设置参数后点击【运行】按钮进行预测")
    
    # ===== 右侧：统计 =====
    with col_stats:
        st.markdown('<div class="section-header">📈 统计分析</div>', unsafe_allow_html=True)
        
        if st.session_state.get('calculated') and st.session_state.get('synthesized_img') is not None:
            img = st.session_state.synthesized_img
            flow = st.session_state.flow_data
            
            st.markdown("**温度场**")
            st.metric("最大值", f"{np.max(img):.4f}")
            st.metric("最小值", f"{np.min(img):.4f}")
            st.metric("平均值", f"{np.mean(img):.4f}")
            st.metric("标准差", f"{np.std(img):.4f}")
            
            st.markdown("---")
            
            if flow is not None:
                st.markdown("**流场速度**")
                st.metric("最大速度", f"{np.max(flow['speed']):.4f}")
                st.metric("平均速度", f"{np.mean(flow['speed']):.4f}")
            
            st.markdown("---")
            st.markdown("**图像信息**")
            st.code(f"尺寸: {IMG_HEIGHT}×{IMG_WIDTH}")
        else:
            st.metric("最大值", "—")
            st.metric("最小值", "—")
            st.metric("平均值", "—")
            st.metric("标准差", "—")
            st.markdown("---")
            st.caption("等待计算结果...")


def create_chart(img_data: np.ndarray, flow_data: dict, chart_type: str) -> go.Figure:
    """根据类型创建图表"""
    if chart_type == "heatmap":
        return create_heatmap_chart(img_data)
    elif chart_type == "contour":
        return create_contour_chart(img_data)
    elif chart_type == "vector":
        return create_vector_chart(img_data, flow_data)
    elif chart_type == "streamline":
        return create_streamline_chart(img_data, flow_data)
    elif chart_type == "combined":
        return create_combined_chart(img_data, flow_data)
    return create_heatmap_chart(img_data)


def create_heatmap_chart(img_data: np.ndarray) -> go.Figure:
    """热力图"""
    x = np.arange(IMG_WIDTH)
    y = np.arange(IMG_HEIGHT)
    
    fig = go.Figure()
    
    fig.add_trace(go.Heatmap(
        z=img_data,
        x=x,
        y=y,
        colorscale='jet',
        colorbar=dict(
            title=dict(text="温度值", side="right"),
            thickness=15,
            len=0.9
        )
    ))
    
    fig.update_layout(
        title=dict(
            text=f"温度场热力图 ({IMG_HEIGHT}×{IMG_WIDTH})",
            x=0.5,
            font=dict(size=14, color="#333")
        ),
        xaxis=dict(
            title="X 位置",
            scaleanchor="y",
            scaleratio=1,
            showgrid=False
        ),
        yaxis=dict(
            title="Y 位置",
            autorange="reversed",
            showgrid=False
        ),
        height=550,
        margin=dict(l=50, r=20, t=50, b=40)
    )
    
    return fig


def create_contour_chart(img_data: np.ndarray) -> go.Figure:
    """等值线图"""
    x = np.arange(IMG_WIDTH)
    y = np.arange(IMG_HEIGHT)
    
    fig = go.Figure()
    
    # 填充等值线
    fig.add_trace(go.Contour(
        z=img_data,
        x=x,
        y=y,
        colorscale='jet',
        contours=dict(
            showlabels=True,
            labelfont=dict(size=9, color='white')
        ),
        colorbar=dict(
            title=dict(text="温度值", side="right"),
            thickness=15,
            len=0.9
        ),
        line=dict(width=1)
    ))
    
    fig.update_layout(
        title=dict(
            text=f"温度场等值线图 ({IMG_HEIGHT}×{IMG_WIDTH})",
            x=0.5,
            font=dict(size=14, color="#333")
        ),
        xaxis=dict(
            title="X 位置",
            scaleanchor="y",
            scaleratio=1,
            showgrid=False
        ),
        yaxis=dict(
            title="Y 位置",
            autorange="reversed",
            showgrid=False
        ),
        height=550,
        margin=dict(l=50, r=20, t=50, b=40)
    )
    
    return fig


def create_vector_chart(img_data: np.ndarray, flow_data: dict) -> go.Figure:
    """流场矢量图（统一箭头大小）"""
    x = np.arange(IMG_WIDTH)
    y = np.arange(IMG_HEIGHT)
    
    # 降采样
    step = 8
    x_s = x[::step]
    y_s = y[::step]
    
    u_s = flow_data['u'][::step, ::step]
    v_s = flow_data['v'][::step, ::step]
    speed_s = flow_data['speed'][::step, ::step]
    
    # 归一化：统一箭头大小
    speed_safe = np.where(speed_s == 0, 1, speed_s)
    u_norm = u_s / speed_safe
    v_norm = v_s / speed_safe
    
    fig = go.Figure()
    
    # 背景：速度大小热力图
    fig.add_trace(go.Heatmap(
        z=flow_data['speed'],
        x=x,
        y=y,
        colorscale='Blues',
        opacity=0.6,
        colorbar=dict(
            title=dict(text="速度大小", side="right"),
            thickness=15,
            len=0.9,
            x=1.02
        )
    ))
    
    # 创建箭头
    annotations = []
    scale = 5
    
    for i in range(len(y_s)):
        for j in range(len(x_s)):
            if speed_s[i, j] > 0.001:
                annotations.append(dict(
                    x=x_s[j] + u_norm[i, j] * scale,
                    y=y_s[i] + v_norm[i, j] * scale,
                    ax=x_s[j],
                    ay=y_s[i],
                    xref="x",
                    yref="y",
                    axref="x",
                    ayref="y",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=1.5,
                    arrowcolor="red"
                ))
    
    fig.update_layout(
        title=dict(
            text=f"流场矢量图 ({IMG_HEIGHT}×{IMG_WIDTH})",
            x=0.5,
            font=dict(size=14, color="#333")
        ),
        xaxis=dict(
            title="X 位置",
            scaleanchor="y",
            scaleratio=1,
            showgrid=False,
            range=[0, IMG_WIDTH]
        ),
        yaxis=dict(
            title="Y 位置",
            autorange="reversed",
            showgrid=False,
            range=[0, IMG_HEIGHT]
        ),
        height=550,
        margin=dict(l=50, r=70, t=50, b=40),
        annotations=annotations
    )
    
    return fig


def create_streamline_chart(img_data: np.ndarray, flow_data: dict) -> go.Figure:
    """流线图"""
    x = np.arange(IMG_WIDTH)
    y = np.arange(IMG_HEIGHT)
    
    fig = go.Figure()
    
    # 背景：温度场热力图
    fig.add_trace(go.Heatmap(
        z=img_data,
        x=x,
        y=y,
        colorscale='jet',
        opacity=0.5,
        colorbar=dict(
            title=dict(text="温度值", side="right"),
            thickness=15,
            len=0.9
        )
    ))
    
    # 流线计算
    u = flow_data['u']
    v = flow_data['v']
    speed = flow_data['speed']
    
    # 生成流线起点
    step = 6
    
    for sy in range(0, IMG_HEIGHT, step * 2):
        for sx in range(0, IMG_WIDTH, step * 2):
            line_x = [sx]
            line_y = [sy]
            px, py = float(sx), float(sy)
            
            # 沿流线方向追踪
            for _ in range(25):
                if 0 <= int(py) < IMG_HEIGHT and 0 <= int(px) < IMG_WIDTH:
                    uu = u[int(py), int(px)]
                    vv = v[int(py), int(px)]
                    ss = speed[int(py), int(px)]
                    
                    if ss > 0.001:
                        # 归一化并移动
                        px += uu / ss * 2.0
                        py += vv / ss * 2.0
                        
                        if 0 <= px < IMG_WIDTH and 0 <= py < IMG_HEIGHT:
                            line_x.append(px)
                            line_y.append(py)
                        else:
                            break
                    else:
                        break
                else:
                    break
            
            # 添加流线
            if len(line_x) > 2:
                fig.add_trace(go.Scatter(
                    x=line_x,
                    y=line_y,
                    mode='lines',
                    line=dict(color='white', width=1.2),
                    showlegend=False,
                    hoverinfo='skip'
                ))
    
    fig.update_layout(
        title=dict(
            text=f"流线分布图 ({IMG_HEIGHT}×{IMG_WIDTH})",
            x=0.5,
            font=dict(size=14, color="#333")
        ),
        xaxis=dict(
            title="X 位置",
            scaleanchor="y",
            scaleratio=1,
            showgrid=False,
            range=[0, IMG_WIDTH]
        ),
        yaxis=dict(
            title="Y 位置",
            autorange="reversed",
            showgrid=False,
            range=[0, IMG_HEIGHT]
        ),
        height=550,
        margin=dict(l=50, r=20, t=50, b=40)
    )
    
    return fig


def create_combined_chart(img_data: np.ndarray, flow_data: dict) -> go.Figure:
    """组合图（等值线+矢量）"""
    x = np.arange(IMG_WIDTH)
    y = np.arange(IMG_HEIGHT)
    
    # 降采样
    step = 10
    x_s = x[::step]
    y_s = y[::step]
    
    u_s = flow_data['u'][::step, ::step]
    v_s = flow_data['v'][::step, ::step]
    speed_s = flow_data['speed'][::step, ::step]
    
    # 归一化
    speed_safe = np.where(speed_s == 0, 1, speed_s)
    u_norm = u_s / speed_safe
    v_norm = v_s / speed_safe
    
    fig = go.Figure()
    
    # 等值线填充
    fig.add_trace(go.Contour(
        z=img_data,
        x=x,
        y=y,
        colorscale='jet',
        opacity=0.7,
        contours=dict(showlabels=False),
        colorbar=dict(
            title=dict(text="温度值", side="right"),
            thickness=15,
            len=0.9
        ),
        line=dict(width=0.5, color='white')
    ))
    
    # 矢量箭头
    annotations = []
    scale = 6
    
    for i in range(len(y_s)):
        for j in range(len(x_s)):
            if speed_s[i, j] > 0.001:
                annotations.append(dict(
                    x=x_s[j] + u_norm[i, j] * scale,
                    y=y_s[i] + v_norm[i, j] * scale,
                    ax=x_s[j],
                    ay=y_s[i],
                    xref="x",
                    yref="y",
                    axref="x",
                    ayref="y",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=1.5,
                    arrowcolor="black"
                ))
    
    fig.update_layout(
        title=dict(
            text=f"等值线+矢量组合图 ({IMG_HEIGHT}×{IMG_WIDTH})",
            x=0.5,
            font=dict(size=14, color="#333")
        ),
        xaxis=dict(
            title="X 位置",
            scaleanchor="y",
            scaleratio=1,
            showgrid=False,
            range=[0, IMG_WIDTH]
        ),
        yaxis=dict(
            title="Y 位置",
            autorange="reversed",
            showgrid=False,
            range=[0, IMG_HEIGHT]
        ),
        height=550,
        margin=dict(l=50, r=20, t=50, b=40),
        annotations=annotations
    )
    
    return fig


def create_empty_chart() -> go.Figure:
    """空白占位图"""
    fig = go.Figure()
    
    # 边框
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=IMG_WIDTH, y1=IMG_HEIGHT,
        fillcolor="rgba(240, 248, 255, 0.5)",
        line=dict(color="#1565C0", width=2, dash="dash")
    )
    
    # 提示文字
    fig.add_annotation(
        x=IMG_WIDTH/2, y=IMG_HEIGHT/2,
        text="等待预测...",
        font=dict(size=20, color="#1565C0"),
        showarrow=False
    )
    
    fig.update_layout(
        xaxis=dict(
            range=[-5, IMG_WIDTH+5],
            scaleanchor="y",
            scaleratio=1,
            showgrid=False,
            showticklabels=False
        ),
        yaxis=dict(
            range=[IMG_HEIGHT+5, -5],
            showgrid=False,
            showticklabels=False
        ),
        height=550,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    return fig


def run_synthesis(p1: float, p2: float, p3: float, p4: float):
    """执行热力特性场预测"""
    
    # 检查文件
    if not os.path.exists(EXCEL_FILE_PATH):
        st.error(f"❌ 数据文件不存在: {EXCEL_FILE_PATH}")
        st.info("请将Excel数据文件放置于项目 data 文件夹下")
        return
    
    try:
        with st.spinner("正在预测热力特性场..."):
            # 读取Excel数据
            df = pd.read_excel(EXCEL_FILE_PATH, header=None)
            
            # 验证数据
            if df.shape[1] < 8:
                st.error(f"❌ 数据文件需要至少8列，当前只有{df.shape[1]}列")
                return
            
            expected_rows = IMG_HEIGHT * IMG_WIDTH
            if df.shape[0] != expected_rows:
                st.error(f"❌ 数据行数({df.shape[0]})与图像尺寸({expected_rows})不匹配")
                return
            
            # 计算8个系数
            coefficients = calculate_coefficients(p1, p2, p3, p4)
            
            # 加权合成
            synthesized = np.zeros(df.shape[0])
            for i in range(8):
                synthesized += coefficients[i] * df.iloc[:, i].values
            
            # 重塑为图像
            synthesized_img = synthesized.reshape(IMG_HEIGHT, IMG_WIDTH)
            
            # 计算流场数据（梯度）
            v, u = np.gradient(synthesized_img)
            v = -v  # 反转v方向以匹配坐标系
            speed = np.sqrt(u**2 + v**2)
            
            flow_data = {
                'u': u,
                'v': v,
                'speed': speed
            }
            
            # 保存到session state
            st.session_state.synthesized_img = synthesized_img
            st.session_state.flow_data = flow_data
            st.session_state.calculated = True
        
        st.success("✅ 预测完成！")
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ 预测失败: {str(e)}")

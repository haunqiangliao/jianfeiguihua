import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 设置页面配置
st.set_page_config(
    page_title="身材管理器",
    page_icon="💪",
    layout="wide"
)

# 应用标题
st.title("💪 身材管理器")
st.markdown("根据您的身体数据和健身目标，生成个性化的饮食和运动计划")

# 定义数据
diet_library = {
    "lose": ["鸡胸肉沙拉", "燕麦粥", "清蒸鱼", "西兰花炒虾仁", "水煮蛋", "全麦面包", "无糖酸奶"],
    "gain": ["牛肉炒饭", "蛋白粉奶昔", "坚果拼盘", "全麦面包", "鸡胸肉", "红薯", "香蕉"],
    "shape": ["三文鱼", "希腊酸奶", "藜麦沙拉", "水煮蛋", "牛油果", "混合蔬菜", "低糖水果"]
}

exercise_library = {
    "lose": ["慢跑", "跳绳", "HIIT", "游泳", "有氧舞蹈", "骑自行车", "爬山"],
    "gain": ["举重", "深蹲", "卧推", "硬拉", "引体向上", "哑铃训练", "俯卧撑"],
    "shape": ["瑜伽", "普拉提", "动感单车", "核心训练", "舞蹈", "拉伸", "平衡训练"]
}

# 计算BMI
def calculate_bmi(weight, height):
    return round(weight / ((height / 100) ** 2), 1)

# 获取BMI分类
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "偏瘦"
    elif 18.5 <= bmi < 24:
        return "正常"
    elif 24 <= bmi < 28:
        return "过重"
    else:
        return "肥胖"

# 生成一周饮食计划
def generate_diet_plan(target, days=7):
    diet_options = diet_library[target]
    breakfast = np.random.choice(diet_options, days)
    lunch = np.random.choice(diet_options, days)
    dinner = np.random.choice(diet_options, days)
    
    plan = pd.DataFrame({
        "日期": [datetime.now() + timedelta(days=i) for i in range(days)],
        "早餐": breakfast,
        "午餐": lunch,
        "晚餐": dinner
    })
    
    return plan

# 生成一周运动计划
def generate_exercise_plan(target, age, days=7):
    exercise_options = exercise_library[target]
    
    # 根据年龄调整运动强度
    if age < 30:
        intensity = "高强度"
    elif age < 50:
        intensity = "中等强度"
    else:
        intensity = "低强度"
    
    # 生成每天的运动计划
    plan = []
    for i in range(days):
        exercise = np.random.choice(exercise_options)
        duration = np.random.randint(30, 60)  # 随机30-60分钟
        plan.append({
            "日期": datetime.now() + timedelta(days=i),
            "运动类型": exercise,
            "时长(分钟)": duration,
            "强度": intensity
        })
    
    return pd.DataFrame(plan)

# 主界面
with st.form("body_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        weight = st.number_input("当前体重 (kg)", min_value=30.0, max_value=200.0, step=0.1)
    
    with col2:
        height = st.number_input("身高 (cm)", min_value=100.0, max_value=250.0, step=0.1)
    
    with col3:
        age = st.number_input("年龄", min_value=12, max_value=100, step=1)
    
    st.markdown("### 选择健身目标")
    target = st.radio(
        "请选择您的主要健身目标",
        ["减肥", "增肌", "塑形"],
        horizontal=True
    )
    
    # 根据目标类型显示不同的目标值输入
    if target == "减肥":
        target_weight = st.number_input("目标体重 (kg)", min_value=30.0, max_value=weight, step=0.1)
    elif target == "增肌":
        target_weight = st.number_input("目标体重 (kg)", min_value=weight, max_value=200.0, step=0.1)
    else:  # 塑形
        target_fat = st.number_input("目标体脂率 (%)", min_value=5.0, max_value=40.0, step=0.1)
    
    submitted = st.form_submit_button("生成计划")

# 处理表单提交
if submitted:
    # 计算BMI和目标描述
    bmi = calculate_bmi(weight, height)
    bmi_category = get_bmi_category(bmi)
    
    if target == "减肥":
        weight_diff = weight - target_weight
        target_desc = f"从 {weight}kg 减至 {target_weight}kg (减少 {weight_diff:.1f}kg)"
    elif target == "增肌":
        weight_diff = target_weight - weight
        target_desc = f"从 {weight}kg 增至 {target_weight}kg (增加 {weight_diff:.1f}kg)"
    else:
        target_desc = f"达到体脂率 {target_fat}%"
    
    # 生成计划
    diet_plan = generate_diet_plan(target.lower())
    exercise_plan = generate_exercise_plan(target.lower(), age)
    
    # 显示结果
    st.success("🎉 您的个性化身材管理计划已生成！")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 身体指标分析")
        st.metric("BMI", f"{bmi} ({bmi_category})")
        st.markdown(f"**目标**: {target} - {target_desc}")
    
    with col2:
        st.subheader("📅 计划概览")
        st.metric("饮食计划", f"{len(diet_plan)}天定制食谱")
        st.metric("运动计划", f"{len(exercise_plan)}天训练安排")
    
    st.subheader("🍎 一周饮食计划")
    diet_plan["日期"] = diet_plan["日期"].dt.strftime("%m-%d %a")
    st.dataframe(diet_plan, use_container_width=True)
    
    st.subheader("💪 一周运动计划")
    exercise_plan["日期"] = exercise_plan["日期"].dt.strftime("%m-%d %a")
    st.dataframe(exercise_plan, use_container_width=True)
    
    # 小贴士
    st.info("💡 小贴士: 请根据个人情况调整计划，运动前记得热身，保持充足睡眠和水分摄入！")

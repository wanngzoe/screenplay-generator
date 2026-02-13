"""
短剧剧本生成器 - Streamlit Demo
运行方式: streamlit run app.py
"""

import streamlit as st
import time

# 页面配置
st.set_page_config(
    page_title="短剧剧本生成器",
    page_icon="📝",
    layout="wide"
)

# 标题
st.title("📝 短剧剧本生成器")
st.markdown("输入小说，自动生成专业格式的短剧剧本")

# 侧边栏配置
with st.sidebar:
    st.header("配置参数")
    title = st.text_input("剧本标题", value="短剧剧本", help="默认为'短剧剧本'")

    genre = st.selectbox(
        "题材类型",
        ["都市", "古装宅斗", "仙侠玄幻", "甜宠", "重生复仇", "穿越", "豪门"],
        help="选择剧本的题材类型"
    )

    episodes = st.slider("总集数", min_value=3, max_value=50, value=30, help="建议 20-40 集")

    opt_level = st.selectbox(
        "优化级别",
        ["standard", "basic", "deep"],
        format_func=lambda x: {"standard": "标准优化", "basic": "基础优化", "deep": "深度优化"}[x],
        help="标准优化包含格式+表演提示；深度优化增加配角记忆点优化"
    )

    st.divider()

    st.markdown("""
    **字数建议**
    - < 5,000字：3-5集
    - 5,000-15,000字：10-15集
    - 15,000-30,000字：20-30集
    - > 30,000字：建议分批
    """)

    st.divider()

    st.markdown("""
    **提示**
    - 当前为演示版本
    - 点击生成后等待 10-30 秒
    - 生成完成后可下载剧本
    """)

# 主内容区
novel_input = st.text_area(
    "小说原文",
    height=300,
    placeholder="请粘贴小说原文...",
    help="建议字数：5,000 - 30,000 字"
)

# 生成按钮
if st.button("🎬 生成剧本", type="primary", disabled=not novel_input):
    if not novel_input.strip():
        st.error("请输入小说内容")
    else:
        with st.spinner("正在生成剧本，请稍候..."):
            # TODO: 接入真实AI模型
            # result = call_ai_model(novel, title, genre, episodes, opt_level)

            # 模拟生成（演示用）
            time.sleep(3)  # 模拟API延迟

            # 生成示例剧本
            script_content = generate_mock_script(title, genre, episodes)

            # 生成优化报告
            report = {
                "格式问题修复": 3,
                "表演提示补充": 5,
                "特写镜头补充": 2,
                "配角记忆点补充": 1
            }

        st.success("生成完成！")

        # 显示优化报告
        with st.expander("📊 优化报告", expanded=True):
            cols = st.columns(4)
            for i, (item, count) in enumerate(report.items()):
                cols[i % 4].metric(item, count)

        # 显示剧本
        st.subheader("📄 生成的剧本")

        # 剧本预览（可折叠）
        with st.expander("预览完整剧本", expanded=True):
            st.markdown(script_content)

        # 下载按钮
        st.download_button(
            label="📥 下载剧本",
            data=script_content,
            file_name=f"{title}.md",
            mime="text/markdown"
        )

# 底部说明
st.divider()
st.markdown("""
---
**格式说明**

| 标记 | 用途 |
|------|------|
| 1-1, 1-2... | 场次编号 |
| 日/夜 + 内/外 | 场景标注 |
| 【特写】 | 关键情感镜头 |
| 【★表演提示】 | 表演要点 |
| 【画外音·人物名】 | 内心独白 |
| 【切镜】【字幕】 | 转场技巧 |
""")

# 辅助函数：生成模拟脚本
def generate_mock_script(title, genre, episodes):
    return f'''# 短剧剧本：{title}

**题材：** {genre}
**总集数：** {episodes}集

**故事梗概：** 丫鬟苏清晏被逼替小姐与姑爷同床三年，求解放时被迫与侯府病弱大公子沈景珩结阴亲，在照顾沈景珩的过程中渐生情愫。

**人物小传：**

| 角色 | 年龄 | 身份/职业 | 性格特点 | 核心背景 |
|------|------|-----------|---------|----------|
| 苏清晏 | 18岁 | 陪嫁丫鬟 | 隐忍坚韧 | 家生子，全家性命握在小姐手中 |
| 沈景珩 | 27岁 | 侯府嫡长子 | 清冷才子 | 幼年被借命，注定早逝 |
| 沈昭烈 | 25岁 | 侯府二公子 | 纨绔霸道 | 暗恋大哥光环 |

**表演记忆点：**

| 角色 | 性格标签 | 口头禅 | 标志性动作 |
|------|---------|--------|------------|
| 苏清晏 | 隐忍坚韧 | "奴婢不敢" | 低眉顺眼 |
| 沈景珩 | 清冷深情 | "你真是……" | 耳根泛红 |
| 沈昭烈 | 霸道狂妄 | "本侯" | 下巴微抬 |

---

**第1集：替身丫鬟**
**核心剧情：** 苏清晏是小姐的陪嫁丫鬟，新婚之夜起便每晚替小姐承受姑爷的宠爱。

1-1   小姐房中    夜    内
人物：小姐  沈昭烈  苏清晏

▲ 烛火摇曳，暖帐低垂。

【画外音·苏清晏】 小姐体弱，侯爷武将出身太过威猛，一连三晚都没能圆房。

沈昭烈（调情）：「怎么磨磨蹭蹭的？」

【★表演提示】苏清晏说谎时目光躲闪，双手交握

苏清晏（轻声）：「在外面赏了会儿雪景。」

...

---

（共{episodes}集，完整剧本需要调用AI模型生成）

**注意：** 当前为演示版本，接入真实AI模型后可生成完整剧本。
'''

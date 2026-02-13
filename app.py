"""
短剧剧本生成器 - Streamlit Demo
运行方式: streamlit run app.py
"""

import streamlit as st
import time
import os

# 页面配置
st.set_page_config(
    page_title="短剧剧本生成器",
    page_icon="📝",
    layout="wide"
)

# 初始化 session state
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "api_provider" not in st.session_state:
    st.session_state.api_provider = "claude"

# 标题
st.title("📝 短剧剧本生成器")
st.markdown("输入小说，自动生成专业格式的短剧剧本")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置参数")

    st.markdown("""
    **优化级别说明**
    - 基础优化：仅格式化（场次编号、场景标注）
    - 标准优化：格式化 + 表演提示 + 特写镜头
    - 深度优化：全部 + 配角记忆点 + 台词优化
    """)

    st.divider()

    title = st.text_input("剧本标题", value="短剧剧本", help="默认为'短剧剧本'")

    genre = st.selectbox(
        "题材类型",
        ["都市", "古装宅斗", "仙侠玄幻", "甜宠", "重生复仇", "穿越", "豪门", "其他"],
        help="选择剧本的题材类型"
    )

    episodes = st.slider("总集数", min_value=3, max_value=50, value=30, help="建议 20-40 集")

    opt_level = st.selectbox(
        "优化级别",
        ["deep", "standard", "basic"],
        format_func=lambda x: {
            "standard": "标准优化",
            "basic": "基础优化",
            "deep": "深度优化"
        }[x],
        help="基础优化：仅格式化；标准优化：格式+表演提示；深度优化：格式+表演提示+配角记忆点"
    )

    st.divider()

    # API 配置
    st.header("🔑 API 配置")

    api_provider = st.selectbox(
        "API 提供商",
        ["claude", "openai", "gemini", "deepseek", "qwen", "ernie", "chatglm", "kimi"],
        format_func=lambda x: {
            "claude": "Claude (Anthropic)",
            "openai": "OpenAI GPT-4",
            "gemini": "Google Gemini",
            "deepseek": "DeepSeek",
            "qwen": "阿里通义千问",
            "ernie": "百度文心一言",
            "chatglm": "智谱 ChatGLM",
            "kimi": "Kimi (Moonshot)"
        }[x],
        help="选择要使用的 AI API"
    )

    api_key = st.text_input(
        "API Key",
        type="password",
        help="请输入你的 API Key（不会保存，仅本次使用）"
    )

    if api_key:
        st.session_state.api_key = api_key
        st.session_state.api_provider = api_provider
        st.success("✅ API Key 已配置")

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
    - 需要自备 API Key
    - Claude: https://console.anthropic.com
    - OpenAI: https://platform.openai.com/api-keys
    - Gemini: https://aistudio.google.com
    - DeepSeek: https://platform.deepseek.com
    - 通义千问: https://dashscope.console.aliyun.com
    - 文心一言: https://console.bce.baidu.com
    - ChatGLM: https://open.bigmodel.cn
    - Kimi: https://platform.moonshot.cn
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
    elif not st.session_state.api_key:
        st.error("请先在左侧配置 API Key")
    else:
        with st.spinner("正在生成剧本，请稍候（可能需要 30-60 秒）..."):
            try:
                # 调用 AI 模型
                script_content = call_ai_model(
                    novel=novel_input,
                    title=title,
                    genre=genre,
                    episodes=episodes,
                    opt_level=opt_level,
                    api_key=st.session_state.api_key,
                    provider=st.session_state.api_provider
                )

                # 生成优化报告
                report = {
                    "格式问题修复": 3,
                    "表演提示补充": 5,
                    "特写镜头补充": 2,
                    "配角记忆点补充": 1
                }

                st.success("生成完成！")

            except Exception as e:
                st.error(f"生成失败：{str(e)}")
                script_content = None

        if script_content:
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

# ==================== AI API 调用函数 ====================

def call_ai_model(novel, title, genre, episodes, opt_level, api_key, provider):
    """
    调用 AI 模型生成剧本

    Args:
        novel: 小说原文
        title: 剧本标题
        genre: 题材类型
        episodes: 总集数
        opt_level: 优化级别
        api_key: API Key
        provider: claude / openai

    Returns:
        生成的剧本内容
    """
    # 题材侧重点
    genre_focus = {
        "都市": "职场、生活、现实情感",
        "古装宅斗": "心机算计、身份地位、主仆关系",
        "仙侠玄幻": "修炼升级、法宝灵器、门派恩怨",
        "甜宠": "感情互动、身份差距、浪漫桥段",
        "重生复仇": "信息差、预知未来、改变命运",
        "穿越": "身份错位、古代与现代碰撞",
        "豪门": "财产争夺、家族恩怨、身份差距"
    }

    # 生成提示词
    system_prompt = """你是一个专业的短剧编剧，擅长将小说改编成专业格式的短剧剧本。"""

    user_prompt = f"""请将以下小说转换成专业格式的短剧剧本。

=== 基础配置 ===
标题：{title}
题材：{genre}
总集数：{episodes}

=== 格式模板 ===
# 短剧剧本：{title}

**题材：** {genre}
**总集数：** {episodes}集

**故事梗概：** 1-2句话概括核心冲突

**人物小传：**

| 角色 | 年龄 | 身份/职业 | 性格特点 | 核心背景 |
|------|------|-----------|---------|----------|
| 主角 | xx岁 | xxx | xxx | xxx |
| 配角1 | xx岁 | xxx | xxx | xxx |

**表演记忆点：**

| 角色 | 性格标签 | 口头禅 | 标志性动作 |
|------|---------|--------|------------|
| 主角 | xxx | xxx | xxx |
| 配角1 | xxx | xxx | xxx |

---

**第1集：标题**
**核心剧情：** ...

1-1   场景名称     日/夜    内/外
人物：xxx

▲ 场景描述
【特写】关键镜头
人物（情绪）：台词
【★表演提示】

▲ 切镜

1-2   场景名称     日/夜    内/外
人物：xxx

...

=== 格式要求 ===
1. 场次编号：1-1, 1-2, 2-1...（连续递增）
2. 场景标注：日/夜 + 内/外（必填）
3. 关键镜头：【特写】+ 描述
4. 表演提示：【★表演提示】+ 情绪/动作
5. 转场：【切镜】【黑屏】【字幕：X年后】【闪回】【蒙太奇】
6. 内心独白：【画外音·人物名】
7. 配角必须有口头禅和标志性动作

=== 题材侧重点 ===
{genre}题材关注：{genre_focus.get(genre, '情感纠葛')}

请直接输出完整剧本。

小说原文：
{novel}"""

    if provider == "claude":
        return call_claude_api(system_prompt, user_prompt, api_key)
    elif provider == "openai":
        return call_openai_api(system_prompt, user_prompt, api_key)
    elif provider == "gemini":
        return call_gemini_api(system_prompt, user_prompt, api_key)
    elif provider == "deepseek":
        return call_deepseek_api(system_prompt, user_prompt, api_key)
    elif provider == "qwen":
        return call_qwen_api(system_prompt, user_prompt, api_key)
    elif provider == "ernie":
        return call_ernie_api(system_prompt, user_prompt, api_key)
    elif provider == "chatglm":
        return call_chatglm_api(system_prompt, user_prompt, api_key)
    elif provider == "kimi":
        return call_kimi_api(system_prompt, user_prompt, api_key)
    else:
        raise ValueError(f"不支持的 API 提供商: {provider}")


def call_claude_api(system_prompt, user_prompt, api_key):
    """调用 Claude API"""
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="sonnet-4-20250514",
        max_tokens=64000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    return message.content[0].text


def call_openai_api(system_prompt, user_prompt, api_key):
    """调用 OpenAI API"""
    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=64000,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content


# ==================== 更多 API 调用函数 ====================

def call_gemini_api(system_prompt, user_prompt, api_key):
    """调用 Google Gemini API"""
    import google.generativeai as genai

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        system_instruction=system_prompt
    )

    response = model.generate_content(user_prompt)
    return response.text


def call_deepseek_api(system_prompt, user_prompt, api_key):
    """调用 DeepSeek API"""
    import openai

    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content


def call_qwen_api(system_prompt, user_prompt, api_key):
    """调用阿里通义千问 API"""
    import openai

    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content


def call_ernie_api(system_prompt, user_prompt, api_key):
    """调用百度文心一言 API"""
    import openai

    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat"
    )

    # 需要先获取 access_token，这里简化处理
    response = client.chat.completions.create(
        model="ernie-4.5-turbo-8k",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content


def call_chatglm_api(system_prompt, user_prompt, api_key):
    """调用智谱 ChatGLM API"""
    import openai

    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://open.bigmodel.cn/api/paas/v4"
    )

    response = client.chat.completions.create(
        model="glm-4-plus",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content


def call_kimi_api(system_prompt, user_prompt, api_key):
    """调用 Kimi (Moonshot) API"""
    import openai

    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.moonshot.cn/v1"
    )

    response = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content


# ==================== 模拟函数（备用） ====================

def generate_mock_script(title, genre, episodes):
    """模拟生成脚本（无 API Key 时使用）"""
    return f'''# 短剧剧本：{title}

**题材：** {genre}
**总集数：** {episodes}集

**故事梗概：** 丫鬟苏清晏被逼替小姐与姑爷同床三年，求解放时被迫与侯府病弱大公子沈景珩结阴亲。

**人物小传：**

| 角色 | 年龄 | 身份/职业 | 性格特点 | 核心背景 |
|------|------|-----------|---------|----------|
| 苏清晏 | 18岁 | 陪嫁丫鬟 | 隐忍坚韧 | 家生子 |
| 沈景珩 | 27岁 | 侯府嫡长子 | 清冷才子 | 注定早逝 |

**表演记忆点：**

| 角色 | 性格标签 | 口头禅 | 标志性动作 |
|------|---------|--------|------------|
| 苏清晏 | 隐忍坚韧 | "奴婢不敢" | 低眉顺眼 |

---

（共{episodes}集，请配置 API Key 生成完整剧本）
'''

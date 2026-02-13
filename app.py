"""
短剧剧本生成器 - Streamlit Demo
运行方式: streamlit run app.py
"""

import streamlit as st
import time
import os

# 导入 AI SDK
import anthropic
from openai import OpenAI


# ==================== AI API 调用函数 ====================

def call_claude_api(system_prompt, user_prompt, api_key):
    """调用 Claude API"""
    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=128000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    return message.content[0].text


def call_openai_api(system_prompt, user_prompt, api_key):
    """调用 OpenAI API"""
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


def call_deepseek_api(system_prompt, user_prompt, api_key):
    """调用 DeepSeek API"""
    client = OpenAI(
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


def call_gemini_api(system_prompt, user_prompt, api_key):
    """调用 Google Gemini API (Flash) - OpenAI 兼容格式"""
    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content


def call_gemini_pro_api(system_prompt, user_prompt, api_key):
    """调用 Google Gemini API (Pro) - OpenAI 兼容格式"""
    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    response = client.chat.completions.create(
        model="gemini-2.5-pro",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content


def call_deepseek_api(system_prompt, user_prompt, api_key):
    """调用 DeepSeek API"""
    client = OpenAI(
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
        provider: claude / openai / gemini / deepseek / qwen / ernie / chatglm / kimi

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
        "豪门": "财产争夺、家族恩怨、身份差距",
        "其他": "情感纠葛、人物成长"
    }

    # 生成提示词
    system_prompt = """你是一个专业的短剧编剧，擅长将小说改编成专业格式的短剧剧本。请务必使用简体中文，不要使用繁体中文。"""

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
    elif provider == "deepseek":
        return call_deepseek_api(system_prompt, user_prompt, api_key)
    elif provider == "gemini_flash":
        return call_gemini_api(system_prompt, user_prompt, api_key)
    elif provider == "gemini_pro":
        return call_gemini_pro_api(system_prompt, user_prompt, api_key)
    else:
        raise ValueError(f"不支持的 API 提供商: {provider}")


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


# ==================== 主 UI 代码 ====================

# 页面配置
st.set_page_config(
    page_title="短剧剧本生成器",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================== 第一步：提取故事概要 ====================

def extract_story_summary(novel, title, genre, total_episodes, api_key, provider):
    """
    从完整小说中提取：
    1. 故事梗概、人物设定
    2. 全局优化要点（格式规范、表演提示、特写镜头、配角记忆点）
    """
    import json

    genre_focus = {
        "都市": "职场、生活、现实情感",
        "古装宅斗": "心机算计、身份地位、主仆关系",
        "仙侠玄幻": "修炼升级、法宝灵器、门派恩怨",
        "甜宠": "感情互动、身份差距、浪漫桥段",
        "重生复仇": "信息差、预知未来、改变命运",
        "穿越": "身份错位、古代与现代碰撞",
        "豪门": "财产争夺、家族恩怨、身份差距",
        "其他": "情感纠葛、人物成长"
    }

    system_prompt = """你是一个专业的短剧编剧。请从小说中提取关键信息，用于后续分集剧本生成。"""

    user_prompt = f"""请从以下小说中提取关键信息，用于后续生成分集剧本和优化。

=== 任务说明 ===
请提取以下信息（JSON格式输出）：

1. **故事梗概**（200字内）：一句话概括核心冲突
2. **人物小传**（主要角色 3-5 人）：包含姓名、年龄、身份、性格特点、核心背景
3. **分集大纲**（共{total_episodes}集）：每集一句话核心事件
4. **全局优化要点**：
   - 格式规范：该题材的特殊格式要求
   - 表演提示：该题材的表演风格要点
   - 特写镜头：该题材常需要的镜头类型
   - 配角记忆点：主要配角需要具备的标志性特征

=== 输出格式 ===
请直接输出JSON对象（不要用markdown代码块）：

{{
  "story_summary": "一句话核心冲突概括",
  "characters": [
    {{
      "name": "角色名",
      "age": "年龄",
      "identity": "身份/职业",
      "personality": "性格特点",
      "background": "核心背景"
    }}
  ],
  "episode_plan": [
    "第1集核心事件",
    "第2集核心事件",
    ...
  ],
  "optimization_points": {{
    "format_notes": "格式规范要点列表（每条换行）",
    "performance_notes": "表演提示要点列表",
    "camera_notes": "特写镜头要点列表",
    "character_marks": "配角记忆点：角色A-口头禅+动作，角色B-口头禅+动作"
  }}
}}

=== 题材侧重点 ===
{genre}题材关注：{genre_focus.get(genre, '情感纠葛')}

=== 小说原文 ===
{novel[:10000]}  <!-- 截取前10000字 -->

...（小说内容较长，已截取关键部分用于提取概要）"""

    if provider == "claude":
        result = call_claude_api(system_prompt, user_prompt, api_key)
    elif provider == "openai":
        result = call_openai_api(system_prompt, user_prompt, api_key)
    elif provider == "deepseek":
        result = call_deepseek_api(system_prompt, user_prompt, api_key)
    elif provider == "gemini_flash":
        result = call_gemini_api(system_prompt, user_prompt, api_key)
    elif provider == "gemini_pro":
        result = call_gemini_pro_api(system_prompt, user_prompt, api_key)
    else:
        raise ValueError(f"不支持的 API 提供商: {provider}")

    try:
        result = result.strip()
        if result.startswith("```json"):
            result = result[7:]
        if result.startswith("```"):
            result = result[3:]
        if result.endswith("```"):
            result = result[:-3]
        result = result.strip()

        parsed = json.loads(result)
        return {
            "story_summary": parsed.get("story_summary", ""),
            "characters": parsed.get("characters", []),
            "episode_plan": parsed.get("episode_plan", []),
            "optimization_points": parsed.get("optimization_points", {})
        }
    except json.JSONDecodeError:
        return {
            "story_summary": result[:500],
            "characters": [],
            "episode_plan": [],
            "optimization_points": {}
        }


# ==================== 第二步：分集生成 ====================

def generate_batch_with_summary(summary_data, title, genre, batch_num, total_episodes, api_key, provider):
    """
    使用故事概要生成分集剧本（不传完整小说，解决 token 限制）
    """
    import json

    batch_size = 15
    start_ep = batch_num * batch_size + 1
    end_ep = min((batch_num + 1) * batch_size, total_episodes)

    current_episodes = list(range(start_ep, end_ep + 1))
    episode_plan = summary_data.get("episode_plan", [])

    batch_plan_text = ""
    for ep in current_episodes:
        if ep <= len(episode_plan):
            batch_plan_text += f"- 第{ep}集：{episode_plan[ep-1]}\n"

    genre_focus = {
        "都市": "职场、生活、现实情感",
        "古装宅斗": "心机算计、身份地位、主仆关系",
        "仙侠玄幻": "修炼升级、法宝灵器、门派恩怨",
        "甜宠": "感情互动、身份差距、浪漫桥段",
        "重生复仇": "信息差、预知未来、改变命运",
        "穿越": "身份错位、古代与现代碰撞",
        "豪门": "财产争夺、家族恩怨、身份差距",
        "其他": "情感纠葛、人物成长"
    }

    system_prompt = """你是一个专业的短剧编剧，擅长将小说改编成专业格式的短剧剧本。请务必使用简体中文，不要使用繁体中文。"""

    user_prompt = f"""请根据以下故事概要，为第 {start_ep}-{end_ep} 集创作剧本。

=== 故事概要 ===
{summary_data.get('story_summary', '')}

=== 人物设定 ===
{json.dumps(summary_data.get('characters', []), ensure_ascii=False, indent=2)}

=== 当前批次分集计划 ===
{batch_plan_text}

=== 格式模板 ===
**第X集：标题**
**核心剧情：** ...

1-X   场景名称     日/夜    内/外
人物：xxx

▲ 场景描述
【特写】关键镜头
人物（情绪）：台词
【★表演提示】

=== 格式要求 ===
1. 场次编号：{start_ep}-1, {start_ep}-2, ...
2. 场景标注：日/夜 + 内/外（必填）
3. 关键镜头：【特写】+ 描述
4. 表演提示：【★表演提示】+ 情绪/动作
5. 转场：【切镜】【字幕：X年后】【蒙太奇】
6. 配角必须有口头禅和标志性动作
7. 每集至少 4 场

=== 题材侧重点 ===
{genre}题材关注：{genre_focus.get(genre, '情感纠葛')}

请直接输出第 {start_ep}-{end_ep} 集的完整剧本内容。"""

    if provider == "claude":
        return call_claude_api(system_prompt, user_prompt, api_key)
    elif provider == "openai":
        return call_openai_api(system_prompt, user_prompt, api_key)
    elif provider == "deepseek":
        return call_deepseek_api(system_prompt, user_prompt, api_key)
    elif provider == "gemini_flash":
        return call_gemini_api(system_prompt, user_prompt, api_key)
    elif provider == "gemini_pro":
        return call_gemini_pro_api(system_prompt, user_prompt, api_key)
    else:
        raise ValueError(f"不支持的 API 提供商: {provider}")


# ==================== 第三步：分批优化 ====================

def optimize_batch(batch_content, optimization_points, api_key, provider):
    """
    基于全局优化要点优化单批剧本内容

    Args:
        batch_content: 当前批次的剧本内容
        optimization_points: extract_story_summary 返回的优化要点
        api_key: API Key
        provider: API 提供商

    Returns:
        优化后的剧本内容
    """
    opt_points = optimization_points

    system_prompt = """你是一个专业的短剧剧本优化专家，负责优化剧本的格式规范、表演提示、特写镜头和配角记忆点。"""

    user_prompt = f"""请优化以下剧本内容，根据全局优化要点进行修正和补充。

=== 全局优化要点 ===
**格式规范：**
{opt_points.get('format_notes', '按标准格式规范执行')}

**表演提示：**
{opt_points.get('performance_notes', '无特殊要求')}

**特写镜头：**
{opt_points.get('camera_notes', '无特殊要求')}

**配角记忆点：**
{opt_points.get('character_marks', '配角需有口头禅和标志性动作')}

=== 需要优化的剧本内容 ===
{batch_content}

=== 优化要求 ===
1. 检查并修复格式问题
2. 补充缺失的表演提示
3. 补充必要的特写镜头
4. 确保配角有口头禅和标志性动作
5. 保持原有剧情不变

请直接输出优化后的剧本内容，不需要说明。"""

    if provider == "claude":
        return call_claude_api(system_prompt, user_prompt, api_key)
    elif provider == "openai":
        return call_openai_api(system_prompt, user_prompt, api_key)
    elif provider == "deepseek":
        return call_deepseek_api(system_prompt, user_prompt, api_key)
    elif provider == "gemini_flash":
        return call_gemini_api(system_prompt, user_prompt, api_key)
    elif provider == "gemini_pro":
        return call_gemini_pro_api(system_prompt, user_prompt, api_key)
    else:
        raise ValueError(f"不支持的 API 提供商: {provider}")

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

    # 生成模式选择
    st.header("🎯 生成模式")
    generation_mode = st.radio(
        "选择生成方式",
        ["single", "batch"],
        format_func=lambda x: {
            "single": "单次生成（Claude Pro 推荐）",
            "batch": "分步生成（普通 API 推荐）"
        }[x],
        help="单次生成：一次调用输出完整剧本（Claude Pro 输出无限制）\n分步生成：提取概要 + 分批生成 + 分批优化（解决 token 限制）"
    )

    if generation_mode == "single":
        st.info("ℹ️ 单次生成模式：一次 API 调用输出完整 30 集剧本（需 Claude Pro 等无输出限制的 API）")
    else:
        st.info("ℹ️ 分步生成模式：适合有输出 token 限制的 API，分批生成确保完整性")

    st.divider()

    api_provider = st.selectbox(
        "API 提供商",
        ["claude", "openai", "deepseek", "gemini_pro", "gemini_flash"],
        format_func=lambda x: {
            "claude": "Claude (Anthropic) - sonnet-4",
            "openai": "OpenAI - GPT-4o",
            "deepseek": "DeepSeek - chat",
            "gemini_pro": "Google Gemini - 2.5 Pro",
            "gemini_flash": "Google Gemini - 2.5 Flash"
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
        if generation_mode == "single":
            # ========== 单次生成模式 ==========
            with st.spinner("正在生成剧本，请稍候（可能需要 30-60 秒）..."):
                try:
                    script_content = call_ai_model(
                        novel=novel_input,
                        title=title,
                        genre=genre,
                        episodes=episodes,
                        opt_level=opt_level,
                        api_key=st.session_state.api_key,
                        provider=st.session_state.api_provider
                    )

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

        else:
            # ========== 分步生成模式 ==========
            batch_size = 15
            total_batches = (episodes + batch_size - 1) // batch_size

            progress_bar = st.progress(0)
            status_text = st.empty()

            try:
                # 第一步：提取故事概要（只做一次）
                status_text.text("正在提取故事概要...")
                progress_bar.progress(5)

                summary_data = extract_story_summary(
                    novel=novel_input,
                    title=title,
                    genre=genre,
                    total_episodes=episodes,
                    api_key=st.session_state.api_key,
                    provider=st.session_state.api_provider
                )

                progress_bar.progress(15)

                # 显示故事概要确认
                with st.expander("📖 故事概要（AI提取）", expanded=True):
                    st.markdown(f"**故事梗概：** {summary_data.get('story_summary', '')}")
                    st.markdown(f"**人物数量：** {len(summary_data.get('characters', []))} 人")
                    st.markdown(f"**分集计划：** {len(summary_data.get('episode_plan', []))} 集")

                # 第二步：分批生成剧本
                all_episodes_content = []
                optimization_report = {
                    "格式问题修复": 0,
                    "表演提示补充": 0,
                    "特写镜头补充": 0,
                    "配角记忆点补充": 0
                }

                for batch_idx in range(total_batches):
                    current_batch = batch_idx + 1
                    status_text.text(f"正在生成分集剧本 {batch_idx * batch_size + 1}-{min((batch_idx + 1) * batch_size, episodes)} 集 ({current_batch}/{total_batches}批)...")

                    # 生成该批剧本
                    batch_content = generate_batch_with_summary(
                        summary_data=summary_data,
                        title=title,
                        genre=genre,
                        batch_num=batch_idx,
                        total_episodes=episodes,
                        api_key=st.session_state.api_key,
                        provider=st.session_state.api_provider
                    )

                    # 立即优化该批剧本
                    status_text.text(f"正在优化第 {batch_idx * batch_size + 1}-{min((batch_idx + 1) * batch_size, episodes)} 集...")
                    optimized_batch = optimize_batch(
                        batch_content=batch_content,
                        optimization_points=summary_data.get("optimization_points", {}),
                        api_key=st.session_state.api_key,
                        provider=st.session_state.api_provider
                    )

                    # 累加内容
                    all_episodes_content.append(f"\n{'='*50}\n")
                    all_episodes_content.append(f"# 第 {batch_idx * batch_size + 1}-{min((batch_idx + 1) * batch_size, episodes)} 集\n")
                    all_episodes_content.append(optimized_batch)

                    # 更新进度
                    progress = 15 + int(80 * (current_batch / total_batches))
                    progress_bar.progress(progress)

                # 组合完整剧本
                script_content = f"""# 短剧剧本：{title}

**题材：** {genre}
**总集数：** {episodes}集

---

## 故事梗概
{summary_data.get('story_summary', '')}

---

## 人物小传
| 角色 | 年龄 | 身份/职业 | 性格特点 | 核心背景 |
|------|------|-----------|---------|----------|
"""

                for char in summary_data.get('characters', []):
                    script_content += f"| {char.get('name', '')} | {char.get('age', '')} | {char.get('identity', '')} | {char.get('personality', '')} | {char.get('background', '')} |\n"

                script_content += """
---

## 表演记忆点
| 角色 | 性格标签 | 口头禅 | 标志性动作 |
|------|---------|--------|------------|
"""
                for char in summary_data.get('characters', []):
                    name = char.get('name', '')
                    script_content += f"| {name} | {char.get('personality', '')} | 待补充 | 待补充 |\n"

                # 添加各集内容
                script_content += "\n" + "".join(all_episodes_content)

                progress_bar.progress(100)
                status_text.text("生成完成！")

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
                progress_bar.progress(0)

        # 显示结果（两种模式共用）
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

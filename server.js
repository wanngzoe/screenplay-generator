// server.js - 剧本生成后端服务
// 运行方式: node server.js

const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const PORT = 3000;

// 中间件
app.use(cors());
app.use(bodyParser.json({ limit: '10mb' }));

// 生成剧本接口
app.post('/api/generate', async (req, res) => {
    try {
        const { novel, title, genre, episodes, optLevel } = req.body;

        if (!novel || novel.trim().length < 100) {
            return res.status(400).json({ error: '小说内容至少100字' });
        }

        // TODO: 实际调用AI模型生成
        // const generatedScript = await callAIModel({
        //     system: '你是一个专业的短剧编剧...',
        //     user: generatePrompt(novel, title, genre, episodes)
        // });

        // 模拟返回（实际开发时替换为真实调用）
        const mockScript = generateMockScript(title, genre, episodes);

        // TODO: 调用优化引擎
        // const optimized = await optimizeScript(mockScript, optLevel);

        res.json({
            success: true,
            script: mockScript,
            meta: {
                title,
                genre,
                episodes,
                words: novel.length,
                generatedAt: new Date().toISOString()
            }
        });

    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 优化剧本接口（独立调用）
app.post('/api/optimize', async (req, res) => {
    try {
        const { script, level } = req.body;

        if (!script) {
            return res.status(400).json({ error: '请提供剧本内容' });
        }

        // TODO: 调用优化模型
        // const optimized = await callOptimizeModel(script, level);

        // 模拟优化报告
        const mockReport = {
            '格式问题修复': Math.floor(Math.random() * 5),
            '表演提示补充': Math.floor(Math.random() * 10),
            '特写镜头补充': Math.floor(Math.random() * 5),
            '配角记忆点补充': Math.floor(Math.random() * 3)
        };

        res.json({
            success: true,
            optimizedScript: script, // 实际返回优化后的内容
            report: mockReport
        });

    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 健康检查
app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// 辅助函数：生成模拟脚本（开发测试用）
function generateMockScript(title, genre, episodes) {
    return `# 短剧剧本：${title}

**题材：** ${genre}
**总集数：** ${episodes}集

**故事梗概：** 这是一个示例剧本，完整剧本需要调用AI模型生成。

**人物小传：**

| 角色 | 年龄 | 身份/职业 | 性格特点 | 核心背景 |
|------|------|-----------|---------|----------|
| 主角 | xx岁 | xxx | xxx | xxx |

**表演记忆点：**

| 角色 | 性格标签 | 口头禅 | 标志性动作 |
|------|---------|--------|------------|
| 主角 | xxx | xxx | xxx |

---

**第1集：标题**
**核心剧情：** ...

1-1   场景名称    日    内
人物：xxx

▲ 场景描述...

（共${episodes}集，完整内容请调用AI生成）
`;
}

// 辅助函数：生成提示词
function generatePrompt(novel, title, genre, episodes) {
    return `请将以下小说转换成专业格式的短剧剧本。

=== 基础配置 ===
标题：${title}
题材：${genre}
总集数：${episodes}

=== 格式模板 ===
# 短剧剧本：${title}

**题材：** ${genre}
**总集数：** ${episodes}集

**故事梗概：** ...

**人物小传：** ...

**表演记忆点：** ...

---

**第1集：标题**
**核心剧情：** ...

1-1   场景名称    日/夜    内/外
人物：xxx

▲ 场景描述
【特写】关键镜头
人物（情绪）：台词
【★表演提示】

...

=== 格式要求 ===
1. 场次编号连续
2. 场景标注完整
3. 配角有口头禅和标志性动作

请直接输出完整剧本。

小说原文：
${novel}`;
}

// 启动服务
app.listen(PORT, () => {
    console.log(`
========================================
  短剧剧本生成服务已启动
========================================
  本地访问: http://localhost:${PORT}
  API端点: http://localhost:${PORT}/api/generate

  示例请求:
  curl -X POST http://localhost:${PORT}/api/generate \\
    -H "Content-Type: application/json" \\
    -d '{"novel":"小说内容","title":"标题","genre":"都市","episodes":30}'
========================================
    `);
});

# 短剧剧本生成工具

## 项目结构

```
产品文档/
├── app.py                  # Streamlit 应用（推荐）
├── index.html              # 原生 HTML 页面
├── server.js               # Node.js 后端 API
├── package.json            # 依赖配置
├── requirements.txt        # Python 依赖
├── 短剧剧本生成工具_PRD.md     # 产品需求文档
└── 剧本生成_提示词手册.md      # 开发提示词手册
```

---

## 方式一：Streamlit（推荐）

### 本地运行

```bash
# 1. 安装 Streamlit
pip install streamlit

# 2. 启动应用
streamlit run app.py

# 3. 访问 http://localhost:8501
```

### 免费部署到 Streamlit Cloud

1. 将项目上传到 GitHub 仓库
2. 访问 https://share.streamlit.io
3. 绑定你的 GitHub 仓库
4. 自动部署，获得公开访问链接

---

## 方式二：Vercel（HTML 版本）

### 本地运行

直接用浏览器打开 `index.html` 即可预览。

### 免费部署

1. 上传 `index.html` 到 GitHub
2. 访问 https://vercel.com
3. 导入 GitHub 项目
4. 自动部署，获得公开访问链接

---

## 部署对比

| 特性 | Streamlit | Vercel |
|------|-----------|--------|
| 技术栈 | Python | HTML/JS |
| AI 集成 | 原生支持 | 需后端 API |
| 免费额度 | 足够 | 足够 |
| 上手难度 | 简单 | 简单 |

---

## API 接口（后端开发参考）

### 生成剧本
```bash
POST /api/generate
Content-Type: application/json

{
  "novel": "小说原文...",
  "title": "剧本标题",
  "genre": "古装宅斗",
  "episodes": 30,
  "optLevel": "standard"
}
```

### 优化剧本（独立调用）
```bash
POST /api/optimize
Content-Type: application/json

{
  "script": "待优化的剧本...",
  "level": "standard"
}
```

---

## 下一步开发

1. **接入真实 AI 模型**
   - 在 `app.py` 中替换 `generate_mock_script()` 为真实 API 调用
   - 可接入 Claude API / OpenAI API / 其他大模型

2. **完善优化引擎**
   - 实现 `格式规范化` 提示词
   - 实现 `表演提示补全` 提示词
   - 实现 `配角记忆点校验` 提示词

3. **增强功能**
   - 分集生成（长文本）
   - 优化报告可视化
   - 历史记录存储
   - 批量导出

---

## 提示词位置

所有提示词模板请参考：`剧本生成_提示词手册.md`

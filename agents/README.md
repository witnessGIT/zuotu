# 免费做图 Agent 方案

当前项目优先采用真正可自托管、软件本身免费的组合：

1. **ComfyUI**：负责图像生成、局部重绘、放大、工作流编排。
2. **comfy-mcp**：把 ComfyUI 暴露成 MCP 工具，让 Codex/Agent 可以直接调用生成图片。
3. **GitHub + HTML/SVG/CSS**：负责文字、排版、版本管理和可重复生成海报。

## 为什么先用这套

- ComfyUI 开源，可本地运行，不强制购买云端额度。
- comfy-mcp 可以让 AI Agent 直接调用 ComfyUI，而不是人工点节点。
- 海报的中文文字继续由 HTML/SVG/CSS 排版，避免图像模型生成中文时出现错字。
- 人物照片、背景图、装饰素材由 ComfyUI 处理；最终排版仍保留为可编辑源码。

## 推荐流水线

```text
用户需求
  ↓
文案 Agent
  ↓
素材 Agent
  ↓
ComfyUI / comfy-mcp
  ↓
图片素材
  ↓
HTML / SVG 海报模板
  ↓
PNG 导出
  ↓
GitHub 归档
```

## 免费与成本说明

- ComfyUI：免费开源。
- comfy-mcp：免费开源。
- 使用本机 GPU：不产生模型 API 费用。
- 如果没有 GPU，可以接第三方 GPU/云端；这部分可能收费，不能算完全免费。
- 某些开源“设计 Agent”虽然项目本身免费，但它们调用的模型 API 可能收费，因此暂不作为默认方案。

## 当前状态

项目已经为 Agent 接入预留 `agents/` 目录。下一步是在有可运行 ComfyUI 的机器上配置 MCP 地址，然后 Agent 就可以直接请求出图。

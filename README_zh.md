# Feishu Remote MCP Skill

[English Version](./README.md) | 中文版本

该技能允许您调用飞书的远程 MCP（Model Context Protocol）服务，与飞书云文档和用户管理进行交互。它设计用于与 Claude 的自定义技能系统配合使用。

## 功能特点

- **用户管理**：搜索用户、获取用户信息、获取文件内容
- **云文档管理**：搜索、创建、查看、更新、列出文档以及管理评论
- **灵活的认证方式**：支持 User Access Token (UAT) 和 Tenant Access Token (TAT)
- **完善的错误处理**：正确处理飞书 MCP 错误响应
- **模块化设计**：遵循最佳实践的良好组织代码结构

## 项目结构

```
feishu-remote-mcp-skill/
├── scripts/
│   └── feishu_mcp_tools.py  # MCP 服务调用的核心实现
├── skill.py                 # 技能入口点
├── Skill.md                 # 技能元数据和文档
├── README.md                # 英文说明文档
├── README_zh.md             # 中文说明文档
└── requirements.txt         # 依赖项
```

## 安装

1. **克隆仓库**：
   ```bash
   git clone <repository-url>
   cd feishu-remote-mcp-skill
   ```

2. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

3. **配置技能**：
   - 提供您的飞书访问令牌（UAT 或 TAT）
   - 可选：指定允许使用的工具列表

## 配置参数

### 必需参数
- `accessToken`：飞书访问令牌（User Access Token 或 Tenant Access Token）

### 可选参数
- `useUAT`：是否使用 User Access Token（默认：false，使用 Tenant Access Token）
- `allowedTools`：允许调用的工具列表

## 使用示例

### 基本使用

1. **初始化 MCP 会话**：
   ```python
   result = skill.call("initializeFeishuMCP", {})
   ```

2. **列出可用工具**：
   ```python
   result = skill.call("listFeishuMCPTools", {})
   ```

### 用户管理

- **搜索用户**：
  ```python
  result = skill.call("searchFeishuUser", {
      "keyword": "张三"
  })
  ```

- **获取用户信息**：
  ```python
  result = skill.call("getFeishuUser", {
      "userId": "user123"
  })
  ```

- **获取文件内容**：
  ```python
  result = skill.call("fetchFeishuFile", {
      "fileToken": "file123"
  })
  ```

### 云文档管理

- **搜索文档**：
  ```python
  result = skill.call("searchFeishuDoc", {
      "keyword": "项目计划"
  })
  ```

- **创建文档**：
  ```python
  result = skill.call("createFeishuDoc", {
      "title": "会议纪要",
      "content": "# 会议纪要\n\n- 主题：项目讨论\n- 日期：2026-03-17"
  })
  ```

- **查看文档**：
  ```python
  result = skill.call("fetchFeishuDoc", {
      "documentLink": "https://bytedance.larkoffice.com/docx/xxxxxx"
  })
  ```

- **更新文档**：
  ```python
  result = skill.call("updateFeishuDoc", {
      "documentToken": "doc123",
      "content": "更新的内容"
  })
  ```

- **列出文档**：
  ```python
  result = skill.call("listFeishuDocs", {
      "nodeToken": "node123",
      "pageSize": 20
  })
  ```

- **获取评论**：
  ```python
  result = skill.call("getFeishuDocComments", {
      "documentToken": "doc123"
  })
  ```

- **添加评论**：
  ```python
  result = skill.call("addFeishuDocComments", {
      "documentToken": "doc123",
      "content": "做得好！"
  })
  ```

- **更新文档权限**：
  ```python
  result = skill.call("updateFeishuDocPermission", {
      "documentToken": "doc123",
      "permissionSettings": {
          "external_access_entity": "closed",
          "security_entity": "anyone_can_view",
          "comment_entity": "anyone_can_view",
          "manage_collaborator_entity": "collaborator_full_access",
          "copy_entity": "anyone_can_view"
      }
  })
  ```

## 权限要求

请确保您的飞书应用拥有使用所需工具的必要权限：

### 用户工具
- `search-user`：`contact:user:search`
- `get-user`：`contact:contact.base:readonly`、`contact:user.base:readonly`
- `fetch-file`：`docs:document.media:download`、`board:whiteboard:node:read`

### 云文档工具
- `search-doc`：`search:docs:read`、`wiki:wiki:readonly`
- `create-doc`：`docx:document:create`、`wiki:node:read`、`wiki:node:create`、`docs:document.media:upload`、`board:whiteboard:node:create`、`docx:document:write_only`、`docx:document:readonly`
- `fetch-doc`：`docx:document:readonly`、`task:task:read`、`im:chat:read`
- `update-doc`：与 create-doc 相同
- `list-docs`：`wiki:wiki:readonly`
- `get-comments`：`docs:document.comment:read`、`contact:contact.base:readonly`
- `add-comments`：`docs:document.comment:create`
- `update-doc-permission`：`drive:document`（或其他相关权限）

## 错误处理

该技能根据飞书 MCP 错误响应格式处理错误：
- 当 API 请求成功但工具执行失败时，HTTP 状态码仍然为 200，但结果中包含 `isError: true` 和错误消息
- 当请求本身无效（例如认证失败、方法名称错误）时，它会返回顶层错误对象

## 限制

- `fetch-file` 的文件大小限制：5 MB
- `search-doc` 仅支持 doc 和 docx 文档类型
- `create-doc` 不支持插入现有的电子表格、OKR、任务、日程、飞书项目等
- `fetch-doc` 不支持读取电子表格、OKR、任务、群名片、日程、飞书项目等中的内容
- `get-comments` 仅支持表情、文本和文档类型的评论；不支持获取评论中的图片
- `add-comments` 仅支持添加全文评论；不支持划词评论或向评论中上传图片

## 参考文档

- **飞书 MCP 服务文档**：[开发者调用远程 MCP 服务](https://open.feishu.cn/document/mcp_open_tools/developers-call-remote-mcp-server)
- **Claude Skill 规范**：[How to create custom Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)

## 贡献

欢迎贡献！请随时提交 Pull Request。

## 许可证

MIT License

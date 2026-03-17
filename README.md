# Feishu Remote MCP Skill

[中文版本](./README_zh.md) | English Version

This skill allows you to call Feishu's remote MCP (Model Context Protocol) services to interact with Feishu Cloud Documents and user management. It's designed to work with Claude's custom skills system.

## Features

- **User Management**: Search users, get user information, and fetch file content
- **Cloud Document Management**: Search, create, view, update, list documents, and manage comments
- **Flexible Authentication**: Support for both User Access Token (UAT) and Tenant Access Token (TAT)
- **Comprehensive Error Handling**: Properly handles Feishu MCP error responses
- **Modular Design**: Well-organized code structure following best practices

## Project Structure

```
feishu-remote-mcp-skill/
├── scripts/
│   └── feishu_mcp_tools.py  # Core implementation for MCP service calls
├── skill.py                 # Skill entry point
├── Skill.md                 # Skill metadata and documentation
├── README.md                # This file
└── requirements.txt         # Dependencies
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd feishu-remote-mcp-skill
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the skill**:
   - Provide your Feishu access token (UAT or TAT)
   - Optionally specify which tools to allow

## Configuration

### Required Parameters
- `accessToken`: Feishu access token (User Access Token or Tenant Access Token)

### Optional Parameters
- `useUAT`: Whether to use User Access Token (default: false, using Tenant Access Token)
- `allowedTools`: List of allowed tools to call

## Usage

### Basic Usage

1. **Initialize MCP session**:
   ```python
   result = skill.call("initializeFeishuMCP", {})
   ```

2. **List available tools**:
   ```python
   result = skill.call("listFeishuMCPTools", {})
   ```

### User Management

- **Search users**:
  ```python
  result = skill.call("searchFeishuUser", {
      "keyword": "John"
  })
  ```

- **Get user information**:
  ```python
  result = skill.call("getFeishuUser", {
      "userId": "user123"
  })
  ```

- **Fetch file content**:
  ```python
  result = skill.call("fetchFeishuFile", {
      "fileToken": "file123"
  })
  ```

### Cloud Document Management

- **Search documents**:
  ```python
  result = skill.call("searchFeishuDoc", {
      "keyword": "Project Plan"
  })
  ```

- **Create document**:
  ```python
  result = skill.call("createFeishuDoc", {
      "title": "Meeting Notes",
      "content": "# Meeting Notes\n\n- Topic: Project Discussion\n- Date: 2026-03-17"
  })
  ```

- **View document**:
  ```python
  result = skill.call("fetchFeishuDoc", {
      "documentLink": "https://bytedance.larkoffice.com/docx/xxxxxx"
  })
  ```

- **Update document**:
  ```python
  result = skill.call("updateFeishuDoc", {
      "documentToken": "doc123",
      "content": "Updated content"
  })
  ```

- **List documents**:
  ```python
  result = skill.call("listFeishuDocs", {
      "nodeToken": "node123",
      "pageSize": 20
  })
  ```

- **Get comments**:
  ```python
  result = skill.call("getFeishuDocComments", {
      "documentToken": "doc123"
  })
  ```

- **Add comments**:
  ```python
  result = skill.call("addFeishuDocComments", {
      "documentToken": "doc123",
      "content": "Great work!"
  })
  ```

## Permissions

Make sure your Feishu application has the necessary permissions based on the tools you need to use:

### User Tools
- `search-user`: `contact:user:search`
- `get-user`: `contact:contact.base:readonly`, `contact:user.base:readonly`
- `fetch-file`: `docs:document.media:download`, `board:whiteboard:node:read`

### Cloud Document Tools
- `search-doc`: `search:docs:read`, `wiki:wiki:readonly`
- `create-doc`: `docx:document:create`, `wiki:node:read`, `wiki:node:create`, `docs:document.media:upload`, `board:whiteboard:node:create`, `docx:document:write_only`, `docx:document:readonly`
- `fetch-doc`: `docx:document:readonly`, `task:task:read`, `im:chat:read`
- `update-doc`: Same as create-doc
- `list-docs`: `wiki:wiki:readonly`
- `get-comments`: `docs:document.comment:read`, `contact:contact.base:readonly`
- `add-comments`: `docs:document.comment:create`
- `update-doc-permission`: `drive:document` (或其他相关权限)

## Error Handling

The skill handles errors according to the Feishu MCP error response format:
- When the API request succeeds but the tool execution fails, the HTTP status code is still 200, but the result contains `isError: true` and error message
- When the request itself is invalid (e.g., authentication failure, method name error), it returns a top-level error object

## Limitations

- File size limit for `fetch-file`: 5 MB
- `search-doc` only supports doc and docx document types
- `create-doc` does not support inserting existing spreadsheets, OKRs, tasks, schedules, Feishu projects, etc.
- `fetch-doc` does not support reading content from spreadsheets, OKRs, tasks, group cards, schedules, Feishu projects, etc.
- `get-comments` only supports emoji, text, and document type comments; does not support getting images in comments
- `add-comments` only supports adding full-text comments; does not support inline comments or uploading images to comments

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

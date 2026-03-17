---
name: Feishu Remote MCP
version: 1.2.0
description: 调用飞书远程 MCP 服务，实现与飞书云文档和用户管理的交互
dependencies:
  - requests
---

# Feishu Remote MCP Skill

This skill allows you to call Feishu's remote MCP (Model Context Protocol) services to interact with Feishu Cloud Documents and user management.

## Configuration

### Required Parameters
- `accessToken`: Feishu access token (User Access Token or Tenant Access Token)

### Optional Parameters
- `useUAT`: Whether to use User Access Token (default: false, using Tenant Access Token)
- `allowedTools`: List of allowed tools to call

## Tools

### Base Tools
- `initializeFeishuMCP`: Initialize Feishu MCP session
- `listFeishuMCPTools`: List available MCP tools

### User Tools
- `searchFeishuUser`: Search users in the enterprise by keyword
- `getFeishuUser`: Get user information by user ID
- `fetchFeishuFile`: Get file content by file token

### Cloud Document Tools
- `searchFeishuDoc`: Search cloud documents by keyword
- `createFeishuDoc`: Create a new cloud document
- `fetchFeishuDoc`: View cloud document content by document link
- `updateFeishuDoc`: Update cloud document content
- `listFeishuDocs`: List cloud documents under a specific knowledge space node
- `getFeishuDocComments`: View comments in a cloud document
- `addFeishuDocComments`: Add comments to a cloud document
- `updateFeishuDocPermission`: Update cloud document permission settings

## Usage Examples

### Search for a user
```python
result = skill.call("searchFeishuUser", {
    "keyword": "John"
})
```

### Create a document
```python
result = skill.call("createFeishuDoc", {
    "title": "Meeting Notes",
    "content": "# Meeting Notes\n\n- Topic: Project Discussion\n- Date: 2026-03-17"
})
```

### View document content
```python
result = skill.call("fetchFeishuDoc", {
    "documentLink": "https://bytedance.larkoffice.com/docx/xxxxxx"
})
```

### Update document permission (with default settings)
```python
result = skill.call("updateFeishuDocPermission", {
    "documentToken": "doc123"
})
```

### Update document permission (with custom settings)
```python
result = skill.call("updateFeishuDocPermission", {
    "documentToken": "doc123",
    "permissionSettings": {
        "external_access_entity": "closed",
        "link_share_entity": "tenant_editable",
        "comment_entity": "anyone_can_view"
    },
    "fileType": "docx"
})
```

## Authentication

You can use either User Access Token (UAT) or Tenant Access Token (TAT) for authentication:
- UAT: Represents user identity, suitable for scenarios that require simulating specific user operations
- TAT: Represents application identity, suitable for server-to-server call scenarios

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
- `update-doc-permission`: `drive:document` (or other related permissions)

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
- `update-doc-permission` requires appropriate permissions to modify document settings; ensure the calling identity has manage permissions on the document

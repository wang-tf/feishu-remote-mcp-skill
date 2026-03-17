from copaw import register_skill
import requests

class FeishuMCPTools:
    def __init__(self, config):
        self.config = config
        self.base_url = "https://mcp.feishu.cn/mcp"
        self.headers = {
            "Content-Type": "application/json"
        }
        # 添加认证凭证
        if config.get("useUAT", False):
            self.headers["X-Lark-MCP-UAT"] = config.get("accessToken")
        else:
            self.headers["X-Lark-MCP-TAT"] = config.get("accessToken")
        # 添加允许的工具列表
        if config.get("allowedTools"):
            self.headers["X-Lark-MCP-Allowed-Tools"] = ",".join(config.get("allowedTools"))
    
    def _make_request(self, method, params=None, request_id=1):
        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method
        }
        if params:
            payload["params"] = params
        
        response = requests.post(self.base_url, headers=self.headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "error" in result:
            raise Exception(f"MCP 调用失败: {result['error']['message']}")
        
        if result.get("result", {}).get("isError", False):
            error_message = result["result"]["content"][0]["text"]
            raise Exception(f"工具执行失败: {error_message}")
        
        return result["result"]
    
    def initialize(self):
        return self._make_request("initialize")
    
    def list_tools(self):
        return self._make_request("tools/list")
    
    def call_tool(self, tool_name, arguments, request_id=1):
        params = {
            "name": tool_name,
            "arguments": arguments
        }
        return self._make_request("tools/call", params, request_id)
    
    # 通用工具
    def search_user(self, keyword):
        return self.call_tool("search-user", {"keyword": keyword})
    
    def get_user(self, user_id):
        return self.call_tool("get-user", {"user_id": user_id})
    
    def fetch_file(self, file_token):
        return self.call_tool("fetch-file", {"file_token": file_token})
    
    # 云文档工具
    def search_doc(self, keyword):
        return self.call_tool("search-doc", {"keyword": keyword})
    
    def create_doc(self, title, content, parent_node_token=None):
        arguments = {
            "title": title,
            "content": content
        }
        if parent_node_token:
            arguments["parent_node_token"] = parent_node_token
        return self.call_tool("create-doc", arguments)
    
    def fetch_doc(self, document_link):
        return self.call_tool("fetch-doc", {"document_link": document_link})
    
    def update_doc(self, document_token, content):
        return self.call_tool("update-doc", {
            "document_token": document_token,
            "content": content
        })
    
    def list_docs(self, node_token, page_size=20, page_token=""):
        return self.call_tool("list-docs", {
            "node_token": node_token,
            "page_size": page_size,
            "page_token": page_token
        })
    
    def get_comments(self, document_token):
        return self.call_tool("get-comments", {"document_token": document_token})
    
    def add_comments(self, document_token, content):
        return self.call_tool("add-comments", {
            "document_token": document_token,
            "content": content
        })

@register_skill
def feishu_remote_mcp_skill():
    return {
        "name": "feishu-remote-mcp",
        "version": "1.0.0",
        "description": "调用飞书远程 MCP 服务的 skill",
        "configuration": {
            "accessToken": {
                "type": "string",
                "required": True,
                "description": "飞书访问令牌 (User Access Token 或 Tenant Access Token)"
            },
            "useUAT": {
                "type": "boolean",
                "required": False,
                "default": False,
                "description": "是否使用 User Access Token (默认使用 Tenant Access Token)"
            },
            "allowedTools": {
                "type": "array",
                "required": False,
                "description": "允许调用的工具列表"
            }
        },
        "tools": [
            {
                "name": "initializeFeishuMCP",
                "description": "初始化飞书 MCP 会话",
                "parameters": {},
                "handler": lambda params, config: FeishuMCPTools(config).initialize()
            },
            {
                "name": "listFeishuMCPTools",
                "description": "列出可用的 MCP 工具",
                "parameters": {},
                "handler": lambda params, config: FeishuMCPTools(config).list_tools()
            },
            {
                "name": "searchFeishuUser",
                "description": "根据关键词搜索企业内的用户",
                "parameters": {
                    "keyword": {
                        "type": "string",
                        "required": True,
                        "description": "搜索关键词，如姓名、邮箱等"
                    }
                },
                "handler": lambda params, config: FeishuMCPTools(config).search_user(params["keyword"])
            },
            {
                "name": "getFeishuUser",
                "description": "获取用户个人信息",
                "parameters": {
                    "userId": {
                        "type": "string",
                        "required": True,
                        "description": "用户 ID"
                    }
                },
                "handler": lambda params, config: FeishuMCPTools(config).get_user(params["userId"])
            },
            {
                "name": "fetchFeishuFile",
                "description": "获取文件内容",
                "parameters": {
                    "fileToken": {
                        "type": "string",
                        "required": True,
                        "description": "文件 ID (file_token)"
                    }
                },
                "handler": lambda params, config: FeishuMCPTools(config).fetch_file(params["fileToken"])
            },
            {
                "name": "searchFeishuDoc",
                "description": "搜索云文档",
                "parameters": {
                    "keyword": {
                        "type": "string",
                        "required": True,
                        "description": "搜索关键词"
                    }
                },
                "handler": lambda params, config: FeishuMCPTools(config).search_doc(params["keyword"])
            },
            {
                "name": "createFeishuDoc",
                "description": "创建云文档",
                "parameters": {
                    "title": {
                        "type": "string",
                        "required": True,
                        "description": "文档标题"
                    },
                    "content": {
                        "type": "string",
                        "required": True,
                        "description": "文档内容"
                    },
                    "parentNodeToken": {
                        "type": "string",
                        "required": False,
                        "description": "父节点 token，用于指定文档创建位置"
                    }
                },
                "handler": lambda params, config: FeishuMCPTools(config).create_doc(
                    params["title"], params["content"], params.get("parentNodeToken")
                )
            },
            {
                "name": "fetchFeishuDoc",
                "description": "查看云文档",
                "parameters": {
                    "documentLink": {
                        "type": "string",
                        "required": True,
                        "description": "文档链接"
                    }
                },
                "handler": lambda params, config: FeishuMCPTools(config).fetch_doc(params["documentLink"])
            },
            {
                "name": "updateFeishuDoc",
                "description": "更新云文档",
                "parameters": {
                    "documentToken": {
                        "type": "string",
                        "required": True,
                        "description": "文档 token"
                    },
                    "content": {
                        "type": "string",
                        "required": True,
                        "description": "新的文档内容"
                    }
                },
                "handler": lambda params, config: FeishuMCPTools(config).update_doc(
                    params["documentToken"], params["content"]
                )
            },
            {
                "name": "listFeishuDocs",
                "description": "获取指定知识空间节点下的云文档列表",
                "parameters": {
                    "nodeToken": {
                        "type": "string",
                        "required": True,
                        "description": "知识空间节点 token"
                    },
                    "pageSize": {
                        "type": "integer",
                        "required": False,
                        "default": 20,
                        "description": "每页数量"
                    },
                    "pageToken": {
                        "type": "string",
                        "required": False,
                        "default": "",
                        "description": "分页 token"
                    }
                },
                "handler": lambda params, config: FeishuMCPTools(config).list_docs(
                    params["nodeToken"], params.get("pageSize", 20), params.get("pageToken", "")
                )
            },
            {
                "name": "getFeishuDocComments",
                "description": "查看指定云文档中的评论",
                "parameters": {
                    "documentToken": {
                        "type": "string",
                        "required": True,
                        "description": "文档 token"
                    }
                },
                "handler": lambda params, config: FeishuMCPTools(config).get_comments(params["documentToken"])
            },
            {
                "name": "addFeishuDocComments",
                "description": "在指定云文档中添加评论",
                "parameters": {
                    "documentToken": {
                        "type": "string",
                        "required": True,
                        "description": "文档 token"
                    },
                    "content": {
                        "type": "string",
                        "required": True,
                        "description": "评论内容"
                    }
                },
                "handler": lambda params, config: FeishuMCPTools(config).add_comments(
                    params["documentToken"], params["content"]
                )
            }
        ]
    }

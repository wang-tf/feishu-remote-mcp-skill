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

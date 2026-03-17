import requests
import json
import os

class FeishuMCPTools:
    def __init__(self, config):
        self.config = config
        self.base_url = "https://mcp.feishu.cn/mcp"
        self.headers = {
            "Content-Type": "application/json"
        }
        
        # 优先从环境变量读取
        self.app_id = os.environ.get("FEISHU_APP_ID")
        self.app_secret = os.environ.get("FEISHU_APP_SECRET")
        
        # 如果环境变量不存在，从配置文件读取
        if not self.app_id or not self.app_secret:
            config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
            if os.path.exists(config_file):
                with open(config_file, "r", encoding="utf-8") as f:
                    config_data = json.load(f)
                    if not self.app_id:
                        self.app_id = config_data.get("app_id")
                    if not self.app_secret:
                        self.app_secret = config_data.get("app_secret")
        
        # 处理环境变量占位符
        if self.app_id == "$FEISHU_APP_ID":
            self.app_id = None
        if self.app_secret == "$FEISHU_APP_SECRET":
            self.app_secret = None
        
        # 添加认证凭证
        access_token = config.get("accessToken")
        if not access_token and self.app_id and self.app_secret:
            # 如果没有提供 accessToken，尝试使用 app_id 和 app_secret 获取
            access_token = self._get_tenant_access_token()
        
        if access_token:
            if config.get("useUAT", False):
                self.headers["X-Lark-MCP-UAT"] = access_token
            else:
                self.headers["X-Lark-MCP-TAT"] = access_token
        
        # 添加允许的工具列表
        if config.get("allowedTools"):
            self.headers["X-Lark-MCP-Allowed-Tools"] = ",".join(config.get("allowedTools"))
    
    def _get_tenant_access_token(self):
        """获取租户访问令牌"""
        if not self.app_id or not self.app_secret:
            return None
        
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            if result.get("code") == 0:
                return result.get("tenant_access_token")
            return None
        except Exception as e:
            print(f"获取租户访问令牌失败: {e}")
            return None
    
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

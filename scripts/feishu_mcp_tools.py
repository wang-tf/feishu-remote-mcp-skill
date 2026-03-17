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
        allowed_tools = config.get("allowedTools")
        if not allowed_tools:
            # 默认添加所有工具
            allowed_tools = [
                "search-user", "get-user", "fetch-file",
                "search-doc", "create-doc", "fetch-doc", "update-doc", "list-docs", "get-comments", "add-comments"
            ]
        self.headers["X-Lark-MCP-Allowed-Tools"] = ",".join(allowed_tools)
    
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
    
    def update_doc_permission(self, document_token, permission_settings):
        """更新云文档权限设置"""
        url = f"https://open.feishu.cn/open-apis/drive/v2/permissions/{document_token}/public"
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": self.headers.get("X-Lark-MCP-TAT") or self.headers.get("X-Lark-MCP-UAT")
        }
        
        # 确保 authorization 格式正确
        if headers["Authorization"] and not headers["Authorization"].startswith("Bearer "):
            headers["Authorization"] = f"Bearer {headers["Authorization"]}"
        
        payload = permission_settings
        
        try:
            response = requests.patch(url, headers=headers, json=payload, params={"type": "docx"})
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"更新文档权限失败: {e}")
    
    def create_doc(self, title, content, parent_node_token=None):
        arguments = {
            "title": title,
            "content": content
        }
        if parent_node_token:
            arguments["parent_node_token"] = parent_node_token
        
        # 创建文档
        result = self.call_tool("create-doc", arguments)
        
        # 获取文档 token
        document_token = None
        if isinstance(result, dict):
            # 解析返回结果，提取文档 token
            if "content" in result:
                for item in result["content"]:
                    if isinstance(item, dict) and "text" in item:
                        import json
                        try:
                            text_data = json.loads(item["text"])
                            if "data" in text_data and "document_token" in text_data["data"]:
                                document_token = text_data["data"]["document_token"]
                                break
                        except:
                            pass
        
        # 设置文档权限为“组织内获得链接的人可编辑”
        if document_token:
            permission_settings = {
                "external_access_entity": "closed",  # 不允许分享到组织外
                "security_entity": "anyone_can_view",  # 拥有可阅读权限的用户可以复制、打印、下载
                "comment_entity": "anyone_can_view",  # 拥有可阅读权限的用户可以评论
                "manage_collaborator_entity": "collaborator_full_access",  # 只有拥有可管理权限的用户可以管理协作者
                "copy_entity": "anyone_can_view"  # 拥有可阅读权限的用户可以复制内容
            }
            # 注意：具体的权限设置可能需要根据飞书 API 的要求进行调整
            # 这里的设置是一个示例，实际使用时可能需要根据具体需求进行修改
            try:
                self.update_doc_permission(document_token, permission_settings)
            except Exception as e:
                print(f"设置文档权限失败: {e}")
        
        return result

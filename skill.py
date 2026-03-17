from scripts.feishu_mcp_tools import FeishuMCPTools

def get_skill():
    return {
        "name": "feishu-remote-mcp",
        "version": "1.2.0",
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
            },
            {
                "name": "updateFeishuDocPermission",
                "description": "更新云文档权限设置",
                "parameters": {
                    "documentToken": {
                        "type": "string",
                        "required": True,
                        "description": "文档 token"
                    },
                    "permissionSettings": {
                        "type": "object",
                        "required": True,
                        "description": "权限设置对象",
                        "properties": {
                            "external_access_entity": {
                                "type": "string",
                                "description": "是否允许内容被分享到组织外",
                                "enum": ["open", "closed", "allow_share_partner_tenant"]
                            },
                            "security_entity": {
                                "type": "string",
                                "description": "谁可以创建副本、打印、下载",
                                "enum": ["anyone_can_view", "anyone_can_edit", "only_full_access"]
                            },
                            "comment_entity": {
                                "type": "string",
                                "description": "谁可以评论",
                                "enum": ["anyone_can_view", "anyone_can_edit"]
                            },
                            "manage_collaborator_entity": {
                                "type": "string",
                                "description": "谁可以查看、添加、移除协作者",
                                "enum": ["collaborator_can_view", "collaborator_can_edit", "collaborator_full_access"]
                            },
                            "copy_entity": {
                                "type": "string",
                                "description": "谁可以复制内容",
                                "enum": ["anyone_can_view", "anyone_can_edit", "only_full_access"]
                            }
                        }
                    },
                    "fileType": {
                        "type": "string",
                        "required": False,
                        "default": "docx",
                        "description": "文档类型",
                        "enum": ["doc", "docx", "sheet", "file", "wiki", "bitable"]
                    }
                },
                "handler": lambda params, config: FeishuMCPTools(config).update_doc_permission(
                    params["documentToken"], params.get("permissionSettings"), params.get("fileType", "docx")
                )
            }
        ]
    }

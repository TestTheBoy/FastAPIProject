## fastapi_Demo介绍
fastapi_Demo 是一个 fastapi 企业级快速开发平台，基于经典技术组合（fastapi、Vue3、Vben Admin、Ant Design Of Vue），内置模块如：用户管理、在线用户、角色管理、菜单管理、前端路由同步、部门管理、岗位管理等。在线开发：支持元数据管理、代码生成。


演示环境账号密码：admin/123456

本地环境账号密码：superAdmin/123456


## 目录结构
```lua
fastapi_Demo/
├── cli.py                          -- 命令行工具入口，提供代码生成和表结构查看功能
├── main.py                         -- 应用主入口，配置FastAPI应用、中间件和生命周期管理
├── database.py                     -- 数据库配置与连接，包括MySQL和Redis配置
├── requirements.txt                -- 依赖包清单
├── README.md                       -- 项目说明文档
├── pyrightconfig.json              -- Python类型检查配置文件
├── generator/                      -- 代码生成器相关
│   ├── code_generator.py           -- 代码生成器核心类，负责从数据库表生成代码
│   ├── config.json                 -- 生成器配置文件，定义模板和生成路径
│   └── templates/                  -- 代码模板目录
│       ├── controller.ftl          -- 控制器模板，生成API接口控制器
│       ├── model.ftl               -- 模型模板，生成数据库模型类
│       ├── param.ftl               -- 参数模板，生成请求参数类
│       ├── service.ftl             -- 服务模板，生成业务逻辑服务类
│       └── vo.ftl                  -- VO模板，生成视图对象类
├── App_Demo/                         -- 核心框架代码
│   ├── __init__.py
│   ├── util.py                     -- 通用工具类，提供字符串处理等常用功能
│   ├── low_code_util.py            -- 低代码工具类，支持低代码平台功能
│   ├── base/                       -- 基础模块
│   │   ├── __init__.py
│   │   ├── api_model.py            -- API模型定义，如统一返回结果类
│   │   └── orm_model.py            -- ORM模型基类，所有数据库模型的基类
│   └── core/                       -- 核心组件
│       ├── __init__.py
│       ├── auto_router.py          -- 自动路由加载器，自动扫描并注册控制器
│       ├── constant_context.py     -- 常量上下文，管理系统配置常量
│       ├── constant_context_holder.py -- 常量上下文持有者
│       ├── db_types.py             -- 数据库类型定义
│       ├── dict_loader.py          -- 字典加载器，加载系统数据字典
│       ├── enums.py                -- 枚举基类
│       ├── exception.py            -- 自定义异常类
│       ├── exception_handler.py    -- 异常处理器，统一处理系统异常
│       ├── ioc_container.py        -- IOC容器，实现依赖注入
│       ├── permission.py           -- 权限控制相关
│       ├── query_param_context.py  -- 查询参数上下文
│       ├── redis_token_store.py    -- Redis令牌存储实现
│       ├── request_context.py      -- 请求上下文管理
│       ├── snawflake_id_generator.py -- 雪花ID生成器
│       ├── token_manager.py        -- 令牌管理器
│       ├── token_store.py          -- 令牌存储接口定义
│       ├── user_context.py         -- 用户上下文管理
│       └── middleware/             -- 中间件
│           ├── demo_permission_middleware.py -- 演示环境权限中间件
│           ├── query_param_middleware.py     -- 查询参数中间件
│           └── user_context_middleware.py    -- 用户上下文中间件
└── modules/                        -- 业务模块目录
    └── sys/                        -- 系统管理模块
        ├── __init__.py
        ├── controllers/            -- 控制器层（路由），定义API接口
        │   ├── auth_controller.py      -- 认证接口控制器
        │   ├── config_controller.py    -- 配置管理控制器
        │   ├── dept_controller.py      -- 部门管理控制器
        │   ├── dict_controller.py      -- 字典管理控制器
        │   ├── dict_item_controller.py -- 字典项管理控制器
        │   ├── low_code_controller.py  -- 低代码功能控制器
        │   ├── menu_controller.py      -- 菜单管理控制器
        │   ├── post_controller.py      -- 岗位管理控制器
        │   ├── rbac_controller.py      -- RBAC权限管理控制器
        │   ├── role_controller.py      -- 角色管理控制器
        │   ├── user_controller.py      -- 用户管理控制器
        │   ├── vis_log_controller.py   -- 访问日志控制器
        │   └── __init__.py
        ├── models/                 -- 数据模型，对应数据库表结构
        │   ├── config.py           -- 配置模型
        │   ├── dept.py             -- 部门模型
        │   ├── dict.py             -- 字典模型
        │   ├── dict_item.py        -- 字典项模型
        │   ├── menu.py             -- 菜单模型
        │   ├── post.py             -- 岗位模型
        │   ├── role.py             -- 角色模型
        │   ├── role_menu.py        -- 角色菜单关系模型
        │   ├── user.py             -- 用户模型
        │   ├── user_role.py        -- 用户角色关系模型
        │   ├── vis_log.py          -- 访问日志模型
        │   └── __init__.py
        ├── params/                 -- 参数对象，用于接收和校验请求参数
        │   ├── config_param.py     -- 配置参数类
        │   ├── dept_param.py       -- 部门参数类
        │   ├── dict_param.py       -- 字典参数类
        │   ├── dict_item_param.py  -- 字典项参数类
        │   ├── login_param.py      -- 登录参数类
        │   ├── menu_param.py       -- 菜单参数类
        │   ├── post_param.py       -- 岗位参数类
        │   ├── role_param.py       -- 角色参数类
        │   ├── role_menu_param.py  -- 角色菜单参数类
        │   ├── user_param.py       -- 用户参数类
        │   ├── user_role_param.py  -- 用户角色参数类
        │   ├── vis_log_param.py    -- 访问日志参数类
        │   └── __init__.py
        ├── services/               -- 业务服务层，实现业务逻辑
        │   ├── auth_service.py     -- 认证服务
        │   ├── config_service.py   -- 配置服务
        │   ├── dept_service.py     -- 部门服务
        │   ├── dict_service.py     -- 字典服务
        │   ├── dict_item_service.py -- 字典项服务
        │   ├── menu_service.py     -- 菜单服务
        │   ├── post_service.py     -- 岗位服务
        │   ├── rbac_service.py     -- RBAC权限服务
        │   ├── role_service.py     -- 角色服务
        │   ├── role_menu_service.py -- 角色菜单服务
        │   ├── user_service.py     -- 用户服务
        │   ├── user_role_service.py -- 用户角色服务
        │   ├── vis_log_service.py  -- 访问日志服务
        │   └── __init__.py
        ├── vos/                    -- VO对象（View Object），用于接口返回数据
        │   ├── config_vo.py        -- 配置VO
        │   ├── dept_vo.py          -- 部门VO
        │   ├── dict_vo.py          -- 字典VO
        │   ├── dict_item_vo.py     -- 字典项VO
        │   ├── login_token_vo.py   -- 登录令牌VO
        │   ├── menu_vo.py          -- 菜单VO
        │   ├── post_vo.py          -- 岗位VO
        │   ├── role_vo.py          -- 角色VO
        │   ├── role_menu_vo.py     -- 角色菜单VO
        │   ├── user_vo.py          -- 用户VO
        │   ├── user_role_vo.py     -- 用户角色VO
        │   ├── vis_log_vo.py       -- 访问日志VO
        │   └── __init__.py
        └── enums/                  -- 枚举定义
            ├── admin_type_enum.py  -- 管理员类型枚举
            ├── dict_data_type_enum.py -- 字典数据类型枚举
            ├── menu_app_code_enum.py -- 菜单应用代码枚举
            ├── role_data_scope_enum.py -- 角色数据范围枚举
            ├── role_type_enum.py   -- 角色类型枚举
            ├── sex_enum.py         -- 性别枚举
            ├── vis_type_enum.py    -- 访问类型枚举
            ├── yes_no_enum.py      -- 是/否枚举
            └── __init__.py
```
项目采用清晰的分层架构设计，主要包括以下几个层次：

* 入口层：main.py和cli.py作为应用入口和命令行工具
* 核心框架层：App_Demo/目录包含框架核心组件，如异常处理、中间件、上下文管理等
* 业务模块层：modules/目录包含各业务模块，每个模块按照MVC模式划分为控制器、模型、服务、参数和VO等子目录
* 代码生成器：generator/目录提供从数据库表自动生成代码的功能

这种结构设计使得项目易于维护和扩展，符合企业级应用开发的最佳实践。

## 技术栈

### 后端技术栈
- **核心框架**: [FastAPI](https://fastapi.tiangolo.com/zh/) v0.116.1 - 高性能Python Web框架
- **ORM框架**: [SQLAlchemy](https://www.sqlalchemy.org/) v2.0.43 - Python SQL工具包和对象关系映射器
- **数据库**: MySQL 5.7+ - 关系型数据库
- **缓存数据库**: Redis - 高性能键值数据库
- **Web服务器**: [Uvicorn](https://www.uvicorn.org/) - 基于uvloop和httptools的ASGI服务器
- **模板引擎**: [Jinja2](https://jinja.palletsprojects.com/) - 现代化和设计友好的Python模板引擎
- **数据校验**: [Pydantic](https://docs.pydantic.dev/) v2.10.6 - 基于Python类型提示的数据校验和设置管理
- **命令行工具**: [Typer](https://typer.tiangolo.com/) - 用于构建CLI应用的库
- **异步支持**: [AnyIO](https://anyio.readthedocs.io/) 和 [async-timeout](https://github.com/aio-libs/async-timeout)
- **HTTP客户端**: [HTTPX](https://www.python-httpx.org/) - 异步HTTP客户端

### 核心依赖组件
- **数据库连接**: PyMySQL - 纯Python MySQL客户端库
- **Redis客户端**: redis-py - Python Redis客户端
- **环境配置**: python-dotenv - 从.env文件加载环境变量
- **文件上传**: python-multipart - 支持多部分表单数据解析
- **用户代理解析**: user-agents - 用户代理字符串解析库
- **富文本终端**: rich - 在终端中提供富文本和美观格式

### 开发工具
- **类型检查**: typing-extensions - 提供向后兼容的类型提示功能
- **代码热重载**: watchfiles - 监控文件变化并触发重载
- **异步支持**: uvloop 和 httptools - 提升异步性能

### 项目架构特点
1. **分层架构**: 采用经典的分层架构设计，包括控制器层、服务层、模型层和参数层
2. **自动路由注册**: 通过注解自动扫描并注册路由控制器
3. **依赖注入**: 实现了简单的IOC容器进行依赖管理
4. **统一异常处理**: 集中处理系统异常，提供一致的错误响应格式
5. **上下文管理**: 实现了用户上下文、查询参数上下文等请求级上下文管理
6. **代码生成器**: 基于Jinja2模板引擎的代码自动生成工具，支持从数据库表生成完整CRUD代码
7. **权限控制**: 支持基于角色的访问控制(RBAC)和数据权限控制
8. **令牌管理**: 基于Redis的JWT令牌管理机制

这套技术栈组合提供了高性能、高可维护性的企业级应用开发能力，特别适合构建现代化的RESTful API服务。

## 环境安装
- Python3安装（略）
- NodeJS 16 （略）
- Mysql （略）
- Redis（略）
- NodeJS版本管理工具nvm（略），如果安装了nvm，可不用单独安装nodejs
- IDEA/PyCharm（略）
- Git Bash (略)
- VSCode（略）
- ApiFox或Postman 接口测试及管理工具（略）
## 快速开始
### 创建虚拟环境
```shell
python -m venv ./venv
```
### 激活虚拟环境
```shell
source venv/Scripts/activate
```
### 安装依赖
```shell
pip3 install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```
### 设置环境变量
```shell
# 按需示例修改
export DB_HOST=192.168.1.160
export DB_PORT=3306
export DB_USER=root
export DB_PASSWORD=123456
export DB_NAME=App_Demo
export REDIS_HOST=192.168.1.160
export REDIS_PORT=6379
export REDIS_PASSWORD=123456
```
### 运行
```shell
python main.py
```
### 其他命令
#### 代码生成
```shell
# 生成指定表
python cli.py gen  -t sys_user
# 生成多张表
python cli.py gen -t sys_dict,sys_dict_item
# 模糊匹配生成
python cli.py gen -t sys_%
```
#### 生成依赖文件
```shell
pip3 freeze > requirements.txt
```


## 功能清单

- [ ] 系统设置
	- [x] 用户管理
        - [x] 扮演用户
        - [x] 重置密码
        - [x] 授权角色/
    - [x] 在线用户
        - [x] 详情
        - [x] 踢下线
        - [x] 强制注销
	- [x] 角色管理
        - [x] 授权菜单
        - [x] 成员管理
	- [x] 菜单管理
	- [x] 前端路由
        - [x] 同步路由清单
	- [x] 部门管理
	- [x] 岗位管理
    - [x] 数据字典
    - [x] 参数配置
    - [x] 登录日志
    - [ ] 系统日志
	- [ ] 系统通知
- [x] 工作流程
	- [x] 流程设计
        - [x] 流程设计
        - [x] 表单设计
        - [x] 部署流程
        - [x] 导出流程
        - [x] 导入流程
    - [x] 流程定义
	- [x] 发起申请
	- [x] 我发起的
	- [x] 我的待办
      - [x] 同意
      - [x] 拒绝
      - [x] 退回上一步
      - [x] 退回发起人
      - [x] 跳转
      - [x] 转办
      - [x] 委托
      - [x] 抄送
      - [ ] 转发
      - [x] 加签
      - [x] 减签
	- [x] 我的已办
	- [x] 我的抄送
- [ ] 在线开发
    - [ ] 模型分组
    - [ ] 数据模型
        - [ ] 导入数据库表
        - [ ] 查看元数据
        - [ ] 模型字段管理
        - [ ] 在线预览

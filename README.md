# HLY_AUTO_TEST


> 开发环境: Pycharm
>
> 开发语言&版本:  python3.9
>
> 测试框架: Pytest、测试报告: Allure
>
> 版本管理: Git

## 项目目录结构

- api	-- 模仿PO模式, 抽象出页面类, 页面类内包含页面所包含所有接口, 并封装成方法可供其他模块直接调用
- config    -- 配置文件目录
- data    -- 测试数据目录
- doc    -- 文档存放目录
- log    -- 日志
- report    -- 测试报告
- scripts    -- 测试脚本存放目录
- tools    -- 工具类目录
- .gitignore    -- git忽略
- app.py    -- 命令行启动入口
- pytest.ini    -- pytest测试框架配置文件
- README.md    -- 开发说明文档

## 代码分析

**pytest.ini**

> pytest框架的配置文件

```python
[pytest]
addopts = --html=../report/report.html    # pytest-html报告插件配置 
;addopts = -s --alluredir report    # allure-pytest报告插件配置
testpaths = ./scripts    # 设置用例目录识别名称
python_files = test*_*.py    # 设置测试文件识别名称
python_classes = Test*    # 设置测试类识别名称
python_functions = test_*    # 设置测试方法识别名称
```

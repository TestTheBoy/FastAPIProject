import json
import os
import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine

from App_Demo.util import StrUtil


PROJECT_ROOT = Path(__file__).resolve().parent.parent
GENERATOR_ROOT = Path(__file__).resolve().parent


class CodeGenerator:
    """
    代码生成器
    """
    db = None
    engine = None
    table_list = []
    config = None

    def __init__(self, engine: Engine = None):
        if engine:
            self.engine = engine

    def print_table(self):
        """
        打印元数据信息
        :return:
        """
        for table in self.table_list:
            print(json.dumps(table, sort_keys=False, ensure_ascii=False))

    def build_table(self, tableName: str = ""):
        """
        根据表名称构建元数据-重新组织元数据
        :param tableName: 表名称
        :return:
        """
        if self.engine is None:
            raise Exception("engine is None")
        if not tableName:
            raise Exception("tableName is None")
        isLike = False
        if "%" in tableName:
            isLike = True
            tableName = tableName.replace("%", "")
        metadata_obj = MetaData()#读取数据库所有表的 Table 对象
        with self.engine.connect() as conn:
          metadata_obj.reflect(bind=conn)
        tables = metadata_obj.tables
        self.table_list = []
        for table in tables.values():
            if isLike and not table.name.startswith(tableName):
                continue
            if not isLike and table.name != tableName:
                continue
            columns = []
            # 检查是否需要导入特定模块
            need_datetime = False
            need_optional = False
            # 定义基类字段
            base_fields = {'id', 'create_time', 'update_time', 'create_user', 'update_user', 'is_deleted'}
            # 检查是否为树形表（包含id、name、parentId字段）
            column_names = [col.name for col in table.columns]
            is_tree_table = all(field in column_names for field in ['id', 'name', 'parent_id'])
            if not table.comment:
                table.comment = ""
            # 自动识别表前缀（第一个下划线前的部分）
            table_prefix = table.name.split('_')[0] + '_' if '_' in table.name else ''
            m_table = {
                "moduleName": table.name.split('_')[0],
                "treeTable": is_tree_table,
                "tableName": table.name,
                "shortTableName": table.name.replace(table_prefix, ""),
                "tableCamelName": StrUtil.underline_to_camel(table.name.replace(table_prefix, "")),
                "tableHumpName": StrUtil.underline_to_hump(table.name.replace(table_prefix, "")),
                "comment": table.comment,
                "columns": columns,
                "need_datetime": False,
                "need_decimal": False,
                "need_optional": False,
                "need_union": False,
                "is_relation": table.comment.startswith("r_") or table.name.startswith("r_"),
            }
            for col in table.columns:
                m_type = str(col.type.get_dbapi_type)
                # <bound method Integer.get_dbapi_type of INTEGER(display_width=11)>
                # <bound method String.get_dbapi_type of VARCHAR(length=32)>
                # <bound method DateTime.get_dbapi_type of DATETIME()>
                r = re.findall(r'.+method (.+)\.get_dbapi_type', m_type)
                if re.search('BIGINT', m_type):
                    m_type = "BigInteger"
                else:
                    m_type = r[0]
                # 判断是否需要导入特定模块（排除基类字段）
                if col.name not in base_fields:
                    if m_type == 'DateTime':
                        need_datetime = True
                    if col.nullable:
                        need_optional = True
                    if m_type == 'Numeric':
                        m_table["need_decimal"] = True
                    if m_type == 'BigInteger' and col.name == 'sort':
                        m_table["need_union"] = True
                columns.append({
                    "name": col.name,
                    "need_union": m_type == 'BigInteger' and col.name == 'sort',
                    "camelName": StrUtil.underline_to_camel(col.name),
                    "hasLength": False,
                    "comment": col.comment,
                    "primaryKey": col.primary_key,
                    "nullable": col.nullable,
                    "default": col.default,
                    "index": col.index,
                    "unique": col.unique,
                    "autoincrement": col.autoincrement is True,
                    "length": getattr(col.type, 'display_width', getattr(col.type, 'length', None)),
                    "type": m_type,
                    "precision": getattr(col.type, 'precision', None),  # Numeric类型的总位数
                    "scale": getattr(col.type, 'scale', None)  # Numeric类型的小数位数
                  })
            # 更新是否需要导入特定模块的标志
            m_table["need_datetime"] = need_datetime
            m_table["need_optional"] = need_optional
            self.table_list.append(m_table)
            return m_table

    def init_config(self):
        """
        加载配置文件
        :return:
        """
        with open(GENERATOR_ROOT / "config.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)

    def gen_code(self):
        """
        生成代码
        """
        env = Environment(loader=FileSystemLoader(str(GENERATOR_ROOT / "templates")))
        templates = self.config['templates']
        for table in self.table_list:
            # 关系表不生成控制器
            if table.get("is_relation"):
                # 过滤掉控制器模板
                templates_to_generate = [t for t in templates if t['templateFile'] != 'controller.ftl']
            else:
                templates_to_generate = templates
            templateData = {}
            templateData.update(self.config)
            templateData.update({"table": table})
            for item in templates_to_generate:
                if not item.get("selected"):
                    continue
                template = env.get_template(item['templateFile'])
                path = PROJECT_ROOT / self.config['targetProject'] / item['targetPath']
                # 配置参数替换-模板引擎
                path = env.from_string(path).render(templateData)
                # 替换包名为目录
                path = Path(str(path).replace(".", "/"))
                if not path.exists():
                    path.mkdir(parents=True)
                # 配置参数替换-模板引擎
                targetFileName = env.from_string(item['targetFileName']).render(templateData)
                dist = path / targetFileName

                if os.path.exists(dist):
                    if item.get("covered"):
                        with open(dist, 'w', encoding=item.get("encoding")) as f:
                            html = template.render(templateData)
                            f.write(html)
                            print(f"{templateData['table']['tableName']}表代码生成成功-覆盖：{dist}")
                    else:
                        print(f"{dist}文件已存在，不覆盖")
                else:
                    with open(dist, 'w', encoding=item['encoding']) as f:
                        html = template.render(templateData)
                        f.write(html)
                        print(f"{templateData['table']['tableName']}表代码生成成功-新生成：{dist}")
        return 1

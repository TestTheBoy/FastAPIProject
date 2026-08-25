import typer #用于创建命令行界面
from typing import Optional, List # 从typing模块导入类型提示，Optional表示可选参数，List表示列表类型
from database import engine #导入数据库引擎
from generator.code_generator import CodeGenerator

app = typer.Typer()


@app.command()
def gen(tableName: Optional[str] = typer.Option(None, "-t", "--tablename", help="表名称(多个表用英文逗号分隔)")):
    """
    生成代码
    """

    codeGenerator: CodeGenerator = CodeGenerator(engine=engine)
    codeGenerator.init_config()

    # 处理多个表名
    if tableName:
        table_names: List[str] = tableName.split(",")
        for table_name in table_names:
            table_name = table_name.strip()  # 去除空格
            codeGenerator.build_table(table_name)
            codeGenerator.gen_code()
    else:
        codeGenerator.build_table(None)
        codeGenerator.gen_code()


@app.command()
def show(tableName: Optional[str] = typer.Option(None, "-t", "--tablename", help="表名称(多个表用英文逗号分隔)")):
    """
    显示表结构
    """

    codeGenerator: CodeGenerator = CodeGenerator(engine=engine)

    # 处理多个表名
    if tableName:
        table_names: List[str] = tableName.split(",")
        for table_name in table_names:
            table_name = table_name.strip()  # 去除空格
            codeGenerator.build_table(table_name)
            codeGenerator.print_table()
    else:
        codeGenerator.build_table(None)
        codeGenerator.print_table()


if __name__ == "__main__":
    app()
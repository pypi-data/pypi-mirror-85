# Utils for Researcher (适合于研究者的工具类)

> 以简化操作为宗旨，服务没有编程经验的研究者

## 安装

```
pip install Utils4R
```

## 基本介绍

* `console`：输出格式化信息到控制台

* `random`：生成散布于期望值附近的随机数

#### io (I/O 输入/输出)

* `io.load_string`：读取文件所有内容为字符串

* `io.write_string`：将字符串写入到文件中

* `io.load_json`：读取文件所有内容为Json格式对象

* `io.write_json`：将Json格式数据写入到文件中

#### db (数据库)

* `MySQL`：MySQL读写工具类
  * `MySQL()`(`__init__()`)：创建MySQL读写实例
  * `create()`：创建表
  * `insert()`：执行INSERT INTO语句
  * `select()`：执行SELECT语句

#### abc (抽象基类)

* `SingleSpider`：简单单线程爬虫的抽象基类





版本：0.0.5（当前版本暂未正式发布，下一个版本不一定会考虑兼容当前版本）

## 作者

ChangXing 长行

## 支持

如果觉得这个项目可以帮到您，欢迎星标哦。
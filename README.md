# JWT Forge UI

一个基于 Python + Tkinter 的 JWT（JSON Web Token）图形化工具，集 **解析**、**生成**、**密钥爆破** 于一体，无需命令行即可完成常见的 JWT 调试与安全分析工作。

> 适用于接口调试、Token 结构分析、以及授权测试场景下的弱密钥检测。

---

## 功能特性

### 解析 JWT
- 自动拆分并解码 `Header`、`Payload`、`Signature` 三段
- 以格式化的 JSON 展示头部与载荷内容（支持中文，`ensure_ascii=False`）
- 一键将解析结果「复制到生成区」，方便修改后重新签名

### 生成 JWT
- 支持 8 种签名算法：`HS256 / HS384 / HS512`、`RS256 / RS384 / RS512`、`ES256 / ES384 / ES512`
- 自定义 `Header` 与 `Payload` 的 JSON 内容
- 从解析区导入头部时自动匹配对应算法
- 生成结果支持一键复制到剪贴板

### 爆破密钥
- 针对 `HS256 / HS384 / HS512`（HMAC 系列）进行字典爆破
- 支持选择自定义字典文件（每行一个候选密钥）
- 后台线程执行，实时进度条 + 状态提示，可随时中断
- 命中后直接输出正确密钥

---

## 环境要求

- Python 3.7+
- Tkinter（Python 官方发行版自带；Linux 下可能需要 `apt install python3-tk`）
- `PyJWT`

---

## 安装

```bash
git clone https://github.com/LZ-jun/JWT-forge-ui.git
cd JWT-forge-ui
pip install -r requirements.txt
```

---

## 使用方法

```bash
python JWT签名.py
```

程序启动后为三个标签页，对应上述三项功能：

| 标签页 | 说明 |
| --- | --- |
| **解析JWT** | 粘贴完整 JWT 字符串，点击「解析」查看头部、载荷与签名 |
| **生成JWT** | 选择算法、填写密钥与 Header/Payload JSON，点击「生成JWT」 |
| **爆破密钥** | 粘贴目标 JWT、选择字典文件，点击「开始爆破」 |

**爆破密钥示例字典**（`dict.txt`）：

```
secret
password
123456
your-256-bit-secret
```

> 提示：爆破仅对 HMAC 系列算法有效。非对称算法（RS/ES）无法通过字典直接还原私钥。

---

## 项目结构

```
JWT-forge-ui/
├── JWT签名.py        # 主程序（Tkinter GUI）
├── requirements.txt  # 依赖声明（PyJWT）
├── .gitignore
└── README.md
```

---

## 依赖

`PyJWT` 是唯一第三方依赖，直接通过 pip 安装即可。解析与爆破逻辑依赖其 `jwt.decode` 的签名校验能力。

---

## 免责声明

本工具仅用于**授权的安全测试与自有系统调试**。请勿将爆破功能用于未经许可的系统或他人资产。使用者需自行承担因不当使用产生的一切法律责任。

---

## License

MIT

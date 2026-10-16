import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import jwt
import json
from datetime import datetime
import base64
import threading
import time

class JWTools:
    def __init__(self, root):
        self.root = root
        self.root.title("JWT解析与生成工具")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # 线程控制
        self.brute_running = False
        self.brute_stop = False
        
        # 设置字体
        self.font = ('Microsoft YaHei', 10)
        
        # 签名算法列表
        self.algorithms = [
            "HS256", "HS384", "HS512",
            "RS256", "RS384", "RS512",
            "ES256", "ES384", "ES512"
        ]
        
        # 创建标签页
        self.tab_control = ttk.Notebook(root)
        
        # 解析标签页
        self.tab_parse = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_parse, text="解析JWT")
        
        # 生成标签页
        self.tab_generate = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_generate, text="生成JWT")
        
        # 爆破标签页
        self.tab_brute = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_brute, text="爆破密钥")
        
        self.tab_control.pack(expand=1, fill="both", padx=10, pady=10)
        
        # 初始化标签页
        self.init_parse_tab()
        self.init_generate_tab()
        self.init_brute_tab()

    def init_parse_tab(self):
        # 输入框
        ttk.Label(self.tab_parse, text="请输入JWT:", font=self.font).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.jwt_input = scrolledtext.ScrolledText(self.tab_parse, width=80, height=3, font=self.font)
        self.jwt_input.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="we")
        
        # 按钮区
        btn_frame = ttk.Frame(self.tab_parse)
        btn_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        ttk.Button(btn_frame, text="解析", command=self.parse_jwt).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="复制到生成区", command=self.copy_to_generate).pack(side=tk.LEFT, padx=5)
        
        # 头部区域
        ttk.Label(self.tab_parse, text="头部 (Header):", font=self.font).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.header_text = scrolledtext.ScrolledText(self.tab_parse, width=80, height=6, font=self.font)
        self.header_text.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="we")
        
        # 载荷区域
        ttk.Label(self.tab_parse, text="载荷 (Payload):", font=self.font).grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.payload_text = scrolledtext.ScrolledText(self.tab_parse, width=80, height=10, font=self.font)
        self.payload_text.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="we")
        
        # 签名区域
        ttk.Label(self.tab_parse, text="签名 (Signature):", font=self.font).grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.signature_text = scrolledtext.ScrolledText(self.tab_parse, width=80, height=3, font=self.font)
        self.signature_text.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="we")
        
        # 设置权重
        self.tab_parse.grid_columnconfigure(0, weight=1)
        self.tab_parse.grid_rowconfigure(4, weight=1)
        self.tab_parse.grid_rowconfigure(6, weight=1)
        self.tab_parse.grid_rowconfigure(8, weight=1)

    def init_generate_tab(self):
        # 算法选择
        ttk.Label(self.tab_generate, text="签名算法:", font=self.font).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.alg_var = tk.StringVar(value="HS256")
        self.alg_combobox = ttk.Combobox(self.tab_generate, textvariable=self.alg_var, values=self.algorithms, state="readonly", font=self.font)
        self.alg_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # 密钥输入
        ttk.Label(self.tab_generate, text="密钥 (Secret/Key):", font=self.font).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.secret_input = ttk.Entry(self.tab_generate, show="*", width=50, font=self.font)
        self.secret_input.grid(row=1, column=1, padx=10, pady=5, sticky="we")
        self.secret_input.insert(0, "secret")  # 默认密钥
        
        # 头部输入
        ttk.Label(self.tab_generate, text="头部 (Header JSON):", font=self.font).grid(row=2, column=0, padx=10, pady=5, sticky="nw")
        self.gen_header_text = scrolledtext.ScrolledText(self.tab_generate, width=60, height=5, font=self.font)
        self.gen_header_text.grid(row=2, column=1, padx=10, pady=5, sticky="we")
        self.gen_header_text.insert(tk.END, '{"alg": "HS256", "typ": "JWT"}')
        
        # 载荷输入
        ttk.Label(self.tab_generate, text="载荷 (Payload JSON):", font=self.font).grid(row=3, column=0, padx=10, pady=5, sticky="nw")
        self.gen_payload_text = scrolledtext.ScrolledText(self.tab_generate, width=60, height=10, font=self.font)
        self.gen_payload_text.grid(row=3, column=1, padx=10, pady=5, sticky="we")
        # 默认载荷
        default_payload = {
            "sub": "1234567890",
            "name": "Jeanne",
            "iat": int(datetime.now().timestamp())
        }
        self.gen_payload_text.insert(tk.END, json.dumps(default_payload, indent=2))
        
        # 生成按钮
        ttk.Button(self.tab_generate, text="生成JWT", command=self.generate_jwt).grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        
        # 结果区域
        ttk.Label(self.tab_generate, text="生成的JWT:", font=self.font).grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.result_jwt = scrolledtext.ScrolledText(self.tab_generate, width=80, height=3, font=self.font)
        self.result_jwt.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="we")
        
        # 复制按钮
        ttk.Button(self.tab_generate, text="复制到剪贴板", command=self.copy_to_clipboard).grid(row=7, column=0, columnspan=2, padx=10, pady=5)
        
        # 设置权重
        self.tab_generate.grid_columnconfigure(1, weight=1)
        self.tab_generate.grid_rowconfigure(3, weight=1)
        self.tab_generate.grid_rowconfigure(6, weight=1)

    def init_brute_tab(self):
        # JWT输入
        ttk.Label(self.tab_brute, text="目标JWT:", font=self.font).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.brute_jwt_input = scrolledtext.ScrolledText(self.tab_brute, width=70, height=3, font=self.font)
        self.brute_jwt_input.grid(row=0, column=1, padx=10, pady=5, sticky="we")
        
        # 字典文件选择
        ttk.Label(self.tab_brute, text="字典文件:", font=self.font).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.dict_path = tk.StringVar()
        ttk.Entry(self.tab_brute, textvariable=self.dict_path, width=50, font=self.font).grid(row=1, column=1, padx=10, pady=5, sticky="we")
        ttk.Button(self.tab_brute, text="浏览", command=self.select_dict_file).grid(row=1, column=2, padx=5, pady=5)
        
        # 状态和结果
        ttk.Label(self.tab_brute, text="爆破状态:", font=self.font).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.brute_status = tk.StringVar(value="未开始")
        ttk.Label(self.tab_brute, textvariable=self.brute_status, font=self.font).grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        ttk.Label(self.tab_brute, text="进度:", font=self.font).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.tab_brute, variable=self.progress_var, length=400)
        self.progress_bar.grid(row=3, column=1, padx=10, pady=5, sticky="we")
        
        ttk.Label(self.tab_brute, text="结果:", font=self.font).grid(row=4, column=0, padx=10, pady=5, sticky="nw")
        self.brute_result = scrolledtext.ScrolledText(self.tab_brute, width=70, height=10, font=self.font)
        self.brute_result.grid(row=4, column=1, padx=10, pady=5, sticky="we")
        
        # 按钮
        btn_frame = ttk.Frame(self.tab_brute)
        btn_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        ttk.Button(btn_frame, text="开始爆破", command=self.start_brute).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="停止", command=self.stop_brute).pack(side=tk.LEFT, padx=5)
        
        # 提示
        ttk.Label(
            self.tab_brute, 
            text="提示：仅支持HS256/HS384/HS512算法，需准备包含可能密钥的字典文件（一行一个密钥）", 
            font=('Microsoft YaHei', 9), 
            foreground="gray"
        ).grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        # 设置权重
        self.tab_brute.grid_columnconfigure(1, weight=1)
        self.tab_brute.grid_rowconfigure(4, weight=1)

    def parse_jwt(self):
        jwt_str = self.jwt_input.get("1.0", tk.END).strip()
        if not jwt_str:
            messagebox.showwarning("警告", "请输入JWT字符串")
            return
            
        parts = jwt_str.split('.')
        if len(parts) != 3:
            messagebox.showerror("错误", "无效的JWT格式")
            return
            
        try:
            # 解析头部
            header_b64 = parts[0]
            header_b64 += '=' * ((4 - len(header_b64) % 4) % 4)
            header_json = base64.urlsafe_b64decode(header_b64).decode('utf-8')
            header = json.loads(header_json)
            self.header_text.delete("1.0", tk.END)
            self.header_text.insert(tk.END, json.dumps(header, indent=2, ensure_ascii=False))
            
            # 解析载荷
            payload_b64 = parts[1]
            payload_b64 += '=' * ((4 - len(payload_b64) % 4) % 4)
            payload_json = base64.urlsafe_b64decode(payload_b64).decode('utf-8')
            payload = json.loads(payload_json)
            self.payload_text.delete("1.0", tk.END)
            self.payload_text.insert(tk.END, json.dumps(payload, indent=2, ensure_ascii=False))
            
            # 显示签名
            self.signature_text.delete("1.0", tk.END)
            self.signature_text.insert(tk.END, parts[2])
            
        except Exception as e:
            messagebox.showerror("解析错误", f"解析失败: {str(e)}")

    def copy_to_generate(self):
        """将解析结果复制到生成区"""
        header_str = self.header_text.get("1.0", tk.END).strip()
        payload_str = self.payload_text.get("1.0", tk.END).strip()
        
        if not header_str or not payload_str:
            messagebox.showwarning("警告", "请先解析有效的JWT")
            return
            
        try:
            # 复制头部
            self.gen_header_text.delete("1.0", tk.END)
            self.gen_header_text.insert(tk.END, header_str)
            
            # 复制载荷
            self.gen_payload_text.delete("1.0", tk.END)
            self.gen_payload_text.insert(tk.END, payload_str)
            
            # 自动选择算法
            header = json.loads(header_str)
            if "alg" in header and header["alg"] in self.algorithms:
                self.alg_var.set(header["alg"])
                
            messagebox.showinfo("提示", "已复制到生成区")
        except Exception as e:
            messagebox.showerror("错误", f"复制失败: {str(e)}")

    def generate_jwt(self):
        try:
            algorithm = self.alg_var.get()
            secret = self.secret_input.get().strip()
            if not secret:
                messagebox.showwarning("警告", "请输入密钥")
                return
                
            header_str = self.gen_header_text.get("1.0", tk.END).strip()
            if not header_str:
                messagebox.showwarning("警告", "请输入头部JSON")
                return
            header = json.loads(header_str)
            
            payload_str = self.gen_payload_text.get("1.0", tk.END).strip()
            if not payload_str:
                messagebox.showwarning("警告", "请输入载荷JSON")
                return
            payload = json.loads(payload_str)
            
            # 生成JWT
            token = jwt.encode(
                payload,
                secret,
                algorithm=algorithm,
                headers=header
            )
            
            self.result_jwt.delete("1.0", tk.END)
            self.result_jwt.insert(tk.END, token)
            
        except json.JSONDecodeError:
            messagebox.showerror("错误", "JSON格式不正确")
        except Exception as e:
            messagebox.showerror("生成错误", f"生成失败: {str(e)}")

    def copy_to_clipboard(self):
        jwt_str = self.result_jwt.get("1.0", tk.END).strip()
        if jwt_str:
            self.root.clipboard_clear()
            self.root.clipboard_append(jwt_str)
            messagebox.showinfo("提示", "已复制到剪贴板")
        else:
            messagebox.showwarning("警告", "没有可复制的JWT")

    def select_dict_file(self):
        """选择字典文件"""
        file_path = filedialog.askopenfilename(
            title="选择字典文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if file_path:
            self.dict_path.set(file_path)

    def start_brute(self):
        """开始爆破密钥（在新线程中运行）"""
        if self.brute_running:
            messagebox.showwarning("警告", "爆破正在进行中")
            return
            
        jwt_str = self.brute_jwt_input.get("1.0", tk.END).strip()
        dict_path = self.dict_path.get().strip()
        
        if not jwt_str or not dict_path:
            messagebox.showwarning("警告", "请输入JWT和字典文件路径")
            return
            
        # 检查JWT格式
        parts = jwt_str.split('.')
        if len(parts) != 3:
            messagebox.showerror("错误", "无效的JWT格式")
            return
            
        # 解析算法
        try:
            header_b64 = parts[0]
            header_b64 += '=' * ((4 - len(header_b64) % 4) % 4)
            header = json.loads(base64.urlsafe_b64decode(header_b64).decode('utf-8'))
            algorithm = header.get("alg", "")
            if not algorithm.startswith("HS"):
                messagebox.showerror("错误", "仅支持HS256/HS384/HS512算法")
                return
        except:
            messagebox.showerror("错误", "无法解析JWT头部")
            return
            
        # 启动爆破线程
        self.brute_stop = False
        self.brute_running = True
        self.brute_status.set("正在爆破...")
        self.brute_result.delete("1.0", tk.END)
        self.progress_var.set(0)
        
        threading.Thread(
            target=self.brute_force,
            args=(jwt_str, dict_path, algorithm),
            daemon=True
        ).start()

    def stop_brute(self):
        """停止爆破"""
        if self.brute_running:
            self.brute_stop = True
            self.brute_status.set("正在停止...")

    def brute_force(self, jwt_str, dict_path, algorithm):
        """爆破密钥核心逻辑"""
        try:
            # 统计字典总行数
            total_lines = 0
            with open(dict_path, 'r', encoding='utf-8', errors='ignore') as f:
                for _ in f:
                    total_lines += 1
            
            if total_lines == 0:
                self.brute_status.set("字典文件为空")
                self.brute_running = False
                return
                
            # 逐行尝试密钥
            current_line = 0
            with open(dict_path, 'r', encoding='utf-8', errors='ignore') as f:
                for secret in f:
                    if self.brute_stop:
                        self.brute_status.set("已停止")
                        self.brute_running = False
                        return
                        
                    secret = secret.strip()
                    if not secret:
                        current_line += 1
                        continue
                        
                    try:
                        # 验证密钥是否正确
                        jwt.decode(
                            jwt_str,
                            secret,
                            algorithms=[algorithm],
                            options={"verify_signature": True}
                        )
                        # 找到密钥
                        self.brute_result.insert(tk.END, f"找到密钥: {secret}\n")
                        self.brute_status.set("爆破成功")
                        self.progress_var.set(100)
                        self.brute_running = False
                        return
                    except:
                        pass
                        
                    current_line += 1
                    # 更新进度
                    progress = (current_line / total_lines) * 100
                    self.progress_var.set(progress)
                    # 每100行更新一次状态（避免频繁刷新UI）
                    if current_line % 100 == 0:
                        self.brute_status.set(f"正在爆破... (已尝试 {current_line}/{total_lines})")
            
            # 完成但未找到
            self.brute_status.set("爆破完成，未找到密钥")
            self.progress_var.set(100)
            
        except Exception as e:
            self.brute_status.set(f"错误: {str(e)}")
        finally:
            self.brute_running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = JWTools(root)
    root.mainloop()
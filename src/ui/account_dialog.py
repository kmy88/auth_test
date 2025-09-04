import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict

class AccountDialog:
    def __init__(self, parent, title="계정 정보", initial_data: Optional[Dict] = None):
        self.result = None
        
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry("400x250")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        self.window.geometry(f"+{parent.winfo_rootx() + 50}+{parent.winfo_rooty() + 50}")
        
        self.initial_data = initial_data or {}
        self.setup_ui()
        
        self.window.wait_window()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="Alias:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.alias_var = tk.StringVar(value=self.initial_data.get('alias', ''))
        self.alias_entry = ttk.Entry(main_frame, textvariable=self.alias_var, width=30)
        self.alias_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5, padx=(10, 0))
        
        if 'alias' in self.initial_data:
            self.alias_entry.config(state='readonly')
        
        ttk.Label(main_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_var = tk.StringVar(value=self.initial_data.get('username', ''))
        self.username_entry = ttk.Entry(main_frame, textvariable=self.username_var, width=30)
        self.username_entry.grid(row=1, column=1, sticky=tk.W+tk.E, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(main_frame, textvariable=self.password_var, show="*", width=30)
        self.password_entry.grid(row=2, column=1, sticky=tk.W+tk.E, pady=5, padx=(10, 0))
        
        if 'alias' in self.initial_data:
            ttk.Label(main_frame, text="(비워두면 기존 비밀번호 유지)", font=("Arial", 8)).grid(
                row=3, column=1, sticky=tk.W, pady=(0, 10), padx=(10, 0)
            )
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="저장", command=self.save).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="취소", command=self.cancel).pack(side=tk.LEFT)
        
        main_frame.columnconfigure(1, weight=1)
        
        if 'alias' not in self.initial_data:
            self.alias_entry.focus()
        else:
            self.username_entry.focus()
        
        self.window.bind('<Return>', lambda e: self.save())
        self.window.bind('<Escape>', lambda e: self.cancel())
    
    def save(self):
        alias = self.alias_var.get().strip()
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not alias:
            messagebox.showerror("오류", "Alias를 입력하세요.")
            self.alias_entry.focus()
            return
        
        if not username:
            messagebox.showerror("오류", "Username을 입력하세요.")
            self.username_entry.focus()
            return
        
        if 'alias' not in self.initial_data and not password:
            messagebox.showerror("오류", "Password를 입력하세요.")
            self.password_entry.focus()
            return
        
        self.result = {
            'alias': alias,
            'username': username,
            'password': password
        }
        
        self.window.destroy()
    
    def cancel(self):
        self.window.destroy()
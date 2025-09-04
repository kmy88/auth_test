import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional

class ApiKeyManagerDialog:
    def __init__(self, parent, auth_service):
        self.auth_service = auth_service
        self.result = None
        
        self.window = tk.Toplevel(parent)
        self.window.title("API 키 관리")
        self.window.geometry("700x400")
        self.window.resizable(True, True)
        self.window.transient(parent)
        self.window.grab_set()
        
        self.window.geometry(f"+{parent.winfo_rootx() + 50}+{parent.winfo_rooty() + 50}")
        
        self.setup_ui()
        self.load_api_keys()
        
        self.window.wait_window()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title_label = ttk.Label(main_frame, text="API 키 관리", font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(button_frame, text="새 키 생성", command=self.create_key).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="키 복사", command=self.copy_key).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="활성화", command=self.activate_key).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="비활성화", command=self.deactivate_key).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="삭제", command=self.delete_key).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="새로고침", command=self.load_api_keys).pack(side=tk.RIGHT)
        
        columns = ("key_name", "api_key", "is_active", "created_at", "last_used")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=12)
        
        self.tree.heading("key_name", text="키 이름")
        self.tree.heading("api_key", text="API 키")
        self.tree.heading("is_active", text="상태")
        self.tree.heading("created_at", text="생성일")
        self.tree.heading("last_used", text="마지막 사용")
        
        self.tree.column("key_name", width=120)
        self.tree.column("api_key", width=200)
        self.tree.column("is_active", width=80)
        self.tree.column("created_at", width=120)
        self.tree.column("last_used", width=120)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        close_frame = ttk.Frame(main_frame)
        close_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(close_frame, text="닫기", command=self.close).pack(side=tk.RIGHT)
    
    def load_api_keys(self):
        try:
            api_keys = self.auth_service.list_api_keys()
            self.tree.delete(*self.tree.get_children())
            
            for key in api_keys:
                masked_key = key.api_key[:12] + "*" * (len(key.api_key) - 16) + key.api_key[-4:]
                last_used = key.last_used.strftime("%Y-%m-%d %H:%M") if key.last_used else "사용 안함"
                
                self.tree.insert("", tk.END, values=(
                    key.key_name,
                    masked_key,
                    "활성" if key.is_active else "비활성",
                    key.created_at.strftime("%Y-%m-%d %H:%M"),
                    last_used
                ))
        except Exception as e:
            messagebox.showerror("오류", f"API 키 목록 로드 실패: {str(e)}")
    
    def create_key(self):
        from tkinter import simpledialog
        key_name = simpledialog.askstring("API 키 생성", "API 키 이름을 입력하세요:")
        if key_name:
            try:
                from ..models.account import ApiKeyCreate
                key_data = ApiKeyCreate(key_name=key_name)
                result = self.auth_service.create_api_key(key_data)
                self.load_api_keys()
                
                self.show_api_key(result.api_key)
            except Exception as e:
                messagebox.showerror("오류", f"API 키 생성 실패: {str(e)}")
    
    def show_api_key(self, api_key):
        dialog = tk.Toplevel(self.window)
        dialog.title("생성된 API 키")
        dialog.geometry("500x200")
        dialog.resizable(False, False)
        dialog.transient(self.window)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="API 키가 생성되었습니다!", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        ttk.Label(main_frame, text="이 키를 안전한 곳에 저장하세요. 다시 표시되지 않습니다.").pack(pady=(0, 10))
        
        key_frame = ttk.Frame(main_frame)
        key_frame.pack(fill=tk.X, pady=(0, 10))
        
        key_text = tk.Text(key_frame, height=3, width=60)
        key_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        key_text.insert(tk.END, api_key)
        key_text.config(state=tk.DISABLED)
        
        ttk.Button(key_frame, text="복사", command=lambda: self.copy_to_clipboard(api_key)).pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Button(main_frame, text="확인", command=dialog.destroy).pack(pady=10)
        
        dialog.geometry(f"+{self.window.winfo_rootx() + 50}+{self.window.winfo_rooty() + 50}")
    
    def copy_to_clipboard(self, text):
        self.window.clipboard_clear()
        self.window.clipboard_append(text)
        messagebox.showinfo("완료", "클립보드에 복사되었습니다.")
    
    def copy_key(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("경고", "복사할 API 키를 선택하세요.")
            return
        
        messagebox.showinfo("안내", "보안상 마스킹된 키는 복사할 수 없습니다. 새로 생성한 키만 복사 가능합니다.")
    
    def activate_key(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("경고", "활성화할 API 키를 선택하세요.")
            return
        
        key_name = self.tree.item(selection[0])['values'][0]
        try:
            self.auth_service.activate_api_key(key_name)
            self.load_api_keys()
            messagebox.showinfo("성공", f"API 키 '{key_name}'이 활성화되었습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"API 키 활성화 실패: {str(e)}")
    
    def deactivate_key(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("경고", "비활성화할 API 키를 선택하세요.")
            return
        
        key_name = self.tree.item(selection[0])['values'][0]
        try:
            self.auth_service.deactivate_api_key(key_name)
            self.load_api_keys()
            messagebox.showinfo("성공", f"API 키 '{key_name}'이 비활성화되었습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"API 키 비활성화 실패: {str(e)}")
    
    def delete_key(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("경고", "삭제할 API 키를 선택하세요.")
            return
        
        key_name = self.tree.item(selection[0])['values'][0]
        if messagebox.askyesno("확인", f"API 키 '{key_name}'을 정말 삭제하시겠습니까?"):
            try:
                self.auth_service.delete_api_key(key_name)
                self.load_api_keys()
                messagebox.showinfo("성공", f"API 키 '{key_name}'이 삭제되었습니다.")
            except Exception as e:
                messagebox.showerror("오류", f"API 키 삭제 실패: {str(e)}")
    
    def close(self):
        self.window.destroy()
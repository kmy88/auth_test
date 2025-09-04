import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import requests
from typing import List
from ..services.account_manager import AccountManager
from ..services.auth import AuthService
from ..services.encryption import EncryptionService
from ..models.database import DatabaseManager
from ..models.account import AccountCreate, AccountUpdate, ApiKeyCreate
from .account_dialog import AccountDialog
from .api_key_manager import ApiKeyManagerDialog

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("개인계정 관리 시스템")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.setup_services()
        self.setup_ui()
        self.load_data()
    
    def setup_services(self):
        self.db_manager = DatabaseManager()
        self.encryption_service = EncryptionService()
        self.account_manager = AccountManager(self.db_manager, self.encryption_service)
        self.auth_service = AuthService(self.db_manager)
        self.full_api_keys = {}  # API 키 전체 텍스트 저장용
    
    def setup_ui(self):
        self.setup_menu()
        self.setup_main_frame()
        self.setup_account_frame()
        self.setup_api_key_frame()
    
    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="파일", menu=file_menu)
        file_menu.add_command(label="새로고침", command=self.refresh_data)
        file_menu.add_separator()
        file_menu.add_command(label="종료", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="도움말", menu=help_menu)
        help_menu.add_command(label="정보", command=self.show_about)
    
    def setup_main_frame(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        self.account_frame = ttk.Frame(notebook)
        self.api_key_frame = ttk.Frame(notebook)
        
        notebook.add(self.account_frame, text="계정 관리")
        notebook.add(self.api_key_frame, text="API 키 관리")
    
    def setup_account_frame(self):
        title_label = ttk.Label(self.account_frame, text="계정 목록", font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))
        
        button_frame = ttk.Frame(self.account_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(button_frame, text="새 계정 추가", command=self.add_account).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="계정 수정", command=self.edit_account).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="계정 삭제", command=self.delete_account).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="새로고침", command=self.refresh_accounts).pack(side=tk.RIGHT)
        
        columns = ("alias", "created_at", "updated_at")
        self.account_tree = ttk.Treeview(self.account_frame, columns=columns, show="headings", height=15)
        
        self.account_tree.heading("alias", text="Alias")
        self.account_tree.heading("created_at", text="생성일")
        self.account_tree.heading("updated_at", text="수정일")
        
        self.account_tree.column("alias", width=200)
        self.account_tree.column("created_at", width=150)
        self.account_tree.column("updated_at", width=150)
        
        scrollbar_accounts = ttk.Scrollbar(self.account_frame, orient=tk.VERTICAL, command=self.account_tree.yview)
        self.account_tree.configure(yscrollcommand=scrollbar_accounts.set)
        
        self.account_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_accounts.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_api_key_frame(self):
        title_label = ttk.Label(self.api_key_frame, text="API 키 목록", font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))
        
        button_frame = ttk.Frame(self.api_key_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(button_frame, text="새 API 키 생성", command=self.create_api_key).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="키 복사", command=self.copy_api_key).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="키 비활성화", command=self.deactivate_api_key).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="키 활성화", command=self.activate_api_key).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="키 삭제", command=self.delete_api_key).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="새로고침", command=self.refresh_api_keys).pack(side=tk.RIGHT)
        
        columns = ("key_name", "api_key", "is_active", "created_at")
        self.api_key_tree = ttk.Treeview(self.api_key_frame, columns=columns, show="headings", height=15)
        
        self.api_key_tree.heading("key_name", text="키 이름")
        self.api_key_tree.heading("api_key", text="API 키")
        self.api_key_tree.heading("is_active", text="상태")
        self.api_key_tree.heading("created_at", text="생성일")
        
        self.api_key_tree.column("key_name", width=150)
        self.api_key_tree.column("api_key", width=300)
        self.api_key_tree.column("is_active", width=80)
        self.api_key_tree.column("created_at", width=150)
        
        scrollbar_keys = ttk.Scrollbar(self.api_key_frame, orient=tk.VERTICAL, command=self.api_key_tree.yview)
        self.api_key_tree.configure(yscrollcommand=scrollbar_keys.set)
        
        self.api_key_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_keys.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_data(self):
        self.refresh_accounts()
        self.refresh_api_keys()
    
    def refresh_data(self):
        self.load_data()
    
    def refresh_accounts(self):
        try:
            accounts = self.account_manager.list_accounts()
            self.account_tree.delete(*self.account_tree.get_children())
            for account in accounts:
                self.account_tree.insert("", tk.END, values=(
                    account.alias,
                    account.created_at.strftime("%Y-%m-%d %H:%M"),
                    account.updated_at.strftime("%Y-%m-%d %H:%M")
                ))
        except Exception as e:
            messagebox.showerror("오류", f"계정 목록 로드 실패: {str(e)}")
    
    def refresh_api_keys(self):
        try:
            api_keys = self.auth_service.list_api_keys()
            self.api_key_tree.delete(*self.api_key_tree.get_children())
            self.full_api_keys = {}  # 전체 API 키를 저장할 딕셔너리
            
            for key in api_keys:
                self.full_api_keys[key.key_name] = key.api_key  # 전체 키 저장
                masked_key = key.api_key[:8] + "*" * (len(key.api_key) - 12) + key.api_key[-4:]
                self.api_key_tree.insert("", tk.END, values=(
                    key.key_name,
                    masked_key,
                    "활성" if key.is_active else "비활성",
                    key.created_at.strftime("%Y-%m-%d %H:%M")
                ))
        except Exception as e:
            messagebox.showerror("오류", f"API 키 목록 로드 실패: {str(e)}")
    
    def add_account(self):
        dialog = AccountDialog(self.root, title="새 계정 추가")
        if dialog.result:
            try:
                account_data = AccountCreate(
                    alias=dialog.result['alias'],
                    username=dialog.result['username'],
                    password=dialog.result['password']
                )
                self.account_manager.create_account(account_data)
                self.refresh_accounts()
                messagebox.showinfo("성공", f"계정 '{dialog.result['alias']}'이 추가되었습니다.")
            except Exception as e:
                messagebox.showerror("오류", f"계정 추가 실패: {str(e)}")
    
    def edit_account(self):
        selection = self.account_tree.selection()
        if not selection:
            messagebox.showwarning("경고", "수정할 계정을 선택하세요.")
            return
        
        alias = self.account_tree.item(selection[0])['values'][0]
        account = self.account_manager.get_account(alias)
        if not account:
            messagebox.showerror("오류", "계정을 찾을 수 없습니다.")
            return
        
        dialog = AccountDialog(self.root, title=f"계정 수정 - {alias}", 
                              initial_data={'alias': alias, 'username': account.username})
        if dialog.result:
            try:
                account_data = AccountUpdate(
                    username=dialog.result['username'],
                    password=dialog.result['password'] if dialog.result['password'] else None
                )
                self.account_manager.update_account(alias, account_data)
                self.refresh_accounts()
                messagebox.showinfo("성공", f"계정 '{alias}'이 수정되었습니다.")
            except Exception as e:
                messagebox.showerror("오류", f"계정 수정 실패: {str(e)}")
    
    def delete_account(self):
        selection = self.account_tree.selection()
        if not selection:
            messagebox.showwarning("경고", "삭제할 계정을 선택하세요.")
            return
        
        alias = self.account_tree.item(selection[0])['values'][0]
        if messagebox.askyesno("확인", f"계정 '{alias}'을 정말 삭제하시겠습니까?"):
            try:
                self.account_manager.delete_account(alias)
                self.refresh_accounts()
                messagebox.showinfo("성공", f"계정 '{alias}'이 삭제되었습니다.")
            except Exception as e:
                messagebox.showerror("오류", f"계정 삭제 실패: {str(e)}")
    
    def create_api_key(self):
        key_name = simpledialog.askstring("API 키 생성", "API 키 이름을 입력하세요:")
        if key_name:
            try:
                key_data = ApiKeyCreate(key_name=key_name)
                result = self.auth_service.create_api_key(key_data)
                self.refresh_api_keys()
                
                self.show_api_key_dialog(result.api_key)
            except Exception as e:
                messagebox.showerror("오류", f"API 키 생성 실패: {str(e)}")
    
    def show_api_key_dialog(self, api_key):
        dialog = tk.Toplevel(self.root)
        dialog.title("생성된 API 키")
        dialog.geometry("600x250")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text="API 키가 생성되었습니다!", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        ttk.Label(main_frame, text="이 키를 안전한 곳에 저장하세요. 다시 표시되지 않습니다.", 
                 foreground="red").pack(pady=(0, 10))
        
        key_frame = ttk.Frame(main_frame)
        key_frame.pack(fill=tk.X, pady=(0, 10))
        
        key_text = tk.Text(key_frame, height=3, width=70, wrap=tk.WORD)
        key_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        key_text.insert(tk.END, api_key)
        key_text.config(state=tk.DISABLED)
        
        copy_button = ttk.Button(key_frame, text="복사", command=lambda: self.copy_to_clipboard(api_key, "API 키가 클립보드에 복사되었습니다!"))
        copy_button.pack(side=tk.RIGHT)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="확인", command=dialog.destroy).pack(side=tk.RIGHT)
        
        dialog.geometry(f"+{self.root.winfo_rootx() + 100}+{self.root.winfo_rooty() + 100}")
    
    def copy_api_key(self):
        selection = self.api_key_tree.selection()
        if not selection:
            messagebox.showwarning("경고", "복사할 API 키를 선택하세요.")
            return
        
        key_name = self.api_key_tree.item(selection[0])['values'][0]
        
        if hasattr(self, 'full_api_keys') and key_name in self.full_api_keys:
            api_key = self.full_api_keys[key_name]
            self.copy_to_clipboard(api_key, f"API 키 '{key_name}'이 클립보드에 복사되었습니다!")
        else:
            messagebox.showwarning("안내", "보안상의 이유로 마스킹된 키는 복사할 수 없습니다.\n새로 생성된 키만 즉시 복사 가능합니다.")
    
    def copy_to_clipboard(self, text, success_message="클립보드에 복사되었습니다."):
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.root.update()  # 클립보드 업데이트 확인
            messagebox.showinfo("완료", success_message)
        except Exception as e:
            messagebox.showerror("오류", f"클립보드 복사 실패: {str(e)}")
    
    def deactivate_api_key(self):
        selection = self.api_key_tree.selection()
        if not selection:
            messagebox.showwarning("경고", "비활성화할 API 키를 선택하세요.")
            return
        
        key_name = self.api_key_tree.item(selection[0])['values'][0]
        try:
            self.auth_service.deactivate_api_key(key_name)
            self.refresh_api_keys()
            messagebox.showinfo("성공", f"API 키 '{key_name}'이 비활성화되었습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"API 키 비활성화 실패: {str(e)}")
    
    def activate_api_key(self):
        selection = self.api_key_tree.selection()
        if not selection:
            messagebox.showwarning("경고", "활성화할 API 키를 선택하세요.")
            return
        
        key_name = self.api_key_tree.item(selection[0])['values'][0]
        try:
            self.auth_service.activate_api_key(key_name)
            self.refresh_api_keys()
            messagebox.showinfo("성공", f"API 키 '{key_name}'이 활성화되었습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"API 키 활성화 실패: {str(e)}")
    
    def delete_api_key(self):
        selection = self.api_key_tree.selection()
        if not selection:
            messagebox.showwarning("경고", "삭제할 API 키를 선택하세요.")
            return
        
        key_name = self.api_key_tree.item(selection[0])['values'][0]
        if messagebox.askyesno("확인", f"API 키 '{key_name}'을 정말 삭제하시겠습니까?"):
            try:
                self.auth_service.delete_api_key(key_name)
                self.refresh_api_keys()
                messagebox.showinfo("성공", f"API 키 '{key_name}'이 삭제되었습니다.")
            except Exception as e:
                messagebox.showerror("오류", f"API 키 삭제 실패: {str(e)}")
    
    def show_about(self):
        messagebox.showinfo("정보", "개인계정 관리 시스템 v1.0\n\n안전한 계정 정보 암호화 및 API 제공")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()
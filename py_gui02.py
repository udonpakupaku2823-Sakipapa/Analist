import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

df = None  # グローバルで保持

def load_file():
    global df
    file_path = filedialog.askopenfilename(
        filetypes=[("Excel Files", "umaData.xlsx")]
    )
    if not file_path:
        return
    
    try:
        df = pd.read_excel(file_path)
        messagebox.showinfo("読み込み完了", f"{file_path} を読み込みました。")
        
        # Treeview の列を更新
        tree["columns"] = list(df.columns)
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
    except Exception as e:
        messagebox.showerror("エラー", f"読み込みに失敗しました\n{e}")

def search():
    if df is None:
        messagebox.showwarning("注意", "先に Excel ファイルを読み込んでください。")
        return
    
    keyword = entry.get()
    result = df[df.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]
    
    # 表をクリア
    for row in tree.get_children():
        tree.delete(row)
    
    # 結果を挿入
    for _, row in result.iterrows():
        tree.insert("", tk.END, values=list(row))

# GUI作成
root = tk.Tk()
root.title("Excel検索ツール")

# ファイル読み込みボタン
load_button = tk.Button(root, text="Excelを読み込む", command=load_file)
load_button.pack()

# 入力欄
label = tk.Label(root, text="検索キーワード：")
label.pack()

entry = tk.Entry(root, width=200)
entry.pack()

button = tk.Button(root, text="検索", command=search)
button.pack()

# 表（Treeview）
tree = ttk.Treeview(root, show="headings")
tree.pack(fill=tk.BOTH, expand=True)

root.mainloop()

import tkinter as tk
from tkinter import Toplevel, messagebox
import os
from tkhtmlview import HTMLLabel


HTML_FILE = "Assets\\doc.html"

def show_documentation_window(parent_root):
    if not os.path.exists(HTML_FILE):
        messagebox.showerror("Hata", f"Dökümantasyon dosyası bulunamadı: {HTML_FILE}")
        return

    try:
        doc_window = Toplevel(parent_root)
        doc_window.title("Dökümantasyon Görüntüleyici")
        doc_window.geometry("700x500")

        with open(HTML_FILE, "r", encoding="utf-8") as f:
            html_data = f.read()
        html_viewer = HTMLLabel(
            doc_window,
            html=html_data,
            background="white",
            font=("Arial", 10)
        )

        html_viewer.pack(fill="both", expand=True, padx=10, pady=10)
        
    except Exception as e:
        messagebox.showerror("Hata", f"Dökümantasyon penceresi açılırken bir hata oluştu: {e}")

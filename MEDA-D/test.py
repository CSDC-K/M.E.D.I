# main.py
import tkinter as tk
from tkinter import messagebox
from Lib import docModule
import os

# 1. Ana pencereyi oluştur
root = tk.Tk()
root.title("Ana Uygulama (Modüler)")
root.geometry("350x180")

# 2. Butona tıklandığında çalışacak ana fonksiyon
def open_documentation():
    """
    docModule içerisindeki show_documentation_window fonksiyonunu çağırır.
    'root' objesini parent olarak gönderiyoruz.
    """
    try:
        # docModule içerisindeki fonksiyonu çağırıyoruz
        docModule.show_documentation_window(root)
    except Exception as e:
        messagebox.showerror("Hata", f"Dökümantasyon modülü çalıştırılamadı: {e}")

# 3. Butonu oluşturma
doc_button = tk.Button(
    root,
    text="Dökümantasyonu Aç (Modülden)",
    command=open_documentation,  # Butona tıklandığında open_documentation çalışacak
    bg="#3F51B5",
    fg="white",
    font=("Arial", 12, "bold"),
    padx=15,
    pady=8
)

doc_button.pack(pady=40, padx=40)

# 4. HTML dosyasının varlığını kontrol et
if not os.path.exists(docModule.HTML_FILE):
    messagebox.showwarning("Uyarı", f"Dökümantasyon HTML dosyası ({docModule.HTML_FILE}) bulunamıyor. Lütfen oluşturun.")

# 5. Ana döngüyü başlat
root.mainloop()
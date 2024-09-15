import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess
import os

dosya_yolu = ""

def check_git_installed():
    """Git'in sistemde kurulu olup olmadığını kontrol eder."""
    try:
        subprocess.run(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except Exception as e:
        return False

def select_file():
    global dosya_yolu
    dosya_yolu = filedialog.askdirectory(title="Klonlanacak konumu Seçin")
    if dosya_yolu:
        gui.title(f"{dosya_yolu}")

def clone_file():
    link = github_url.get()
    if not dosya_yolu:
        messagebox.showerror("Hata", "Lütfen geçerli bir dizin seçin.")
        return
    if not link:
        messagebox.showerror("Hata", "Lütfen geçerli bir GitHub URL'si girin.")
        return
    
    try:
        subprocess.run(["git", "clone", link], cwd=dosya_yolu, check=True)
        gui.title("Git Cloner")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

def install_git():
    try:
        gui.title("Git Yükleniyor")
        subprocess.run(["winget", "install", "--id", "Git.Git", "-e", "--source", "winget"], check=True)
        messagebox.showinfo("Bilgi", "Git başarıyla yüklendi. Uygulama açılacak.")
        gui.title("Git Cloner")
    except Exception as e:
        messagebox.showerror("Hata", f"Git yüklenirken bir hata oluştu: {e}")

gui = tk.Tk()
gui.geometry('400x200')
gui.resizable(0,0)
gui.iconbitmap(default='p.ico')
gui.title("Git Cloner")

# Git'in kurulu olup olmadığını kontrol et
if not check_git_installed():
    result = messagebox.askquestion("Git Eksik", "Git yazılımı sistemde bulunamadı, indirilsin mi? (Yazılımı kullanmak için Git gerekli).")
    if result == 'yes':
        install_git()
    else:
        exit()
    # subprocess.run(["winget", "install", "--id", "Git.Git", "-e", "--source", "winget"], cwd=dosya_yolu, check=True)
    # webbrowser.open_new_tab("https://git-scm.com/download/win")

link_label = tk.Label(
    gui,
    text="Github Repo URL'sini girin."
)
link_label.place(x=3,y=0)

github_url = tk.Entry(
    gui,
    width='38'
)
github_url.place(x=5,y=20)

filedialogbutton = tk.Button(
    gui,
    text='Klonlanacak konumu Seç',
    command=select_file
)
filedialogbutton.place(x=242,y=17)

clonebutton = tk.Button(
    text="KLONLA!",
    command=clone_file
)
clonebutton.place(x=0,y=45)

gui.mainloop()
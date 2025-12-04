import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
# loool
class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor - Untitled")
        self.root.geometry("800x600")
        
        self.current_file = None
        self.is_modified = False
        
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_menu()
        self.create_toolbar()
        self.create_text_area()
        self.create_status_bar()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.text_area.bind('<<Modified>>', self.on_text_modified)
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-Shift-S>', lambda e: self.save_as_file())
    
    def create_toolbar(self):
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        new_btn = ttk.Button(toolbar, text="New", command=self.new_file)
        new_btn.pack(side=tk.LEFT, padx=2)
        
        open_btn = ttk.Button(toolbar, text="Open", command=self.open_file)
        open_btn.pack(side=tk.LEFT, padx=2)
        
        save_btn = ttk.Button(toolbar, text="Save", command=self.save_file)
        save_btn.pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        undo_btn = ttk.Button(toolbar, text="Undo", command=self.undo)
        undo_btn.pack(side=tk.LEFT, padx=2)
        
        redo_btn = ttk.Button(toolbar, text="Redo", command=self.redo)
        redo_btn.pack(side=tk.LEFT, padx=2)
    
    def create_text_area(self):
        text_frame = ttk.Frame(self.root)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.text_area = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            undo=True,
            font=('Consolas', 11)
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
    
    def create_status_bar(self):
        self.status_bar = ttk.Label(
            self.root,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def on_text_modified(self, event=None):
        if self.text_area.edit_modified():
            self.is_modified = True
            self.update_title()
            self.text_area.edit_modified(False)
    
    def update_title(self):
        filename = os.path.basename(self.current_file) if self.current_file else "Untitled"
        modified_marker = "*" if self.is_modified else ""
        self.root.title(f"Text Editor - {filename}{modified_marker}")
    
    def new_file(self):
        if self.check_save():
            self.text_area.delete(1.0, tk.END)
            self.current_file = None
            self.is_modified = False
            self.update_title()
            self.status_bar.config(text="New file created")
    
    def open_file(self):
        if self.check_save():
            filepath = filedialog.askopenfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if filepath:
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, content)
                    self.current_file = filepath
                    self.is_modified = False
                    self.update_title()
                    self.status_bar.config(text=f"Opened: {filepath}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to open file:\n{e}")
    
    def save_file(self):
        if self.current_file:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.is_modified = False
                self.update_title()
                self.status_bar.config(text=f"Saved: {self.current_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")
        else:
            self.save_as_file()
    
    def save_as_file(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filepath:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.current_file = filepath
                self.is_modified = False
                self.update_title()
                self.status_bar.config(text=f"Saved as: {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")
    
    def check_save(self):
        if self.is_modified:
            response = messagebox.askyesnocancel(
                "Save Changes",
                "Do you want to save changes before continuing?"
            )
            if response is True:
                self.save_file()
                return True
            elif response is False:
                return True
            else:
                return False
        return True
    
    def on_closing(self):
        if self.check_save():
            self.root.destroy()
    
    def undo(self):
        try:
            self.text_area.edit_undo()
        except:
            pass
    
    def redo(self):
        try:
            self.text_area.edit_redo()
        except:
            pass
    
    def cut(self):
        self.text_area.event_generate("<<Cut>>")
    
    def copy(self):
        self.text_area.event_generate("<<Copy>>")
    
    def paste(self):
        self.text_area.event_generate("<<Paste>>")
    
    def select_all(self):
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)

def main():
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()

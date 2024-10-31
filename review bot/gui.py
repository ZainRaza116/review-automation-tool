import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import sys
import threading
from queue import Queue
from bot_core import bot  # Import the bot function from your original script

class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.queue = Queue()

    def write(self, string):
        self.queue.put(string)
        self.text_widget.after(100, self.check_queue)

    def check_queue(self):
        while not self.queue.empty():
            text = self.queue.get()
            self.text_widget.configure(state='normal')
            self.text_widget.insert('end', text)
            self.text_widget.see('end')
            self.text_widget.configure(state='disabled')

    def flush(self):
        pass

class ReviewBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Review Bot Control Panel")
        self.root.geometry("800x600")
        
        # File paths
        self.accounts_path = tk.StringVar()
        self.proxies_path = tk.StringVar()
        self.review_links_path = tk.StringVar()
        self.comments_path = tk.StringVar()
        
        self.create_gui()
        
    def create_gui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # File Selection Section
        files_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="5")
        files_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Accounts Path
        ttk.Label(files_frame, text="Accounts File:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(files_frame, textvariable=self.accounts_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(files_frame, text="Browse", command=lambda: self.browse_file(self.accounts_path)).grid(row=0, column=2)
        
        # Proxies Path
        ttk.Label(files_frame, text="Proxies File:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(files_frame, textvariable=self.proxies_path, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(files_frame, text="Browse", command=lambda: self.browse_file(self.proxies_path)).grid(row=1, column=2)
        
        # Review Links Path
        ttk.Label(files_frame, text="Review Links:").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(files_frame, textvariable=self.review_links_path, width=50).grid(row=2, column=1, padx=5)
        ttk.Button(files_frame, text="Browse", command=lambda: self.browse_file(self.review_links_path)).grid(row=2, column=2)
        
        # Comments Path
        ttk.Label(files_frame, text="Comments File:").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(files_frame, textvariable=self.comments_path, width=50).grid(row=3, column=1, padx=5)
        ttk.Button(files_frame, text="Browse", command=lambda: self.browse_file(self.comments_path)).grid(row=3, column=2)
        
        # Add spacing between sections
        ttk.Frame(main_frame).grid(row=1, column=0, pady=10)
        
        # Control Buttons
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.start_button = ttk.Button(buttons_frame, text="Start Bot", command=self.start_bot)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(buttons_frame, text="Stop Bot", command=self.stop_bot, state='disabled')
        self.stop_button.grid(row=0, column=1, padx=5)
        
        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief="sunken")
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, mode='determinate', variable=self.progress_var)
        self.progress_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Console Output
        console_frame = ttk.LabelFrame(main_frame, text="Console Output", padding="5")
        console_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        self.console = scrolledtext.ScrolledText(console_frame, wrap=tk.WORD, width=80, height=20)
        self.console.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.console.configure(state='disabled')
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        
        # Redirect stdout to our console
        sys.stdout = RedirectText(self.console)
        
        # Initialize bot state
        self.bot_running = False
        self.bot_thread = None
        
    def browse_file(self, string_var):
        filename = filedialog.askopenfilename(
            title="Select file",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if filename:
            string_var.set(filename)
            
    def start_bot(self):
        if not all([self.accounts_path.get(), self.proxies_path.get(), 
                   self.review_links_path.get(), self.comments_path.get()]):
            print("Please select all required files first!")
            return
            
        self.start_button.configure(state='disabled')
        self.stop_button.configure(state='normal')
        self.bot_running = True
        self.status_var.set("Bot is running...")
        
        # Start bot in a separate thread
        self.bot_thread = threading.Thread(target=self.run_bot)
        self.bot_thread.daemon = True
        self.bot_thread.start()
        
    def stop_bot(self):
        self.bot_running = False
        self.status_var.set("Stopping bot...")
        self.stop_button.configure(state='disabled')
        
    def run_bot(self):
        try:
            bot(
                self.accounts_path.get(),
                self.proxies_path.get(),
                self.review_links_path.get(),
                self.comments_path.get()
            )
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            self.bot_running = False
            self.start_button.configure(state='normal')
            self.stop_button.configure(state='disabled')
            self.status_var.set("Ready")

def main():
    root = tk.Tk()
    app = ReviewBotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import ttk
from ping3 import ping
import threading
import darkdetect


class PingTestApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Server Ping Test")
        # Set the icon (make sure to have an icon.png file)
        root.iconphoto(False, tk.PhotoImage(file='./assets/icon.png'))

        # Detect system theme
        self.is_dark = darkdetect.isDark() if hasattr(darkdetect, 'isDark') else False

        # Server list
        self.servers = {
            "US-E": "pingtest-atl.brawlhalla.com",
            "US-W": "pingtest-cal.brawlhalla.com",
            "EU": "pingtest-ams.brawlhalla.com",
            "SEA": "pingtest-sgp.brawlhalla.com",
            "AUS": "pingtest-aus.brawlhalla.com",
            "BRAZIL": "pingtest-brs.brawlhalla.com",
            "JAPAN": "pingtest-jpn.brawlhalla.com",
            "MIDDLE EAST": "pingtest-mde.brawlhalla.com",
            "SOUTHERN AFRICA": "pingtest-saf.brawlhalla.com"
        }

        # Style configuration
        self.style = ttk.Style()
        self.configure_themes()

        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        # Title
        self.title_label = ttk.Label(self.main_frame, text="Server Ping Tester",
                                     font=("Helvetica", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Theme toggle button (small icon)
        self.theme_btn = ttk.Button(self.main_frame, text="☀/🌙", width=3,
                                    command=self.toggle_theme, style="Custom.TButton")
        self.theme_btn.grid(row=0, column=2, pady=10, sticky=tk.E)

        # Create server list frame
        self.server_frame = ttk.LabelFrame(
            self.main_frame, text="Servers", padding="5")
        self.server_frame.grid(
            row=1, column=0, columnspan=3, pady=10, sticky="nsew")

        # Dictionary to store ping results and buttons
        self.ping_labels = {}
        self.ping_buttons = {}

        # Create server entries
        for i, (name, address) in enumerate(self.servers.items()):
            ttk.Label(self.server_frame, text=name).grid(
                row=i, column=0, padx=5, pady=5, sticky=tk.W)
            result_label = ttk.Label(
                self.server_frame, text="N/A ms", width=10)
            result_label.grid(row=i, column=1, padx=5, pady=5)
            self.ping_labels[name] = result_label
            ping_btn = ttk.Button(self.server_frame, text="Ping",
                                  command=lambda s=name: self.ping_server(s),
                                  style="Custom.TButton")
            ping_btn.grid(row=i, column=2, padx=5, pady=5)
            ping_btn.bind("<Enter>", lambda e: ping_btn.config(cursor="hand2"))
            ping_btn.bind("<Leave>", lambda e: ping_btn.config(cursor=""))
            self.ping_buttons[name] = ping_btn

        # Ping All button
        self.ping_all_btn = ttk.Button(self.main_frame, text="Ping All Servers",
                                       command=self.ping_all, style="Custom.TButton")
        self.ping_all_btn.grid(row=2, column=0, columnspan=3, pady=10)
        self.ping_all_btn.bind(
            "<Enter>", lambda e: self.ping_all_btn.config(cursor="hand2"))
        self.ping_all_btn.bind(
            "<Leave>", lambda e: self.ping_all_btn.config(cursor=""))

        # Status label
        self.status_label = ttk.Label(self.main_frame, text="")
        self.status_label.grid(row=3, column=0, columnspan=3, pady=5)

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        # Apply initial theme
        self.apply_theme()

        # Update window size based on content
        self.root.update()
        self.root.geometry(
            f"{self.root.winfo_reqwidth()}x{self.root.winfo_reqheight()}")

    def configure_themes(self):
        # Light theme
        self.style.theme_create("light", parent="clam", settings={
            "TFrame": {"configure": {"background": "#f0f0f0"}},
            "TLabel": {"configure": {"background": "#f0f0f0", "foreground": "#000000"}},
            "TLabelframe": {"configure": {"background": "#f0f0f0", "foreground": "#000000"}},
            "TLabelframe.Label": {"configure": {"background": "#f0f0f0", "foreground": "#000000"}},
            "Custom.TButton": {
                "configure": {
                    "background": "#e0e0e0",
                    "foreground": "#000000",
                    "borderwidth": 1,
                    "relief": "flat",
                    "padding": 4
                },
                "map": {
                    "background": [("active", "#d0d0d0"), ("disabled", "#f0f0f0")],
                    "foreground": [("disabled", "#808080")]
                }
            }
        })

        # Dark theme
        self.style.theme_create("dark", parent="clam", settings={
            "TFrame": {"configure": {"background": "#2d2d2d"}},
            "TLabel": {"configure": {"background": "#2d2d2d", "foreground": "#30f1dd"}},
            "TLabelframe": {"configure": {"background": "#2d2d2d", "foreground": "#ffffff"}},
            "TLabelframe.Label": {"configure": {"background": "#2d2d2d", "foreground": "#ffffff"}},
            "Custom.TButton": {
                "configure": {
                    "background": "#404040",
                    "foreground": "#ffffff",
                    "borderwidth": 1,
                    "relief": "flat",
                    "padding": 4
                },
                "map": {
                    "background": [("active", "#505050"), ("disabled", "#303030")],
                    "foreground": [("disabled", "#808080")]
                }
            }
        })

    def apply_theme(self):
        self.style.theme_use("dark" if self.is_dark else "light")
        self.root.configure(bg="#2d2d2d" if self.is_dark else "#f0f0f0")

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.apply_theme()
        self.root.update()
        self.root.geometry(
            f"{self.root.winfo_reqwidth()}x{self.root.winfo_reqheight()}")

    def ping_server(self, server_name):
        def ping_thread():
            self.ping_buttons[server_name].config(state="disabled")
            self.status_label.config(text=f"Pinging {server_name}...")

            try:
                result = ping(self.servers[server_name], timeout=2, unit="ms")
                if result is not None:
                    self.ping_labels[server_name].config(
                        text=f"{int(result)} ms")
                else:
                    self.ping_labels[server_name].config(text="Timeout")
            except Exception:
                self.ping_labels[server_name].config(text="Error")

            self.ping_buttons[server_name].config(state="normal")
            self.status_label.config(text="")

        threading.Thread(target=ping_thread, daemon=True).start()

    def ping_all(self):
        def ping_all_thread():
            self.ping_all_btn.config(state="disabled")
            self.status_label.config(text="Pinging all servers...")

            for server_name in self.servers:
                self.ping_server(server_name)

            self.ping_all_btn.config(state="normal")
            self.status_label.config(text="All servers pinged")

        threading.Thread(target=ping_all_thread, daemon=True).start()


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = PingTestApp(root)
        root.mainloop()
    except ImportError as e:
        print(f"Error: {e}")
        print("Please install required packages: pip install ping3 darkdetect")

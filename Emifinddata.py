import customtkinter as ctk
import pandas as pd
import numpy as np
from PIL import Image
from tkinter import filedialog, messagebox
import os


class ProfilerLogic:
    @staticmethod
    def get_stats(series):
        """Calculates professional quality metrics for a column."""
        nulls = series.isnull().sum()
        unique_pct = (series.nunique() / len(series)) * 100 if len(series) > 0 else 0

        # Outlier Detection (Standard IQR Method)
        outliers = 0
        if pd.api.types.is_numeric_dtype(series) and not series.empty:
            q1, q3 = series.quantile(0.25), series.quantile(0.75)
            iqr = q3 - q1
            outliers = ((series < (q1 - 1.5 * iqr)) | (series > (q3 + 1.5 * iqr))).sum()

        is_key = "🔑 Unique ID" if (series.is_unique and nulls == 0) else "Standard"
        return nulls, outliers, is_key, unique_pct


class EmiFindData(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EmiFindData Professional")
        self.geometry("1400x950")
        ctk.set_appearance_mode("dark")
        self.datasets = {}

        # SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0, fg_color="#0a0a0a")
        self.sidebar.pack(side="left", fill="y")

        # LOGO (Main Brand)
        try:
            logo_img = ctk.CTkImage(Image.open("IMG_8009.jpeg"), size=(200, 280))
            ctk.CTkLabel(self.sidebar, image=logo_img, text="").pack(pady=20)
        except:
            ctk.CTkLabel(self.sidebar, text="EmiFindData", font=("Impact", 32)).pack(pady=20)

        # BUTTONS (Icons + Labels)
        self.create_icon_btn("IMG_8017.jpeg", "Import Data", self.load_files, (60, 80))

        # Folder Icon Header
        try:
            f_img = ctk.CTkImage(Image.open("IMG_8015.jpeg"), size=(50, 70))
            ctk.CTkLabel(self.sidebar, image=f_img, text="").pack(pady=(30, 0))
        except:
            pass
        ctk.CTkLabel(self.sidebar, text="Active Datasets", font=("Arial", 14, "bold")).pack()

        # FILE LIST
        self.file_list = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        self.file_list.pack(fill="both", expand=True, padx=10, pady=10)

        # MAIN VIEW
        self.tabs = ctk.CTkTabview(self, corner_radius=15)
        self.tabs.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        self.tab_prof = self.tabs.add("🔬 Data Profiler")
        self.tab_view = self.tabs.add("🗂️ Table Browser")

    def create_icon_btn(self, img_path, label, cmd, img_size):
        try:
            img = ctk.CTkImage(Image.open(img_path), size=img_size)
            btn = ctk.CTkButton(self.sidebar, image=img, text="", fg_color="transparent",
                                hover_color="#1a1a1a", command=cmd, width=img_size[0])
            btn.pack(pady=(10, 0))
            ctk.CTkLabel(self.sidebar, text=label, font=("Arial", 12)).pack()
        except:
            ctk.CTkButton(self.sidebar, text=label, command=cmd).pack(pady=10)

    def load_files(self):
        paths = filedialog.askopenfilenames(filetypes=[("Data", "*.csv *.xlsx")])
        for path in paths:
            name = os.path.basename(path)
            self.datasets[name] = pd.read_csv(path) if path.endswith('.csv') else pd.read_excel(path)
        self.update_sidebar()

    def update_sidebar(self):
        for w in self.file_list.winfo_children(): w.destroy()
        for name in self.datasets.keys():
            row = ctk.CTkFrame(self.file_list, fg_color="#1a1a1a", corner_radius=8)
            row.pack(fill="x", pady=3)
            ctk.CTkButton(row, text=name[:15], fg_color="transparent", anchor="w",
                          command=lambda n=name: self.run_profiler(n)).pack(side="left", padx=5, fill="x", expand=True)
            # THE DELETE OPTION
            ctk.CTkButton(row, text="🗑️", width=30, fg_color="transparent", text_color="red",
                          command=lambda n=name: self.remove_data(n)).pack(side="right", padx=5)

    def remove_data(self, name):
        if messagebox.askyesno("EmiFindData", f"Remove {name}?"):
            del self.datasets[name]
            self.update_sidebar()

    def run_profiler(self, name):
        df = self.datasets[name]
        for w in self.tab_prof.winfo_children(): w.destroy()
        scroll = ctk.CTkScrollableFrame(self.tab_prof, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        ctk.CTkLabel(scroll, text=f"Analysis: {name}", font=("Arial", 22, "bold")).pack(pady=15)

        for col in df.columns:
            nulls, outliers, key_status, unique = ProfilerLogic.get_stats(df[col])
            card = ctk.CTkFrame(scroll, corner_radius=10, border_width=1, border_color="#333")
            card.pack(fill="x", pady=5, padx=10)

            msg = (f"COLUMN: {col}\n• Type: {df[col].dtype} | Missing: {nulls}\n"
                   f"• Outliers: {outliers} | Uniqueness: {unique:.1f}%\n• Status: {key_status}")
            ctk.CTkLabel(card, text=msg, justify="left", font=("Consolas", 13)).pack(padx=20, pady=12, anchor="w")

        for w in self.tab_view.winfo_children(): w.destroy()
        tb = ctk.CTkTextbox(self.tab_view, font=("Consolas", 12))
        tb.pack(fill="both", expand=True)
        tb.insert("0.0", df.head(50).to_string())


if __name__ == "__main__":
    EmiFindData().mainloop()

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import config
from .patientlist import PatientList
import runner
from typing import cast
import platform

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("App ký tên tự động HIS SAKURA")
        from os import path

        if platform.system() == "Windows":
            path_to_ico = path.abspath(
                path.join(path.dirname(path.dirname(__file__)), "icon.ico")
            )
            self.iconbitmap(path_to_ico)
        self.columnconfigure(0, weight=1)

        self.bind_class(
            "Entry",
            "<Control-a>",
            lambda e: cast(tk.Entry, e.widget).select_range(0, "end"),
        )

        bs_username_var = tk.StringVar()
        bs_password_var = tk.StringVar()
        dd_username_var = tk.StringVar()
        dd_password_var = tk.StringVar()

        staff_info = ttk.LabelFrame(self, text="Thông tin đăng nhập")
        bacsi = ttk.LabelFrame(staff_info, text="Bác sĩ")
        bs_username_label = ttk.Label(bacsi, text="username")
        bs_username_entry = ttk.Entry(bacsi, textvariable=bs_username_var)
        bs_password_label = ttk.Label(bacsi, text="password")
        bs_passord_entry = ttk.Entry(bacsi, show="*", textvariable=bs_password_var)
        dieuduong = ttk.LabelFrame(staff_info, text="Điều dưỡng")
        dd_username_label = ttk.Label(dieuduong, text="username")
        dd_username_entry = ttk.Entry(dieuduong, textvariable=dd_username_var)
        dd_password_label = ttk.Label(dieuduong, text="password")
        dd_password_entry = ttk.Entry(dieuduong, show="*", textvariable=dd_password_var)

        staff_info.grid(row=0, column=0, sticky="N", columnspan=2)
        bacsi.grid(row=0, column=0)
        bs_username_label.grid(row=0, column=0)
        bs_password_label.grid(row=1, column=0)
        bs_username_entry.grid(row=0, column=1)
        bs_passord_entry.grid(row=1, column=1)
        dieuduong.grid(row=0, column=1)
        dd_username_label.grid(row=0, column=0)
        dd_password_label.grid(row=1, column=0)
        dd_username_entry.grid(row=0, column=1)
        dd_password_entry.grid(row=1, column=1)

        headers = ttk.Frame(self)
        url_header = ttk.Label(headers, text="url", relief="raised", anchor="center")
        ky_xetnghiem_header = ttk.Label(headers, text="Ký xét nghiệm", relief="raised", anchor="center")
        ky_todieutri_header = ttk.Label(headers, text="Ký tờ điều trị", relief="raised", anchor="center")
        vitri_ky_3tra_header = ttk.Label(
            headers, text="Vị trí ký 3tra", relief="raised", anchor="center"
        )
        delete_header = ttk.Label(headers, text="Xóa", relief="raised", anchor="center")

        headers.grid(row=1, column=0, sticky="WE")
        headers.columnconfigure(0, weight=1, minsize=200)
        headers.columnconfigure(1, minsize=120)
        headers.columnconfigure(2, minsize=120)
        headers.columnconfigure(3, minsize=180)
        headers.columnconfigure(4, minsize=80)
        url_header.grid(row=0, column=0, sticky="NSEW")
        ky_xetnghiem_header.grid(row=0, column=1, sticky="NSEW")
        ky_todieutri_header.grid(row=0, column=2, sticky="NSEW")
        vitri_ky_3tra_header.grid(row=0, column=3, sticky="NSEW")
        delete_header.grid(row=0, column=4, sticky="NSWE", padx=(0, 15))

        listframe = PatientList(self)
        listframe.grid(row=2, column=0, sticky="NSEW", rowspan=6)

        def load():
            listframe.clear()
            cf = config.load()
            bs_username_var.set(cf["bacsi"]["username"])
            bs_password_var.set(cf["bacsi"]["password"])
            dd_username_var.set(cf["dieuduong"]["username"])
            dd_password_var.set(cf["dieuduong"]["password"])
            for p in cf["patients"]:
                listframe.add_patient(p)

        def get_config() -> config.Config:
            return {
                "bacsi": {
                    "username": bs_username_var.get(),
                    "password": bs_password_var.get(),
                },
                "dieuduong": {
                    "username": dd_username_var.get(),
                    "password": dd_password_var.get(),
                },
                "patients": listframe.get_patients(),
            }

        def save():
            config.save(get_config())
            if messagebox.askyesno(message="Save?"):
                messagebox.Message(default=messagebox.OK, message="Đã lưu").show()

        def run():
            cf = get_config()

            if config.is_bs_valid(cf):
                runner.run_bs(cf)
            else:
                messagebox.showinfo(message="bs not valid")

            if config.is_dd_valid(cf):
                runner.run_dd(cf)
            else:
                messagebox.showinfo(message="dd not valid")
            messagebox.showinfo(message="finish")

        load_btn = tk.Button(self, text="Load", command=load, width=10)
        load_btn.grid(row=2, column=1)
        save_btn = tk.Button(self, text="Save", command=save, width=10)
        save_btn.grid(row=3, column=1)

        new_btn = tk.Button(
            self, text="Add", command=lambda: listframe.add_new(), width=10
        )
        new_btn.grid(row=5, column=1)
        run_btn = tk.Button(
            self, text="RUN", command=run, width=10, bg="#ff0073", fg="#ffffff"
        )
        run_btn.grid(row=6, column=1, padx=20)

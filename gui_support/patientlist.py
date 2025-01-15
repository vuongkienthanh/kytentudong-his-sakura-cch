from .scrollframe import ScrollFrame
import tkinter as tk
from config import Patient
from typing import cast

class PatientList(ScrollFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.viewPort.columnconfigure(0, weight=1)

    def add_new(self):
        line = Line(self.viewPort)
        line.grid(row=len(self.viewPort.grid_slaves()), column=0, sticky="EW")

    def add_patient(self, patient: Patient):
        line = Line(self.viewPort)
        line.set_patient(patient)
        line.grid(row=len(self.viewPort.grid_slaves()), column=0, sticky="EW")

    def get_patients(self) -> list[Patient]:
        return [cast(Line, p).to_patient() for p in self.viewPort.grid_slaves()]

    def clear(self):
        for w in self.viewPort.grid_slaves():
            w.destroy()

class Line(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.url_var = tk.StringVar()
        self.note_var = tk.StringVar()
        self.xn_var = tk.BooleanVar()
        self.tdt_var = tk.BooleanVar()
        self.bs_0_var = tk.BooleanVar()
        self.bs_1_var = tk.BooleanVar()
        self.bs_2_var = tk.BooleanVar()
        self.bs_3_var = tk.BooleanVar()
        self.bs_4_var = tk.BooleanVar()
        self.dd_0_var = tk.BooleanVar()
        self.dd_1_var = tk.BooleanVar()
        self.dd_2_var = tk.BooleanVar()
        self.dd_3_var = tk.BooleanVar()
        self.dd_4_var = tk.BooleanVar()
        info_frame = tk.Frame(self)
        url_entry = tk.Entry(info_frame, textvariable=self.url_var)
        note_label = tk.Label(info_frame, text="note")
        note_entry = tk.Entry(info_frame, textvariable=self.note_var)

        xn_checkbox = tk.Checkbutton(
            self, variable=self.xn_var, command=lambda: self.xn_var
        )
        tdt_checkbox = tk.Checkbutton(
            self, variable=self.tdt_var, command=lambda: self.tdt_var
        )
        tdt_checkbox.select()
        k3t = tk.Frame(self, borderwidth=10)
        k3t_bs = tk.LabelFrame(k3t, text="Bác sĩ")
        k3t_dd = tk.LabelFrame(k3t, text="Điều dưỡng")
        k3t_bs_0 = tk.Checkbutton(
            k3t_bs, variable=self.bs_0_var, command=lambda: self.bs_0_var
        )
        k3t_bs_1 = tk.Checkbutton(
            k3t_bs, variable=self.bs_1_var, command=lambda: self.bs_1_var
        )
        k3t_bs_2 = tk.Checkbutton(
            k3t_bs, variable=self.bs_2_var, command=lambda: self.bs_2_var
        )
        k3t_bs_3 = tk.Checkbutton(
            k3t_bs, variable=self.bs_3_var, command=lambda: self.bs_3_var
        )
        k3t_bs_4 = tk.Checkbutton(
            k3t_bs, variable=self.bs_4_var, command=lambda: self.bs_4_var
        )
        k3t_dd_0 = tk.Checkbutton(
            k3t_dd, variable=self.dd_0_var, command=lambda: self.dd_0_var
        )
        k3t_dd_1 = tk.Checkbutton(
            k3t_dd, variable=self.dd_1_var, command=lambda: self.dd_1_var
        )
        k3t_dd_2 = tk.Checkbutton(
            k3t_dd, variable=self.dd_2_var, command=lambda: self.dd_2_var
        )
        k3t_dd_3 = tk.Checkbutton(
            k3t_dd, variable=self.dd_3_var, command=lambda: self.dd_3_var
        )
        k3t_dd_4 = tk.Checkbutton(
            k3t_dd, variable=self.dd_4_var, command=lambda: self.dd_4_var
        )
        delete_button = tk.Button(self, text="Xóa", command=self.destroy)
        self.columnconfigure(0, weight=1, minsize=200)
        self.columnconfigure(1, minsize=120)
        self.columnconfigure(2, minsize=120)
        self.columnconfigure(3, minsize=180)
        self.columnconfigure(4, minsize=80)
        info_frame.columnconfigure(1, weight=1)
        info_frame.grid(row=0, column=0, sticky="WE")
        url_entry.grid(row=0, column=0, sticky="WE", columnspan=2)
        note_label.grid(row=1, column=0)
        note_entry.grid(row=1, column=1, sticky="WE")
        xn_checkbox.grid(row=0, column=1)
        tdt_checkbox.grid(row=0, column=2)
        k3t.grid(row=0, column=3)
        delete_button.grid(row=0, column=4)
        k3t_bs.grid(row=0, column=0)
        k3t_bs_0.grid(row=0, column=0)
        k3t_bs_1.grid(row=0, column=1)
        k3t_bs_2.grid(row=0, column=2)
        k3t_bs_3.grid(row=0, column=3)
        k3t_bs_4.grid(row=0, column=4)
        k3t_dd.grid(row=1, column=0)
        k3t_dd_0.grid(row=0, column=0)
        k3t_dd_1.grid(row=0, column=1)
        k3t_dd_2.grid(row=0, column=2)
        k3t_dd_3.grid(row=0, column=3)
        k3t_dd_4.grid(row=0, column=4)

    def set_patient(self, patient: Patient):
        self.url_var.set(patient["url"])
        self.note_var.set(patient["note"])
        self.xn_var.set(patient["ky_xetnghiem"])
        self.tdt_var.set(patient["ky_todieutri"])
        self.bs_0_var.set(patient["vitri_ky_3tra"]["bacsi"][0])
        self.bs_1_var.set(patient["vitri_ky_3tra"]["bacsi"][1])
        self.bs_2_var.set(patient["vitri_ky_3tra"]["bacsi"][2])
        self.bs_3_var.set(patient["vitri_ky_3tra"]["bacsi"][3])
        self.bs_4_var.set(patient["vitri_ky_3tra"]["bacsi"][4])
        self.dd_0_var.set(patient["vitri_ky_3tra"]["dieuduong"][0])
        self.dd_1_var.set(patient["vitri_ky_3tra"]["dieuduong"][1])
        self.dd_2_var.set(patient["vitri_ky_3tra"]["dieuduong"][2])
        self.dd_3_var.set(patient["vitri_ky_3tra"]["dieuduong"][3])
        self.dd_4_var.set(patient["vitri_ky_3tra"]["dieuduong"][4])

    def to_patient(self) -> Patient:
        return {
            "url": self.url_var.get(),
            "note": self.note_var.get(),
            "ky_xetnghiem": self.xn_var.get(),
            "ky_todieutri": self.tdt_var.get(),
            "vitri_ky_3tra": {
                "bacsi": (
                    self.bs_0_var.get(),
                    self.bs_1_var.get(),
                    self.bs_2_var.get(),
                    self.bs_3_var.get(),
                    self.bs_4_var.get(),
                ),
                "dieuduong": (
                    self.dd_0_var.get(),
                    self.dd_1_var.get(),
                    self.dd_2_var.get(),
                    self.dd_3_var.get(),
                    self.dd_4_var.get(),
                ),
            },
        }

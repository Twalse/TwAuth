import customtkinter as ctk
import pyotp
import pyperclip
import time
import json
import os
import webbrowser
import sys

x_f1 = "auth_data.json"
x_f2 = "settings.json"

class App(ctk.CTk):
    def resource_path(self, relative_path):
        """ Получает абсолютный путь к ресурсу, работает для .py и для PyInstaller .exe """
        if hasattr(sys, '_MEIPASS'):
            # Если запущено из .exe, берем путь временной папки распаковки
            return os.path.join(sys._MEIPASS, relative_path)
        # Если запущен .py, берем обычный относительный путь
        return os.path.join(os.path.abspath("."), relative_path)
    def __init__(self):
        super().__init__()
        self.geometry("380x600")
        self.title("TWAuth")
        try:
            ico_path = self.resource_path("icon.ico")
            if os.path.exists(ico_path):
                self.iconbitmap(ico_path)
        except Exception:
            pass # Если что-то пошло не так, просто игнорируем иконку
        self.z_set = self.l_s()
        self.z_acc = self.l_a()
        self.d = {}
        self.z_lang = self.z_set.get("l", "RU")
        self.x_pin = self.z_set.get("p", None)
        self.a_t()
        if self.x_pin:
            self.b_p()
        else:
            self.b_m()

    def a_t(self):
        x = self.z_set.get("t", "dark")
        if x == "light":
            ctk.set_appearance_mode("light")
            self.z_c = {"bg": "#ebebeb", "fg": "#dbdbdb", "t": "black", "a": "#3da0f5"}
        elif x == "green":
            ctk.set_appearance_mode("dark")
            self.z_c = {"bg": "#121212", "fg": "#1c1c1e", "t": "white", "a": "#2ecc71"}
        elif x == "purple":
            ctk.set_appearance_mode("dark")
            self.z_c = {"bg": "#121212", "fg": "#1c1c1e", "t": "white", "a": "#b83bfa"}
        else:
            ctk.set_appearance_mode("dark")
            self.z_c = {"bg": "#121212", "fg": "#1c1c1e", "t": "white", "a": "#3da0f5"}

    def l_s(self):
        if os.path.exists(x_f2):
            with open(x_f2, "r", encoding="utf-8") as x:
                return json.load(x)
        return {"t": "dark", "l": "RU", "p": None}

    def s_s(self):
        with open(x_f2, "w", encoding="utf-8") as x:
            json.dump(self.z_set, x)

    def l_a(self):
        if os.path.exists(x_f1):
            with open(x_f1, "r", encoding="utf-8") as x:
                return json.load(x)
        return {}

    def s_a(self):
        with open(x_f1, "w", encoding="utf-8") as x:
            json.dump(self.z_acc, x, ensure_ascii=False)

    def b_p(self):
        for x in self.winfo_children():
            x.destroy()
        self.z_p_f = ctk.CTkFrame(self, fg_color=self.z_c["bg"])
        self.z_p_f.pack(expand=True, fill="both")
        y = "Введите PIN" if self.z_lang == "RU" else "Enter PIN"
        self.z_l1 = ctk.CTkLabel(self.z_p_f, text=y, font=("Arial", 20), text_color=self.z_c["t"])
        self.z_l1.pack(pady=(150, 20))
        self.z_e1 = ctk.CTkEntry(self.z_p_f, show="*")
        self.z_e1.pack(pady=10)
        self.z_b1 = ctk.CTkButton(self.z_p_f, text="OK", fg_color=self.z_c["a"], command=self.c_p)
        self.z_b1.pack(pady=10)
        y2 = "Сбросить (удалит коды)" if self.z_lang == "RU" else "Reset (erases codes)"
        self.z_b2 = ctk.CTkButton(self.z_p_f, text=y2, fg_color="red", command=self.r_a_p)
        self.z_b2.pack(pady=50)

    def c_p(self):
        x = self.z_e1.get()
        if x == self.x_pin:
            self.b_m()
        else:
            y = "Неверный PIN!" if self.z_lang == "RU" else "Wrong PIN!"
            self.z_l1.configure(text=y, text_color="red")

    def r_a_p(self):
        self.z_set["p"] = None
        self.x_pin = None
        self.s_s()
        self.z_acc = {}
        self.s_a()
        self.b_m()

    def b_m(self):
        for x in self.winfo_children():
            x.destroy()
        self.configure(fg_color=self.z_c["bg"])
        self.z_ov = None
        self.z_bg = None
        y1 = ctk.CTkFrame(self, fg_color="transparent")
        y1.pack(fill="x", padx=20, pady=(20, 10))
        y2 = ctk.CTkButton(y1, text="⚙", width=40, fg_color=self.z_c["a"], command=self.o_s)
        y2.pack(side="left")
        self.z_tl = ctk.CTkLabel(y1, text="Authenticator", font=("Arial", 24, "bold"), text_color=self.z_c["t"])
        self.z_tl.pack(side="left", padx=20)
        y3 = ctk.CTkButton(y1, text="+", width=40, fg_color=self.z_c["a"], command=self.o_a)
        y3.pack(side="right")
        self.z_pr = ctk.CTkProgressBar(self, height=4, progress_color=self.z_c["a"])
        self.z_pr.pack(fill="x", padx=20, pady=(0, 10))
        self.z_sf = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.z_sf.pack(fill="both", expand=True, padx=10, pady=5)
        self.r_l()
        self.u_c()

    def r_l(self):
        for x in self.z_sf.winfo_children():
            x.destroy()
        self.d.clear()
        for x, y in self.z_acc.items():
            z = ctk.CTkFrame(self.z_sf, corner_radius=15, fg_color=self.z_c["fg"])
            z.pack(fill="x", padx=10, pady=8)
            x1 = ctk.CTkFrame(z, fg_color="transparent")
            x1.pack(fill="x", padx=15, pady=10)
            y1 = ctk.CTkLabel(x1, text=x, font=("Arial", 14), text_color=self.z_c["t"])
            y1.pack(side="left")
            z1 = ctk.CTkButton(x1, text="⋮", width=30, fg_color=self.z_c["a"], command=lambda a=x: self.o_m(a))
            z1.pack(side="right")
            x2 = ctk.CTkLabel(z, text="------", font=("Arial", 36, "bold"), text_color=self.z_c["a"])
            x2.pack(anchor="w", padx=15, pady=(0, 10))
            for y2 in (z, x1, y1, x2):
                y2.bind("<Button-1>", lambda e, s=y, n=x: self.c_t_c(s, n))
            self.d[x] = {"l": x2, "s": y}

    def c_t_c(self, x, y):
        try:
            z = pyotp.TOTP(x)
            pyperclip.copy(z.now())
            self.z_tl.configure(text="Copied!" if self.z_lang == "EN" else "Скопировано!")
            self.after(2000, lambda: self.z_tl.configure(text="Authenticator"))
        except:
            pass

    def u_c(self):
        x = time.time()
        y = 30 - (x % 30)
        self.z_pr.set(y / 30)
        for z, x1 in self.d.items():
            try:
                y1 = pyotp.TOTP(x1["s"]).now()
                z1 = f"{y1[:3]} {y1[3:]}"
                if x1["l"].cget("text") != z1:
                    x1["l"].configure(text=z1)
            except:
                x1["l"].configure(text="ERR")
        self.z_u_id = self.after(100, self.u_c)

    def s_o(self, x):
        self.z_bg = ctk.CTkFrame(self, fg_color=("#e0e0e0", "#121212"))
        self.z_bg.place(relwidth=1, relheight=1)
        x.lift()
        x.place(relx=0.5, rely=0.5, anchor="center")

    def c_o(self, x):
        x.destroy()
        if self.z_bg:
            self.z_bg.destroy()

    def o_s(self):
        x = ctk.CTkFrame(self, width=300, height=450, fg_color=self.z_c["fg"])
        x.pack_propagate(False)
        y1 = "Настройки" if self.z_lang == "RU" else "Settings"
        ctk.CTkLabel(x, text=y1, font=("Arial", 20), text_color=self.z_c["t"]).pack(pady=10)
        y2 = ctk.CTkOptionMenu(x, values=["dark", "light", "green", "purple"], fg_color=self.z_c["a"], command=self.c_t)
        y2.set(self.z_set["t"])
        y2.pack(pady=5)
        y3 = ctk.CTkOptionMenu(x, values=["RU", "EN"], fg_color=self.z_c["a"], command=self.c_l)
        y3.set(self.z_set["l"])
        y3.pack(pady=5)
        y4 = "Установить PIN" if self.z_lang == "RU" else "Set PIN"
        ctk.CTkButton(x, text=y4, fg_color=self.z_c["a"], command=lambda: self.s_p_d(x)).pack(pady=5)
        y5 = "Сброс PIN" if self.z_lang == "RU" else "Reset PIN"
        ctk.CTkButton(x, text=y5, fg_color=self.z_c["a"], command=lambda: self.r_p_d(x)).pack(pady=5)
        y6 = "Стереть коды" if self.z_lang == "RU" else "Erase codes"
        ctk.CTkButton(x, text=y6, fg_color="red", command=self.e_c).pack(pady=5)
        y7 = "Поделиться" if self.z_lang == "RU" else "Share"
        ctk.CTkButton(x, text=y7, fg_color=self.z_c["a"], command=lambda: webbrowser.open("https://github.com/Twalse")).pack(pady=5)
        ctk.CTkLabel(x, text="Twalse | GitHub", text_color=self.z_c["t"]).pack(pady=10)
        y8 = "Закрыть" if self.z_lang == "RU" else "Close"
        ctk.CTkButton(x, text=y8, fg_color=self.z_c["a"], command=lambda: self.c_o(x)).pack(pady=10)
        self.s_o(x)

    def c_t(self, x):
        self.z_set["t"] = x
        self.s_s()
        self.a_t()
        self.after(100, self.b_m)
        
    def c_l(self, x):
        self.z_set["l"] = x
        self.z_lang = x
        self.s_s()
        self.after(100, self.b_m)

    def e_c(self):
        self.z_acc = {}
        self.s_a()
        self.r_l()

    def s_p_d(self, x):
        self.c_o(x)
        y = ctk.CTkFrame(self, width=250, height=250, fg_color=self.z_c["fg"])
        y.pack_propagate(False)
        ctk.CTkLabel(y, text="PIN 1:", text_color=self.z_c["t"]).pack(pady=5)
        z1 = ctk.CTkEntry(y, show="*")
        z1.pack(pady=5)
        ctk.CTkLabel(y, text="PIN 2:", text_color=self.z_c["t"]).pack(pady=5)
        z2 = ctk.CTkEntry(y, show="*")
        z2.pack(pady=5)
        def z3():
            a = z1.get()
            b = z2.get()
            if a == b and a != "":
                self.z_set["p"] = a
                self.x_pin = a
                self.s_s()
                self.c_o(y)
        ctk.CTkButton(y, text="OK", fg_color=self.z_c["a"], command=z3).pack(pady=10)
        ctk.CTkButton(y, text="X", fg_color=self.z_c["a"], command=lambda: self.c_o(y)).pack(pady=5)
        self.s_o(y)

    def r_p_d(self, x):
        self.c_o(x)
        y = ctk.CTkFrame(self, width=250, height=200, fg_color=self.z_c["fg"])
        y.pack_propagate(False)
        ctk.CTkLabel(y, text="Текущий PIN:" if self.z_lang == "RU" else "Current PIN:", text_color=self.z_c["t"]).pack(pady=10)
        z1 = ctk.CTkEntry(y, show="*")
        z1.pack(pady=10)
        def z2():
            if z1.get() == self.x_pin:
                self.z_set["p"] = None
                self.x_pin = None
                self.s_s()
                self.c_o(y)
        ctk.CTkButton(y, text="OK", fg_color=self.z_c["a"], command=z2).pack(pady=10)
        ctk.CTkButton(y, text="X", fg_color=self.z_c["a"], command=lambda: self.c_o(y)).pack(pady=5)
        self.s_o(y)

    def o_a(self):
        x = ctk.CTkFrame(self, width=280, height=280, fg_color=self.z_c["fg"])
        x.pack_propagate(False)
        ctk.CTkLabel(x, text="Имя:" if self.z_lang == "RU" else "Name:", text_color=self.z_c["t"]).pack(pady=5)
        y1 = ctk.CTkEntry(x)
        y1.pack(pady=5)
        ctk.CTkLabel(x, text="Ключ:" if self.z_lang == "RU" else "Key:", text_color=self.z_c["t"]).pack(pady=5)
        y2 = ctk.CTkEntry(x)
        y2.pack(pady=5)
        z1 = ctk.CTkLabel(x, text="", text_color="red")
        z1.pack(pady=2)
        def z2():
            a = y1.get().strip()
            b = y2.get().strip().replace(" ", "")
            if not a or not b:
                return
            try:
                pyotp.TOTP(b).now()
                self.z_acc[a] = b
                self.s_a()
                self.r_l()
                self.c_o(x)
            except:
                z1.configure(text="ERR")
        ctk.CTkButton(x, text="OK", fg_color=self.z_c["a"], command=z2).pack(pady=10)
        ctk.CTkButton(x, text="X", fg_color=self.z_c["a"], command=lambda: self.c_o(x)).pack(pady=5)
        self.s_o(x)

    def o_m(self, x):
        y = ctk.CTkFrame(self, width=250, height=200, fg_color=self.z_c["fg"])
        y.pack_propagate(False)
        ctk.CTkLabel(y, text=x, font=("Arial", 16), text_color=self.z_c["t"]).pack(pady=10)
        def z1():
            self.c_o(y)
            self.e_a(x)
        def z2():
            del self.z_acc[x]
            self.s_a()
            self.r_l()
            self.c_o(y)
        ctk.CTkButton(y, text="Изменить" if self.z_lang == "RU" else "Edit", fg_color=self.z_c["a"], command=z1).pack(pady=10)
        ctk.CTkButton(y, text="Удалить" if self.z_lang == "RU" else "Delete", fg_color="red", command=z2).pack(pady=10)
        ctk.CTkButton(y, text="X", fg_color=self.z_c["a"], command=lambda: self.c_o(y)).pack(pady=5)
        self.s_o(y)

    def e_a(self, x):
        y = ctk.CTkFrame(self, width=280, height=280, fg_color=self.z_c["fg"])
        y.pack_propagate(False)
        ctk.CTkLabel(y, text="Новое имя:" if self.z_lang == "RU" else "New Name:", text_color=self.z_c["t"]).pack(pady=5)
        y1 = ctk.CTkEntry(y)
        y1.insert(0, x)
        y1.pack(pady=5)
        ctk.CTkLabel(y, text="Новый ключ:" if self.z_lang == "RU" else "New Key:", text_color=self.z_c["t"]).pack(pady=5)
        y2 = ctk.CTkEntry(y)
        y2.insert(0, self.z_acc[x])
        y2.pack(pady=5)
        z1 = ctk.CTkLabel(y, text="", text_color="red")
        z1.pack(pady=2)
        def z2():
            a = y1.get().strip()
            b = y2.get().strip().replace(" ", "")
            if not a or not b:
                return
            try:
                pyotp.TOTP(b).now()
                del self.z_acc[x]
                self.z_acc[a] = b
                self.s_a()
                self.r_l()
                self.c_o(y)
            except:
                z1.configure(text="ERR")
        ctk.CTkButton(y, text="OK", fg_color=self.z_c["a"], command=z2).pack(pady=10)
        ctk.CTkButton(y, text="X", fg_color=self.z_c["a"], command=lambda: self.c_o(y)).pack(pady=5)
        self.s_o(y)

if __name__ == "__main__":
    app = App()
    app.mainloop()
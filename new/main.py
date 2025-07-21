from tkinter import colorchooser, filedialog, messagebox

import customtkinter as ctk
import qrcode
from customtkinter import CTkImage, CTkScrollableFrame
from PIL import Image
from pybrcode.pix import Pix

# Modo e tema
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Tipos de QR disponíveis
QR_TYPES = [
    "Texto livre",
    "Link/URL",
    "Telefone",
    "SMS",
    "E-mail",
    "Contato (vCard)",
    "Localização/Mapa",
    "Wi-Fi",
    "Evento (Calendário)",
    "WhatsApp",
    "Pix",
    "Dados Bancários (texto)",
]


class QRApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerador de QR Code Personalizado")
        self.geometry("500x720")
        self.minsize(400, 600)
        self.resizable(True, True)

        # Frame rolável que contém toda a UI
        self.scroll_frame = CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True)

        # Defaults
        self.qr_fg_color = "#000000"
        self.qr_bg_color = "#ffffff"
        self.logo_path = None
        self.qr_img = None

        # Dados de geração
        self.error_levels = {
            "L": qrcode.constants.ERROR_CORRECT_L,
            "M": qrcode.constants.ERROR_CORRECT_M,
            "Q": qrcode.constants.ERROR_CORRECT_Q,
            "H": qrcode.constants.ERROR_CORRECT_H,
        }

        self.setup_widgets()
        self.update_fields()

    def setup_widgets(self):
        # 1) Seletor de tipo
        top = ctk.CTkFrame(self.scroll_frame)
        top.pack(pady=8, fill="x", padx=10)
        ctk.CTkLabel(top, text="Tipo de QR Code:").grid(row=0, column=0, sticky="w")
        self.cb_type = ctk.CTkComboBox(
            top, values=QR_TYPES, command=lambda _: self.update_fields()
        )
        self.cb_type.set(QR_TYPES[0])
        self.cb_type.grid(row=0, column=1, padx=8, sticky="we")
        top.grid_columnconfigure(1, weight=1)

        # 2) Campos dinâmicos
        self.dynamic_frame = ctk.CTkFrame(self.scroll_frame)
        self.dynamic_frame.pack(pady=4, fill="x", padx=10)

        # 3) Aparência (cores & logo)
        custom = ctk.CTkFrame(self.scroll_frame)
        custom.pack(pady=6, fill="x", padx=10)

        # Cor do QR
        ctk.CTkLabel(custom, text="Cor do QR:").grid(row=0, column=0, sticky="w")
        ctk.CTkButton(custom, text="Escolher", command=self.choose_fg_color).grid(
            row=0, column=1, padx=4
        )
        ctk.CTkButton(custom, text="Remover", command=self.remove_fg_color).grid(
            row=0, column=2, padx=4
        )

        # Cor de Fundo
        ctk.CTkLabel(custom, text="Cor de Fundo:").grid(row=1, column=0, sticky="w")
        ctk.CTkButton(custom, text="Escolher", command=self.choose_bg_color).grid(
            row=1, column=1, padx=4
        )
        ctk.CTkButton(custom, text="Remover", command=self.remove_bg_color).grid(
            row=1, column=2, padx=4
        )

        # Logo
        ctk.CTkLabel(custom, text="Logo Central:").grid(row=2, column=0, sticky="w")
        ctk.CTkButton(custom, text="Selecionar Logo", command=self.choose_logo).grid(
            row=2, column=1, padx=4
        )
        ctk.CTkButton(custom, text="Remover", command=self.remove_logo).grid(
            row=2, column=2, padx=4
        )

        custom.grid_columnconfigure(1, weight=1)

        # 4) Opções avançadas (tamanho, borda, correção)
        opts = ctk.CTkFrame(self.scroll_frame)
        opts.pack(pady=4, fill="x", padx=10)

        # Tamanho
        ctk.CTkLabel(opts, text="Tamanho do QR (px):").grid(row=0, column=0, sticky="w")
        self.qr_size_var = ctk.IntVar(value=240)
        slider_size = ctk.CTkSlider(
            opts, from_=120, to=600, number_of_steps=24, variable=self.qr_size_var
        )
        slider_size.grid(row=0, column=1, sticky="we", padx=4)

        # Borda
        ctk.CTkLabel(opts, text="Borda:").grid(row=1, column=0, sticky="w")
        self.qr_border_var = ctk.IntVar(value=4)
        slider_border = ctk.CTkSlider(
            opts, from_=1, to=10, number_of_steps=9, variable=self.qr_border_var
        )
        slider_border.grid(row=1, column=1, sticky="we", padx=4)

        # Correção de erro
        ctk.CTkLabel(opts, text="Correção de erro:").grid(row=2, column=0, sticky="w")
        self.qr_error_var = ctk.StringVar(value="H")
        combo_err = ctk.CTkComboBox(
            opts, values=list(self.error_levels.keys()), variable=self.qr_error_var
        )
        combo_err.grid(row=2, column=1, sticky="w", padx=4)

        # Redefinir tudo
        btn_reset = ctk.CTkButton(
            opts, text="Redefinir Tudo", fg_color="red", command=self.reset_all
        )
        btn_reset.grid(row=3, column=1, pady=8, sticky="w")

        opts.grid_columnconfigure(1, weight=1)

        # 5) Botão gerar
        self.btn_generate = ctk.CTkButton(
            self.scroll_frame,
            text="Gerar QR Code",
            fg_color="green",
            command=self.generate_qrcode,
        )
        self.btn_generate.pack(pady=(12, 8))

        # 6) Preview e salvar
        ctk.CTkLabel(self.scroll_frame, text="Prévia:").pack()
        self.qr_canvas = ctk.CTkLabel(self.scroll_frame, text="")
        self.qr_canvas.pack(pady=6)
        self.btn_save = ctk.CTkButton(
            self.scroll_frame,
            text="Salvar QR Code",
            command=self.save_qrcode,
            state="disabled",
        )
        self.btn_save.pack(pady=8)

    def clear_dynamic(self):
        for w in self.dynamic_frame.winfo_children():
            w.destroy()

    def update_fields(self):
        self.clear_dynamic()
        t = self.cb_type.get()
        self.dynamic_inputs = {}

        def add(label, key, default=""):
            ctk.CTkLabel(self.dynamic_frame, text=label).pack(anchor="w", pady=(4, 0))
            e = ctk.CTkEntry(self.dynamic_frame)
            e.insert(0, default)
            e.pack(fill="x", padx=4, pady=(0, 4))
            self.dynamic_inputs[key] = e

        if t == "Texto livre":
            add("Texto:", "text")
        elif t == "Link/URL":
            add("URL:", "url")
        elif t == "Telefone":
            add("Número (+55...):", "phone")
        elif t == "SMS":
            add("Número (+55...):", "sms_num")
            add("Mensagem:", "sms_msg")
        elif t == "E-mail":
            add("E-mail:", "email")
            add("Assunto:", "subject")
            add("Mensagem:", "body")
        elif t == "Contato (vCard)":
            add("Nome:", "vcard_name")
            add("Telefone:", "vcard_phone")
            add("E-mail:", "vcard_email")
            add("Empresa:", "vcard_company")
        elif t == "Localização/Mapa":
            add("Latitude:", "lat")
            add("Longitude:", "lng")
        elif t == "Wi-Fi":
            add("SSID:", "wifi_ssid")
            add("Senha:", "wifi_pwd")
            add("Tipo (WPA/WEP):", "wifi_type", "WPA")
        elif t == "Evento (Calendário)":
            add("Título:", "evt_title")
            add("Local:", "evt_location")
            add("Início (YYYYMMDDTHHMM):", "evt_start")
            add("Fim (YYYYMMDDTHHMM):", "evt_end")
        elif t == "WhatsApp":
            add("Número (+55...):", "wa_num")
            add("Mensagem:", "wa_msg")
        elif t == "Pix":
            add("Chave Pix:", "pix_key")
            add("Nome do Recebedor:", "pix_name")
            add("Cidade:", "pix_city")
            add("Valor (opcional):", "pix_valor")
            add("Identificador (opcional):", "pix_txid")
            add("Descrição (opcional):", "pix_msg")
        elif t == "Dados Bancários (texto)":
            add("Banco:", "bank_name")
            add("Agência:", "bank_agency")
            add("Conta:", "bank_account")
            add("Titular:", "bank_holder")
            add("CPF/CNPJ:", "bank_doc")

    def choose_fg_color(self):
        c = colorchooser.askcolor(title="Cor do QR")[1]
        if c:
            self.qr_fg_color = c

    def remove_fg_color(self):
        self.qr_fg_color = "#000000"
        messagebox.showinfo("OK", "Cor do QR redefinida para preto.")

    def choose_bg_color(self):
        c = colorchooser.askcolor(title="Cor de Fundo")[1]
        if c:
            self.qr_bg_color = c

    def remove_bg_color(self):
        self.qr_bg_color = "#ffffff"
        messagebox.showinfo("OK", "Cor de fundo redefinida para branco.")

    def choose_logo(self):
        f = filedialog.askopenfilename(
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp")]
        )
        if f:
            self.logo_path = f

    def remove_logo(self):
        self.logo_path = None
        messagebox.showinfo("OK", "Logo removido.")

    def reset_all(self):
        self.qr_fg_color = "#000000"
        self.qr_bg_color = "#ffffff"
        self.logo_path = None
        self.cb_type.set(QR_TYPES[0])
        self.qr_size_var.set(240)
        self.qr_border_var.set(4)
        self.qr_error_var.set("H")
        self.update_fields()
        self.qr_canvas.configure(image=None, text="")
        self.btn_save.configure(state="disabled")

    def get_data_for_type(self, t):
        gi = lambda k: self.dynamic_inputs[k].get().strip()
        try:
            if t == "Texto livre":
                v = gi("text") or messagebox.showerror("Erro", "Preencha!")
                return v
            if t == "Link/URL":
                u = gi("url")
                if not (u.startswith("http://") or u.startswith("https://")):
                    return messagebox.showerror("Erro", "URL inválida!")
                return u
            if t == "Telefone":
                p = gi("phone") or messagebox.showerror("Erro", "Preencha!")
                return f"tel:{p}"
            if t == "SMS":
                return f"sms:{gi('sms_num')}:{gi('sms_msg')}"
            if t == "E-mail":
                return f"mailto:{gi('email')}?subject={gi('subject')}&body={gi('body')}"
            if t == "Contato (vCard)":
                return (
                    "BEGIN:VCARD\nVERSION:3.0\n"
                    f"FN:{gi('vcard_name')}\nORG:{gi('vcard_company')}\n"
                    f"TEL;TYPE=CELL:{gi('vcard_phone')}\nEMAIL:{gi('vcard_email')}\nEND:VCARD"
                )
            if t == "Localização/Mapa":
                return f"geo:{gi('lat')},{gi('lng')}"
            if t == "Wi-Fi":
                return (
                    f"WIFI:T:{gi('wifi_type')};S:{gi('wifi_ssid')};P:{gi('wifi_pwd')};;"
                )
            if t == "Evento (Calendário)":
                return (
                    "BEGIN:VEVENT\n"
                    f"SUMMARY:{gi('evt_title')}\nLOCATION:{gi('evt_location')}\n"
                    f"DTSTART:{gi('evt_start')}\nDTEND:{gi('evt_end')}\nEND:VEVENT"
                )
            if t == "WhatsApp":
                return (
                    f"https://wa.me/{gi('wa_num').replace('+','')}?text={gi('wa_msg')}"
                )
            if t == "Pix":
                d = {
                    k: gi(k)
                    for k in (
                        "pix_key",
                        "pix_name",
                        "pix_city",
                        "pix_valor",
                        "pix_txid",
                        "pix_msg",
                    )
                }
                if not all([d["pix_key"], d["pix_name"], d["pix_city"]]):
                    return messagebox.showerror(
                        "Erro", "Chave, nome e cidade obrigatórios!"
                    )
                return d
            if t == "Dados Bancários (texto)":
                return (
                    f"Banco: {gi('bank_name')}\nAgência: {gi('bank_agency')}\n"
                    f"Conta: {gi('bank_account')}\nTitular: {gi('bank_holder')}\nCPF/CNPJ: {gi('bank_doc')}"
                )
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        return None

    def generate_qrcode(self):
        t = self.cb_type.get()
        data = self.get_data_for_type(t)
        if data is None:
            return

        size = self.qr_size_var.get()
        border = int(self.qr_border_var.get())
        err = self.error_levels[self.qr_error_var.get()]

        # Gera o payload
        if t == "Pix":
            pix = Pix(
                chave=data["pix_key"],
                nome_recebedor=data["pix_name"][:25],
                cidade=data["pix_city"][:15],
                valor=data["pix_valor"] or None,
                info_adicional=data["pix_msg"] or None,
                txid=data["pix_txid"] or None,
            )
            payload = pix.payload
        else:
            payload = data

        # Monta o QRCode
        qr = qrcode.QRCode(version=1, error_correction=err, box_size=10, border=border)
        qr.add_data(payload)
        qr.make(fit=True)
        img = qr.make_image(
            fill_color=self.qr_fg_color, back_color=self.qr_bg_color
        ).convert("RGBA")

        # Logo no centro
        if self.logo_path:
            logo = Image.open(self.logo_path).convert("RGBA")
            logo.thumbnail((img.size[0] // 3, img.size[1] // 3), Image.LANCZOS)
            pos = ((img.width - logo.width) // 2, (img.height - logo.height) // 2)
            img.paste(logo, pos, mask=logo)

        self.qr_img = img
        self.tk_qr = CTkImage(img, size=(size, size))
        self.qr_canvas.configure(image=self.tk_qr, text="")
        self.btn_save.configure(state="normal")

    def save_qrcode(self):
        if not self.qr_img:
            return
        f = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG", "*.png")]
        )
        if f:
            self.qr_img.save(f)
            messagebox.showinfo("Sucesso", "Salvo!")


if __name__ == "__main__":
    app = QRApp()
    app.mainloop()

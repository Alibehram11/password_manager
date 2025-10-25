import sqlite3
import bcrypt
import os
from tkinter import *
from tkinter import messagebox
from datetime import datetime

# --- 1. GÜVENLİK VE VERİTABANI İŞLEMLERİ (Backend) ---

DB_NAME = 'sifreler_gui.db'

def veritabani_baglan():
    """SQLite veritabanına bağlantı kurar ve cursor ile conn nesnelerini döndürür."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    return conn, cursor

def tablo_kur(cursor):
    """Gerekli 'sifreler' tablosunu oluşturur (Eğer yoksa)."""
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sifreler (
        site TEXT NOT NULL,          
        kullanici_adi TEXT NOT NULL, 
        sifre_hash BLOB NOT NULL,     
        sifre_duzmetin BLOB NOT NULL,  
        PRIMARY KEY (site, kullanici_adi)
    )
    ''')

def sifre_hashle(sifre):
    """Verilen şifreyi bcrypt ile hash'ler."""
    sifre_bytes = sifre.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12) 
    sifre_hash = bcrypt.hashpw(sifre_bytes, salt)
    return sifre_hash

def sifreyi_coz_ve_goster(site, kullanici_adi):
    """Veritabanından şifrenin bytes halini çeker, çözer ve gösterir."""
    conn, cursor = veritabani_baglan()
    
    cursor.execute(
        "SELECT sifre_duzmetin FROM sifreler WHERE site = ? AND kullanici_adi = ?",
        (site, kullanici_adi)
    )
    sonuc = cursor.fetchone()
    conn.close()

    if sonuc:
        # Saklanan bytes veriyi tekrar string'e çeviriyoruz
        duz_metin_sifre = sonuc[0].decode('utf-8') 
        messagebox.showinfo(
            "Şifre Detayı", 
            f"Site: {site}\nKullanıcı: {kullanici_adi}\nŞifre: {duz_metin_sifre}"
        )
    else:
        messagebox.showerror("Hata", "Kayıt bulunamadı.")


# --- 2. ARAYÜZ İŞLEMLERİ (Frontend) ---

class SifreYoneticisiGUI:
    def __init__(self, master):
        self.master = master
        master.title("Güvenli Şifre Yöneticisi")
        master.geometry("500x550") 
        master.resizable(False, False)

        # Veritabanını hazırla
        conn, cursor = veritabani_baglan()
        tablo_kur(cursor)
        conn.close()
        
        # Stil Ayarları
        self.font_baslik = ('Arial', 14, 'bold')
        self.font_etiket = ('Arial', 10)

        # Arayüz Bileşenlerini Oluştur
        self.olustur_kayit_ekle_alani()
        self.olustur_liste_alani()
        self.listeyi_guncelle()

    def olustur_kayit_ekle_alani(self):
        # --- Kayıt Ekleme Çerçevesi ---
        self.ekle_frame = LabelFrame(self.master, text="Yeni Şifre Ekle", font=self.font_baslik, padx=15, pady=15)
        self.ekle_frame.pack(padx=10, pady=10, fill="x")

        # 1. Site Adı
        Label(self.ekle_frame, text="Site Adı:", font=self.font_etiket).grid(row=0, column=0, sticky=W, pady=5)
        self.site_entry = Entry(self.ekle_frame, width=30)
        self.site_entry.grid(row=0, column=1, padx=10)

        # 2. Kullanıcı Adı
        Label(self.ekle_frame, text="Kullanıcı Adı:", font=self.font_etiket).grid(row=1, column=0, sticky=W, pady=5)
        self.kullanici_entry = Entry(self.ekle_frame, width=30)
        self.kullanici_entry.grid(row=1, column=1, padx=10)

        # 3. Şifre
        Label(self.ekle_frame, text="Şifre:", font=self.font_etiket).grid(row=2, column=0, sticky=W, pady=5)
        self.sifre_entry = Entry(self.ekle_frame, width=30, show="*") 
        self.sifre_entry.grid(row=2, column=1, padx=10)

        # 4. Kaydet Butonu
        Button(self.ekle_frame, text="Kaydet", command=self.kaydetme_islevi, bg="green", fg="white").grid(row=3, column=0, columnspan=2, pady=10)

    def olustur_liste_alani(self):
        # --- Liste Alanı ---
        self.liste_frame = LabelFrame(self.master, text="Kayıtlı Şifreler", font=self.font_baslik, padx=10, pady=10)
        self.liste_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Listeyi tutacak Listbox ve Scrollbar
        self.listbox = Listbox(self.liste_frame, height=10, width=50, font=self.font_etiket)
        self.listbox.pack(pady=10, padx=10, side=LEFT, fill="both", expand=True)
        
        scrollbar = Scrollbar(self.liste_frame, orient=VERTICAL)
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        # Şifreyi Göster Butonu
        Button(self.liste_frame, text="Seçilen Şifreyi Göster", command=self.goster_islevi, bg="blue", fg="white").pack(pady=5, side=BOTTOM, fill='x')

    def kaydetme_islevi(self):
        """Kaydet butonuna basıldığında çalışır."""
        site = self.site_entry.get().strip()
        kullanici = self.kullanici_entry.get().strip()
        sifre = self.sifre_entry.get()

        if not site or not kullanici or not sifre:
            messagebox.showerror("Hata", "Tüm alanları doldurunuz!")
            return

        conn, cursor = veritabani_baglan()
        hashlenmis_sifre = sifre_hashle(sifre)

        try:
            # Hem hash'i hem de düz metni (bytes olarak) saklıyoruz
            cursor.execute(
                "INSERT INTO sifreler (site, kullanici_adi, sifre_hash, sifre_duzmetin) VALUES (?, ?, ?, ?)",
                (site, kullanici, hashlenmis_sifre, sifre.encode('utf-8')) 
            )
            conn.commit()
            messagebox.showinfo("Başarılı", f"'{site}' için şifre başarıyla kaydedildi.")
            
            # Alanları temizle ve listeyi güncelle
            self.site_entry.delete(0, END)
            self.kullanici_entry.delete(0, END)
            self.sifre_entry.delete(0, END)
            self.listeyi_guncelle()

        except sqlite3.IntegrityError:
            messagebox.showerror("Hata", f"'{site}' - '{kullanici}' kaydı zaten mevcut.")
        finally:
            conn.close()

    def listeyi_guncelle(self):
        """Veritabanındaki tüm kayıtları Listbox'a yükler."""
        self.listbox.delete(0, END) # Listeyi temizle
        conn, cursor = veritabani_baglan()
        
        cursor.execute("SELECT site, kullanici_adi FROM sifreler ORDER BY site ASC")
        kayitlar = cursor.fetchall()
        conn.close()
        
        for site, kullanici in kayitlar:
            self.listbox.insert(END, f"[{site}] - Kullanıcı: {kullanici}")

    def goster_islevi(self):
        """Listbox'ta seçilen öğenin şifresini gösterir."""
        try:
            secili_index = self.listbox.curselection()[0]
            secili_deger = self.listbox.get(secili_index)

            # Değerden Site ve Kullanıcı Adını ayıkla
            # Örn: [Google] - Kullanıcı: ali.veli
            site = secili_deger.split(']')[0].strip('[')
            kullanici_adi = secili_deger.split('Kullanıcı:')[1].strip()
            
            # Şifreyi gösteren fonksiyonu çağır
            sifreyi_coz_ve_goster(site, kullanici_adi)

        except IndexError:
            messagebox.showerror("Hata", "Lütfen listeden bir kayıt seçiniz.")

# --- PROGRAM BAŞLANGICI ---
if __name__ == "__main__":
    
    # NOT: Verilerin kalıcı olması için dosya silme kodu kaldırılmıştır.
    # Verileriniz artık sifreler_gui.db dosyasında kalıcıdır.
        
    root = Tk()
    uygulama = SifreYoneticisiGUI(root)
    root.mainloop()

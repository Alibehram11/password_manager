import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class UltraPassManager:
    def __init__(self, master_password):
        self.salt_file = "salt.bin"
        self.data_file = "vault.bin"
        self.key = self._generate_key(master_password)
        self.fernet = Fernet(self.key)

    def _generate_key(self, password):
        # Eğer salt yoksa yeni oluştur, varsa eskisini kullan
        if os.path.exists(self.salt_file):
            with open(self.salt_file, "rb") as f:
                salt = f.read()
        else:
            salt = os.urandom(16)
            with open(self.salt_file, "wb") as f:
                f.write(salt)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def save_password(self, service, account_pass):
        # Mevcut verileri oku veya boş sözlük oluştur
        data = self.load_all()
        data[service] = account_pass
        
        # Veriyi şifrele ve kaydet
        encrypted_data = self.fernet.encrypt(str(data).encode())
        with open(self.data_file, "wb") as f:
            f.write(encrypted_data)
        print(f"✅ {service} için şifre güvenli bir şekilde kaydedildi.")

    def get_password(self, service):
        data = self.load_all()
        return data.get(service, "❌ Kayıt bulunamadı.")

    def load_all(self):
        if not os.path.exists(self.data_file):
            return {}
        try:
            with open(self.data_file, "rb") as f:
                encrypted_content = f.read()
            decrypted_content = self.fernet.decrypt(encrypted_content)
            return eval(decrypted_content.decode())
        except Exception:
            return "❌ Hata: Ana şifre yanlış veya veri bozulmuş!"

# --- KULLANIM ---
master = input("Ana Şifrenizi Belirleyin/Giriniz: ")
manager = UltraPassManager(master)

while True:
    islem = input("\n1-Şifre Ekle  2-Şifre Sorgula  3-Çıkış: ")
    if islem == "1":
        srv = input("Servis adı (örn: Gmail): ")
        pwd = input("Şifre: ")
        manager.save_password(srv, pwd)
    elif islem == "2":
        srv = input("Hangi servisin şifresi? ")
        print(f"Şifreniz: {manager.get_password(srv)}")
    else:
        break

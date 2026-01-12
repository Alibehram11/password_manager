# 🔐 UltraPass Pro: Gelişmiş Kriptografik Şifre Kasası

UltraPass Pro, kişisel verilerinizi ve hesap şifrelerinizi en yüksek güvenlik standartlarıyla yerel makinenizde saklamanız için tasarlanmış, Python tabanlı bir şifre yönetim sistemidir. **"Zero-Knowledge"** (Sıfır Bilgi) mimarisi sayesinde ana şifreniz hiçbir yerde saklanmaz.

---

## 🛡️ Güvenlik Özellikleri

Bu sistem, verilerinizi korumak için askeri düzeyde şifreleme ve modern anahtar türetme tekniklerini bir araya getirir.

### 1. Anahtar Türetme (PBKDF2)
Ana şifreniz (Master Password) doğrudan bir anahtar olarak kullanılmaz. 
- **Tuzlama (Salting):** Her kurulum için benzersiz 16 byte'lık bir `salt.bin` oluşturulur.
- **İterasyon:** Şifreniz, **SHA-256** algoritması kullanılarak **200.000 kez** işlenir. Bu süreç, kaba kuvvet (brute-force) saldırılarını imkansız hale getirir.



### 2. AES-256 Fernet Şifreleme
Verileriniz disk üzerinde her zaman şifreli (ciphertext) halde tutulur. Kullanılan Fernet yapısı, verilerin hem gizliliğini sağlar hem de veride herhangi bir değişiklik yapılıp yapılmadığını (bütünlük kontrolü) denetler.



---

## 🚀 Öne Çıkan Fonksiyonlar

- ✅ **Askeri Düzey Şifreleme:** AES-256 standardı ile tam koruma.
- ✅ **Kriptografik Şifre Üretici:** Tahmin edilmesi imkansız, yüksek entropili şifreler oluşturma.
- ✅ **Sıfır Bilgi Mimarisi:** Ana şifreniz bellekte tutulmaz ve hiçbir sunucuya gönderilmez.
- ✅ **Yerel Veritabanı:** Verileriniz tamamen sizin kontrolünüzdeki `vault.bin` dosyasında saklanır.

---

## 📦 Kurulum ve Çalıştırma

### Gereksinimler
Sistemi çalıştırmak için bilgisayarınızda Python 3.8+ yüklü olmalıdır.

### Adımlar
1. Gerekli kriptografi kütüphanesini yükleyin:
   ```bash
   pip install cryptography

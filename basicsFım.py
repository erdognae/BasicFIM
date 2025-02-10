import hashlib  
import time  
import os  

# İzlenmesi gereken dosyaların listesi

files_to_monitor = ["/etc/passwd", "/etc/shadow"]                   # Bu dosyalar, Linux sistemlerde hassas bilgilere sahiptir.
hash_dict = {}                                                      # Dosyaların başlangıçtaki hash değerlerini saklamak için bir sözlük (dictionary).

# Dosyanın hash değerini (SHA-256) hesaplayan fonksiyon
def get_file_hash(file_path): 
    with open(file_path, 'rb') as f:  # Dosyayı binary modda açıyoruz (sadece okunur).
        return hashlib.sha256(f.read()).hexdigest()  # Dosya içeriğini hashleyip SHA-256 hash değerini döndürüyoruz.

# Tüm dosyaların başlangıçtaki hash değerlerini hesaplayan ve saklayan fonksiyon
def initialize_hashes(): 
    for file in files_to_monitor:  # İzlenecek dosyalar üzerinde döngü.
        hash_dict[file] = get_file_hash(file)  # Her bir dosyanın hash değeri hesaplanıp hash_dict sözlüğüne ekleniyor.

# Dosya bütünlüğünü kontrol eden fonksiyon
def check_integrity(): 
    for file, initial_hash in hash_dict.items():  # İzlenen dosyaların başlangıç hash değerlerini kontrol ediyoruz.
        if not os.path.exists(file):  # Dosyanın var olup olmadığını kontrol et.
            print(f"{file} not found!")  
            continue  # Bir sonraki dosyaya geç.
        current_hash = get_file_hash(file)  # Dosyanın şu anki hash değerini hesapla.
        if current_hash != initial_hash:  # Hash değerleri eşleşmiyorsa dosyada değişiklik yapılmıştır.
            print(f"A change has been detected in {file}!")  # Değişiklik tespit mesajı yazdır.

# İlk olarak hash değerlerini hesapla ve kaydet
initialize_hashes()

# Sürekli izleme döngüsü
while True:
    try:
        check_integrity()
        time.sleep(3600)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
        break
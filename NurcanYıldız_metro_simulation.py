from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if id not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        # Geçerli ID kontrolü
        if baslangic_id not in self.istasyonlar:
            print("Başlangıç istasyonu geçersiz.")
            return None
        if hedef_id not in self.istasyonlar:
            print("Hedef istasyonu geçersiz.")
            return None

        basla = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        # BFS yapısı için kuyruk başlattım.
        # Kuyrukta mevcut_istasyon ve şu_ana_kadar_izlenen_yol tutuluyor.
        kuyruk = deque()
        kuyruk.append((basla, [basla]))

        # Ziyaret edilen istasyonlar, tekrar işlememek için burada tutulur
        ziyaret_edilen = set()
        ziyaret_edilen.add(basla.idx)

        while kuyruk:
            aktif, yol = kuyruk.popleft()

            # Eğer hedefe ulaştıysak, o ana kadar biriken yolu döndür
            if aktif.idx == hedef.idx:
                return yol

            # Komşu istasyonları sıraya ekliyoruz
            for komsu, _ in aktif.komsular:
                if komsu.idx not in ziyaret_edilen:
                    ziyaret_edilen.add(komsu.idx)
                    kuyruk.append((komsu, yol + [komsu]))

        # Hedefe ulaşılamadıysa None döner
        print("Bir yol bulunamadı.")
        return None


    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        # Geçerli ID kontrolü
        if baslangic_id not in self.istasyonlar:
            print("Başlangıç istasyonu geçersiz.")
            return None
        if hedef_id not in self.istasyonlar:
            print("Hedef istasyonu geçersiz.")
            return None

        basla = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        # min-heap heapq modülü ile sıralı şekilde işlenir.
        # toplam_sure, id, istasyon, rota
        oncelik_kuyrugu = [(0, id(basla), basla, [basla])]

        # Zaten işlenmiş olan istasyonlar, tekrar işlenmesin diye tutulur
        islenmis = set()

        while oncelik_kuyrugu:
            guncel_sure, _, mevcut, izlenen_yol = heapq.heappop(oncelik_kuyrugu)

            # Hedefe ulaştıysak sonuç döner
            if mevcut.idx == hedef.idx:
                return izlenen_yol, guncel_sure

            if mevcut.idx in islenmis:
                continue

            islenmis.add(mevcut.idx)

            # Komşular sıraya ekleniyor, süre toplanarak
            for komsu, gecis_suresi in mevcut.komsular:
                if komsu.idx not in islenmis:
                    yeni_sure = guncel_sure + gecis_suresi
                    heapq.heappush(oncelik_kuyrugu, (yeni_sure, id(komsu), komsu, izlenen_yol + [komsu]))

        print("Hedefe ulaşan bir rota bulunamadı.")
        return None

    def temiz_istasyon_adlari(rota: List[Istasyon]) -> List[str]:
        """Aynı istasyon adını art arda yazmamak için filtreleme yapar"""
        isimler = []
        onceki = None
        for istasyon in rota:
            if istasyon.ad != onceki:
                isimler.append(istasyon.ad)
                onceki = istasyon.ad
        return isimler


# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota)) 
        

    print("----NEW TESTS----")

    # Senaryo 4: Ulus'tan AŞTİ'ye (tek hat + aktarma)
    print("\n4. Ulus'tan AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("K2", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    else:
        print("Rota bulunamadı.")

    sonuc = metro.en_hizli_rota_bul("K2", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    else:
        print("Rota bulunamadı.")

    # Senaryo 5: Aynı başlangıç ve bitiş (Kızılay’dan Kızılay’a)
    print("\n5. Kızılay'dan Kızılay'a:")
    rota = metro.en_az_aktarma_bul("M2", "K1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    else:
        print("Rota bulunamadı.")

    sonuc = metro.en_hizli_rota_bul("M2", "K1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    else:
        print("Rota bulunamadı.")

    # Senaryo 6: Aynı hat üzerinde doğrudan (Demetevler -> OSB)
    print("\n6. Demetevler'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("K3", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    else:
        print("Rota bulunamadı.")

    sonuc = metro.en_hizli_rota_bul("K3", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    else:
        print("Rota bulunamadı.")

    # Senaryo 7: Geçersiz istasyon ID'si
    print("\n7. Geçersiz ID ile test (X1 -> OSB):")
    rota = metro.en_az_aktarma_bul("X1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    else:
        print("Rota bulunamadı.")

    sonuc = metro.en_hizli_rota_bul("X1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    else:
        print("Rota bulunamadı.")

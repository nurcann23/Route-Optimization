# Route-Optimization
# Sürücüsüz Metro Simülasyonu – Rota Optimizasyonu

Bu projede, bir metro ağı üzerinde iki istasyon arasındaki **en az aktarmalı** ve **en hızlı rotayı** bulmak için bir simülasyon geliştirdim. Grafik veri yapısı ve temel algoritmalar kullanarak, gerçek hayattaki ulaşım sistemlerine benzer bir yapı kurmaya çalıştım. Proje boyunca BFS ve A* algoritmalarını araştırarak uyguladım ve çeşitli test senaryolarıyla doğrulamasını yaptım.


## Kullanılan Teknolojiler ve Kütüphaneler

**Python 3.10+**  
**collections.deque** → BFS algoritmasında kuyruk yapısı için kullanıldı.  
  Kaynak: https://docs.python.org/3/library/collections.html  
**heapq** → A* algoritmasında öncelik sırasına göre istasyon seçimi yapabilmek için kullanıldı.  
  Kaynak: https://docs.python.org/3/library/heapq.html  
**typing** → Kodun okunabilirliği için `List`, `Optional`, `Tuple` gibi tip ipuçları kullanıldı.


## Algoritmaların Çalışma Mantığı

### BFS (Breadth-First Search) – En Az Aktarmalı Rota

BFS algoritması, bir grafikte başlangıç düğümünden itibaren tüm komşulara genişlik öncelikli olarak ulaşır. Bu sayede hedefe **en az adımda** (bu projede en az aktarma) ulaşılan rota bulunabilir.

Uygulamada:
Başlangıç istasyonu kuyruk yapısına eklenir (`deque`).
Her adımda istasyonun komşuları kontrol edilir.
Ziyaret edilen istasyonlar `set` ile tutulur.
Hedef istasyona ulaşıldığında rota döndürülür.

Kaynaklar:  
https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/  
https://www.youtube.com/watch?v=oDqjPvD54Ss


### A* Algoritması – En Hızlı Rota (Dakika Bazlı)

A* algoritması, her istasyonun **toplam maliyetini** (burada süre) hesaplayarak hedefe en kısa sürede ulaşan rotayı bulur. Bu projede `heuristic` kısmı basitleştirilmiş olup, doğrudan süre toplanarak Dijkstra benzeri bir yapı kurulmuştur.

Uygulamada:
`heapq` ile minimum süreye sahip istasyonlar öncelikli işlenir.
Rotalar liste olarak tutulur.
Ziyaret edilen istasyonlar `set` içinde saklanır.
Hedef bulunduğunda toplam süre ve rota döndürülür.

Kaynaklar:  
https://www.redblobgames.com/pathfinding/a-star/introduction.html  
https://www.geeksforgeeks.org/a-search-algorithm/


### Neden Bu Algoritmalar Kullanıldı?

**BFS**, aktarma sayısını minimize etmek için uygundur çünkü grafikteki adım sayısına odaklanır.
**A\*** (veya sadeleştirilmiş haliyle Dijkstra), zaman gibi ağırlıklı metriklerde en kısa süreli rotayı bulmak için tercih edilir.

Gerçek dünyada ulaşım sistemlerinde de bu iki kriter (aktarma sayısı ve süre) kritik olduğundan, bu algoritmalar en uygun seçim oldu.


## Örnek Kullanım ve Test Sonuçları

Kod çalıştırıldığında aşağıdaki gibi çıktılar elde edilmiştir:

1. AŞTİ'den OSB'ye:
En az aktarmalı rota: AŞTİ -> Kızılay -> Ulus -> Demetevler -> OSB
En hızlı rota (25 dakika): AŞTİ -> Kızılay -> Ulus -> Demetevler -> OSB

2. Batıkent'ten Keçiören'e:
En az aktarmalı rota: Batıkent -> Demetevler -> Gar -> Keçiören
En hızlı rota (21 dakika): Batıkent -> Demetevler -> Gar -> Keçiören

3. Keçiören'den AŞTİ'ye:
En az aktarmalı rota: Keçiören -> Gar -> Sıhhiye -> Kızılay -> AŞTİ
En hızlı rota (19 dakika): Keçiören -> Gar -> Sıhhiye -> Kızılay -> AŞTİ

4. Ulus’tan AŞTİ’ye:
En az aktarmalı rota: Ulus -> Kızılay -> AŞTİ
En hızlı rota (11 dakika): Ulus -> Kızılay -> AŞTİ

5. Kızılay’dan Kızılay’a:
En az aktarmalı rota: Kızılay -> Kızılay
En hızlı rota (2 dakika): Kızılay -> Kızılay

6. Demetevler’den OSB’ye:
En az aktarmalı rota: Demetevler -> OSB
En hızlı rota (8 dakika): Demetevler -> OSB

7. Geçersiz ID testi:
Başlangıç istasyonu geçersiz.
Rota bulunamadı.

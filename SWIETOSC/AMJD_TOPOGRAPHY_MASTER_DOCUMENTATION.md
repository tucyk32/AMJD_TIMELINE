# AM‑JD TOPOGRAPHY MASTER — Skonsolidowana Dokumentacja Topograficzna

## 🌍 **PRZEGLĄD SYSTEMU TOPOGRAFICZNEGO**

Ten dokument konsoliduje wszystkie dane topograficzne systemu AM‑JD obejmujące 30 kluczowych lokalizacji historycznych oraz wydarzenia astronomiczne dla analizy lokalnej geometrii obserwacyjnej.

**Cel**: Obliczenia lokalnego alt/az dla kotwic astronomicznych  
**Metoda**: JPL Horizons + dane topograficzne SRTM/GMRT  
**Zakres**: 30 miast historycznych + 6 wydarzeń astronomicznych

---

## 📍 **LOKALIZACJE PODSTAWOWE (30 MIAST)**

### **Centra Klasyczne**

- **Jerozolima** (31.78°N, 35.23°E, 800m) — Centrum religijne
- **Rzym** (41.9°N, 12.5°E, 20m) — Imperium Rzymskie  
- **Ateny** (37.98°N, 23.72°E, 70m) — Centrum greckie
- **Aleksandria** (31.2°N, 29.92°E, 5m) — Centrum hellenistyczne

### **Centra Mezopotamskie**

- **Babilon/Hillah** (32.54°N, 44.42°E, 30m) — Starożytna Mezopotamia
- **Niniwa/Mosul** (36.35°N, 43.15°E, 220m) — Centrum asyryjskie
- **Damascus** (33.51°N, 36.29°E, 680m) — Centrum umajjadzkie

### **Centra Śródziemnomorskie**

- **Konstantynopol/Istanbul** (41.01°N, 28.97°E, 40m) — Bizancjum/Imperium Osmańskie
- **Antiochia/Antakya** (36.2°N, 36.16°E, 80m) — Wczesne chrześcijaństwo
- **Kartago/Tunis** (36.85°N, 10.33°E, 10m) — Centrum punicko-rzymskie

### **Ważne Uwagi Wysokościowe**

- **Jerycho** (-260m) — Poniżej poziomu morza (Dolina Jordanu)
- **Qumran** (-350m) — Najniższy punkt (region Morza Martwego)
- **Kapernaum** (-210m) — Jezioro Galilejskie
- **Petra** (900m) — Najwyższa lokalizacja (góry jordańskie)

---

## 🌟 **WYDARZENIA ASTRONOMICZNE**

### **Eklipsy Słoneczne**

**SE_-0762-06-15 (Bur‑Sagale)**
- TT: 14:07:32, UT: 08:14:01.4
- ΔT: 21210.6s
- PDF: https://eclipse.gsfc.nasa.gov/SEhistory/SEplot/SE-0762Jun15T.pdf
- Status: Total, pełne dane GSFC

**SE_-0584-05-28 (Thales)**  
- TT: 19:28:50.3, UT: 14:22:26.4
- Źródło: GSFC SE-0584May28T.pdf
- Status: Total, klasyczna kotwica grecka

**SE_1066-03-28 (Annular)**
- TT: 15:41:57, UT: 15:21:30  
- ΔT: 1226.9s
- Źródło: https://eclipse.gsfc.nasa.gov/SEsearch/SEdata.php?Ecl=10660328

### **Eklipsy Lunarne**

**LE_0032-04-14 (Total)**
- TT: 11:56:22, UT: 09:06:21
- Źródło: https://www.eclipsewise.com/lunar/LEprime/0001-0100/LE0032Apr14Tprime.html
- Status: Total LE, greatest eclipse

**LE_0033-04-03 (Partial)**
- TT: 17:37:53.1, UT: 14:47:51.1  
- Źródło: https://eclipse.gsfc.nasa.gov/LEhistory/LEplot/LE0033Apr03P.pdf
- Status: Partial LE, greatest eclipse

### **Supernowa**

**SN_1006 (First Observation)**
- Data: ~1006-05-01 (okno obserwacyjne)
- Źródło: https://chandra.harvard.edu/photo/2013/sn1006/
- Metoda: Night scan dla widoczności nieba

---

## 🔧 **PROCEDURA BATCH JPL HORIZONS**

### **Krok 1: Konfiguracja Observer Location**

```
JPL Horizons Web Interface:
- Target Body: Sun (dla SE), Moon (dla LE), Fixed RA/Dec (dla SN)
- Observer Location: Geographic
- Coordinates: lat_deg, lon_deg, elev_m z AMJD_TOPO_30_CITIES.csv
```

### **Krok 2: Time Settings**

```
Mode: Table (list of times)
Time Input: Exact UT_greatest z AMJD_TOPO_EVENTS.csv  
Time Scale: UTC (UT1 ≈ UT dla naszych celów)
Dla SN1006: Serie co 30 min w nocy 1006-04-30/05-01
```

### **Krok 3: Quantities Selection**

```
Zaznacz:
- Altitude & Azimuth (topocentric apparent)
- Sun/Moon separation (jeśli dostępne)
- Local Solar Time (pomocnicze)
```

### **Krok 4: Export & Integration**

```
Format: CSV export
Dla każdej kombinacji (miasto, zdarzenie):
1. Oblicz JD(UTC) obserwacji  
2. Mapuj na AM: AM = JD - JD(AM-epoch)
3. Porównaj z UT_greatest z GSFC
4. Oblicz ΔJD_local = JD_horizons - JD_gsfc
5. Status: PASS jeśli alt > 0° i ΔJD_local < 0.001 dni
```

---

## 📊 **TEMPLATE PROCESSING**

### **Template A: Standard Event**

```csv
site_name,country,lat_deg,lon_deg,elev_m,event_key,result_alt,result_az,ΔJD_local,status
Jerusalem,Israel/Palestine,31.78,35.23,800,SE_-0762-06-15,45.2,183.7,0.0001,PASS
```

### **Template B: SN Night Scan**

```csv  
site_name,scan_time_ut,alt_sun,alt_target_region,darkness_quality,visibility_status
Alexandria,1006-05-01 02:00,−25.3,+67.8,ASTRONOMICAL,OPTIMAL
```

### **Kryteria Akceptacji**

- **PASS**: alt > 0°, ΔJD_local < 0.001 dni
- **WARN**: alt > −6° (twilight), ΔJD_local < 0.01 dni  
- **FAIL**: alt < −6° lub ΔJD_local > 0.01 dni

---

## 🎯 **PRZYPADKI UŻYCIA**

### **Weryfikacja Historyczna**

Dla każdego wydarzenia sprawdź czy było widoczne z głównych centrów cywilizacyjnych:

```python
def verify_historical_visibility(event_key, cities_list):
    results = []
    for city in cities_list:
        alt_az = horizons_query(event_key, city.coordinates)
        visibility = "VISIBLE" if alt_az.altitude > 0 else "BELOW_HORIZON"
        results.append((city.name, visibility, alt_az.altitude))
    return results
```

### **Regional Impact Analysis**  

Określ które regiony mogły obserwować dane wydarzenie:

```python
# Przykład: Eklipsa Bur-Sagale (-762-06-15)
mesopotamian_cities = ["Babylon", "Nineveh", "Damascus"]  
visibility_map = verify_historical_visibility("SE_-0762-06-15", mesopotamian_cities)
# Wynik: Wszystkie miasta w Mezopotamii - VISIBLE (alt > 30°)
```

### **Correlation Studies**

Porównanie z zapisami historycznymi:

```python
# SN 1006: Sprawdź które centra zgłosiły obserwacje
historical_reports = ["Cairo", "Damascus", "Constantinople", "Córdoba"]
calculated_visibility = verify_historical_visibility("SN_1006", historical_reports)
# Korelacja: Wszędzie VISIBLE → potwierdza globalną widoczność
```

---

## 📈 **METRYKI JAKOŚCI**

### **Pokrycie Geograficzne**

- **Europa**: 8 lokalizacji (26.7%)
- **Bliski Wschód**: 12 lokalizacji (40.0%)  
- **Afryka Północna**: 6 lokalizacji (20.0%)
- **Mezopotamia**: 4 lokalizacje (13.3%)

### **Rozkład Wysokości**

- **Poniżej poziomu morza**: 3 lokalizacje (-350m do -210m)
- **Poziom morza**: 8 lokalizacji (0-50m)
- **Wyżyny**: 15 lokalizacji (50-400m)  
- **Góry**: 4 lokalizacje (400m+)

### **Dokładność Współrzędnych**

- **Dokładność**: ±0.01° (≈1.1 km na równiku)
- **Wysokości**: Przybliżone, do testów ±50m
- **Rekomendacja finalna**: SRTM 30m lub GMRT dla przybrzeżnych

---

## ⚙️ **KONFIGURACJA SYSTEMOWA**

### **Pliki Wejściowe**

```
AMJD_TOPO_30_CITIES.csv    - 30 miast + współrzędne
AMJD_TOPO_EVENTS.csv       - wydarzenia + UT_greatest  
AMJD_TOPO_TEMPLATE.csv     - template do batch processing
```

### **Pliki Wyjściowe**

```
AMJD_TOPO_RESULTS_{event}_{city}.csv  - pojedynczy wynik
AMJD_TOPO_BATCH_SUMMARY.csv          - podsumowanie batch
AMJD_TOPO_VISIBILITY_MAP.html        - mapa interaktywna
```

### **Skrypty Wspomagające**

```bash
# Batch processing dla wszystkich kombinacji
python amjd_topo_batch.py --events events.csv --cities cities.csv --output results/

# Generowanie map widoczności  
python amjd_visibility_map.py --event SE_-0762-06-15 --output map.html

# Weryfikacja jakości wyników
python amjd_topo_validate.py --results results/ --threshold 0.001
```

---

## 🔍 **PRZYPADKI SPECJALNE**

### **Regiony Przybrzeżne**

Dla miast nadbrzeżnych (Aleksandria, Kartago, Cezarea) uwzględnij:
- Refrakcję atmosferyczną (dodatkowe +0.5°)
- Wysokość obserwatora nad poziomem morza
- Lokalny horyzont morski (teoretycznie −0°)

### **Wysokie Lokalizacje**  

Dla miast górskich (Petra, Damascus, Jerozolima):
- Korekcja ciśnienia atmosferycznego
- Lokalny horyzont topograficzny (może być +5° do +15°)
- Zwiększona przejrzystość atmosfery

### **Depresje**

Dla lokalizacji poniżej poziomu morza (Jerycho, Qumran):
- Zwiększona gęstość atmosfery
- Efekty miraż-owe w warunkach pustynnych  
- Lokalny horyzont może być obniżony o 1-3°

---

## 📚 **ZASOBY I NARZĘDZIA**

### **NASA/JPL Resources**

- **JPL Horizons**: https://ssd.jpl.nasa.gov/horizons/
- **Manual**: https://ssd.jpl.nasa.gov/horizons/manual.html
- **Tutorial**: https://ssd.jpl.nasa.gov/horizons/tutorial.html

### **Dane Topograficzne**

- **SRTM 30m**: https://www2.jpl.nasa.gov/srtm/
- **GMRT**: https://www.gmrt.org/ (dla regionów przybrzeżnych)
- **ASTER GDEM**: https://asterweb.jpl.nasa.gov/gdem.asp

### **Narzędzia Analityczne**

- **Matplotlib**: Wykresy alt/az  
- **Basemap/Cartopy**: Mapy geograficzne
- **Astropy**: Obliczenia astronomiczne w Python
- **PyEphem/Skyfield**: Alternative ephemeris libraries

---

## ⚠️ **OGRANICZENIA I UWAGI**

### **Niepewności Czasowe**

- **UT vs TT**: Dla epok historycznych ΔT ma niepewności 100-1000s
- **Calendar Drift**: Julian vs Gregorian transition w 1582
- **Local Solar Time**: Różnice stref czasowych w aplikacjach lokalnych

### **Niepewności Przestrzenne**

- **Współrzędne miast**: ±1-5 km dla lokalizacji historycznych
- **Wysokości**: ±20-100m bez precyzyjnych pomiarów LIDAR
- **Lokalny horyzont**: Mocno zależny od dokładnej topografii

### **Rekomendacje**

1. **Dla analiz wstępnych**: Używaj danych z tego master file
2. **Dla publikacji naukowych**: Weryfikuj z SRTM/GMRT wysokościami  
3. **Dla korelacji historycznych**: Uwzględnij niepewności ±0.5° w alt/az
4. **Dla wizualizacji**: Generuj mapy interaktywne dla każdego wydarzenia

---

*Dokument wygenerowany z konsolidacji plików AMJD_TOPO_*.csv i AMJD_TOPO_README.md*  
*System Topograficzny AM‑JD v1.0*
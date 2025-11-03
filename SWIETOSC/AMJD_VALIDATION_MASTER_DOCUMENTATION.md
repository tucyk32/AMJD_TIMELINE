# AM‑JD VALIDATION MASTER — Skonsolidowana Dokumentacja Walidacyjna

## 📋 **PRZEGLĄD SYSTEMOWY**

Ten dokument konsoliduje wszystkie pakiety walidacyjne systemu AM‑JD (Anno Mateusz - Julian Day) w jedną spójną całość. Łączy dane z pakietów GSFC, NASA/JPL, zapisów historycznych oraz dokumentacji topograficznej.

**Epoka AM**: `0001‑09‑01 00:00 UT` (Julian Calendar)  
**Zakres czasowy**: od -763 AM (763 BCE) do 1605 AM (1605 CE)  
**Źródła danych**: GSFC Eclipse Catalogs, JPL Horizons, Chinese/Japanese Records, Historical Chronicles

---

## 🎯 **METODOLOGIA WALIDACJI**

### **Klasy Statusów**
- **PASS**: Pełne dane TT/UT z NASA GSFC, ΔT obliczone, wszystkie parametry zweryfikowane
- **WARN**: Niepełne dane czasowe, wymaga dodatkowej weryfikacji lub doprecyzowania
- **FAIL**: Niespójności w danych, błędy kalkulacji lub źródłach  
- **DOCUMENTED**: Wydarzenia historyczne z zapisów, bez precyzyjnych czasów UT/TT
- **PENDING**: Oczekujące na uzupełnienie danych z kolejnych źródeł GSFC

### **Struktura Budżetu Niepewności**
```
σ_time_s = √(σ_ΔT² + σ_catalog² + σ_historical²)
gdzie:
- σ_ΔT: niepewność ΔT (Terrestrial Time - Universal Time)
- σ_catalog: niepewność katalogu (GSFC/JPL)  
- σ_historical: niepewność źródeł historycznych
```

---

## 📊 **PAKIETY DANYCH ŹRÓDŁOWYCH**

### **PAKIET MASTER** (Źródło: AMJD_VALIDACJA_MASTER_AM.csv)
Główne kotwice astronomiczne z pełnymi danymi GSFC:
- Eklipsy lunarne: -0003‑03‑13, 0032‑04‑14, 0033‑04‑03
- Eklipsy słoneczne: -0762‑06‑15 (Bur‑Sagale), -0584‑05‑28 (Thales)  
- Komety Halleya: -0011‑10‑05, 1066‑03‑23
- Supernowe: SN 1006, SN 1054, SN 1181, SN 1572, SN 1604
- Wydarzenia specjalne: VAT4956 aurora (-0566‑03‑12)

### **PAKIET 3** (SN Modern Era)
Supernowe epoki średniowiecza i renesansu:
- SN 1181 (Chińskie/Japońskie zapisy)
- SN 1572 Tycho (pre‑reforma kalendarzowa)  
- SN 1604 Kepler (post‑reforma Gregoriańska)
- Halley -239 (najwcześniejszy zapis Shiji)

### **PAKIET 4** (Halley Pre‑Modern)
Aparycje komety Halleya przed erą precyzyjnych obserwacji:
- Aparycja 837 (rok‑only, placeholder mid‑year)
- Aparycja 912 (rok‑only, placeholder mid‑year)

### **PAKIET 5** (Candidates & Pending)
Wydarzenia wymagające dalszej weryfikacji:
- LE 1 BCE (kandydat Herodian)
- SE 1066‑08‑01 (Europa, zapisy kronik)

### **PAKIET 6** (Quality Assurance)
Pełne dane jakościowe z flagami PASS/WARN/FAIL:
- Kontrola jakości dla głównych eklips lunarnych
- Weryfikacja spójności ΔT z katalogami GSFC
- Analiza niepewności dla mapowania AM

---

## 🔍 **ANALIZA KLUCZOWYCH WYDARZEŃ**

### **Eklipsa Bur‑Sagale (-762‑06‑15)**
```
TT: 14:07:32.0
UT: 08:14:01.4  
ΔT: 21210.6 s
AM: -763 AM, Dec 06 08:14:01.400
Status: PASS
```
Kotwica asyryjska z precyzyjnymi danymi GSFC. Kluczowe dla datowania rejonów Mezopotamii.

### **Eklipsa Talesa (-584‑05‑28)**
```
TT: 19:28:50.3
UT: 14:22:26.4
ΔT: 18383.9 s  
AM: -585 AM, Jan 02 14:22:26.400
Status: PASS
```
Klasyczna kotwica grecka. Bitwa Lydów i Medów według Herodota.

### **Kometa Halleya 1066**
```
Perihelion: 1066‑03‑23
AM: 1066 AM, Dec 14 00:00:00.000
Status: DOCUMENTED
```
Aparycja poprzedzająca bitwę pod Hastings. Zapisy w Chronicle of Bayeux Tapestry.

### **SN 1006**
```
First Sighting: ~1006‑05‑01
AM: 1006 AM, Jan 07 00:00:00.000
Status: DOCUMENTED
```
Najjaśniejsza supernowa w historii. Zapisy z Egiptu, Chin, Japonii, Europy.

---

## 🌍 **INTEGRACJA TOPOGRAFICZNA**

System AM‑JD integruje dane walidacyjne z 30 kluczowymi lokalizacjami historycznymi:

**Centra Klasyczne**: Jerozolima, Rzym, Aleksandria, Ateny, Konstantynopol  
**Centra Mezopotamskie**: Babilon, Niniwa, Damascus  
**Centra Fenickie**: Tyr, Sydon, Byblos  
**Centra Egipskie**: Memfis, Teby, Kair

### **Procedura Topograficzna**
1. **JPL Horizons**: Obliczenia alt/az dla każdego miasta w momencie UT_greatest
2. **Weryfikacja widoczności**: Status PASS dla alt > 0°
3. **Mapowanie lokalne**: ΔJD_local dla korekcji topograficznych
4. **Integracja AM**: Przeliczenie na lokalny czas AM dla każdej lokalizacji

---

## 📈 **WSKAŹNIKI JAKOŚCI**

### **Dystrybucja Statusów**
- **PASS**: 45% (pełne dane GSFC/JPL)
- **DOCUMENTED**: 35% (zapisy historyczne)  
- **PENDING**: 15% (oczekujące na weryfikację)
- **WARN**: 5% (wymagające uwagi)

### **Pokrycie Czasowe**
- **Era Antyczna** (-763 do 0 AM): 8 wydarzeń kluczowych
- **Era Wczesnochrześcijańska** (0 do 500 AM): 4 wydarzenia
- **Era Średniowieczna** (500 do 1200 AM): 6 wydarzeń  
- **Era Późnośredniowieczna** (1200+ AM): 4 wydarzenia

### **Niepewności Typowe**
- **Eklipsy GSFC**: ±1-5 sekund (UT)
- **Wydarzenia historyczne**: ±1-30 dni
- **Perihelia komet**: ±3-7 dni (pre‑837)
- **Supernowe**: ±7-14 dni (pierwsze obserwacje)

---

## 🔧 **UŻYCIE PRAKTYCZNE**

### **Komenda Walidacji**
```bash
python amjd_validator.py --input validation_master.csv --mode full --output validation_report.html
```

### **API Zapytań**
```python
import amjd_system

# Pobierz wydarzenie po kluczu
event = amjd_system.get_event("SE_-0762_BurSagale")
print(f"AM Date: {event.am_full}")
print(f"Status: {event.status}")

# Mapowanie JD -> AM
am_date = amjd_system.jd_to_am(1442902.84307)
print(f"AM: {am_date}")  # Output: -763 AM, Dec 06 08:14:01.400
```

### **Eksport Raportów**
System generuje raporty w formatach:
- **CSV**: Dane surowe do analizy
- **HTML**: Raporty interaktywne z wykresami
- **PDF**: Dokumentacja formalna
- **JSON**: API endpoints dla aplikacji

---

## 📚 **ŹRÓDŁA I REFERENCJE**

### **Katalogi Astronomiczne**
- **NASA GSFC**: Five Millennium Solar Eclipse Catalog
- **NASA GSFC**: Lunar Eclipse Catalog  
- **JPL Horizons**: Ephemeris calculations
- **EclipseWise**: Fred Espenak eclipse predictions

### **Źródła Historyczne**
- **Chińskie kroniki**: Shiji, Tang shu, Song shi
- **Asyryjskie tablice**: Bur‑Sagale eclipse record
- **Greckie źródła**: Herodot, Tukidydes, Ksenofon
- **Europejskie kroniki**: Bayeux Tapestry, Saxon Chronicle

### **Literatura Naukowa**
- Stephenson, F.R. (2004): "Aurora observations in ancient China", A&G 45  
- Kiang, T. (1972): "The past orbit of Halley's Comet", MNRAS 160
- Morrison, L.V. & Stephenson, F.R. (2004): "Historical values of the Earth's clock error ΔT", JHA 35

---

## ⚠️ **UWAGI METODOLOGICZNE**

1. **ΔT Evolution**: Wartości ΔT dla epok historycznych mają niepewności 100-1000s
2. **Calendar Systems**: Przejście Julian→Gregorian (1582) wymaga uwagi przy datowaniu
3. **Coordinate Systems**: ICRS dla katalogów modern, FK4 dla danych historycznych pre‑1950
4. **Time Scales**: UTC/UT1 różni się od TT; uwzględnić ΔT w obliczeniach precyzyjnych

---

*Dokument wygenerowany automatycznie z konsolidacji pakietów AMJD_VALIDACJA_PAKIET*.csv*  
*Ostatnia aktualizacja: System Konsolidacji v1.0*
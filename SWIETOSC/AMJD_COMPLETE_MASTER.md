# AM‑JD — COMPLETE MASTER DOCUMENTATION

**Cel**: Jedno spójne źródło prawdy o systemie AM‑JD — co to jest, jak liczy, jakie przyjmuje konwencje, jak go testować, jak go falsyfikować i jak integrować z efemerydami NASA/JPL. Zero mgły, sama mechanika.

_Wersja:_ Master Consolidated · _Zbudowano:_ 2025-11-02 · _Autor systemu:_ Mateusz (AM) · _Format:_ Markdown

---

## 0) TL;DR — o co chodzi w AM‑JD
- **AM** = dowolna skala „Anno Mundi/Anno Mateusz" z przesunięciem względem JD: `AM = JD + C` (stała `C`).  
- **JD** = Julian Day (ciągły licznik dni, doba liczona od **południa** UT).  
- **Idea:** Mapujesz **cywilny zapis daty** → `JD_record`, a **astronomiczne zjawisko** → `JD_ephem`. Porównujesz `ΔJD = JD_record − JD_ephem`. Jeśli |ΔJD| ≤ **tolerancja**, zapis jest **spójny**.
- **Inwariancja offsetu:** stała `C` **znosi się** w różnicy (`(JD+C)-(JD'+C)=JD-JD'`). Dlatego spory o „epoki/etykiety" są poza matematyką rdzenia.

---

## 1) Kanon konwencji (AM‑JD Canon)
**Po co kanon?** Żeby wszyscy liczyli tak samo i wyniki były replikowalne.

1. **Skala czasu:** UT (dla dat cywilnych). Do efemeryd możesz użyć TT/TDB (zwracaj uwagę na ΔT).
2. **Epoka JD:** `midnight` w praktyce raportowania → 00:00 UT ma ułamek **.5** (bo „prawdziwy" JD zmienia się w południe).  
3. **Numeracja lat:** **astronomiczna** (1 BCE = 0; 2 BCE = −1; …).  
4. **Kalendarz cywilny:** do 1582‑10‑15 **juliański**, potem **gregoriański** (z lokalnym dniem przyjęcia, jeśli istotne).  
5. **Styl doby:** jeśli źródło liczy dobę **od północy** → dodaj `jd_offset = +0.5`. Jeśli od **zachodu** → zastosuj właściwą frakcję w zależności od godziny zachodu (jeśli brak — oceń tolerancją ±1 d).  
6. **Tolerancje:** `PASS` |ΔJD| ≤ 0.5 d; `WARN` 0.5–5 d; `FAIL` > 5 d.  
7. **Zasada jawności:** publikuj ścieżkę: **kalendarz → (y,m,d) → JDN → JD + offset**, oraz **godzinę**, jeśli ją znasz.

> ***Gwiazdkowa ściąga błędów***  
> ★ Południe vs północ JD → ustaw epokę raportową **midnight** (00:00 UT ⇒ +0.5).  
> ★ Rok 0 → w astronomii **istnieje**; w historii nie. Licz na numeracji astronomicznej.  
> ★ Kalendarz → **juliański** dla starożytności; proleptyczny gregoriański daje przesunięcia.  
> ★ Święta hebrajskie → mapuj **Hebrew → (lokalny) juliański → JD** i jawnie deklaruj ΔT/widzialność.

---

## 1.1) Zakres ważności i klasy jakości

**AM-JD** to instrument. Nie tworzy faktów – **odsłania spójność** (albo jej brak).
**PASS** gdy mamy twarde kotwice (GSFC, Horizons). **WARN** gdy wchodzą modele (ΔT w antyku), brak godziny lub integracje komet przed 837 n.e. **FAIL** gdy hipoteza nie przechodzi przez geometrię albo przez własne założenia. Dane biblijne trzymamy w warstwie interpretacyjnej z pełnym **„łańcuchem założeń"**.
**Wartość**: powtarzalność i audytowalność. **Granica**: źródła pierwotne (ich jakość wyznacza nasz σ).

### Klasy jakości (pole `status`):

- **PASS** — moment zdarzenia określony w **TT** i/lub **UT/UT1** z renomowanego katalogu (np. GSFC), **JD_TT/JD_UT** policzone.
- **WARN** — brak godziny lub ΔT z modelu; wpis dostaje **zakres**: `JD_min–JD_max` i/lub `σ_time`.
- **FAIL** — hipoteza niezgodna z geometrią/efemerydą w zadanym modelu ΔT (ΔJD przekracza próg).

### Budżet niepewności (pole `sigma_time_s`):

- **Eklipsy GSFC**: niepewność praktycznie zerowa względem wybranej ΔT; jeśli ΔT pochodzi z modelu (antyk), podajemy **σ_ΔT** wg Stephenson-Morrison.
- **Komety Halley'a < 837**: wpisujemy **±1–3 d** (przegląd źródeł + integracje Yeomans & Kiang).
- **Supernowe**: domyślnie **±0,5 d** (dzień bez godziny); większy zakres, jeśli źródła niezgodne.

### Skale czasu:

- **TT = TAI + 32,184 s**; **UT/UT1** wiąże się z rotacją Ziemi (nierównomierną); **ΔT = TT − UT1**; geometrię efemeryd liczymy w **TT/TDB** (Horizons). W CSV trzymamy **obydwa JD** (TT i UT), żeby nie mieszać analiz.

### Reguły dla różnych typów źródeł:

**Eklipsy (GSFC/EclipseWise) → PASS**
- Używamy momentu *Greatest* w **TT** i **UT/UT1** + **ΔT = TT−UT** z tabel/algorytmów GSFC. To są najlepsze dostępne dane obserwacyjne i rekonstrukcje dla ostatnich 5 tys. lat.

**ΔT przed ~700 p.n.e. → WARN (model), nie „pomiar"**
- W starożytności ΔT odtwarza się z opisów zaćmień; precyzja dramatycznie spada wraz z cofnięciem w czasie. Dla zaćmienia asyryjskiego (−762) ΔT rzędu **~21 000 s** traktujemy jako **modelowy** punkt pracy, nie obserwację.

**Komety przed 837 n.e. (szczególnie 1P/Halley) → WARN**
- Orbita Halley'a jest dobrze kontrolowana dopiero od powrotu **837 n.e.**; bardzo bliskie zbliżenie do Ziemi w 837 (min. ~0,04 AU) rozrywa stabilność integracji do wcześniejszych epok.

**Supernowe historyczne → zwykle tylko data dzienna (WARN)**
- SN 1006 i SN 1054 mają świetne relacje (Chiny/Japonia/świat arabski), ale **godzin brak**; da się odtworzyć zakres dobowy i długość widoczności, nie „18:34 UT".

**Wydarzenia biblijne → warstwa interpretacyjna (WARN/FAIL zależnie od hipotezy)**
- „Spór o Heroda" (4 p.n.e. vs 1 p.n.e.) zależy od interpretacji Józefa Flawiusza i doboru zaćmienia towarzyszącego; system ma pokazać **oba warianty** jako hipotezy, nie rozstrzygać.

---

## 2) Errata (typowe źródła błędów)

1. **Południe vs północ JD** — JD domyślnie zmienia się w południe UT. W praktyce stosuj epokę **midnight** (00:00 UT ⇒ JD +0.5), aby etykiety „00:00" były spójne.

2. **Rok 0** — w astronomii rok 0 istnieje (1 BCE=0, 2 BCE=−1...). W historii nie. W obliczeniach używaj **roku astronomicznego**.

3. **Kalendarz** — dla dat < 1582‑10‑15 używaj **kalendarza juliańskiego**. Proleptyczny gregoriański daje błędy rzędu dni–tygodni.

4. **Święta hebrajskie (np. 14 Nisan)** — wymagają konwersji: **Hebrew → lokalny cywilny juliański → JD** z jawnym modelem ΔT i regułą widzialności.

**Noty stosowania**
- Publikuj **ścieżkę konwersji** i **godzinę**; brak godziny = 00:00 UT.
- Dla dat proroczych podawaj też konwersję **gregoriańską**.

---

## 3) Definicje i warstwy
- **JD/JDN**: JDN = część całkowita JD. JD to JDN ± frakcja doby (południowy start).
- **Warstwa roczna** (dendro/¹⁴C/lód) → mówi „rok/okno/sezon".  
- **Warstwa kalendarzowa** → reguły kulturowe (proleptyka, interkalacje, początek doby/roku).  
- **Warstwa dzienna** → redukcja zapisu do `JD_record`.  
- **Weryfikacja** → efemeryda (`JD_ephem`) vs `JD_record`: liczysz `ΔJD`.

**Zakaz**: mieszania rocznej z dzienną **bez** przejścia przez warstwę kalendarzową — to tworzy pseudo‑konflikty.

---

## 4) Algorytm mapowania „zapis → JD_record"
**Wejście:** `(calendar, year, month, day, jd_offset)`  
**Wyjście:** `JD_record = JDN(calendar, y,m,d) + jd_offset`

**Fliegel–Van Flandern (JDN):**
```text
# Gregoriański
a = (14 - m) // 12
y2 = y + 4800 - a
m2 = m + 12a - 3
JDN = d + (153m2 + 2)//5 + 365y2 + y2//4 - y2//100 + y2//400 - 32045

# Juliański
a = (14 - m) // 12
y2 = y + 4800 - a
m2 = m + 12a - 3
JDN = d + (153m2 + 2)//5 + 365y2 + y2//4 - 32083
```

**Epoka raportowa `midnight`:** Jeśli wpis jest „00:00 UT (cywilnie)", dodaj **+0.5** do JDN, by dostać JD.

**Inwariancja offsetu (dowód w 1 linijce):**  
`(JD_record + C) − (JD_ephem + C) = JD_record − JD_ephem` → różnice **nie zależą** od wyboru epoki/etykiet.

---

## 5) Walidacja na efemerydach NASA/JPL
**Cel:** nie „wiara", lecz **liczby**. Procedura minimalna:
1. Z mapowanego zapisu wylicz `JD_record` (zgodnie z Kanonem).  
2. Z **JPL Horizons/GSFC** pobierz czasy zjawiska (UT/TT) i przelicz na `JD_ephem`.  
3. Policz `ΔJD` i oceń względem tolerancji.  
4. Udokumentuj: skala czasu (UT/TT/TDB), ΔT jeśli użyte, lokalizacja obserwatora.

**Przykładowe kotwice:**
- **0033‑04‑03 (jul.)** — częściowe **zaćmienie Księżyca** (maks. ~14:55:49 UT) → `JD_ephem ≈ 1733204.622`.  
- **0066‑01‑26 (jul.)** — peryhelium **komety Halleya** (powrót 66 CE); obserwacje do marca/kwietnia.  
- **Potrójna koniunkcja Jowisz–Saturn, 7 BCE** — trzy okna (maj, wrzesień, grudzień).

---

## 6) Harness testowy (replikowalność)
**Format wejścia CSV:** `id,event,calendar,year,month,day,jd_ephem,jd_offset,notes`  
- `calendar`: „Julian"/„Gregorian" (jawnie, bez magii 1582).  
- `year`: **astronomiczny**.  
- `jd_offset`: zwykle `0.5` gdy doba „od północy".

**Statusy:** `PASS` jeśli |ΔJD| ≤ tolerancja; `WARN` gdy brak precyzyjnej godziny lub źródło niepewne; `FAIL` gdy |ΔJD| > 5d lub hipoteza niezgodna z efemerydą.

### Rozszerzone pola CSV dla kontroli jakości

**Podstawowe:** `id,event,calendar,year,month,day,jd_ephem,jd_offset,notes`
**Dodatkowe dla kontroli jakości:**
- `status` — PASS/WARN/FAIL  
- `sigma_time_s` — niepewność w sekundach (np. 43200 = ±0.5d)
- `dt_model` — model ΔT (np. "Stephenson-Morrison")
- `dt_source_url` — źródło danych ΔT
- `date_kind` — typ daty (exact_time/day_only/year_only)
- `source_quality` — GSFC/literature/model/hypothesis

**Linie komend (pojedyncze, zgodnie z Twoją preferencją):**
- **PowerShell:** `python .\am_jd_test_harness.py .\cases.csv .\results.csv 1.0`  
- **CMD:** `python am_jd_test_harness.py cases.csv results.csv 1.0`  
- **Bash/WSL:** `python am_jd_test_harness.py cases.csv results.csv 1.0`  
- **VS Code:** `python am_jd_test_harness.py cases.csv results.csv 1.0`

**Kryterium zaliczenia:** ≥ **90% PASS** przy progu |ΔJD| ≤ **1.0 d**.

---

## 7) Przykłady historyczne z diagnostyką
> Uwaga: poniżej **schemat** prezentacji. Tabele referencyjne i pełne wyprowadzenia w sekcjach walidacyjnych.

### 7.1 Narodziny (5 XII 7 BCE, jul. 00:00 UT)
- `JD_record = 1719205.0` (midnight ⇒ +0.5)  
- Etykieta „oczekiwana" była `1719570.5` → **ΔJD = −365.5 d**  
- ★ **Uwaga (rok 0):** 7 BCE = **astron. −6**. Licz w **juliańskim** dla starożytności.  
- **Dlaczego juliański:** bo to ściśle cywilny kalendarz epoki; proleptyczny gregoriański fałszuje dzień.

**Obliczenie (Meeus, kroki):**
- D = d + 0.5 = 5.5
- Jeśli m ≤ 2 ⇒ Y'=-6, M'=12
- B = 0 (dla kalendarza juliańskiego)
- term1 = int(365.25 × (Y' + 4716)) = 1720327
- term2 = int(30.6001 × (M' + 1)) = 397
- JD = term1 + term2 + D + B − 1524.5 = **1719205.0**

### 7.2 Ukrzyżowanie a zaćmienie (0033‑04‑03, jul.)
- `JD_ephem (max LUN eclipse) ≈ 1733204.622` (GSFC/JPL)  
- Jeśli chcesz dowiązać wydarzenie — data cywilna musi przejść przez **reguły żydowskie** → lokalny juliański → JD.  
- ★ **Uwaga (epoki/TT):** do porównań z efemerydą dokumentuj **UT/TT/TDB** i ΔT.

### 7.3 Halley 66 CE (okno widoczności a TP)
- `TP` (peryhelium) ~ **66‑01‑26 (jul.)**, obserwacje także **marzec–kwiecień**.  
- Wpis **25‑03‑66** leży w oknie po TP → sensowne `ΔJD`.

### 7.4 Zdarzenia nie‑astronomiczne (np. 70 CE)
- JPL nie „potwierdza" dat historycznych bez zjawisk; tu stosujesz tylko **warstwę kalendarzową** i spójność AM↔JD.

---

## 8) Pakiety walidacyjne

### 8.1 Walidacja z NASA GSFC – zestaw 3–5 + Halley 66 + SN1054

**Konwencje**: daty przed 1582 w kalendarzu juliańskim; czasy największej fazy zaćmień w skali TT (GSFC), UT=TT−ΔT.

| key              | label                                                            | calendar   | julian_date   | TT_time   | UT_time      |   ΔT_s |         JD_TT |         JD_UT | notes                                                                                                                   |
|:-----------------|:-----------------------------------------------------------------|:-----------|:--------------|:----------|:-------------|-------:|--------------:|--------------:|:------------------------------------------------------------------------------------------------------------------------|
| E1_4BCE_LunarEcl | Lunar eclipse (partial) — 13 Mar 4 BCE (astronomical year −0003) | Julian     | -0003-03-13   | 03:37:06  | 00:41:04.000 |  10562 |   1.72003e+06 |   1.72003e+06 | GSFC Five Millennium Catalog row −0003‑03‑13 with ΔT=10562 s (TT of greatest eclipse).                                  |
| E2_32CE_LunarEcl | Lunar eclipse (total) — 14 Apr 32 CE                             | Julian     | 0032-04-14    | 11:56:36  | 09:06:24.000 |  10212 |   1.73285e+06 |   1.73285e+06 | GSFC 0001–0100 catalog row 0032‑04‑14 with ΔT=10212 s (TT of greatest eclipse).                                         |
| E3_33CE_LunarEcl | Lunar eclipse (partial) — 3 Apr 33 CE                            | Julian     | 0033-04-03    | 17:37:53  | 14:47:51.000 |  10202 |   1.7332e+06  |   1.7332e+06  | GSFC 0001–0100 catalog row 0033‑04‑03 with ΔT=10202 s (TT of greatest eclipse).                                         |
| E4_Halley66CE    | Halley's Comet — perihelion AD 66 (historical reconstructions)   | Julian     | 0066-01-26    |           |              |    nan | nan           | nan           | Perihelion epoch uncertain pre‑837; Holetschek set T≈66 Jan 26.5; Kiang (1972) discusses range (Jan 26.5 to early Feb). |
| E5_SN1054        | SN 1054 (Crab) — first sighting in Chinese records               | Julian     | 1054-07-04    |           |              |    nan | nan           | nan           | Exact time-of-day not preserved; provide date only.                                                                     |

### 8.2 MASTER: Batch GSFC (LE/SE) + Anchors

**Assumptions**
- Calendar on GSFC pages: *Julian* before 1582-10-15, *Gregorian* afterwards. We keep the same.
- Times labelled **TT (TD)** are Terrestrial Time; **UT** computed as TT − ΔT (seconds).
- AM epoch = 0001-09-01 (Julian) 00:00:00 = AM day 0. AM year runs Sep 1 → Aug 31.
- For non-eclipse anchors (SN 1006, VAT 4956) exact times are unknown → status = WARN.

**PASS/WARN/FAIL**
- PASS = GSFC gives TD and ΔT; UT derived deterministically.
- WARN = time uncertain or placeholder (needs Horizons/topocentric fit).
- FAIL = insufficient fields to compute UT/JD.

| tag | kind | Date (Y-M-D) [cal] | TT | ΔT [s] | UT | JD(UT) | AM idx | AM date (Y_AM, M, D) | status | note |
|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| AssyrianEclipse | SE | 00-762-06-15 [julian] | 14:07:32.000 | 21210.6 | 08:14:01.400 | 1442902.8430717592 | -278764 | 00-763, 06, 15 | PASS | Assyrian Eponym Canon anchor. |
| ThalesEclipse | SE | 00-584-05-28 [julian] | 19:28:50.300 | 18383.9 | 14:22:26.400 | 1507900.0989166666 | -213767 | 00-585, 05, 28 | PASS | Thales eclipse (Lydia–Media). |
| SE_0132_06_01 | SE | 00+132-06-01 [julian] | 11:17:12.000 | 9242.0 | 08:43:10.000 | 1769422.8633101853 | 47756 | 00+131, 05, 32 | PASS | Total solar eclipse (TD, ΔT from GSFC). |
| SE_1028_09_21 | SE | 0+1028-09-21 [julian] | 08:01:19.000 | 1409.0 | 07:37:50.000 | 2096798.8179398149 | 375132 | 0+1028, 09, 21 | PASS | Total solar eclipse. |
| SE_1032_01_15 | SE | 0+1032-01-15 [julian] | 11:33:38.000 | 1392.0 | 11:10:26.000 | 2098009.9655787037 | 376343 | 0+1031, 01, 15 | PASS | Total solar eclipse. |
| SE_1066_03_28 | SE | 0+1066-03-28 [julian] | 15:41:57.000 | 1227.0 | 15:21:30.000 | 2110501.1399305556 | 388834 | 0+1065, 03, 28 | PASS | Annular solar eclipse. |
| SE_1068_02_06 | SE | 0+1068-02-06 [julian] | 04:53:52.000 | 1218.0 | 04:33:34.000 | 2111180.689976852 | 389514 | 0+1067, 02, 06 | PASS | Total solar eclipse. |
| SE_1071_05_31 | SE | 0+1071-05-31 [julian] | 23:56:38.000 | 1203.0 | 23:36:35.000 | 2112391.483738426 | 390724 | 0+1070, 05, 31 | PASS | Total solar eclipse. |
| LE_0014_04_04 | LE | 000+14-04-04 [julian] | 04:41:23.000 | 10391.0 | 01:48:12.000 | 1726264.5751388888 | 4598 | 000+13, 04, 04 | PASS | Total lunar eclipse (T+). |
| LE_0032_04_14 | LE | 000+32-04-14 [julian] | 11:56:36.000 | 10212.0 | 09:06:24.000 | 1732849.8794444446 | 11183 | 000+31, 04, 14 | PASS | Total lunar eclipse (T+). |
| LE_0032_10_07 | LE | 000+32-10-07 [julian] | 15:38:15.000 | 10207.0 | 12:48:08.000 | 1733026.033425926 | 11359 | 000+32, 10, 07 | PASS | Total lunar eclipse (T-). |
| LE_0036_01_31 | LE | 000+36-01-31 [julian] | 19:07:10.000 | 10174.0 | 16:17:36.000 | 1734237.1788888888 | 12570 | 000+35, 01, 31 | PASS | Total lunar eclipse (T-). |
| LE_0054_02_11 | LE | 000+54-02-11 [julian] | 03:28:21.000 | 9997.0 | 00:41:44.000 | 1740822.5289814814 | 19156 | 000+53, 02, 11 | PASS | Total lunar eclipse (century's largest umbral magnitude). |
| LE_0054_08_07 | LE | 000+54-08-07 [julian] | 07:23:25.000 | 9992.0 | 04:36:53.000 | 1740999.6922800925 | 19333 | 000+53, 08, 07 | PASS | Total lunar eclipse (century's longest total). |
| LE_0086_11_09 | LE | 000+86-11-09 [julian] | 17:21:11.000 | 9679.0 | 14:39:52.000 | 1752782.1110185185 | 31115 | 000+86, 11, 09 | PASS | Total lunar eclipse. |
| LE_0094_06_17 | LE | 000+94-06-17 [julian] | 04:30:25.000 | 9606.0 | 01:50:19.000 | 1755558.5766087964 | 33892 | 000+93, 06, 17 | PASS | Total lunar eclipse. |
| LE_0116_04_14 | LE | 00+116-04-14 [julian] | 13:20:59.000 | 8885.0 | 10:52:54.000 | 1763530.9534027777 | 41864 | 00+115, 04, 14 | PASS | Total lunar eclipse. |
| LE_0177_06_28 | LE | 00+177-06-28 [julian] | 11:51:41.000 | 8395.0 | 09:31:46.000 | 1785885.8970601852 | 64219 | 00+176, 06, 28 | PASS | Total lunar eclipse. |
| SN_1006_FirstObs | SN | 0+1006-05-01 [julian] | — | — | — | — | — | — | WARN | First sightings around 1006-05-01 (Julian); time unknown. |
| VAT_4956 | TABLET | 00-568-01-01 [julian] | — | — | — | — | — | — | WARN | Babylonian astronomical diary (Neb II yr 37). Placeholder date; needs detailed fit. |

### 8.3 Walidacja — Pakiet 6 (PASS/WARN/FAIL)

Próg PASS: |UT_from_TT_minus_ΔT − UT_given| ≤ 0.5 dnia.

| key            | label                        | calendar   | civil_date   | TT_time   | UT_time   |   ΔT_s |       JD_TT |       JD_UT |   AM_day_float | AM_full                      |   ΔJD_days_from_TT_minus_ΔT_vs_UT | status   | notes                                                             |
|:---------------|:-----------------------------|:-----------|:-------------|:----------|:----------|-------:|------------:|------------:|---------------:|:-----------------------------|----------------------------------:|:---------|:------------------------------------------------------------------|
| LE_-0003_03_13 | Lunar eclipse — 13 Mar 4 BCE | Julian     | -0003-03-13  | 03:37:06  | 00:41:04  |  10562 | 1.72003e+06 | 1.72003e+06 |       -1632.97 | -004 AM, Mar 12 00:41:04.000 |                                 0 | PASS     | GSFC ΔT=10562 s; TT and UT from catalog (TD of greatest eclipse). |
| LE_0032_04_14  | Lunar eclipse — 14 Apr 32 CE | Julian     | 0032-04-14   | 11:56:36  | 09:06:24  |  10212 | 1.73285e+06 | 1.73285e+06 |       11183.4  | 0031 AM, Apr 22 09:06:24.000 |                                 0 | PASS     | GSFC ΔT=10212 s.                                                  |
| LE_0033_04_03  | Lunar eclipse — 3 Apr 33 CE  | Julian     | 0033-04-03   | 17:37:53  | 14:47:51  |  10202 | 1.7332e+06  | 1.7332e+06  |       11537.6  | 0032 AM, Apr 11 14:47:51.000 |                                 0 | PASS     | GSFC ΔT=10202 s.                                                  |

---

## 9) Test „w ciemno" dla krytyków (jak zamknąć dyskusję)
1. Przygotuj ≥ 15 **nowych** zapisów dziennych (zaćmienia, komety).  
2. Wypełnij CSV/JSON (klucze jak wyżej).  
3. Odpal harness i **wklej results.csv** z kolumnami: `JD_record, JD_ephem, ΔJD, OffsetInvarianceCheck, Status`.  
4. Jeśli FAIL → wskaż **który krok** (kalendarz, interkalacja, styl doby) i zaproponuj alternatywę; licz ponownie.  
5. Jeśli ≥90% PASS → warstwa **dzienna** przechodzi; kolejne spory przenoszą się na **warstwę roczną** (dendro/¹⁴C/lód).

**Statement do cytowania:** „**Kiedy liczę — AM/JD wygrywa; kiedy wierzę — przegrywa.**"

---

## 10) Instrukcja Master — Kotwice GSFC/JPL/SN/Komety → JD → AM

**Epoka AM**: `AM=0` w chwili `0001‑09‑01 00:00 UT` (kalendarz juliański).  
**Zasada**: przeliczamy *tylko to, co wiemy*; brak godzin = `date‑only` (00:00), explicite w `notes`.

### Kolumny danych (kanon)
- `key`, `label`, `tier`, `typ` (SE/LE/SN/kometa/diary/biblijne)  
- `calendar` (Julian/Gregorian), `civil_date` (YYYY‑MM‑DD, rok astronomiczny),  
- `TT_time`, `UT_time`, `ΔT_s`, `JD_TT`, `JD_UT`, `scale_note`,  
- `AM_day_float` (= `JD_UT − JD(0001‑09‑01 00:00 UT)`),  
- `AM_full` (np. `123456 AM, May 07 04:12:33`),  
- `loc` (opcjonalnie: dł./szer./wys.), `uncertainty`, `source_primary`, `note`.

### Procedura (dla każdej pozycji)
1. **Wybór kalendarza**: przed 1582‑10‑15 → **Julian**, po reformie → **Gregorian** (zgodnie ze źródłem).  
2. **Eklipsy (SE/LE)**: bierz **TT** i **UT** z PDF GSFC; ΔT = TT−UT podane w tabeli.  
3. **Komety (np. Halley)**: perihelia przed 837 r. → **niepewność dobowo‑kilkudniowa**; raportuj **okno/„date‑only"**.  
4. **Supernowe (SN)**: przyjmij **dzień** z kronik; brak godziny → `date‑only`.  
5. **Dzienniki (VAT 4956, itd.)**: wybierz **dzień cywilny** konkretnej obserwacji; opisz typ zjawiska.  
6. **JD(UT)**: licz algorytmem Fliegel–Van Flandern dla właściwego kalendarza.  
7. **AM**: `AM = JD(UT) − JD_creation`; zrób `AM_full` przez konwersję (Sep30...Aug31; 365 dni).  
8. **Niepewność**: opisuj jawnie (np. `±2 d perihelion`, `date‑only`, `hour unknown`). Zero „dopisywania godzin".

### Minimalne poprawki do danych (reguły implementacji)

- **Komety**: wszystkie wpisy **< 837 n.e.** oznaczyć `status=WARN`, dodać `sigma_time_s≈(1–3)d`. U Halley'a jawnie dopisać notę „pre-837 orbit = extrapolacja o ograniczonej wiarygodności".
- **Supernowe**: dodać kolumny `date_kind=day_only`, `sigma_time_s=43200` i źródło (np. „Stephenson & Green 2003").
- **ΔT (antyk)**: w polu `dt_model` wpisać „Stephenson–Morrison (GSFC)", z `dt_source_url` i `dt_sigma` jeżeli publikacja ją podaje/z grubsza wynika z rozrzutu.
- **Wydarzenia biblijne**: rozdzielić **warstwę faktograficzną** (np. eklipsy, kalendarz żydowski) od **hipotez** (Herod 1 p.n.e. vs 4 p.n.e.) — oba warianty jako oddzielne rekordy z `status=WARN` i pełnymi założeniami.

**Walidacja**

- **PASS** (eklipsy): |ΔJD| ≤ 0.5 d (po poprawnym TT→UT).  
- **WARN** (komety pre-837, supernowe date-only): brak precyzyjnej godziny, ale data wiarygodna.
- **FAIL** (hipotezy niezgodne): |ΔJD| > 5d lub konflikt z efemerydą.
- **SN/komety (date‑only)**: walidacja jakościowa; brak ΔJD do godziny — nie fikcjonizujemy danych.

---

## 11) Pierwszy pakiet kotwic (kanon praktyczny)

*(Daty podaję w konwencji **astronomicznej**: 1 BCE = rok 0, 2 BCE = −1 itd.; dla okresu < 1582 używamy **kalendarza juliańskiego** proleptycznego. Czasy TT/UT1 i ΔT z NASA/GSFC/Eclipsewise; źródła przy każdym wierszu.)*

| #  | Zdarzenie                                    | Data kalendarzowa (prol. jul./jul.)      | TT (TD) – „Greatest"     |      ΔT (s) | UT1 – „Greatest"              | Nota ✱                                                     |
| -- | -------------------------------------------- | ---------------------------------------- | ------------------------ | ----------: | ----------------------------- | ---------------------------------------------------------- |
| 1  | **Zaćmienie Słońca Asyryjskie (Bur-Sagale)** | −0762-06-15                              | —                        | **21210.6** | — (mapa i ΔT)                 | ✱ juliański; kotwica kronik AEC                            |
| 2  | **Zaćmienie Słońca „Thalesa"**               | −0584-05-28                              | —                        |           — | —                             | ✱ juliański; klasyka Herodota                              |
| 3  | **LE przed śmiercią Heroda**                 | −0003-03-13                              | (czasy zakresowe w lit.) |           — | (max ~02:40 lokalnie wg lit.) | ✱ juliański; spór 4 BCE vs 1 BCE – kotwica do porównań     |
| 4  | **LE 14 Nisan 32 CE (hipoteza 32)**          | 0032-04-14                               | **11:56:22 TD**          |           — | **09:06:21 UT1**              | ✱ juliański; używaj roku astronomicznego                   |
| 5  | **LE 3 IV 33 CE (klasyczny kandydat)**       | 0033-04-03                               | **17:37:38 TD**          |           — | **14:47:47 UT1**              | ✱ juliański; porównywać z 14 Nisan 33                      |
| 6  | **1P/Halley – powrót 66 CE**                 | ~0066 (peryhelium)                       | —                        |           — | —                             | ✱ kometa – używać efemeryd JPL (rekonstrukcja historyczna) |
| 7  | **SN 1006 (najjaśniejsza)**                  | 1006-04/05 (pierwsze meldunki 30 IV–1 V) | —                        |           — | —                             | ✱ źródła chińskie/arabskie; brak „czasu greatest"          |
| 8  | **SN 1054 (Krab)**                           | 1054-07-04 (tradycyjny start)            | —                        |           — | —                             | ✱ źródła chińskie/anię; data dzienna zachowana             |
| 9  | **1P/Halley – powrót 1066**                  | 1066 (widoczność kronikarska)            | —                        |           — | —                             | ✱ w ikonografii – Tkanina z Bayeux                         |
| 10 | **VAT 4956 (rok 37 Nabuchodonozora II)**     | 568/567 BCE (wiosna-wiosna)              | —                        |           — | —                             | ✱ dziennik klinowy – absolutna kotwica dla Mezopotamii     |

### Reguły i „gwiazdki" (co wpisuję przy każdym rekordzie)

* **✱ Kalendarz:** dla < 1582-10-15 używamy **proleptycznego juliańskiego**; po tej dacie – **gregoriański**. Brak roku 0 w kronikach **korygujemy** do astronomicznego (1 BCE → 0, 2 BCE → −1 itd.).
* **✱ Skale czasu:** TT/TD z katalogu NASA/Eclipsewise; **UT1** = TT − ΔT. ΔT bierzemy wprost z kart GSFC (jeśli podane) albo z modeli Stephenson-Morrison.
* **✱ Topocentryka:** gdy ważne są relacje z kronik (wschód/zmierzch/położenie), generujemy **lokalne** czasy kontaktów (λ, φ, h) – via Horizons/LE/SE Explorer – i porównujemy z geometrią świtu/zmierzchu.
* **✱ Cytowanie:** przy każdej pozycji trzymamy URL do **konkretnej karty GSFC/Eclipsewise** lub pracy.

### Jak to łączymy z AM i JD (mechanika)

* Definiujemy **AM-epoch**: *AM-1 start = 1 IX 0001 (astron.) jul.*
* **AMJD = JD(TT lub UT1 – wybierasz warstwę) − JD(AM-1 start) + offset_do_AM0**.
* Do **proroctw** stosujemy przelicznik **rok proroczy = 360 dni** (12×30). Najpierw liczba dni **w czystym 360-d** → dopiero potem **nakładamy** to na oś JD i mapujemy na kalendarz (jul/greg) wg reguł powyżej.
* Dla wydarzeń z godziną podanych w **UT1** robimy JD(UT1); gdy mamy tylko **TT**, notujemy obie wersje i wyprowadzamy UT1 przez ΔT.

---

## 12) FAQ / Debug
- **ΔJD ≈ ±0.5 d?** → epoka JD (południe/północ). Ustaw `midnight` i raportuj `+0.5`.
- **ΔJD ≈ ±365 d?** → **rok 0**/numeracja BCE vs astronomiczna.
- **ΔJD w dniach 1–40?** → **kalendarz** (juliański vs proleptyczny gregoriański).
- **Brak zgodności z JPL?** → sprawdź **skalę czasu** (UT/TT/TDB) i **ΔT**; ew. lokalizację obserwatora.
- **Święta żydowskie (14 Nisan etc.)?** → jawny model interkalacji i widzialności + ΔT.

---

## 13) Schemat danych (CSV/JSON)
**CSV kolumny:** `id,event,calendar,year,month,day,jd_ephem,jd_offset,notes`  
**JSON:** lista obiektów z tymi samymi kluczami. `year` w **astronomicznej** numeracji.

---

## 14) Minimalne wymagania publikacji AM‑JD
- Publiczny **kanon konwencji** (ten dokument).  
- **Repo z harness'em** i przykładowymi pakietami sprawdzającymi.  
- **Załączone results.csv** dla zewnętrznych zestawów (≥ 15 rekordów).  
- Opis **różnic** (ΔJD) i ich przyczyn (gwiazdki), bez ideologii — tylko liczby.

---

## 15) Słowniczek
- **JD/JDN** — Julian Day/Number.  
- **UT/TT/TDB** — skale czasu (cywilna/atomowa/barycentryczna).  
- **ΔT** — różnica TT−UT.  
- **Proleptyczny gregoriański** — rozszerzenie kalendarza gregoriańskiego wstecz przed 1582 (nie używaj do starożytności).

---

## 16) Credits i wersjonowanie
- Koncepcja/autor: **Mateusz** (AM).  
- Niniejszy dokument łączy: **Białą Księgę**, **kanon**, **erratę**, **raporty z przykładami**, **protokół testów** oraz **wszystkie pakiety walidacyjne**.  
- Wersja Master Consolidated — stabilna pod testy „w ciemno".

---

**Koniec dokumentu głównego.**

---

## APPENDIX: Dodatkowe pakiety walidacyjne

### A.1 Walidacja GSFC/JPL — Pakiet 2

| key                | label                                                      | calendar   | julian_date   | TT_time    | UT_time    |    ΔT_s |        JD_TT |       JD_UT |   AM_day_float | AM_full                      | notes                                                                                              |
|:-------------------|:-----------------------------------------------------------|:-----------|:--------------|:-----------|:-----------|--------:|-------------:|------------:|---------------:|:-----------------------------|:---------------------------------------------------------------------------------------------------|
| SE_-0762_BurSagale | Total Solar Eclipse — 15 Jun 763 BCE (Bur‑Sagale)          | Julian     | -0762-06-15   | 14:07:32.0 | 08:14:01.4 | 21210.6 |   1.4429e+06 | 1.4429e+06  |        -278764 | -763 AM, Dec 06 08:14:01.400 | GSFC SE-0762Jun15T.pdf: Greatest Eclipse TD (14:07:32.0) and UT (08:14:01.4).                      |
| SE_-0584_Thales    | Total Solar Eclipse — 28 May 585 BCE (Thales)              | Julian     | -0584-05-28   | 19:28:50.3 | 14:22:26.4 | 18383.9 |   1.5079e+06 | 1.5079e+06  |        -213766 | -585 AM, Jan 02 14:22:26.400 | GSFC SE-0584May28T.pdf: Greatest Eclipse TD (19:28:50.3) and UT (14:22:26.4).                      |
| HALLEY_-0011_peri  | 1P/Halley — perihelion (date-only) — 5 Oct 12 BCE          | Julian     | -0011-10-05   |            |            |   nan   | nan          | 1.71732e+06 |          -4349 | -011 AM, Oct 02 00:00:00.000 | Perihelion date per historical reconstructions (uncertainty few days pre‑837); no exact UT.        |
| HALLEY_1066_peri   | 1P/Halley — perihelion (date-only) — 23 Mar 1066           | Julian     | 1066-03-23    |            |            |   nan   | nan          | 2.1105e+06  |         388829 | 1066 AM, Dec 14 00:00:00.000 | Perihelion date per historical reconstructions; early apparitions ±days; no exact UT.              |
| SN_1006_first      | SN 1006 — first sighting in records — 1 May 1006           | Julian     | 1006-05-01    |            |            |   nan   | nan          | 2.08862e+06 |         366953 | 1006 AM, Jan 07 00:00:00.000 | Historical sources compile a first-sighting window ~Apr 30/May 1; time unknown — date-only.        |
| VAT4956_aurora     | VAT 4956 — auroral 'red glow' observation — 12 Mar 567 BCE | Julian     | -0566-03-12   |            |            |   nan   | nan          | 1.5144e+06  |        -207270 | -567 AM, Oct 21 00:00:00.000 | Stephenson (A&G 2004): aurora dated to the night of 12/13 Mar 567 BCE; use 12 Mar as civil anchor. |

### A.2 Walidacja — Pakiet 3

| key                  | label                                                               | calendar   | civil_date   | TT_time   | UT_time   | ΔT_s   | JD_TT   |       JD_UT |   AM_day_float | AM_full                      | notes                                                                                    |
|:---------------------|:--------------------------------------------------------------------|:-----------|:-------------|:----------|:----------|:-------|:--------|------------:|---------------:|:-----------------------------|:-----------------------------------------------------------------------------------------|
| SN_1181_first        | SN 1181 — first sightings (date-only, window early Aug)             | Julian     | 1181-08-06   |           |           |        |         | 2.15264e+06 |         430969 | 1181 AM, May 28 00:00:00.000 | Chinese/Japanese records; adopt 1181‑08‑06 (Julian) as canonical day-only; hour unknown. |
| SN_1572_Tycho        | SN 1572 (Tycho) — first report (date-only)                          | Julian     | 1572-11-11   |           |           |        |         | 2.29555e+06 |         573879 | 1573 AM, Dec 09 00:00:00.000 | Pre‑1582 region uses Julian; first reports 1572‑11‑11 (Julian).                          |
| SN_1604_Kepler       | SN 1604 (Kepler) — first report (date-only)                         | Gregorian  | 1604-10-09   |           |           |        |         | 2.30719e+06 |         585524 | 1605 AM, Nov 04 00:00:00.000 | Post‑reform; Gregorian date 1604‑10‑09 used in literature (hour unknown).                |
| HALLEY_-0239_midyear | 1P/Halley — earliest Shiji record (year-only; mid‑year placeholder) | Julian     | -0239-07-01  |           |           |        |         | 1.63394e+06 |         -87722 | -240 AM, May 02 00:00:00.000 | Shiji gives a year; choose 01 Jul as neutral civil anchor for AM mapping (hour unknown). |

### A.3 Walidacja — Pakiet 4 (Halley multi‑epochs)

| key                 | label                                                              | calendar   | civil_date   | TT_time   | UT_time   | ΔT_s   | JD_TT   |       JD_UT |   AM_day_float | AM_full                      | notes                                                                                                                     |
|:--------------------|:-------------------------------------------------------------------|:-----------|:-------------|:----------|:----------|:-------|:--------|------------:|---------------:|:-----------------------------|:--------------------------------------------------------------------------------------------------------------------------|
| HALLEY_837_midyear  | 1P/Halley — apparition year 837 (year‑only; mid‑year placeholder)  | Julian     | 0837-07-01   |           |           |        |         | 2.02695e+06 |         305287 | 0837 AM, Jan 26 00:00:00.000 | Literature gives year; precise perihelion pre‑modern often ±days. Using 01 Jul 00:00 UT as neutral anchor for AM mapping. |
| HALLEY_912_midyear  | 1P/Halley — apparition year 912 (year‑only; mid‑year placeholder)  | Julian     | 0912-07-01   |           |           |        |         | 2.05435e+06 |         332681 | 0912 AM, Feb 14 00:00:00.000 | Literature gives year; precise perihelion pre‑modern often ±days. Using 01 Jul 00:00 UT as neutral anchor for AM mapping. |
| HALLEY_989_midyear  | 1P/Halley — apparition year 989 (year‑only; mid‑year placeholder)  | Julian     | 0989-07-01   |           |           |        |         | 2.08247e+06 |         360805 | 0989 AM, Mar 05 00:00:00.000 | Literature gives year; precise perihelion pre‑modern often ±days. Using 01 Jul 00:00 UT as neutral anchor for AM mapping. |
| HALLEY_1145_midyear | 1P/Halley — apparition year 1145 (year‑only; mid‑year placeholder) | Julian     | 1145-07-01   |           |           |        |         | 2.13945e+06 |         417784 | 1145 AM, Apr 13 00:00:00.000 | Literature gives year; precise perihelion pre‑modern often ±days. Using 01 Jul 00:00 UT as neutral anchor for AM mapping. |
| HALLEY_1222_midyear | 1P/Halley — apparition year 1222 (year‑only; mid‑year placeholder) | Julian     | 1222-07-01   |           |           |        |         | 2.16757e+06 |         445908 | 1222 AM, May 02 00:00:00.000 | Literature gives year; precise perihelion pre‑modern often ±days. Using 01 Jul 00:00 UT as neutral anchor for AM mapping. |
| HALLEY_1301_midyear | 1P/Halley — apparition year 1301 (year‑only; mid‑year placeholder) | Julian     | 1301-07-01   |           |           |        |         | 2.19643e+06 |         474763 | 1301 AM, May 22 00:00:00.000 | Literature gives year; precise perihelion pre‑modern often ±days. Using 01 Jul 00:00 UT as neutral anchor for AM mapping. |
| HALLEY_1456_midyear | 1P/Halley — apparition year 1456 (year‑only; mid‑year placeholder) | Julian     | 1456-07-01   |           |           |        |         | 2.25304e+06 |         531377 | 1456 AM, Jun 30 00:00:00.000 | Literature gives year; precise perihelion pre‑modern often ±days. Using 01 Jul 00:00 UT as neutral anchor for AM mapping. |
| HALLEY_1531_midyear | 1P/Halley — apparition year 1531 (year‑only; mid‑year placeholder) | Julian     | 1531-07-01   |           |           |        |         | 2.28044e+06 |         558770 | 1531 AM, Jul 18 00:00:00.000 | Literature gives year; precise perihelion pre‑modern often ±days. Using 01 Jul 00:00 UT as neutral anchor for AM mapping. |
| HALLEY_1607_midyear | 1P/Halley — apparition year 1607 (year‑only; mid‑year placeholder) | Julian     | 1607-07-01   |           |           |        |         | 2.3082e+06  |         586529 | 1607 AM, Aug 06 00:00:00.000 | Literature gives year; precise perihelion pre‑modern often ±days. Using 01 Jul 00:00 UT as neutral anchor for AM mapping. |
| HALLEY_1682_midyear | 1P/Halley — apparition year 1682 (year‑only; mid‑year placeholder) | Julian     | 1682-07-01   |           |           |        |         | 2.33559e+06 |         613923 | 1682 AM, Aug 25 00:00:00.000 | Literature gives year; precise perihelion pre‑modern often ±days. Using 01 Jul 00:00 UT as neutral anchor for AM mapping. |
| HALLEY_1759_midyear | 1P/Halley — apparition year 1759 (year‑only; mid‑year placeholder) | Julian     | 1759-07-01   |           |           |        |         | 2.36371e+06 |         642047 | 1760 AM, Sep 13 00:00:00.000 | Literature gives year; precise perihelion pre‑modern often ±days. Using 01 Jul 00:00 UT as neutral anchor for AM mapping. |

### A.4 Walidacja — Pakiet 5 (dodatkowe kotwice)

| key           | label                                                          | calendar   | civil_date   | TT_time   | UT_time   | ΔT_s   | JD_TT   |       JD_UT |   AM_day_float | AM_full                      | notes                                                                                       |
|:--------------|:---------------------------------------------------------------|:-----------|:-------------|:----------|:----------|:-------|:--------|------------:|---------------:|:-----------------------------|:--------------------------------------------------------------------------------------------|
| LE_0000_01_10 | Lunar eclipse — 10 Jan 1 BCE (astronomical year 0) — date‑only | Julian     | 0000-01-10   |           |           |        |         | 1.72107e+06 |           -600 | -001 AM, Jan 09 00:00:00.000 | Alternative Herodian lunar eclipse candidate; hour not fixed here (to be filled from GSFC). |
| SE_1066_08_01 | Solar eclipse — 01 Aug 1066 (Europe) — date‑only               | Julian     | 1066-08-01   |           |           |        |         | 2.11063e+06 |         388960 | 1066 AM, Apr 24 00:00:00.000 | Widely noted in chronicles; UT/TT to be taken from GSFC in next pass.                       |

---

## 9) Kotwice MIYAKE i reguły AUTO-LOCK/AUTO-SNAP

**Co to są kotwice MIYAKE?** Globalne skoki koncentracji ¹⁴C w słojach drzew spowodowane zwiększoną intensywnością promieniowania kosmicznego. Wykryte w słojach na całym świecie, dają **kotwice roczne** o precyzji ±1 rok.

### 9.1 Mechanizm i wykrywalność

**Fizyka zjawiska:**
- **Zdarzenia kosmiczne** (burze słoneczne, supernowe pobliskie, eksplozje gamma) → zwiększona produkcja ¹⁴C w atmosferze
- **Wbudowanie ¹⁴C** w słoje drzew podczas sezonu wegetacyjnego  
- **Globalny sygnał** — wykrywalny w drzewach z różnych kontynentów
- **Precyzja roczna** — każdy słój = dokładnie jeden rok wzrostu

**Potwierdzenia laboratoryjne:**
- Replikacje w laboratoriach europejskich, amerykańskich, japońskich
- Spójność dat C14 z różnych regionów geograficznych (±1-2 lata)
- Cross-validation z innymi proxy (rdzenie lodowe, korale)

### 9.2 Zidentyfikowane kotwice MIYAKE

**MIYAKE-0775 (775 CE):**
- **Sygnał**: Skok ¹⁴C o ~100‰ w słoju 774/775 CE
- **Źródło**: Miyake et al. (2012) Nature, potwierdzenia globalne
- **Status**: `AUTO-LOCK(year)` — rok 775 CE zabezpieczony  
- **Aplikacja**: Kotwica dla słojów drzew i obiektów drewnianych VIII wieku

**MIYAKE-0994 (994 CE):**  
- **Sygnał**: Skok ¹⁴C o ~80‰ w słoju 993/994 CE
- **Źródło**: Miyake et al. (2013) Nature Communications
- **Status**: `AUTO-LOCK(year)` — rok 994 CE zabezpieczony
- **Aplikacja**: Kotwica dla obiektów końca X wieku

### 9.3 Workflow bayesowski L(t)·A(t)

**Idea: P(t) ∝ L(t)·A(t)**

**L(t) — Likelihood radiocarbon:**
- **IntCal20** kalibracja ¹⁴C  
- **HPD intervals** z OxCal
- **Kotwice MIYAKE** jako delta functions w L(t)

**A(t) — Astronomical priors:**
- **Eklipsy** z NASA GSFC (TT/UT/ΔT)
- **Fazy Księżyca** z JPL Horizons  
- **Widoczność planet** (Wenus, Mars, Jowisz, Saturn)

**Posterior P(t):**
- **Kombinacja** L(t) × A(t) przez Bayes
- **95% HPD** → pole `posterior_hpd_days`
- **Status automatyczny**: PASS/WARN/FAIL na podstawie HPD width

### 9.4 Reguły AUTO-LOCK i AUTO-SNAP

**AUTO-LOCK** — **Żelazne** kotwice (wysokie zaufanie):
```
AUTO-LOCK(eclipse): TT/UT z NASA GSFC + widoczność potwierdzona + lokalny czas zgodny
→ 95% HPD ≤ 1 dzień, sigma_time_s = ΔT uncertainty

AUTO-LOCK(year): Kotwice MIYAKE + dendrochronologia kompletna  
→ 95% HPD ≤ 365 dni, sigma_time_s = 31536000 (1 rok w sekundach)

AUTO-LOCK(day): Kombinacja eclipse + MIYAKE + dodatkowe constrainty
→ 95% HPD ≤ 1 dzień, ultra-precyzyjne datowanie
```

**AUTO-SNAP** — **Miękkie** kotwice (ograniczone zaufanie):
```
AUTO-SNAP(historical): Zapisy historyczne z datą cywilną
→ 95% HPD ≤ 30 dni, sigma_time_s = brak (data-only)

AUTO-SNAP(astronomical): ΔT > 1000s (antyk) lub godzina nieznana
→ 95% HPD ≤ 7 dni, sigma_time_s = ΔT + modeling uncertainty  

AUTO-SNAP(radiocarbon): Standard C14 bez kotwic MIYAKE
→ 95% HPD ≤ 100 dni, sigma_time_s = lab error + calibration
```

### 9.5 Przykład: L'Anse aux Meadows 1021 CE

**Problem**: Kiedy dokładnie Nordowie byli w Ameryce Północnej?

**Dane dendrochronologiczne:**
- **Próbka drewna** z L'Anse aux Meadows z zachowaną korą
- **Miyake 993/994** jako punkt odniesienia w słojach
- **28 słojów** od sygnału Miyake do krawędzi kory

**Kalkulacja:**
```
Year_Miyake = 994 CE (kotwica AUTO-LOCK)
Tree_rings_count = 28 (od Miyake do kory)  
Year_cutting = 994 + 28 = 1022 CE
Seasonal_correction = -1 (cięcie prawdopodobnie jesienią 1021)
→ Final estimate: 1021 CE ±1 rok
```

**Status w MASTER RAW:**
```csv
HIST-1021-LAM,L'Anse aux Meadows — Norse presence 1021 CE,HIST,Julian,1021,,,
,,,,2096647.5,373981.0,"1021 AM Jun 08 00:00:00.000",PASS,,
Tree ring counting from Miyake 993/994 to bark edge — year 1021 secured,
AUTO-LOCK(year),365
```

### 9.6 Kontrola jakości i walidacja

**Pola QA w MASTER RAW:**

- **`status`**: PASS/WARN/FAIL/AUTO-LOCK/AUTO-SNAP
- **`sigma_time_s`**: Uncertainty budget w sekundach  
- **`status_reason`**: Opis źródła i metody
- **`auto_rule`**: Zastosowana reguła automatycznego klasyfikowania
- **`posterior_hpd_days`**: Szerokość 95% HPD w dniach

**Progi jakości:**
```
PASS: posterior_hpd_days ≤ 1.0 AND ≥2 niezależne źródła
WARN: posterior_hpd_days ≤ 30.0 AND pojedyncze źródło reliable  
FAIL: posterior_hpd_days > 30.0 OR sprzeczne źródła
```

**Replikowalność:**
- **Wszystkie obliczenia** dokumentowane w `status_reason`
- **Źródła danych** linkowane w `source_url`
- **Kody laboratoryjne** dla próbek C14 w `note`
- **Współrzędne geograficzne** dla lokalizacji próbek

### 9.7 Przyszłe rozszerzenia

**Więcej kotwic MIYAKE:**
- **5480 BCE** (kandydat w słojach subfosilnych)
- **660 BCE** (sygnał w lodach grenlandzkich + dendro)  
- **1052 CE** (słabszy sygnał, wymaga potwierdzenia)

**Integracja z wulkanizmem:**
- **SO₄²⁻ spikes** w rdzeniach lodowych
- **Volcanic glass** fingerprinting z tef
- **Cross-correlation** z zapisami historycznymi

**Machine Learning enhancement:**
- **Automated pattern recognition** w sygnałach C14
- **Probabilistic dating** z uncertainty propagation
- **Real-time updates** gdy pojawiają się nowe dane laboratoryjne

---

*AM‑JD Complete Master Documentation — Enhanced with MIYAKE Anchors*  
*System Version: Production Ready v1.0*  
*MIYAKE Integration: 775 CE, 994 CE, L'Anse aux Meadows 1021 CE*
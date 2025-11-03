# 🔐 FOLDER SWIETOSC – SACRED ARCHIVE

## 📌 Status po reorganizacji 2025‑11‑03
- **Tryb dostępu:** wyłącznie odczyt (read-only). Żadne pliki w tym katalogu nie mogą być edytowane bezpośrednio.
- **Nowa ścieżka robocza:** wszelkie skrypty, raporty i pliki tymczasowe rozwijamy w katalogu `../AMJD/`.
- **Autorytatywne zasoby:** jedynym źródłem danych dla aplikacji jest zunifikowana baza `AMJD_UNIFIED_TIMELINE_DATABASE.json/.csv`.
- **Miary bezpieczeństwa:** checksumy MD5, polityka “no manual edits”, pełne kopie zapasowe w `../AMJD/BACKUP_BEFORE_ORGANIZATION/`.

---

## 🌟 Kluczowe zbiory (read-only)
- `AMJD_UNIFIED_TIMELINE_DATABASE.csv` / `.json` – aktualna, przepuszczona przez pipeline baza timeline’u.
- `AMJD_MASTER_RAW.csv`, `AMJD_COMPLETE_MASTER.md` – pierwotne rekordy bazowe z kotwicami MIYAKE.
- `AMJD_BIBLICAL_CITATIONS_DATABASE.json`, `AMJD_PRECISE_BIBLICAL_CITATIONS.json` – zasób cytatów biblijnych wykorzystywany przy scalaniu.
- `AMJD_ASTRONOMICAL_DATA.csv`, `de421.bsp`, `de422.bsp` – dane astronomiczne i efemerydy.
- `AMJD_HISTORICAL_EVENTS_MASTER.csv` + specjalistyczne podzbiory (`..._VOLCANO_EVENTS.csv`, `..._SUPERNOVA_EVENTS.csv`, itp.).

Te pliki traktujemy jako **źródła wejściowe**. Pipeline w katalogu `../AMJD/` zaczytuje je, scalając w jedną bazę timeline’u. Żadne nowe kolumny ani korekty nie są dopisywane bezpośrednio w tym folderze.

---

## 🧭 Gdzie znaleźć logikę i narzędzia
- `../AMJD/03_CORE_APPLICATIONS/AMJD_TIMELINE_BROWSER_GUI.py` – GUI korzystające z `SWIETOSC/AMJD_UNIFIED_TIMELINE_DATABASE.*`.
- `../AMJD/04_DATA_PROCESSORS/` – procesory danych, w tym docelowo przebudowany `AMJD_UNIFY_ALL_DATA.py`.
- `../AMJD/WIKIPEDIA_EVENTS/`, `../AMJD/UNIFIED_EVENTS/` – pliki wyjściowe/wspomagające, które można swobodnie generować i porządkować.
- `../AMJD/trash/` – docelowe miejsce na historyczne raporty, które nie są już używane w pipeline.

---

## 🛡️ Procedura aktualizacji danych
1. **Pracuj w `../AMJD/`** – konfiguracje, translacje, pliki pomocnicze trzymaj poza `SWIETOSC`.
2. **Uruchom pipeline** (`AMJD_UNIFY_ALL_DATA.py` po refaktoryzacji) z katalogu nadrzędnego; skrypt ma tylko odczytywać dane z `SWIETOSC`, a wyniki zapisywać do `SWIETOSC/AMJD_UNIFIED_TIMELINE_DATABASE.*`.
3. **Waliduj** – sprawdź sumy kontrolne, liczność rekordów, flagi `date_estimated`, zgodność z zasadą `am_day > 0`.
4. **Zabezpiecz** – zaktualizuj `AMJD_SACRED_ARCHIVE_STATUS.md`, zapisz nowy snapshot w `../AMJD/BACKUP_BEFORE_ORGANIZATION/`.

---

## ⚠️ Zasady bezpieczeństwa
- Bezpośrednia edycja plików w `SWIETOSC/` jest zabroniona.
- Wszelkie zmiany logiki muszą być wdrażane poprzez skrypty w `../AMJD/`.
- Kotwice MIYAKE (775, 994 CE) są nienaruszalne – każda modyfikacja wymaga osobnej weryfikacji.
- Po każdej aktualizacji wykonujemy kontrolę integralności (`AMJD_CHECKSUMS.md5`) i dokumentujemy wynik.

**Święte Archiwum pozostaje sercem kroniki AM‑JD – jego zawartość jest tylko do odczytu, natomiast rozwój systemu toczy się w katalogu `AMJD/`.** 🔐

---

## 🗄️ Główna baza danych: `amjd_master.db`
- **Plik:** `amjd_master.db` – zunifikowana baza SQLite zawierająca wszystkie wydarzenia historyczne, biblijne i astronomiczne.
- **Struktura:**
  - Tabela `events`: id, hash (unikalny), name, date_ce, am_day, location, event_type, description, source, wikipedia_url, exists_in_wikipedia, raw_json.
  - Tabela `provenance`: id, event_hash, file_path, inserted_at – śledzenie źródła każdego wydarzenia.
- **Liczba rekordów:** 979 unikalnych wydarzeń (po deduplikacji).
- **Zawartość:** Wydarzenia z wulkanów, komet, biblijne (np. Creation of Adam, Noah's Flood), MIYAKE spikes, historyczne katastrofy.
- **Użycie:** Baza jest autorytatywnym źródłem dla aplikacji; skrypty czytają z niej dane do analiz i wizualizacji.
- **Aktualizacja:** Baza jest budowana automatycznie przez skrypty merger; nie edytować ręcznie.

**Wszystkie dane zostały skonsolidowane w tej bazie dla optymalnej wydajności.** 📊

---

## 📊 Scalone pliki danych
Po konsolidacji, rozciągnięte pliki zostały scalone w większe jednostki:

- **`AMJD_ALL_EVENTS.csv`**: Wszystkie wydarzenia historyczne (wulkany, komety, trzęsienia, itp.) – 162 wydarzenia.
- **`AMJD_BIBLICAL_CITATIONS_MASTER.csv`**: Wszystkie cytaty biblijne i powiązania – 531 wpisów.
- **`AMJD_CONSOLIDATED_DATA.csv`**: Wszystkie pozostałe dane CSV (radiowęglowe, topograficzne, walidacyjne) – 3493 wiersze, z kolumną `source_file` wskazującą źródło.

**Dzięki temu zmniejszono liczbę plików z ~30 do 3 głównych CSV, zachowując wszystkie dane.** 🔄

---

## 🧹 Czyszczenie folderu
Po konsolidacji usunięto niepotrzebne pliki:
- **Skrypty Python**: 3 pliki (AMJD_CONSOLIDATE_DATABASES.py, itp.) – narzędzia do przetwarzania, niepotrzebne dla linii czasu.
- **Raporty Markdown**: 5 plików (AMJD_ENHANCEMENT_REPORT.md, itp.) – raporty procesów.
- **Duplikaty JSON**: 9 plików – dane już w CSV i DB.
- **Cache**: wikipedia_cache.db – dane w głównej bazie.

**Folder zawiera teraz tylko dane, dokumentację i zasoby potrzebne do linii czasu.** 🕰️

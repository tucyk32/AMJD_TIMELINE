# AMJD RADIOCARBON CALIBRATION TOOLKIT
## Zestaw Narzędzi do Kalibracji C14 w Systemie AM-JD

**Cel:** Integracja nowoczesnych krzywych kalibracyjnych C14 z systemem AM-JD  
**Status:** GOTOWY DO UŻYCIA  
**Kompatybilność:** OxCal 4.4+, MIYAKE anchors, AUTO-LOCK/AUTO-SNAP

---

## KOMPONENTY SYSTEMU

### 1. PYTHON CONVERTER
**`AMJD_from_OxCalJSON.py`**
- Konwertuje OxCal JSON export → AM-JD format CSV
- Ekstraktuje 95.4% HPD intervals
- Mapuje calendar years → JD intervals → AM days
- Usage: `python AMJD_from_OxCalJSON.py export.json --am0jd <epoch> --out result.csv`

### 2. ATMOSPHERIC CURVES
**Northern Hemisphere:**
- `NHPine16.14c` - Hogg et al 2016 Pine curve (5-year resolution)
- `NHPine16Raw.14c` - Raw measurements

**Southern Hemisphere:**  
- `SHKauri16.14c` - Hogg et al 2016 Kauri curve (5-year resolution)
- `SHKauri16Raw.14c` - Raw measurements

### 3. COMPARISON SCRIPTS
**`NHCompare.oxcal`** - IntCal13 vs NHPine16 comparison  
**`SHCompare.oxcal`** - SHCal13 vs SHKauri16 comparison

---

## WORKFLOW INTEGRATION

### STANDARD C14 → AM-JD PIPELINE:
```
1. Import sample to OxCal
2. Apply appropriate curve (NH/SH based on location)  
3. Calibrate with 95.4% intervals
4. Export to JSON
5. Run: python AMJD_from_OxCalJSON.py sample.json --am0jd 1721425.5
6. Merge results into AMJD_MASTER_RAW.csv
7. Apply AUTO-LOCK/AUTO-SNAP rules based on HPD width
```

### QUALITY CLASSIFICATION:
- **HPD ≤ 30 days** → AUTO-LOCK(month)
- **HPD ≤ 365 days** → AUTO-LOCK(year)  
- **HPD ≤ 10 years** → AUTO-SNAP(decade)
- **HPD > 10 years** → status=WARN

---

## MIYAKE EVENTS INTEGRATION

**COSMIC RAY SPIKES jako C14 ANCHORS:**
- **775 CE** - MIYAKE event in tree rings
- **994 CE** - MIYAKE event in tree rings
- **L'Anse aux Meadows 1021** - dendro + archaeological anchor

Te eventi są **niezależne od atmospheric curves** ale **koherentne** z C14 system.

---

## TECHNICAL SPECIFICATIONS

### INPUT FORMATS:
- OxCal JSON exports (standard format)
- .14c atmospheric curve files (Hogg et al 2016)
- Raw radiocarbon measurements

### OUTPUT FORMAT:
```csv
name,cal_era,cal_start_Y,cal_end_Y,JD_min,JD_max,AM_day_min,AM_day_max
Sample_001,CE,1015,1025,2087925.5,2091580.5,366500.0,370155.0
```

### AM-JD FIELDS MAPPING:
- `JD_min/max` → `JD_UT` bounds
- `AM_day_min/max` → `AM_day_float` bounds  
- `95.4% HPD` → `posterior_hpd_days`
- Auto-classification → `auto_rule`, `status`

---

## ADVANTAGES OVER STANDARD APPROACHES

### ✅ **PRECISION:**
- Hogg et al 2016 curves - latest atmospheric reconstruction
- 5-year resolution vs standard 10-year
- Raw data preservation for detailed analysis

### ✅ **INTEGRATION:**
- Direct JD conversion (no intermediate steps)
- AM-JD epoch alignment 
- MIYAKE anchor compatibility  
- AUTO-LOCK/AUTO-SNAP workflow

### ✅ **HEMISPHERE SPECIFICITY:**
- NH curves for European/Asian samples
- SH curves for Southern Hemisphere samples
- Proper magnetic field corrections

---

## USAGE EXAMPLES

### Europe/Mediterranean samples:
```bash
python AMJD_from_OxCalJSON.py jerusalem_sample.json --am0jd 1721425.5 --out AMJD_C14_Jerusalem.csv
```

### Southern Hemisphere samples:
```bash  
python AMJD_from_OxCalJSON.py australia_sample.json --am0jd 1721425.5 --out AMJD_C14_Australia.csv
```

### Comparison analysis:
```bash
# Load in OxCal and run comparison scripts
File > Load > NHCompare.oxcal
File > Load > SHCompare.oxcal
```

---

## QUALITY CONTROL

### CURVE VALIDATION:
- Compare against IntCal13/SHCal13 standards
- Check for systematic offsets in time ranges
- Verify 14C age vs cal age relationships

### SAMPLE ASSESSMENT:
- Marine reservoir corrections (if applicable)
- Contamination indicators
- Statistical uncertainty propagation

---

## INTEGRATION WITH MASTER_RAW.csv

Po kalibracji C14 samples, wyniki można **bezpośrednio dodać** do głównego pipeline'u:

```csv
record_type,source_group,key,kind,JD_UT,AM_day_float,status,sigma_time_s,auto_rule,posterior_hpd_days
C14Sample,RADIOCARBON,C14_Jerusalem_001,C14,2088000.0,366575.0,PASS,2628000,AUTO-LOCK(month),25.5
```

---

## REFERENCES

- Hogg et al. (2016) "Decadally Resolved Lateglacial Radiocarbon Evidence from New Zealand Kauri" *Radiocarbon* doi:10.1017/RDC.2016.86
- Reimer et al. (2013) IntCal13 and Marine13 radiocarbon age calibration curves
- MIYAKE events: 775 CE, 994 CE cosmic ray documentation

---

*Radiocarbon Toolkit for AM-JD System - November 2025*
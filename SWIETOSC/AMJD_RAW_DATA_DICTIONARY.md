# AMJD_RAW_DATA — Data Dictionary

**record_type**: 'AstronomyAnchor' | 'EventAnchor' | 'C14CurvePoint' | 'City'  
**source_group**: logical dataset group (e.g., 'GSFC_BATCH6', 'TOPO', 'C14_NHPine16').  
**source_file**: original file name inside /mnt/data.  
**key**: event identifier (e.g., 'SE_-0762-06-15_Assyrian').  
**label**: human label/description if present.  
**kind**: SE/LE/SN/COMET/TABLET/C14/Event type.  
**calendar**: 'Julian' or 'Gregorian' (source convention).  
**Y,M,D**: calendar date (astronomical year numbering).  
**TT_time**: time-of-day in TT/TD if available (HH:MM:SS).  
**UT_time**: time-of-day in UT/UT1/UTC if available (HH:MM:SS[.s]).  
**DeltaT_s**: ΔT in seconds (TT−UT1) if available.  
**JD_TT, JD_UT**: Julian Day at TT / UT where available.  
**AM_day_float, AM_full**: AM index/day and formatted AM datetime.  
**curve_name**: C14 curve ID (e.g., 'NHPine16', 'SHKauri16Raw').  
**calbp, cal_year**: radiocarbon years BP and mapped calendar year (astronomical).  
**c14bp, error_bp, delta14C_permil, sigma_permil**: curve columns.  
**site_name, country, lat_deg, lon_deg, elev_m**: city/observer site.  
**note**: remarks, e.g., 'date-only', 'year-only (anchor)', etc.  
**source_url**: reference URL if present in the source table.


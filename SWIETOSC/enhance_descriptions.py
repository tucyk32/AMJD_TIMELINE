#!/usr/bin/env python3
"""
AMJD Enhance Descriptions Script - Enhanced Version
Aktualizuje opisy wydarzeń w bazie amjd_master.db na podstawie danych z plików CSV.
Używa danych z AMJD_CONSOLIDATED_DATA.csv, AMJD_BIBLICAL_CITATIONS_MASTER.csv i AMJD_ALL_EVENTS.csv.
"""

import sqlite3
import pandas as pd
import os

def load_csv_data():
    """Wczytuje dane z plików CSV."""
    files = {
        'consolidated': 'AMJD_CONSOLIDATED_DATA.csv',
        'citations': 'AMJD_BIBLICAL_CITATIONS_MASTER.csv',
        'events': 'AMJD_ALL_EVENTS.csv'
    }

    data = {}
    for key, filename in files.items():
        if os.path.exists(filename):
            try:
                # Dla consolidated CSV - obsłuż duże pliki z wieloma pustymi kolumnami
                if key == 'consolidated':
                    # Wczytaj tylko potrzebne kolumny lub całą ramkę
                    df = pd.read_csv(filename, low_memory=False)
                    # Filtruj wiersze, które mają dane w kolumnach opisów
                    desc_cols = ['description', 'enhanced_description', 'wikipedia_summary', 'historical_context', 'notes', 'summary', 'biblical_citations_summary']
                    available_cols = [col for col in desc_cols if col in df.columns]
                    if available_cols:
                        # Zachowaj tylko wiersze z niepustymi opisami
                        df = df.dropna(subset=available_cols, how='all')
                    data[key] = df
                else:
                    data[key] = pd.read_csv(filename, low_memory=False)
                print(f"Wczytano {len(data[key])} wierszy z {filename}")
            except Exception as e:
                print(f"Błąd wczytywania {filename}: {e}")
        else:
            print(f"Plik {filename} nie istnieje")
    return data

def create_enhanced_description(row, citations_data=None):
    """Tworzy rozszerzony opis na podstawie dostępnych danych."""
    descriptions = []

    # Lista kolumn do sprawdzenia w kolejności ważności
    desc_columns = [
        'description',
        'enhanced_description',
        'wikipedia_summary',
        'historical_context',
        'biblical_citations_summary',
        'notes',
        'summary'
    ]

    for col in desc_columns:
        if col in row and pd.notna(row[col]) and str(row[col]).strip() and row[col] != 'No description':
            descriptions.append(str(row[col]).strip())

    # Dla wydarzeń biblijnych - dodatkowe dane z citations
    if citations_data is not None and 'name' in row and pd.notna(row['name']):
        name = str(row['name']).strip()
        matching_citations = citations_data[citations_data['name'].str.strip() == name]
        if not matching_citations.empty:
            cit_row = matching_citations.iloc[0]
            if pd.notna(cit_row.get('biblical_citations_summary')):
                descriptions.append(f"Dodatkowe cytaty: {cit_row['biblical_citations_summary']}")

    # Połącz opisy bez duplikatów
    unique_descriptions = []
    seen = set()
    for desc in descriptions:
        if desc not in seen:
            unique_descriptions.append(desc)
            seen.add(desc)

    if unique_descriptions:
        return ' | '.join(unique_descriptions)
    else:
        return None

def update_database_descriptions(data):
    """Aktualizuje opisy w bazie danych."""
    conn = sqlite3.connect('amjd_master.db')
    cursor = conn.cursor()

    updated_count = 0
    total_processed = 0

    # Pobierz wszystkie wydarzenia z bazy
    cursor.execute("SELECT id, name, date_ce, event_type, description FROM events")
    events = cursor.fetchall()

    print(f"Przetwarzanie {len(events)} wydarzeń z bazy...")

    for event in events:
        event_id, name, date_ce, event_type, current_desc = event
        total_processed += 1

        if total_processed % 100 == 0:
            print(f"Przetworzono {total_processed} wydarzeń, zaktualizowano {updated_count}")

        # Szukaj dopasowań w danych CSV
        enhanced_desc = None

        # 1. Sprawdź w consolidated data - najpierw po nazwie, potem po dacie
        if 'consolidated' in data:
            df = data['consolidated']

            # Dopasowanie po nazwie (bez uwzględniania wielkości liter)
            if name:
                name_lower = str(name).lower().strip()
                name_matches = df[df['name'].str.lower().str.strip() == name_lower]
                print(f"Szukam '{name}' - znaleziono {len(name_matches)} dopasowań po nazwie")
                if not name_matches.empty:
                    # Wybierz wiersz z najdłuższym opisem
                    best_row = None
                    best_desc_len = 0
                    for _, row in name_matches.iterrows():
                        temp_desc = create_enhanced_description(row, data.get('citations'))
                        if temp_desc and len(temp_desc) > best_desc_len:
                            best_row = row
                            best_desc_len = len(temp_desc)
                    if best_row is not None:
                        enhanced_desc = create_enhanced_description(best_row, data.get('citations'))
                        print(f"Znaleziono najlepszy opis dla '{name}': {enhanced_desc[:100] if enhanced_desc else 'None'}...")

            # Jeśli nie znaleziono po nazwie, spróbuj po dacie
            if enhanced_desc is None and date_ce:
                date_matches = df[df['date_ce'] == date_ce]
                if not date_matches.empty:
                    # Weź pierwszy dopasowany wiersz
                    for _, row in date_matches.iterrows():
                        temp_desc = create_enhanced_description(row, data.get('citations'))
                        if temp_desc:
                            enhanced_desc = temp_desc
                            break

        # 2. Sprawdź w events data (jeśli nie znaleziono)
        if enhanced_desc is None and 'events' in data:
            df = data['events']
            if name:
                matches = df[df['name'].str.lower().str.strip() == str(name).lower().strip()]
                if not matches.empty:
                    row = matches.iloc[0]
                    enhanced_desc = create_enhanced_description(row)

        # Aktualizuj jeśli znaleziono lepsze dane i opis nie jest pusty
        if enhanced_desc and enhanced_desc.strip() and enhanced_desc != str(current_desc or '').strip():
            cursor.execute("""
                UPDATE events
                SET description = ?
                WHERE id = ?
            """, (enhanced_desc, event_id))
            updated_count += 1
            print(f"Zaktualizowano: {name[:50]}... (długość: {len(enhanced_desc)})")

    conn.commit()
    conn.close()
    print(f"Zaktualizowano {updated_count} wydarzeń z {total_processed} przetworzonych")

def main():
    print("Rozpoczynam rozszerzoną aktualizację opisów w bazie danych...")

    # Wczytaj dane z CSV
    data = load_csv_data()

    if not data:
        print("Brak danych do przetworzenia")
        return

    # Aktualizuj bazę
    update_database_descriptions(data)

    print("Rozszerzona aktualizacja zakończona!")

if __name__ == "__main__":
    main()
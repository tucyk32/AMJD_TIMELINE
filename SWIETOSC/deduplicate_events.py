#!/usr/bin/env python3
"""
AMJD Deduplicate Events Script
Usuwa duplikaty wydarzeń w bazie amjd_master.db, zachowując najlepszy opis.
"""

import sqlite3

def deduplicate_events():
    """Usuwa duplikaty wydarzeń, zachowując te z najlepszymi opisami."""
    conn = sqlite3.connect('amjd_master.db')
    cursor = conn.cursor()

    # Znajdź wszystkie nazwy wydarzeń
    cursor.execute("SELECT DISTINCT name FROM events")
    names = [row[0] for row in cursor.fetchall()]

    removed_count = 0

    for name in names:
        # Znajdź wszystkie wpisy dla tej nazwy
        cursor.execute("SELECT id, description, LENGTH(description) as desc_len FROM events WHERE name = ?", (name,))
        entries = cursor.fetchall()

        if len(entries) > 1:
            print(f"Przetwarzam duplikaty dla: {name} ({len(entries)} wpisów)")

            # Wybierz najlepszy wpis (najdłuższy opis)
            best_entry = max(entries, key=lambda x: x[2])  # x[2] to desc_len
            best_id = best_entry[0]

            # Usuń pozostałe wpisy
            ids_to_remove = [entry[0] for entry in entries if entry[0] != best_id]
            for remove_id in ids_to_remove:
                cursor.execute("DELETE FROM events WHERE id = ?", (remove_id,))
                cursor.execute("DELETE FROM provenance WHERE event_hash = (SELECT hash FROM events WHERE id = ?)", (remove_id,))
                removed_count += 1

            print(f"  Zachowano wpis ID {best_id}, usunięto {len(ids_to_remove)} duplikatów")

    conn.commit()
    conn.close()
    print(f"Usunięto {removed_count} duplikatów")

def main():
    print("Rozpoczynam deduplikację wydarzeń...")
    deduplicate_events()
    print("Deduplikacja zakończona!")

if __name__ == "__main__":
    main()
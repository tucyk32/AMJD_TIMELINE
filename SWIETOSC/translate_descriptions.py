#!/usr/bin/env python3
"""
AMJD Translate Descriptions Script
Tłumaczy opisy wydarzeń w bazie amjd_master.db na język polski.
"""

import sqlite3
import requests
import time
import json

class Translator:
    def __init__(self):
        self.api_url = "https://api.mymemory.translated.net/get"
        self.cache = {}

    def translate(self, text, source_lang='en', target_lang='pl'):
        """Tłumaczy tekst używając MyMemory API."""
        if not text or text.strip() == '':
            return text

        # Sprawdź cache
        cache_key = f"{source_lang}_{target_lang}_{text[:100]}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            params = {
                'q': text[:500],  # Limit długości
                'langpair': f'{source_lang}|{target_lang}'
            }

            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            translated_text = data.get('responseData', {}).get('translatedText', text)

            # Zapisz w cache
            self.cache[cache_key] = translated_text

            # Opóźnienie aby nie przeciążać API
            time.sleep(0.5)

            return translated_text

        except Exception as e:
            print(f"Błąd tłumaczenia: {e}")
            return text  # Zwróć oryginalny tekst w przypadku błędu

def translate_descriptions():
    """Tłumaczy wszystkie opisy wydarzeń na polski."""
    translator = Translator()
    conn = sqlite3.connect('amjd_master.db')
    cursor = conn.cursor()

    # Pobierz wszystkie wydarzenia
    cursor.execute("SELECT id, name, description FROM events WHERE description IS NOT NULL AND description != ''")
    events = cursor.fetchall()

    print(f"Tłumaczę {len(events)} opisów wydarzeń...")

    updated_count = 0

    for event_id, name, description in events:
        try:
            # Tłumacz opis
            translated_desc = translator.translate(description)

            if translated_desc != description:  # Tylko jeśli tłumaczenie się zmieniło
                cursor.execute(
                    "UPDATE events SET description = ? WHERE id = ?",
                    (translated_desc, event_id)
                )
                updated_count += 1

                if updated_count % 50 == 0:
                    print(f"Przetłumaczono {updated_count} opisów...")

        except Exception as e:
            print(f"Błąd tłumaczenia dla {name}: {e}")
            continue

    conn.commit()
    conn.close()

    print(f"Tłumaczenie zakończone! Przetłumaczono {updated_count} opisów.")

def main():
    print("Rozpoczynam tłumaczenie opisów na polski...")
    translate_descriptions()
    print("Tłumaczenie zakończone!")

if __name__ == "__main__":
    main()
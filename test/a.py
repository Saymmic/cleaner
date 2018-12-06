# ▼▼▼ MY TEMP CODE. DELETE ME ▼▼▼
print()
print()
# ▲▲▲ MY TEMP CODE. DELETE ME ▲▲▲
if __name__ == '__main__':
    parser = argparse
    parser = argparse.ArgumentParser(description='Clean files from tagged code.')
    parser.add_argument(
        '--path',
        type=str,
        default='.',
        help='Path to directory with files to process.',
    )
    parser.add_argument(
        '--processor',
        default='delete',
        help='Line processor. What to do with tagged code?',
    )
    args = parser.parse_args()
    # ▼▼▼ MY TEMP CODE. DELETE ME ▼▼▼
    print()
    # ▲▲▲ MY TEMP CODE. DELETE ME ▲▲▲

    clean(args.path, LINE_PROCESSORS[args.processor])

"""
0. Handluje przypadek gdzie nie ma zamkniętego taga
1. Działa jako podstawowa funkcja
2. Działa jako komenda
3. Printuje jakie pliki i linie przetworzyła 
4. Przyjmuje prostą konfigurację w postaci pythonowego pliku
5. Przyjmuje prostą konfigurację jako parametry wywołania komendy
6. Dodać opis
7. Dodać konfigurację pycharma do live templates
"""

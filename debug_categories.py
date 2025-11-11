import sqlite3

conn = sqlite3.connect('test_questions.db')
cursor = conn.cursor()

print("Category settings:")
cursor.execute('SELECT category, percentage FROM category_settings')
settings = cursor.fetchall()
for cat, pct in settings:
    print(f'  {cat}: {pct}%')

print("\nCalculating questions per category for 50 total:")
total = 50
for cat, pct in settings:
    count = round((pct / 100) * total)
    print(f'  {cat}: {count} questions ({pct}%)')

conn.close()
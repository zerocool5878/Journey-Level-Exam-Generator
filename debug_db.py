import sqlite3

conn = sqlite3.connect('test_questions.db')
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM questions')
total = cursor.fetchone()[0]
print(f'Total questions: {total}')

cursor.execute('SELECT category, COUNT(*) FROM questions GROUP BY category ORDER BY category')
categories = cursor.fetchall()
print('Categories:')
for cat, count in categories:
    print(f'  {cat}: {count}')

conn.close()
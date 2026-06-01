import csv
import re

def parse_time_to_seconds(time_str):
    """Функция для перевода строки времени в секунды"""
    # Ищем все пары вида (число, единица_измерения)
    matches = re.findall(r'(\d+)\s+([а-яё\.]+)', time_str)
    seconds = 0
    
    for num, unit in matches:
        num = int(num)
        if unit == 'дн.':
            seconds += num * 24 * 3600
        elif unit in ('ч.', 'час.'):
            seconds += num * 3600
        elif unit == 'мин.':
            seconds += num * 60
        elif unit == 'сек.':
            seconds += num
            
    return seconds


with open('./data/12.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    students = []
    
    for row in reader:
        # Берем только завершенные попытки студентов, игнорируя итоговые строки
        if row['Состояние'] == 'Завершено':
            score = float(row['Оценка/10,00'].replace(',', '.'))
            time_in_seconds = parse_time_to_seconds(row['Затраченное время'])
            
            students.append({
                'last_name': row['Фамилия'],
                'first_name': row['Имя'],
                'score': score,
                'time': time_in_seconds,
                'orig_score': row['Оценка/10,00'],
                'orig_time': row['Затраченное время']
            })

# 1. Считаем общие средние значения по всем записям студентов
total_students = len(students)
avg_score = sum(s['score'] for s in students) / total_students
avg_time = sum(s['time'] for s in students) / total_students

print(f"Общий средний балл: {avg_score:.2f}")
print(f"Общее среднее время: {avg_time / 60:.1f} мин. ({int(avg_time)} сек.)")
print("-" * 50)

# 2. Фильтруем студентов по условию задачи: балл > среднего И время < среднего
matching_students = [
    s for s in students 
    if s['score'] > avg_score and s['time'] < avg_time
]

# 3. Выводим результат
print(f"Количество людей, подходящих под критерии: {len(matching_students)}")
print("Список этих людей:")
for idx, student in enumerate(matching_students, 1):
    print(f"{idx}. {student['last_name']} {student['first_name']} (Оценка: {student['orig_score']}, Время: {student['orig_time']})")
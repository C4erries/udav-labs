import xml.etree.ElementTree as ET

# Укажите имя обрабатываемого файла ('12.osm' или '12 -2.osm')
file_name = './data/12.osm'

# Загружаем XML-структуру OSM карты
tree = ET.parse(file_name)
root = tree.getroot()

# Переменные для расширенного подсчета парковок
surface_count = 0      # Наземные
underground_count = 0  # Подземные
multistorey_count = 0  # Многоуровневые

# Объединяем поиск по всем трем типам объектов в OSM (точки, линии, отношения)
all_elements = root.findall('.//node') + root.findall('.//way') + root.findall('.//relation')

for element in all_elements:
    # Собираем все теги текущего объекта в словарь {ключ: значение}
    tags = {}
    for tag in element.findall('tag'):
        tags[tag.get('k')] = tag.get('v')
    
    # Проверяем, является ли объект парковкой
    if tags.get('amenity') == 'parking':
        parking_type = tags.get('parking')      # Спецификация типа парковки
        levels = tags.get('building:levels')    # Количество этажей здания
        
        # Логика расширенного распределения:
        if parking_type == 'underground':
            underground_count += 1
            
        elif parking_type == 'multi-storey' or (levels and int(levels) > 1):
            # Если тип указан как многоуровневый ИЛИ этажей здания больше одного
            multistorey_count += 1
            
        else:
            # Все остальные (включая surface, street_side и неразченные amenity=parking)
            surface_count += 1

print(f" Наземные парковки:      {surface_count}")
print(f" Подземные парковки:     {underground_count}")
print(f" Многоуровневые парковки: {multistorey_count}")
# Например, дату в соответствующий столбец вставляют буквально прописью. Вместо 10.09.2024 аналитик видит «десятое сентября»
# Сама же стандартизация ака обработка данных в n8n легко выполняется через python-код. Вот пример такого кода:

from datetime import datetime

#Переименовываем столбцы
for item in _input.all():
    item.json['COURSE_NAME'] = item.json.pop('Название курса')
  
for item in _input.all():
    item.json['LEAD_DT'] = item.json.pop('Дата заявки')
  
#Функция, которая заменяет пропуски в выручке на 0
def revenue(data):
    if not data:
        return '0'
    else:
        return data

#Применяем функцию
for item in _input.all():
    item.json['SCHOOL_REVENUE_VAT'] = revenue(item.json['SCHOOL_REVENUE_VAT'])

for item in _input.all():
    item.json['SRAVNI_REVENUE_VAT'] = revenue(item.json['SRAVNI_REVENUE_VAT'])
  
#Функция для обработки даты
def remove_time_from_date(date_time_str):
    if not date_time_str:
        return date_time_str
    
    current_year = datetime.now().year
    
    #Перебираем форматы дат
    formats = ['%d.%m.%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%d.%m.%Y %H:%M', '%d.%m.%Y', '%d.%m', '%d-%m-%Y', '%d.%m.%Y, %H:%M']
    
    for fmt in formats:
        try:
            #Пробуем распарсить дату
            date_time_obj = datetime.strptime(date_time_str, fmt)
            
            #Если формат без года, добавляем текущий год
            if fmt == '%d.%m':
                date_time_obj = date_time_obj.replace(year=current_year)
            
            #Возвращаем дату в формате 'YYYY-MM-DD'
            return date_time_obj.strftime('%Y-%m-%d')
        except ValueError:
            #Если текущий формат не сработал, продолжаем проверку
            continue
    
    #Если ни один формат не подошел, возвращаем исходную строку
    return date_time_str

#Применяем функцию для форматирования даты
for item in _input.all():
    item.json['LEAD_DT'] = remove_time_from_date(item.json['LEAD_DT'])     

for item in _input.all():
    item.json['SALE_DT'] = remove_time_from_date(item.json['SALE_DT'])  

#Прописываем тип курса
for item in _input.all():
    item.json['POSTBACK_TYPE'] = 'Платный'

#Прописываем модель оплаты
for item in _input.all():
    item.json['MODEL'] = 'CPS'
  
# return _input.all()
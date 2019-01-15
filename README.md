oradump
=========

Класс Oradump предназначен для простейшей выгрузки данных в csv формате. Поскольку Oradump работает поверх
нативного клиента Oracle, мы получаем максимальную производительность и удобство.

### Требования

- Установленный клиент Oracle(11g и выше)
- Путь до папки `bin` клиента Oracle необходимо добавить в переменную PATH.
- Выставить переменную NLS_LANG в соотвествии с кодировкой используемой на стороне сервера Oracle.(к примеру сервера АСР БИТТл - `AMERICAN_AMERICA.AL32UTF8`)
- Подготовить скрипт-шаблон в формате стандартного SQL cо специальными вставками(placeholders) для параметров. Список доступных параметров представлен ниже. 


### Использование

Создание экземпляра класса происходит для конкретного источничка данных. Передаваемые параметры:
   - source_code - код источника данных. Используется для  формирования имени файла csv.
   - conn_str - строка подключения к sqlplus в формате `ПОЛЬЗОВАТЕЛЬ/ПАРОЛЬ@TNS_СТРОКА_ПОДКЛЮЧЕНИЯ`.

Пример: 
```python
src_code = 'asr_kar'
con_str = 'user/password@(DESCRIPTION = (ADDRESS_LIST =  (ADDRESS = (PROTOCOL=TCP)(HOST=10.71.200.15)(PORT=1521)))(CONNECT_DATA = (SERVICE_NAME=URALASR.weskaz)))'
oradmp_instance = oradump.OraDump(src, con_str)
```

Вызов функции dump делает основную работу. Передаваемые параметры:

 - [template] - скрипт-шаблон. Стандартный sql-скрипт со вставками для параметров. Для корректного формирования файла csv 
 необходимо выбираемый поля конкатенировать "разделителем"(delimiter). 
Пример:
```sql
select
     field_1
     ||','||id
     ||','||first_name
     ||','||last_name
     ||','||birth_day
     ....
     ||','||field_N 
 from scheme.employees
 where birth_day between to_date('{dtbegin}', 'dd.mm.yyyy') and to_date('{dtend}', 'dd.mm.yyyy')
```

доступные sql параметры на данный момент:
  - dtbegin - начало временного диапазона
  - dtend - конец временного диапазона


 * [csv] - путь до файла csv
 * [params] - параметры которые будут передаваться в шаблон.
 * [compress] - признак необходимости компрессии(gzip, оригинал удаляется). По умолчанию True.
 
Пример: 
```python
csv_rows_cnt, crc_rows_cnt = oradmp_instance.dump(template, csv, params)
```

из примера выше видно что возвращается два значения
* csv_rows_cnt - количество строк считанное непосресдственно из csv-файла после выгрузки
* crc_rows_cnt - количество строк полученное в момент формирования набора данных на стороне сервера(контрольная сумма)

в случае равенства этих двух значений можно говорить о корректной выгрузке.
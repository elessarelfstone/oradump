oradump
=========

Класс Oradump предназначен для простейшей выгрузки данных в csv формате. Поскольку Oradump работает поверх
нативного клиента Oracle, мы получаем максимальную производительность и удобство.

### Требования

- Установленный клиент Oracle(12.2c и выше)
- Путь до папки `bin` клиента Oracle необходимо добавить в переменную PATH.
- Выставить переменную NLS_LANG в соотвествии с кодировкой используемой на стороне сервера Oracle.(к примеру сервера АСР БИТТл - `AMERICAN_AMERICA.AL32UTF8`)
- Подготовить скрипт-шаблон в формате стандартного SQL cо специальными вставками(placeholders) для параметров. 


### Использование

Вызов функции dump делает основную работу. Передаваемые параметры:   
   - conn_str - строка подключения к sqlplus в формате `ПОЛЬЗОВАТЕЛЬ/ПАРОЛЬ@TNS_СТРОКА_ПОДКЛЮЧЕНИЯ`.

 - [template] - скрипт-шаблон. Стандартный sql-скрипт со вставками для параметров.  
Пример:
```sql
select
     field_1,
     id,
     first_name,
     last_name,
     birth_day,
     ....
     field_N ,
 from scheme.employees
 where birth_day = to_date('{date}', 'dd.mm.yyyy')
```



 * [csv] - путь до файла csv
 * [params] - параметры которые будут передаваться в шаблон.
 * [compress] - признак необходимости компрессии(gzip, оригинал удаляется). По умолчанию True.
 
Пример: 
```python
from oradump import OraDump

con_str = 'user/password@(DESCRIPTION = (ADDRESS_LIST =  (ADDRESS = (PROTOCOL=TCP)(HOST=XXX.XXX.XXX.XXX)(PORT=1521)))(CONNECT_DATA = (SERVICE_NAME=SID.alias)))'
rows_count = OraDump.dump(con_str, template, csv, params)
```

Из примера выше видно, что возвращается количество записей в файле csv.


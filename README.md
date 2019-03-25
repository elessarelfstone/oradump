oradump
=========

OraDump is a simple class for extracting data from Oracle database. It works over the native Oracle client,
so you'll have the fastest and convenient way to get your data dumped.

### Requirements
- Since it works directly with native Oracle client, you need to have installed 12.2c(or higher) version of it on your computer.
- Path to BIN directory of Oracle client have to be in PATH variable.
- Set ENV variable `NLS_LANG` to encoding which used on your Oracle server. Like `AMERICAN_AMERICA.AL32UTF8`
- Installed Python 3.6 or higher.


### Installation
    pip install oradump 


### Usage

Before utilize OraDump you need to prepare SQL-statement that will be used for retrieving data. 
For values that will be changing you set placeholders like that `{start_date}`. So you'll have SQL script, but like as a template.

Example:

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


`from oradump import OraDump` 

By now, you can get data only in csv format. So to achieve this, you need to call `dump` or `dump_gziped`(if want get it compressed) functions.

`dump` example:

    rows_cnt = OraDump.dump(conn_str, template, csv, params)

- conn_str - connection string that you specify when you connect to Oracle instance by native client(sqlplus). 
Like `user/password@(DESCRIPTION = (ADDRESS_LIST =  (ADDRESS = (PROTOCOL=TCP)(HOST=XXX.XXX.XXX.XXX)(PORT=1521)))(CONNECT_DATA = (SERVICE_NAME=SID.alias)))`

- template - SQL template described above
- csv - path to target csv file
- params - parameters passing into SQL template and substituting into according placeholders.

`dump_gziped` example:

    rows_cnt = OraDump.dump_gziped(conn_str, template, gzip, params, del_orig=False)
- gzip - path to target gziped csv file
- del_orig - whether if you want to delete csv file that OraDump gets before compressing.

purposes of rest of parameters are the same as in `dump`
 
If all went successful number of retrieved rows is returned. 
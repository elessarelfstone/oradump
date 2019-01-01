OraDump
=========

OraDump is an easy command-line tool for extracting data from
Oracle database. It works over the native Oracle client, so you'll have the fastest and convenient way
to get your data dumped. Also, you can use the API of OraDump, for any kind of purposes, like writing pipelines(Airflow, Luigi). 


### Requirements

 - Since it works directly with native Oracle client, you need to have installed 11g version of it on your computer.
And path to BIN directory have to be in PATH variable. Also, for right encoding it's important to set Oracle
system env variable NLS_LANG. In some cases you might want set it in `AMERICAN_AMERICA.CL8MSWIN1251`.
 - Installed Python over 3.7
 
### Installation 

In terminal go into directory where you have pulled it or downloaded and run this
`pip install --editable .`. After that, in case of success you can use the OraDump.


### Usage
Now, you can use follow options and arguments:
 - sourcecode - specify which server we are connecting to. List of them you can find by opening sources.db file. 
 In case you need to add some other sources. Keep in mind that field `code` have to be unique.
 
 - dtbegin - if you are gonna dump data from table piece by piece specifying date period, you'll need here specify start of period.
 
 - dtend - the same sake as above but for end of period.
 
 - dtsys - the date that this extraction related to. By default it will be current day.
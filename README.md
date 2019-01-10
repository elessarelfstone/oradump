OraDump
=========

OraDump is an easy class for extracting data from Oracle database. It works over the native Oracle client, so you'll have the fastest and convenient way
to get your data dumped. 

### Requirements

 - Since it works directly with native Oracle client, you need to have installed 11g version of it on your computer.
And path to BIN directory have to be in PATH variable. Also, for right encoding it's important to set Oracle
system env variable NLS_LANG. In some cases you might want set it in `AMERICAN_AMERICA.CL8MSWIN1251`.
 - You need to prepare template for sql script that you'll pass to oradump. Examples you can find in `tests` directory. Be sure that the parameters 
 you pass to oradump specified as attributes in OraSqlParams dataclass.
 
 
### Installation 

In terminal go into directory where you have pulled it or downloaded and run this
`pip install --editable .`. After that, in case of success you can use the OraDump.


### Usage


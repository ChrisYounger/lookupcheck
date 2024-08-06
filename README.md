# Description

Analyse lookup files for common errors, such as:
- blank column names
- lines with an unexpected amount of columns
- leading/trailing whitespace in column headings
- does not check for large files but outputs the size so you can decide on your own limits



# Usage: 

- provide a field called "path" which is the full path to the CSV files to check
- Will output fields:
    - lookupcheck_status: the warnings and errors found with the file (or OK)
    - lookupcheck_size: the size of the file in bytes



# Example:

```
| rest splunk_server=local /servicesNS/-/-/data/lookup-table-files 
| rename eai:data as path
| search NOT path IN ("*.kmz", "*.alive")
| table path
| lookupcheck
| search NOT lookupcheck_status="OK"
| table path lookupcheck_status lookupcheck_size
```

Copyright (C) 2024 Chris Younger | [Splunkbase](https://splunkbase.splunk.com/app/) | [Source code](https://github.com/ChrisYounger/lookupcheck) | [My Splunk apps](https://splunkbase.splunk.com/apps/#/author/chrisyoungerjds)

Script ```os_parser.py ``` cheking and parsing CRUD files in OS directories.
Using Watchdog Python library

endpoint - Work directory for parsing
patterns = **["*.mp3"]** - Parsing by format

if ``` Handler.on_create ``` method detect new file. it will send request with file path
to ``` google_api.py ``` script.



``` google_api.py ``` use Google Speech-to-text library for convert voice in text.
**Need Google API Key**.

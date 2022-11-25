"""
libs.string

By default uses 'en-us.json file inside the 'strings' top-level folder    
"""
import json

default_locale = "en-us.json"
cached_strings = {}

def refresh():
    global cached_strings
    with open(f"strings/{default_locale}.json") as f:
        cached_strings = json.load(f)
        
def gettext(name):
    return cached_strings[name]
        
refresh()
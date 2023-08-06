# Airtable Cacher

This plugin is fork of the work done by Ron Mountjoy on `Airtable Caching`
https://github.com/rmountjoy92/AirtableCaching

# Caching
First you must setup a recurring script that will cache the table.

```
from airtable_cacher import Base

airtable = Base(<AIRTABLE_BASE_ID>, <AIRTABLE_API_KEY>)

"""
Main Function
"""

airtable.cache_table(<AIRTABLE_PRODUCTS_TABLE>)

```

You can optionally supply a third argument to `Base()` for setting the json folder like so:

```
from airtable_cacher import Base

airtable = Base(<AIRTABLE_BASE_ID>, <AIRTABLE_API_KEY>, "my_json_folder")
```

## Caching images

If you'd like to cache images, you can do so by supplying an optional fourth argument

# Accessing cached data

```
from airtable_cacher import Table

products_table = Table(<AIRTABLE_BASE_ID>,<AIRTABLE_PRODUCTS_TABLE>)
```

If you have supplied a custom JSON folder path in the caching, you supply that as an optional third argument in
 `Table()`
 
```
from airtable_cacher import Table

products_table = Table(<AIRTABLE_BASE_ID>,<AIRTABLE_PRODUCTS_TABLE>, "my_json_folder")
```

To get all records then use

```
records = products_table.all()
```
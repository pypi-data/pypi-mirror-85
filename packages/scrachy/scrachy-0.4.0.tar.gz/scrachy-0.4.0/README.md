# Scrachy
Scrachy is a flexible cache storage backend for [Scrapy](https://scrapy.org/) that stores its data in a relational database using [SQLAlchemy](https://www.sqlalchemy.org/).
It also comes with a downloader middleware that will optionally ignore requests that are already in the cache.

# Install
You can install the latest version from git:

```
>pip install git+https://bitbucket.org/reidswanson/scrachy.git
``` 

or from PyPI:

```
>pip install scrachy
```

# Documentation
## Storage Backend
To (minimally) use the storage backend you simply need to enable caching by adding the following to your `settings.py` file:  
```python
# Enable caching
HTTPCACHE_ENABLED = True

# Set the storage backend to the one provided by Scrachy.
HTTPCACHE_STORAGE = 'scrachy.middleware.httpcache.AlchemyCacheStorage'

# You do not need any other settings for the engine to work, but by default
# it will use an in memory sqlite database, which is probably not what you
# want. To use another database configure the following settings.
# Set the type of database to use. It must be one of the supported types
# provided by SQLAlchemy.
SCRACHY_DIALECT = <database-dialect>

# Set the driver to use. This must also be recognized by SQLAlchemy, but can
# be None (the default) to use the the SQLAlchemy default driver.
SCRACHY_DRIVER = <database-driver>

# Set the hostname of the database server. This should be None for sqlite 
# databases. If it is None for other databases (the default) it is assumed to be
# localhost.
SCRACHY_HOST = <database-hostname>

# Set the port the database server is listening on. If set, this must be an
# integer. If it is None (the default), the default database port is used.
SCRACHY_PORT = <database-port>

# The schema where the database will be created. This is only valid for
# databases that support schemas (e.g., postgresql).
SCRACHY_SCHEMA = <database-schema>

# Set the name of the database. For sqlite this should be the path to the
# database file, which will be created if it does not exist. For other
# databases this should be the name of the database. Note, the database must
# exist prior to crawling, but all necessary tables will be created on the
# first run. This can only be None for in memory sqlite databases. 
SCRACHY_DATABASE = <database-name>

# A locally accessible file that stores the username and password used to
# connect to the database. Each line contains an '=' separated key/value pair
# where the only valid keys are `username` and `password`. Both are optional,
# but you will not be able to connect if they do not match the security
# settings of your database.
SCRACHY_CREDENTIALS = <credentials-file>

# There is some contention between this storage engine and the
# HttpCompressionMiddleware. I believe this is because of the way encoding
# inference is done in HtmlResponses. The header for (at least some) pages
# that have been compressed specify the encoding as the compression type.
# The first time the page is downloaded the response is compressed and the
# compression middleware recognizes it as such and successfully deflates the
# text. However, the body then gets cached in the database as plain text.
# So, when the page is retrieved from the cache the encoding inference still
# says that it is compressed, but when the compression middleware tries to
# deflate the content, it raises an exception because it is not actually
# compressed. I may try to solve this in a more robust way in the future, but
# for now the easiest solution is to change the priority of the 
# HttpCompressionMiddleware so that it comes after the HttpCacheMiddleware.
# By default the HttpCacheMiddleware has a priority of 900 (higher means lower
# priority).
DOWNLOADER_MIDDLEWARES = {
    # Other middlewares excluded but would go here.
    
    # It's not exactly clear to me the best place for this, but it must be
    # after the HttpCacheMiddleware for now.
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 1000,
}
```
The storage backend also has several other features that are useful for specialized crawling and scraping tasks.
For other configuration options and features please see the full documentation on [Read the Docs](https://scrachy.readthedocs.io/en/latest).

## Ignoring Cached Items
This project also comes with a middleware to ignore any requests that are already cached.
For example, sometimes you want to scrape a domain periodically looking for new pages.
In this scenario it often doesn't make sense, and wastes resources, to reparse the pages you have already cached (unless you have changed your parsing rules of course).
Enabling this middleware will allow you to specify which pages from your cache you would like to ignore.

To activate this middleware simply add the class ``IgnoreCachedResponse`` to the set of ``DOWNLOADER_MIDDLEWARES`` as follows:

```python
DOWNLOADER_MIDDLEWARES = {
    # You probably want this early in the pipeline, because there's no point
    # in the other middleware if its in the cache and we are going to ignore it
    # anyway.
    'scrachy.middleware.ignorecached.IgnoreCachedResponse': 50,

    # Other middlewares excluded but would go here.
}
``` 

You can choose not to ignore requests using 3 methods.

  1. Any request that is excluded from caching by setting the request meta variable ``dont_cache`` to ``True``
  2. A request can be excluded by setting the new request meta variable ``dont_ignore`` to ``True``
  3. A request can be ignored if its url matches a regular expression in the settings variable ``SCRACHY_IGNORE_EXCLUDE_URL_PATTERNS``, which takes a list of strings that can be compiled into regular expressions.

# License
Scrachy is released using the GNU Lesser General Public License.
See the [LICENSE](LICENSE.md) file for more details.
Files that are adapted or use code from other sources are indicated either at the top of the file or at the location of the code snippet.
Some of these files were adapted from code released under a 3-clause BSD license.
Those files should indicate the original copyright in a comment at the top of the file.
See the [BSD_LICENSE](BSD_LICENSE.md) file for details of this license.

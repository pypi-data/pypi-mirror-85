Summary
-------
Simple ElasticSearch indexing integration for CubicWeb


Parameters
~~~~~~~~~~

* elasticsearch-locations (CW_ELASTICSEARCH_LOCATIONS)
* index-name (CW_INDEX_NAME)
* elasticsearch-verify-certs (CW_ELASTICSEARCH_VERIFY_CERTS)

Pyramid debug panel
~~~~~~~~~~~~~~~~~~~

To activate the debug panel, you'll need to install ``pyramid_debugtoolbar``,
typically with::

  pip install pyramid_debugtoolbar

Then, you'll have activate the debug toolbar and include the ElasticSearch
panel in your ``pyramid.ini``:

  pyramid.includes =
      pyramid_debugtoolbar
  debugtoolbar.includes =
      cubicweb_elasticsearch.pviews.espanel


**Alltext** field
~~~~~~~~~~~~~~~~~~

The `cubicweb_elasticsearch.search_helpers.compose_search` referencies
a custom `alltext` field which contains all indexed text. This field  must be
defined in the custom Indexer mapping.
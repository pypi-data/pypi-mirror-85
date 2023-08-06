# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['osmpy']

package_data = \
{'': ['*']}

install_requires = \
['geojson==2.5.0',
 'pandas>=1.0.0,<2.0.0',
 'pyproj',
 'requests==2.23.0',
 'retry',
 'shapely==1.7.0']

setup_kwargs = {
    'name': 'osmpy',
    'version': '0.1.1',
    'description': 'Powerfull wrapper around OSM Overpass Turbo to query regions of any size and shape',
    'long_description': '**Powerfull wrapper around OSM Overpass Turbo to query regions of any size and shape**\n\n```bash\npip install osmpy\n```\n\n#### List precooked queries\n```python\nosmpy.list_queries()\n\n            name                                         docstring\n0      Amenities          Location of amenities within a boundary \n1  AmentiesCount   Number of amenities per type within a boundary \n2     RoadLength     Length of road by roadtype within a boundary \n```\n\n#### Get all amenities in a boundary\n```python\nimport osmpy\nfrom shapely import wkt\n\nboundary = wkt.loads(\'POLYGON((-46.63 -23.54,-46.6 -23.54,-46.62 -23.55,-46.63 -23.55,-46.63 -23.54))\')\nosmpy.get(\'Amenities\', boundary)\n\n    type          id        lat        lon                                               tags\n0   node   661212030 -23.544739 -46.626160           {\'amenity\': \'fuel\', \'name\': \'Posto NGM\'}\n1   node   661212089 -23.547450 -46.626073  {\'amenity\': \'fuel\', \'name\': \'Posto Maserati\', ...\n2   node   745733280 -23.541411 -46.613930  {\'addr:city\': \'São Paulo\', \'addr:housenumber\':...\n3   node   745733292 -23.542070 -46.614916  {\'addr:city\': \'São Paulo\', \'addr:housenumber\':...\n4   node   889763809 -23.542558 -46.620360  {\'addr:housenumber\': \'110/C9\', \'addr:street\': ...\n..   ...         ...        ...        ...                                                ...\n84  node  5663737625 -23.540027 -46.605425  {\'access\': \'yes\', \'addr:city\': \'São Paulo\', \'a...\n85  node  5990269247 -23.540650 -46.607532  {\'addr:city\': \'São Paulo\', \'addr:housenumber\':...\n86  node  6621564995 -23.543880 -46.626414  {\'access\': \'yes\', \'addr:city\': \'São Paulo\', \'a...\n87  node  6625433725 -23.546727 -46.623956  {\'access\': \'yes\', \'addr:city\': \'São Paulo\', \'a...\n88  node  6625433753 -23.547111 -46.624790  {\'access\': \'yes\', \'addr:city\': \'São Paulo\', \'a...\n```\n\n#### Total road length by road type\n```python\nosmpy.get(\'RoadLength\', boundary)\n\n               count     length\nhighway                        \nbus_stop           1     82.624\ncorridor           2    482.195\ncycleway           1    134.197\nfootway          116   5473.419\nliving_street      3    422.378\npath               4    735.539\npedestrian         3     90.327\nplatform           3    239.206\nprimary           28   2067.562\nprimary_link      12   1123.544\n```\n\n#### You can use your own query\n\n```python\n\n## Use `{boundary}` as a placeholder.\nquery = """\n    [out:json];\n    node["amenity"](poly:"{boundary}");\n    out body geom;\n    """\n\nosmpy.get(query, boundary)\n```\n\n## Create a precooked query\n\n```python\nclass YourPrecookedQuery(osmpy.query.QueryType):\n\n    query = """\n    <OSM Overpass Turbo Query>\n    """\n\n    docstring = """\n    <Query description>\n    """\n\n    def postprocess(self, df):\n        """Post process API result\n        """\n        return df[\'tags\'].apply(pd.Series).groupby(\'amenity\').sum()\n\nosmpy.get(YourPrecookedQuery, boundary)\n```\n\n:point_right: Leave an issue or PR if you want to add a new query to the package\n\n## Credits\n\nFree software: MIT license\n\nFunction `katana` from @snorfalorpagus.',
    'author': 'Joao Carabetta',
    'author_email': 'joao.carabetta@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JoaoCarabetta/osmpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

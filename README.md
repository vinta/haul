Haul
====

Find thumbnails and original images from URL or HTML file.


## Usage

``` py
import haul

haul.find_images('http://fancy.com/things/307759676836021549/Patent-Leather-Heels-by-Jimmy-Choo')
```

or

``` py
from haul import Haul

h = Haul()
h.find_images('http://fashion-fever.nl/dressing-up/', propagate=True)
```


## Run Tests

``` bash
$ cd tests
$ python test.py
```

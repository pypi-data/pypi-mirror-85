#### To run tests:

`python setup.py test`

#### To upload to PyPi 

Run the upload script via:

`sh upload.sh`

You'll be prompted for our PyPi username and password, which you can get from Noah if you don't already have it. 

Make sure you've activated a [virtualenv](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) when you run `pip install`, or else this package will be installed globally.

Then, once you're ready to install, just run:

`pip install sgvalidator` 

TODO:
* Coming soon
* Add to the preprocessing step
* Looking for blank or nulls?
* Look at open/close algo from store-locator. Start validating whether our crawls are high quality enough for open/close. 
* Count-validation → Look at only the file from the vendor that is vendor_for_prod (instead of avg Mobius and mozenda together).
 
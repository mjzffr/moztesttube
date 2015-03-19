moztesttube
===========

Motivation
----------

Obtain test data from sources like http://crash-stats.mozilla.com/ or http://bugzilla.mozilla.org/ to help automate the reproduction of bugs.

__Note__: features of this tool may require authorization to access sensitive data about Mozilla users (personally identifiable information -- PII), which in turn may require you to be a Mozilla employee.

Example
-------

Obtain YouTube video urls that appear in recent crash reports. These URLs can be provided to automated playback tests like firefox-media-tests.

   ```sh
   python moztesttube.py --token $your_api_token --max_results 50 --base_query 'platform=Windows&product=Firefox&url=$https://www.youtube.com/watch?v=&url=!~list&url=!~index&version=37.0'
   ```

This returns a selection of YouTube urls associated with the top 10 Firefox crashes in the past week, in ini format.

Setup
-----

* Clone the source. 

* Create a virtualenv called `foo`. (Optional, but highly recommended.)

   ```sh
   $ cd moztestube
   $ virtualenv foo
   $ source foo/bin/activate #or `foo\Scripts\activate` on Windows
   ```

* Install the requirements.

   ```sh
   $ pip install -r requirements.txt
   ```


License
-------
This software is licensed under the [Mozilla Public License v. 2.0](http://mozilla.org/MPL/2.0/).
 

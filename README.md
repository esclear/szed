SZED
====
## SZ Epaper Downloader

This is a simple python script that downloads a set of configurable issues of the Süddeutsche Zeitung.

Note that **you must have a SZ Account** to use this script!

#### Features:
- Configurable Issues
- Configurable Path
- Download Issues of specific dates

#### Usage:
Before you can use it the first time, you have to set your username and password.
To do that, open up szed.py and edit the `username` and the `password` settings in the `CONFIG SECTION`.

By default the downloaded issues are: `Deutschlandausgabe_komplett`, `Bayernausgabe_komplett` and `Stadtausgabe_komplett`.

The available issues are:

- `Bayernausgabe_komplett`
- `Bayernausgabe_basis`
- `Deutschlandausgabe_komplett`
- `Deutschlandausgabe_basis`
- `Stadtausgabe_komplett`
- `Stadtausgabe_basis`
- `Stadtausgabe_Muenchen-City`
- `Stadtausgabe_Muenchen-Nord`
- `Stadtausgabe_Muenchen-Sued`
- `Stadtausgabe_Muenchen-West`
- `Dachau`
- `Ebersberg`
- `Erding`
- `Freising`
- `Fuerstenfeldbruck`
- `Starnberg`
- `Wolfratshausen`

To download ohter issues as well, simply uncomment them!

I would recommend to run the script daily as a cronjob, eg. at 4:00 AM.

#### Arguments:
<pre>
./szed.py [OPTIONS]
    Possible Arguments:
    --place <directory>, -p <directory>
		Set the folder the files shall be downloaded to
	--date <date>, -d <date>
		Set the date of the issue you want to download. Must be in <a href="https://xkcd.com/1179/">ISO 8601 Format</a>.
</pre>

#### License:
SZED is made by Daniel Albert and is released under the MIT License.
Refer to the LICENSE file for further information.

(c) 2013 - 2014 Daniel Albert

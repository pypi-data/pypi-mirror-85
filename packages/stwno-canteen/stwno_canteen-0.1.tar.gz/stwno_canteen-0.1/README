
<p align="center">
  <img style="width:40%"src="https://github.com/somsky/stwno_canteen_python/raw/master/logo.png"/>
</p>

STWNO Canteen is a simple python API for querying the menu of the canteens operated by the STWNO (Studentenwerk Niederbayern/Oberpfalz) in Lower Bavaria and Upper Palatinate.


# Features
* Simple to use API for querying the menu for any given day in any STWNO canteen
* Command Line Interface to print todays menu to the terminal

# Usage

```python
import datetime
import stwno_canteen

today = datetime.date.today()
menu = getMenu(stwno_canteen.Canteen.OTH_RGB_CANTEEN_LUNCH, datetime.date.today())
print(menu)

```

# Requirements
```
$ python --version >= 3.8.0
```

# Installation

You can install the API manually, or by using pip:
```
$ python -m pip install stwno_canteen
```

# Command Line Interface

The command line interface allows to fetch the menu for the current day of a given canteen:

```
$ python -m stwno_canteen -c <canteen_identifier>
```

For a list of available identifiers, check out the Canteens dictionary in the
[constants file](https://github.com/somsky/stwno_canteen_python/blob/master/stwno_constants.py).

# Additional Notes
I do not guarantee for the correctness and completeness of the parsed ingredients/allergenes.
This is mostly because there tend to be errors in the CSV files from STWNO frequently, which
makes it hard to parse. If you suffer from an allergy, you should not rely on this API.


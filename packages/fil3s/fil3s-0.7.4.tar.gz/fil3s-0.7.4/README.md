# Fil3s
Author(s):  Daan van den Bergh.<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved.<br>
Supported Operating Systems: osx & linux.<br>
<br>
<br>
<p align="center">
  <img src="https://github.com/vandenberghinc/storage/blob/master/images/logo.png?raw=true" alt="Bergh-Encryption" width="50"/>
</p>

# Installation
	pip3 install fil3s --upgrade

# Files:

## The Directory object class.
The Files.Directory() object class. 
<br>Check the source code for more functions & options.
```python

# import the package.
import os
from fil3s import Files, Formats

# initialize a directory.
directory = Files.Directory(path='directory/')

# check the directory.
directory.check(
	owner=os.eniron.get('USER'),
	group=None,
	permission=755,
	sudo=True,
	recursive=False,
	silent=False,
	hierarchy={
		"subdir/":{
			"path":"subdir/",
			"directory":True,
			"owner":os.eniron.get('USER'),
			"group":None,
			"permission":755,
			"sudo":True,
		},
	})
# directory.file_path = <Formats.FilePath>
# directory.file_path.path

# content.
paths = directory.paths(
	recursive=False,
	banned=[],# use full file paths.
)

# check contains.
bool = directory.contains("subdir", "/", recursive=False)

# returnable functions.
path = directory.join("subdir", "/")
path = directory.join("subdir/settings", type="json")
path = directory.oldest_path()
path = directory.random_path(length=10, type="/")
path = directory.generate_path(length=10, type="/")
path = directory.structured_join("subdir", type="/", structure="alphabetical")

```

## The Dictionary object class.
The Files.Dictionary() object class. 
<br>Check the source code for more functions & options.
```python

# import the package.
from fil3s import Files, Formats

# initialize the dictionary object.
dictionary = Files.Dictionary(
	path='dictionary.json',
	load=True,
	default={
		"Hello":'World!',
	})
# dictionary.file_path = <Formats.FilePath>
# dictionary.file_path.path

# the dict is already loaded by the load=True parameter.
dictionary.load()
dictionary.dictionary

# saving.
dictionary.save({"Hello":"World!"})
# equal to.
dictionary.dictionary = {"Hello":"World!"}
dictionary.save()

# check dictionary.
dictionary.check(
	save=True,
	default={
		"Hello":'World!',
		"Hi":'World!',
	})

# divide the dictionary into a list of dicts.
list = dictionary.divide(into=2)

```

## The Array object class.
The Files.Array() object class. 
<br>Check the source code for more functions & options.
```python

# import the package.
from fil3s import Files, Formats

# initialize the array object.
array = Files.Array(path="array.json", load=False)

# loading the array.
array.load()
array.array

# saving the array.
array.save([1, 2, 3])
# equal to.
array.array = [1, 2, 4]
array.save()

# sum the array into a string.
str = array.string(joiner=' ')

# remove items from the array by value.
list = array.remove(items=[1])

# divide the array into multiple arrays.
list = array.divide(into=3)

```

## The Zip object class.
The Files.Zip() object class. 
<br>Check the source code for more functions & options.
```python

# import the package.
from fil3s import Files, Formats

# initialize the zip object.
zip = Files.Zip(path="myzip.zip")

# create a zip from one dir / file.
zip.create(
	source="directory/", 
	remove=False, 
	sudo=False)

# create a zip from multiple dirs / files.
zip.create(
	source=["directory/", "file/"], 
	remove=False, 
	sudo=False)

# extracting the zip (leave the base None to use the zips base).
zip.extract(
	base=None, 
	remove=False, 
	sudo=False)

```

# Formats:

## The FilePath object class.
The Formats.FilePath() object class. 
Most Files.* classes contain a FilePath object.
<br>Check the source code for more functions & options.
```python

# import the package.
from fil3s import Files, Formats

# initialize the file path object.
file_path = Formats.FilePath(path='directory/', check_existance=False)
path = file_path.path

# returnable functions.
name = file_path.name()
extension = file_path.extension()
base = file_path.base(back=1)
size = file_path.size(mode="auto", options=["auto", "bytes", "kb", "mb", "gb", "tb"], type=str)
bool = file_path.exists()
bool = file_path.mount()
bool = file_path.directory()

# executable functions.
file_path.delete(forced=False, sudo=False, silent=False)
file_path.move(path="new-directory/", sudo=False, silent=False)
file_path.copy(path="new-directory/", sudo=False, silent=False)
file_path.open(sudo=False)

# file permissions.
permission = file_path.permission.get()
file_path.permission.set(permission=755, sudo=False, recursive=False, silent=False)
file_path.permission.check(permission=permission, sudo=False, recursive=False, silent=False)

# file ownership.
owner, group = file_path.ownership.get()
file_path.ownership.set(owner=owner, group=group, sudo=False, recursive=False, silent=False)
file_path.ownership.check(owner=owner, group=group, sudo=False, recursive=False, silent=False)

```
## The Date object class.
The Formats.Date() object class. 
<br>Check the source code for more functions & options.
```python

# import the package.
from fil3s import Files, Formats

# initialize the date object.
date_object = Formats.Date()

# variables.
date_object.seconds
date_object.minute
date_object.hour
date_object.day
date_object.day_name
date_object.week
date_object.month
date_object.month_name
date_object.year
date_object.date
date_object.timestamp
date_object.shell_timestamp
date_object.seconds_timestamp
date_object.shell_seconds_timestamp
date_object.time

# functions.
stamp = increase(self, date_object.timestamp, weeks=0, days=1, hours=0, seconds=0, format="%d-%m-%y %H:%M")
stamp = decrease(self, date_object.timestamp, weeks=0, days=1, hours=0, seconds=0, format="%d-%m-%y %H:%M")
comparison = compare(self, stamp, date_object.timestamp, format="%d-%m-%y %H:%M")
stamp = convert(self, date_object.timestamp, input="%d-%m-%y %H:%M", output="%Y%m%d")
seconds = to_seconds(self, date_object.timestamp, format="%d-%m-%y %H:%M")
stamp = from_seconds(self, seconds, format="%d-%m-%y %H:%M")

```

### Response Object.
When a function completed successfully, the "success" variable will be "True". When an error has occured the "error" variable will not be "None". The function returnables will also be included in the response.

	{
		"success":False,
		"message":None,
		"error":None,
		"...":"...",
	}
# Serial port enumerator

List USB serial devices on a linux machine using udev.

## Installation

This package is hosted on github only. Please install or upgrade using

```
$ python3 -m pip install -U git+https://github.com/phildubach/serports@main
```

## Running `lser`

When installing the package using pip as described above, a new console script
entry point named `lser` is created and linked from $HOME/.local/bin, which
should be on the $PATH.

Running `lser` without arguments will list all USB serial ports along with
the vendor and model information. The list is ordered by initialization time,
newest entry last.

To keep listing devices as they get added or removed, run `lser -f` or `lser
--follow`. Abort with Ctrl-C.

`lser -l` or `lser --last` lists only the last added device. Only the device
file is returned, without vendor or model information. This can be useful
for starting a terminal program connected to a recently added device, e.g.

```
$ miniterm $(lser -l) 115200
```

Finally, `lser -w` or `lser --wait` is similar to `-l` or `--last`, but this
time, the scripts waits for a new device to be connected. This could be used to
capture serial output from a new device as soon as it becomes available, by
running something like the following command before plugging in the device:

```
$ miniterm $(lser -w) 115200
```


Command line client for [Myki Oximeter](https://mykifamily.com/myki-pulse-oximeter).
Connects over bluetooth to the device and reads heart rate, oxygen saturation and shows the pleth wave.
Tested only with the Myki oximeter but should work with all devices which use a BerryMed sensor.

![Mykioxi](/mykioxi.png)

Installation
---

Python3.5+ is required. Install with `pip3` (preferably into a virtual env):
```
$ pip install mykioxi
```

Usage
---
When started without arguments, it will autodetect the device and show the measurements on a single line which is periodically updated:
```
$ mykioxi
Found: 00:A0:50:AC:38:43 (BerryMed)
Connected: True
BPM: 78  [****      ]  SpO2:  99
```

There is also a `multiline` option which prints every new measurement on a separate line:
```
$ mykioxi --multiline
Found: 00:A0:50:AC:38:43 (BerryMed)
Connected: True
[2020-11-17 10:09:13]   BPM:  83    SpO2:  98
[2020-11-17 10:09:14]   BPM:  85    SpO2:  97
[2020-11-17 10:09:19]   BPM:  82    SpO2:  96
[2020-11-17 10:09:21]   BPM:  80    SpO2:  97
[2020-11-17 10:09:23]   BPM:  75    SpO2:  97
[2020-11-17 10:09:26]   BPM:  76    SpO2:  97
[2020-11-17 10:09:28]   BPM:  75    SpO2:  98
[2020-11-17 10:09:30]   BPM:  73    SpO2:  97
...
```


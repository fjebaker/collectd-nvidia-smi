# collectd-nvidia-smi
Python plugin for collectd, wrapping system calls to nvidia-smi.

I wrote this very quickly, but thought it may be useful for others. This script will provide monitoring data for any nVidia GPU with the nVidia driver, and by default will pass

- free, used, and total GPU memory (mb)
- GPU, memory, encoder and decoder utilization (%)
- temperature (deg C)
- power draw, power limit, enforced power limit, max power limit (Watts)
- fan speed (%)

to collectd.

## Usage
To use this script, place it in some location, hence referred to as `<scriptpath>/gpu_monitor.py`. Then, create `/etc/collectd/collectd.conf.d/gpu_monitor.conf` with the following content:
```
LoadPlugin python

<Plugin python>
    LogTraces false
    Interactive false
    ModulePath "<scriptpath>"
    Import "gpu_monitor"
</Plugin>
```

Make sure 
```
<Include "/etc/collectd/collectd.conf.d">
    Filter "*.conf"
</Include>
```
is in `/etc/collectd/collectd.conf`, else the module will not be loaded.

## Discussion
Depending on which `Python.h` files collectd was compiled with, the native python environment may be 2.x or 3.x, which I have tried to account for in my implementation.

The [collectd python api](https://collectd.org/documentation/manpages/collectd-python.5.shtml) is unfortunately very poorly documented, but in essence most of what occurs in the script is pretty self explanatory -- with more of the `instance` assignments just being document labels in your database.

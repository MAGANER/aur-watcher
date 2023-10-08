# aur-watcher
script for filtered search through AUR.

# Note
this script requires ```requests``` package.<br>

# Usage
```aurwatcher p=micro``` - you will get about 756 found items.<br>
```aurwatcher p=micro d=editor``` you will get about 3 found items, since output is filtered with description that contains ```editor``` substring.<br>

You can filter your output with following flags:<br>
```d``` - to filter with description.<br>
```n``` - to filter with name.<br>
```m``` - to filter with maintainer.<br>

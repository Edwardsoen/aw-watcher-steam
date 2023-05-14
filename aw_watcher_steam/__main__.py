import sys
import os
import aw_watcher_steam
path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, "..")
sys.path.insert(0, path)
aw_watcher_steam.main()



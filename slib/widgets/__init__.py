# -*- coding: utf-8 -*-


from . import system
from . import mlocate
from . import img
from . import yandex
from . import google
from . import twitter

try :
	from . import torrents
except ImportError, err :
	print "ImportError(%s): widgets.torrents.* is disabled" % (str(err))

try :
	from . import steam
except ImportError, err :
	print "ImportError(%s): widgets.steam.* is disabled" % (str(err))

try :
	from . import kf
except ImportError, err :
	print "ImportError(%s): widgets.kf.* is disabled" % (str(err))


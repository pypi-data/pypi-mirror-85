from wx import PyEventBinder

# Based on wxPython
# Copyright: (c) 2018 by Total Control Software
# License:   wxWindows License


def dummy_function(*args, **kwargs):
	return 0


MEDIABACKEND_DIRECTSHOW = 'wxAMMediaBackend'
MEDIABACKEND_GSTREAMER = 'wxGStreamerMediaBackend'
MEDIABACKEND_MCI = 'wxMCIMediaBackend'
MEDIABACKEND_QUICKTIME = 'wxQTMediaBackend'
MEDIABACKEND_REALPLAYER = 'wxRealPlayerMediaBackend'
MEDIABACKEND_WMP10 = 'wxWMP10MediaBackend'
MEDIACTRLPLAYERCONTROLS_DEFAULT = 3
MEDIACTRLPLAYERCONTROLS_NONE = 0
MEDIACTRLPLAYERCONTROLS_STEP = 1
MEDIACTRLPLAYERCONTROLS_VOLUME = 2
MEDIASTATE_PAUSED = 1
MEDIASTATE_PLAYING = 2
MEDIASTATE_STOPPED = 0
class MediaCtrl: ...
class MediaCtrlPlayerControls: ...
class MediaEvent: ...
class MediaState: ...
USE_MEDIACTRL = 0
wxEVT_MEDIA_FINISHED = 0
wxEVT_MEDIA_LOADED = 0
wxEVT_MEDIA_PAUSE = 0
wxEVT_MEDIA_PLAY = 0
wxEVT_MEDIA_STATECHANGED = 0
wxEVT_MEDIA_STOP = 0
EVT_MEDIA_FINISHED = PyEventBinder()
EVT_MEDIA_LOADED = PyEventBinder()
EVT_MEDIA_PAUSE = PyEventBinder()
EVT_MEDIA_PLAY = PyEventBinder()
EVT_MEDIA_STATECHANGED = PyEventBinder()
EVT_MEDIA_STOP = PyEventBinder()

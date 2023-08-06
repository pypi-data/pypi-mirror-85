import wx

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ViewSettings(metaclass=Singleton):
    def __init__(self):
        #print(wx.ScreenDC().GetPPI())
        self.HEADER_FONT = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.TITLE_FONT = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.MAIN_FONT = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.BUTTON_FONT = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.RANGE_EDIT_FONT = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.SMALL_FONT = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.EDIT_FONT = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)

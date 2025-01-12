import datetime
from PIL import ImageGrab
import wx


class MyFrame(wx.App):

    def OnInit(self):
        frame = wx.Frame()
        frame.Show(False)
        self.SetProperties()
        self.CreateCtrls()
        self.BindEvents()

    def SetProperties(self):
        pass

    def CreateCtrls(self):

        self.panel = wx.Panel(self, -1)
        self.btnScreenshot = wx.Button(self.panel, -1, "Take a screenshot")
        self.btnClose = wx.Button(self.panel, -1, "&Close")

    def BindEvents(self):
        """
        Bind some events to an event handler.
        """

        # Bind events to an events handler.
        self.Bind(wx.EVT_BUTTON, self.OnScreenshot, self.btnScreenshot)
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, self.btnClose)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnScreenshot(self, event):
        """
        Thank to Andrea Gavana.
        """

        screen = wx.ScreenDC()
        size = screen.GetSize()

        # Debugging : see if pixel values are okay.
        print(wx.DisplaySize())

        width = size[0]
        height = size[1]
        filename = datetime.datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S.png"
        )  # filename determine
        ImageGrab.grab().save(filename, quality=100)


if __name__ == "__main__":
    app = wx.App()
    app.MainLoop()

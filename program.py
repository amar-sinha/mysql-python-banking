import wx, mysql.connector, time, panels, methods
from datetime import datetime

class Program(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'mysql_python_banking')

        sizer = wx.BoxSizer()
        self.SetSizer(sizer)

        self.panel_one = panels.panelMain(self)
        self.panel_two = panels.panelAcct(self)
        self.panel_three = panels.panelBal(self)
        self.panel_four = panels.panelDep(self)
        self.panel_five = panels.panelWdr(self)
        self.panel_six = panels.panelTfr(self)

        sizer.Add(self.panel_one, 1, wx.EXPAND)

        self.panel_one.btnAcct.Bind(wx.EVT_BUTTON, self.show_panel_two)
        sizer.Add(self.panel_two, 1, wx.EXPAND)
        self.panel_two.btn.Bind(wx.EVT_BUTTON, self.show_panel_one)
        self.panel_two.Hide()

        self.panel_one.btnBal.Bind(wx.EVT_BUTTON, self.show_panel_three)
        sizer.Add(self.panel_three, 1, wx.EXPAND)
        self.panel_three.btn.Bind(wx.EVT_BUTTON, self.show_panel_one)
        self.panel_three.Hide()

        self.panel_one.btnDep.Bind(wx.EVT_BUTTON, self.show_panel_four)
        sizer.Add(self.panel_four, 1, wx.EXPAND)
        self.panel_four.btn.Bind(wx.EVT_BUTTON, self.show_panel_one)
        self.panel_four.Hide()

        self.panel_one.btnWdr.Bind(wx.EVT_BUTTON, self.show_panel_five)
        sizer.Add(self.panel_five, 1, wx.EXPAND)
        self.panel_five.btn.Bind(wx.EVT_BUTTON, self.show_panel_one)
        self.panel_five.Hide()

        self.panel_one.btnTfr.Bind(wx.EVT_BUTTON, self.show_panel_six)
        sizer.Add(self.panel_six, 1, wx.EXPAND)
        self.panel_six.btn.Bind(wx.EVT_BUTTON, self.show_panel_one)
        self.panel_six.Hide()

        self.SetSize((700, 325))
        self.Centre()

    def show_panel_one(self, event):
        self.panel_one.Show()
        self.panel_two.Hide()
        self.panel_three.Hide()
        self.panel_four.Hide()
        self.panel_five.Hide()
        self.panel_six.Hide()
        self.Layout()

    def show_panel_two(self, event):
        self.panel_two.Show()
        emptyArray = [self.panel_two.txtName, self.panel_two.txtOpenBal]
        methods.toggleElements(emptyArray, 2)
        self.panel_one.Hide()
        self.Layout()

    def show_panel_three(self, event):
        self.panel_three.Show()
        emptyArray = [self.panel_three.txtAcctNo]
        hideArray = [self.panel_three.balDisplay]
        methods.toggleElements(emptyArray, 2)
        methods.toggleElements(hideArray, 0)
        self.panel_one.Hide()
        self.Layout()

    def show_panel_four(self, event):
        self.panel_four.Show()
        emptyArray = [self.panel_four.acctNo, self.panel_four.dptAmt]
        hideArray = [self.panel_four.actDtls, self.panel_four.dptAmt, self.panel_four.btnMkDpt, self.panel_four.depAmt]
        methods.toggleElements(emptyArray, 2)
        methods.toggleElements(hideArray, 0)
        self.panel_one.Hide()
        self.Layout()

    def show_panel_five(self, event):
        self.panel_five.Show()
        emptyArray = [self.panel_five.acctNo, self.panel_five.amtWdr]
        hideArray = [self.panel_five.actDtls, self.panel_five.amtWdr, self.panel_five.btnMkWdr, self.panel_five.wdrAmt]
        methods.toggleElements(emptyArray, 2)
        methods.toggleElements(hideArray, 0)
        self.panel_one.Hide()
        self.Layout()

    def show_panel_six(self, event):
        emptyArray = [self.panel_six.srcAcctNo, self.panel_six.tgtAcctNo, self.panel_six.amtTfr]
        hideArray = [self.panel_six.srcActDtls, self.panel_six.tgtActDtls, self.panel_six.amtTfr, self.panel_six.tfrAmt, self.panel_six.btnTfr]
        methods.toggleElements(emptyArray, 2)
        methods.toggleElements(hideArray, 0)
        self.panel_six.Show()
        self.panel_one.Hide()
        self.Layout()
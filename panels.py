import wx, mysql.connector, time
from datetime import datetime

createdb_query = "CREATE DATABASE IF NOT EXISTS mysql_python_banking;"
table_query = """
    CREATE TABLE mysql_python_banking.account (
        account_no int(11) NOT NULL AUTO_INCREMENT,
        name_on_account varchar(100) NOT NULL,
        balance float NOT NULL DEFAULT '0',
        account_open_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (account_no)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;"""

try:
    cnx = mysql.connector.connect(user='root', password='', host='localhost', database='mysql_python_banking')
    cursor = cnx.cursor()

except:
    cnx = mysql.connector.connect(user='root', password='', host='localhost')
    cursor = cnx.cursor()
    cursor.execute(createdb_query)
    cursor.execute(table_query)
    cnx.commit()

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def stringTheDeets(row):
    lblTxt = str(row[0]) + ", " + row[1] + ", $" + str(row[2]) + ", " + str(row[3])
    return lblTxt


def toggleElements(array, tog):
    if tog == 0: # hide static elements
        for element in array:
            element.Hide()
    elif tog == 1: # show static elements
        for element in array:
            element.Show()
    elif tog == 2: # empty textctrl elements
        for element in array:
            element.SetValue("")


def makeDeposit(curBal, dptAmt, acctNo, actDtlsTxt, tfr):
    dptAmt = float(dptAmt.GetValue())
    newBal = curBal + dptAmt
    updateQuery = "UPDATE mysql_python_banking.account SET balance = " + str(newBal) + " WHERE account_no = " + acctNo.GetValue()
    cursor.execute(updateQuery)
    rowLockQuery = "SELECT * FROM mysql_python_banking.account WHERE account_no = " + acctNo.GetValue()
    cursor.execute(rowLockQuery)
    row = cursor.fetchone()
    if row is not None:
            lblTxt = stringTheDeets(row)
            if tfr == 1:
                actDtlsTxt.SetLabelText("Source: "+lblTxt)
            else: actDtlsTxt.SetLabelText(lblTxt)
    else:
        actDtlsTxt.SetLabelText("Invalid query result.")


def makeWithdrawal(curBal, wdrAmt, acctNo, actDtlsTxt, tfr):
    wdrAmt = float(wdrAmt.GetValue())
    if (wdrAmt <= curBal):
        newBal = curBal - wdrAmt
        updateQuery = "UPDATE mysql_python_banking.account SET balance = " + str(newBal) + " WHERE account_no = " + acctNo.GetValue()
        cursor.execute(updateQuery)
        rowLockQuery = "SELECT * FROM mysql_python_banking.account WHERE account_no = " + acctNo.GetValue()
        cursor.execute(rowLockQuery)
        row = cursor.fetchone()
        if row is not None:
            lblTxt = stringTheDeets(row)
            if tfr == 1:
                actDtlsTxt.SetLabelText("Source: "+lblTxt)
            else: actDtlsTxt.SetLabelText(lblTxt)
        else:
            actDtlsTxt.SetLabelText("Invalid query result.")
            return -1
    else:
        actDtlsTxt.SetLabelText("Balance is insufficient for withdrawal in account.")
        return -1


class panelMain(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        title = 'mysql_python_banking'
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        wx.StaticText(self, -1, title, (225, 15)).SetFont(font)

        self.btnAcct = wx.Button(self, -1, "Create Account", (300, 50))
        self.btnBal = wx.Button(self, -1, "Check Balance", (300, 75))
        self.btnDep = wx.Button(self, -1, "Deposit", (300, 100))
        self.btnWdr = wx.Button(self, -1, "Withdraw", (300, 125))
        self.btnTfr = wx.Button(self, -1, "Transfer", (300, 150))


class panelAcct(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        title = 'Create Account'
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        wx.StaticText(self, -1, title, (280, 20)).SetFont(font)

        lblName = 'Name on Account:'
        lblOpenBal = 'Opening Balance:'
        wx.StaticText(self, -1, lblName, (100, 60)).SetFont(font)
        self.txtName = wx.TextCtrl(self, pos=(325, 60), size=(250,24))

        wx.StaticText(self, -1, lblOpenBal, (100, 100)).SetFont(font)
        self.txtOpenBal = wx.TextCtrl(self, pos=(325, 100), size=(250,24))

        btnCreateAcct = wx.Button(self, -1, "Create Account", (225, 150))
        btnCreateAcct.Bind(wx.EVT_BUTTON, self.onCreateAcctPress)

        self.btn = wx.Button(self, -1, "Back to Main Menu", (350, 150))
        self.errMsg = wx.StaticText(self, -1, 'Please enter correct values.', (275, 130))
        self.errMsg.Hide()

    def onCreateAcctPress(self, event):
        if self.txtName.GetValue() != '' and self.txtOpenBal.GetValue() != '' and isfloat(self.txtOpenBal.GetValue()):
            self.errMsg.Hide()
            now = datetime.now()
            strdate = now.strftime("%Y-%m-%d %H:%M:%S")
            addAcctQuery = "INSERT INTO mysql_python_banking.account (name_on_account, balance, account_open_date) VALUES (%s, %s, %s)"
            values = (self.txtName.GetValue(), self.txtOpenBal.GetValue(), strdate)
            cursor.execute(addAcctQuery, values)
            cnx.commit()
        else:
            self.errMsg.Show()

class panelBal(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        title = 'Check Balance'
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        wx.StaticText(self, -1, title, (280, 20)).SetFont(font)

        lblName = 'Account Number:'
        wx.StaticText(self, -1, lblName, (100, 60)).SetFont(font)
        self.txtAcctNo = wx.TextCtrl(self, pos=(325, 60), size=(250, 24))

        btnCheckBal = wx.Button(self, -1, "Check Balance", (225, 150))
        btnCheckBal.Bind(wx.EVT_BUTTON, self.onCheckBalPress)

        self.btn = wx.Button(self, -1, "Back to Main Menu", (350, 150))

        self.balDisplay = wx.StaticText(self, -1, '', (100, 100))
        self.balDisplay.SetFont(font)

    def onCheckBalPress(self, event):
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        checkBalQuery = "SELECT * FROM mysql_python_banking.account WHERE account_no = " + self.txtAcctNo.GetValue()
        cursor.execute(checkBalQuery)
        row = cursor.fetchone()
        if row is not None:
            lblTxt = stringTheDeets(row)
            self.balDisplay.SetLabelText(lblTxt)
            self.balDisplay.Show()
        else:
            self.balDisplay.SetLabelText("Please enter a valid account number.")
            self.balDisplay.Show()


class panelDep(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        title='Deposit'
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        wx.StaticText(self, -1, title, (315, 20)).SetFont(font)

        wx.StaticText(self, -1, 'Account Number:', (100, 50)).SetFont(font)
        self.acctNo = wx.TextCtrl(self, pos=(315, 50), size=(250, 24))
        self.btnShowDetails = wx.Button(self, -1, "Show Account Details", (100, 85))
        self.btnShowDetails.Bind(wx.EVT_BUTTON, self.onShowDetailsPress)

        self.actDtls = wx.StaticText(self, -1, '', (265, 87))
        self.actDtls.Hide()

        self.depAmt = wx.StaticText(self, -1, 'Enter Amount to Deposit:', (100, 115))
        self.depAmt.SetFont(font)
        self.depAmt.Hide()

        self.btnMkDpt = wx.Button(self, -1, "Make Deposit", (100, 150))
        self.btnMkDpt.Bind(wx.EVT_BUTTON, self.onMkDptPress)
        self.btnMkDpt.Hide()

        self.dptAmt = wx.TextCtrl(self, pos=(400, 115), size=(180, 24))
        self.dptAmt.Hide()

        self.btn = wx.Button(self, -1, "Back to Main Menu", (385, 150))
        self.curBal = 0

    def onShowDetailsPress(self, event):
        errmsg = "Please enter a valid account number."
        if self.acctNo.GetValue().isnumeric():
            cursor.execute("START TRANSACTION")
            rowLockQuery = "SELECT * FROM mysql_python_banking.account WHERE account_no = " + self.acctNo.GetValue() + " FOR UPDATE"
            cursor.execute(rowLockQuery)
            row = cursor.fetchone()
            if row is not None:
                lblTxt = stringTheDeets(row)
                self.actDtls.SetLabelText(lblTxt)
                self.curBal = row[2]
                showArray = [self.actDtls, self.depAmt, self.btnMkDpt, self.dptAmt]
                toggleElements(showArray, 1)
            else:
                self.actDtls.SetLabelText(errmsg)
                self.actDtls.Show()
        else:
            self.actDtls.SetLabelText(errmsg)
            self.actDtls.Show()

    def onMkDptPress(self, event):
        makeDeposit(self.curBal, self.dptAmt, self.acctNo, self.actDtls, 0)
        cnx.commit()


class panelWdr(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        title='Withdraw'
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        wx.StaticText(self, -1, title, (310, 20)).SetFont(font)

        wx.StaticText(self, -1, 'Account Number:', (100, 50)).SetFont(font)
        self.acctNo = wx.TextCtrl(self, pos=(315, 50), size=(250, 24))
        self.btnShowDetails = wx.Button(self, -1, "Show Account Details", (100, 85))
        self.btnShowDetails.Bind(wx.EVT_BUTTON, self.onShowDetailsPress)

        self.actDtls = wx.StaticText(self, -1, '', (265, 87))
        self.actDtls.Hide()

        self.wdrAmt = wx.StaticText(self, -1, 'Enter Amount to Withdraw:', (100, 115))
        self.wdrAmt.SetFont(font)
        self.wdrAmt.Hide()

        self.btnMkWdr = wx.Button(self, -1, "Make Withdrawal", (100, 150))
        self.btnMkWdr.Bind(wx.EVT_BUTTON, self.onMkWdrPress)
        self.btnMkWdr.Hide()

        self.amtWdr = wx.TextCtrl(self, pos=(400, 115), size=(170, 24))
        self.amtWdr.Hide()

        self.btn = wx.Button(self, -1, "Back to Main Menu", (385, 150))
        self.curBal = 0

    def onShowDetailsPress(self, event):
        errmsg = "Please enter a valid account number."
        if self.acctNo.GetValue().isnumeric():
            cursor.execute("START TRANSACTION")
            rowLockQuery = "SELECT * FROM mysql_python_banking.account WHERE account_no = " + self.acctNo.GetValue() + " FOR UPDATE"
            cursor.execute(rowLockQuery)
            row = cursor.fetchone()
            if row is not None:
                lblTxt = stringTheDeets(row)
                self.actDtls.SetLabelText(lblTxt)
                self.curBal = row[2]
                showArray = [self.actDtls, self.wdrAmt, self.btnMkWdr, self.amtWdr]
                toggleElements(showArray, 1)
            else:
                self.actDtls.SetLabelText(errmsg)
                self.actDtls.Show()
        else:
            self.actDtls.SetLabelText(errmsg)
            self.actDtls.Show()


    def onMkWdrPress(self, event):
        makeWithdrawal(self.curBal, self.amtWdr, self.acctNo, self.actDtls, 0)
        cnx.commit()


class panelTfr(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        title='Transfer'
        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        wx.StaticText(self, -1, title, (315, 20)).SetFont(font)

        wx.StaticText(self, -1, 'Source Account Number:', (100, 50)).SetFont(font)
        self.srcAcctNo = wx.TextCtrl(self, pos=(400, 50), size=(250, 24))

        wx.StaticText(self, -1, 'Target Account Number:', (100, 85)).SetFont(font)
        self.tgtAcctNo = wx.TextCtrl(self, pos=(400, 85), size=(250, 24))

        self.btnShowDetails = wx.Button(self, -1, "Show Account Details", (100, 115))
        self.btnShowDetails.Bind(wx.EVT_BUTTON, self.onShowDetailsPress)

        self.srcActDtls = wx.StaticText(self, -1, 'test', (100, 145))
        self.tgtActDtls = wx.StaticText(self, -1, 'test', (100, 165))

        self.tfrAmt = wx.StaticText(self, -1, 'Enter Transfer Amount:', (100, 185))
        self.tfrAmt.SetFont(font)
        self.btnTfr = wx.Button(self, -1, "Transfer", (100, 220))
        self.btnTfr.Bind(wx.EVT_BUTTON, self.onTfrPress)
        self.amtTfr = wx.TextCtrl(self, pos=(390, 185), size=(250,24))

        self.btn = wx.Button(self, -1, "Back to Main Menu", (455, 220))
        self.srcCurBal = 0
        self.tgtCurBal = 0

    def onShowDetailsPress(self, event):
        if (self.srcAcctNo.GetValue() == '') or (self.tgtAcctNo.GetValue() == ''):
            self.srcActDtls.SetLabelText("Account numbers cannot be left empty.")
            self.srcActDtls.Show()
            hideArray = [self.tgtActDtls. self.tfrAmt. self.btnTfr, self.amtTfr]
            toggleElements(hideArray, 0)
        elif (self.srcAcctNo.GetValue() != self.tgtAcctNo.GetValue()):
            cursor.execute("START TRANSACTION")
            errmsg = "Please enter a valid account number."

            srcRowLockQuery = "SELECT * FROM mysql_python_banking.account WHERE account_no = " + self.srcAcctNo.GetValue() + " FOR UPDATE"
            cursor.execute(srcRowLockQuery)
            srcRow = cursor.fetchone()
            if srcRow is not None:
                lblTxt = stringTheDeets(srcRow)
                self.srcActDtls.SetLabelText("Source: "+lblTxt)
                self.srcCurBal = srcRow[2]
                self.srcActDtls.Show()
            else:
                self.srcActDtls.SetLabelText("Source: "+errmsg)
                self.srcActDtls.Show()
                self.tfrAmt.Hide()
                self.btnTfr.Hide()
                self.amtTfr.Hide()

            tgtRowLockQuery = "SELECT * FROM mysql_python_banking.account WHERE account_no = " + self.tgtAcctNo.GetValue() + " FOR UPDATE"
            cursor.execute(tgtRowLockQuery)
            tgtRow = cursor.fetchone()
            if tgtRow is not None:
                lblTxt = stringTheDeets(tgtRow)
                self.tgtActDtls.SetLabelText("Target: "+lblTxt)
                self.tgtCurBal = tgtRow[2]
                self.tgtActDtls.Show()
            else:
                self.tgtActDtls.SetLabelText("Target: "+errmsg)
                self.tgtActDtls.Show()
                self.tfrAmt.Hide()
                self.btnTfr.Hide()
                self.amtTfr.Hide()

            if (srcRow is not None) and (tgtRow is not None):
                self.tfrAmt.Show()
                self.btnTfr.Show()
                self.amtTfr.Show()
        else:
            self.srcActDtls.SetLabelText("Source and Target account cannot be the same.")
            self.srcActDtls.Show()
            self.tgtActDtls.Hide()
            self.tfrAmt.Hide()
            self.btnTfr.Hide()
            self.amtTfr.Hide()

    def onTfrPress(self, event):
        withdraw = makeWithdrawal(self.srcCurBal, self.amtTfr, self.srcAcctNo, self.srcActDtls, 1)
        if (withdraw != -1):
            time.sleep(10)
            makeDeposit(self.tgtCurBal, self.amtTfr, self.tgtAcctNo, self.tgtActDtls, 1)
            time.sleep(10)
            cnx.commit()
        else:
            print('error')


class Program(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'mysql_python_banking')

        sizer = wx.BoxSizer()
        self.SetSizer(sizer)

        self.panel_one = panelMain(self)
        self.panel_two = panelAcct(self)
        self.panel_three = panelBal(self)
        self.panel_four = panelDep(self)
        self.panel_five = panelWdr(self)
        self.panel_six = panelTfr(self)

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
        frame.SetTitle('mysql_python_banking')
        self.panel_one.Show()
        self.panel_two.Hide()
        self.panel_three.Hide()
        self.panel_four.Hide()
        self.panel_five.Hide()
        self.panel_six.Hide()
        self.Layout()

    def show_panel_two(self, event):
        frame.SetTitle('Create Account')
        self.panel_two.Show()
        emptyArray = [self.panel_two.txtName, self.panel_two.txtOpenBal]
        toggleElements(emptyArray, 2)
        self.panel_one.Hide()
        self.Layout()

    def show_panel_three(self, event):
        frame.SetTitle('Check Balance')
        self.panel_three.Show()
        emptyArray = [self.panel_three.txtAcctNo]
        hideArray = [self.panel_three.balDisplay]
        toggleElements(emptyArray, 2)
        toggleElements(hideArray, 0)
        self.panel_one.Hide()
        self.Layout()

    def show_panel_four(self, event):
        frame.SetTitle('Deposit')
        self.panel_four.Show()
        emptyArray = [self.panel_four.acctNo, self.panel_four.dptAmt]
        hideArray = [self.panel_four.actDtls, self.panel_four.dptAmt, self.panel_four.btnMkDpt, self.panel_four.depAmt]
        toggleElements(emptyArray, 2)
        toggleElements(hideArray, 0)
        self.panel_one.Hide()
        self.Layout()

    def show_panel_five(self, event):
        frame.SetTitle('Withdraw')
        self.panel_five.Show()
        emptyArray = [self.panel_five.acctNo, self.panel_five.amtWdr]
        hideArray = [self.panel_five.actDtls, self.panel_five.amtWdr, self.panel_five.btnMkWdr, self.panel_five.wdrAmt]
        toggleElements(emptyArray, 2)
        toggleElements(hideArray, 0)
        self.panel_one.Hide()
        self.Layout()

    def show_panel_six(self, event):
        frame.SetTitle('Transfer')
        emptyArray = [self.panel_six.srcAcctNo, self.panel_six.tgtAcctNo, self.panel_six.amtTfr]
        hideArray = [self.panel_six.srcActDtls, self.panel_six.tgtActDtls, self.panel_six.amtTfr, self.panel_six.tfrAmt, self.panel_six.btnTfr]
        toggleElements(emptyArray, 2)
        toggleElements(hideArray, 0)
        self.panel_six.Show()
        self.panel_one.Hide()
        self.Layout()

if __name__ == "__main__":
    app = wx.App()
    frame = Program()
    frame.Show()
    app.MainLoop()

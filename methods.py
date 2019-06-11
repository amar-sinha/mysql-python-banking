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


def makeDeposit(cursor, curBal, dptAmt, acctNo, actDtlsTxt, tfr):
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
                actDtlsTxt.SetLabelText("Target: "+lblTxt)
            else: actDtlsTxt.SetLabelText(lblTxt)
    else:
        actDtlsTxt.SetLabelText("Invalid query result.")


def makeWithdrawal(cursor, curBal, wdrAmt, acctNo, actDtlsTxt, tfr):
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
    else:
        actDtlsTxt.SetLabelText("Balance is insufficient for withdrawal in account.")
        return -1
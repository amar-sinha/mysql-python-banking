# Bank Accounts and Transaction Processing
## A MySQL-Python Integrated Implementation

<i><h4>An improved implementation of a project assignment in "CSE 4701: Principles of Databases" offered at the University of Connecticut.</h4></i>

### <u>Goal</u>
Create a simplified banking software to practice concepts of embedded SQL and database transactions. Information on bank accounts will be persistently stored in a MySQL database on a local computer. The bank account database will have only one table named account with the following details.

### <u>Implementation</u>
The banking software is implemented with a Python program and MySQL databse integration, utilizing the mysql-connector Python package, which provides the communication between Python and MySQL. The Python program provides a graphical user-interface (GUI) implemented using the wxpython GUI toolkit package. Instructions to install the packages on a Windows and macOS machine are provided below.


### <u>Package Installation</u>
Install mysql-connector

    $ pip install mysql-connector-python

Install wxpython

    $ pip install wxPython

### <u>MySQL User Specifications</u>
To ensure the program executes with no errors, make sure that the MySQL user specifications (user name, password, host, database name) in the Python program are correct. These specifications can be found at the top of the program, and look as such:

    cnx = mysql.connector.connect(user='root', password='pwd', host='localhost', database='db_name')
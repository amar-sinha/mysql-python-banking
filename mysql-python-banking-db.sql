--
-- Database: mysql_python_banking
--
CREATE DATABASE IF NOT EXISTS mysql_python_banking;
USE mysql_python_banking;

-- --------------------------------------------------------

--
-- Table structure for table account
--

CREATE TABLE account (
  account_no int(11) NOT NULL AUTO_INCREMENT,
  name_on_account varchar(100) NOT NULL,
  balance float NOT NULL DEFAULT '0',
  account_open_date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (account_no)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
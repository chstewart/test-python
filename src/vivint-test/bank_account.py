import re
import sys
from decimal import Decimal, InvalidOperation


class BankAccount:
  """
  A class to represent a mock Bank Account.

  This class provides methods to deposit, withdraw, and check the balance
  of the account.
  """

  def __init__(self, initial_balance: Decimal = Decimal(0.00), max_overdraft: Decimal = Decimal(-500)):
    """Initialize a new BankAccount with default amounts if not supplied."""
    self.__total_balance: Decimal = Decimal(initial_balance)
    self.__max_overdraft: Decimal = Decimal(max_overdraft)

  def __get_amount_from_console(self, action_type: str) -> Decimal:
    """Get a valid user amount from the console."""
    # I really wanted to move the validations out to its own method
    # But trying to stay with the requirements of having 4 methods I left it all in at the user input level
    # The example shows very basic ints going in but then also says invalid inputs will be tried
    # Seeing as I don't know what constitutes a valid input outside of an int
    # I took some liberty here of what comes to mind when I think of a bank account and currency
    # I essentially sanitize the input if I can safely do so otherwise I have the user retry to enter valid input
    max_attempts: int = 3
    attempts: int = 0
    while attempts < max_attempts:
      try:
        input_amount: str = input(f"Please enter a {action_type} amount: ")
        if "," in input_amount and not len(re.findall(r",\d{3}(?!\d)", input_amount)) == input_amount.count(","):
          print(f"Input Error: {action_type} amount must contain 3 digits after commas when provided.")
          attempts += 1
        else:
          input_amount = input_amount.replace("$", "").replace(",", "")

        decimal_amount: Decimal = Decimal(input_amount)
        decimal_result: int = decimal_amount.as_tuple().exponent.__abs__()
        if "." in input_amount and decimal_result != 2:
          print(f"Input Error: {action_type} amount must contain 2 decimal places when provided.")
          attempts += 1
        elif decimal_amount <= 0:
          print(f"Input Error: {action_type} amount must be greater than 0.")
          attempts += 1
        else:
          break
      except ValueError:
        print(f"Input Error: {type(input_amount)} is not valid. Please enter a valid amount.")
        attempts += 1
      except InvalidOperation:
        print(f"Input Error: {type(input_amount)} is not valid. Please enter a valid amount.")
        attempts += 1
      if attempts == max_attempts:
        print(f"Input Error: Maximum attempts of {max_attempts} reached for a valid {action_type} amount. Exiting....")
        sys.exit()
    return decimal_amount

  def deposit(self):
    """Deposit an amount into the bank account."""
    amount: Decimal = self.__get_amount_from_console("deposit")
    self.__total_balance += amount
    self.balance()
    # print(f"Depositing {amount} into the account.")

  def withdraw(self):
    """Withdraw an amount from the bank account."""
    amount: Decimal = self.__get_amount_from_console("withdraw")
    if self.__total_balance - amount >= self.__max_overdraft:
      self.__total_balance -= amount
    else:
      print(f"Withdrawal denied. Max Overdraft limit is ${self.__max_overdraft:,.2f}.")
    self.balance()
    # print(f"Withdrawing {amount} from the account.")

  def balance(self):
    """Get the current balance of the bank account."""
    print(f"Current Balance: ${self.__total_balance:,.2f}")


# bank_account = BankAccount(initial_balance=600, max_overdraft=-600)
bank_account = BankAccount()
# Verifying unable to modify the total_balance directly
bank_account.__total_balance = 500
bank_account.__total_balance = 500
bank_account.deposit()
bank_account.deposit()
bank_account.withdraw()
bank_account.withdraw()
bank_account.withdraw()

import random

from block import Block
from user import User
from merkle import Merkle
from input import Input
from output import Output

def main():
  random.seed()

  difficulty = 250

  users = [ User() for x in range(3) ]

  blockChain = []
  confirmedTransactions = []
  unconfirmedTransactions = []
  transactionsInOrder = []
  # User 0. mines 50$
  users[0].mine(blockChain, users, confirmedTransactions, unconfirmedTransactions, transactionsInOrder, difficulty)
  # User 0. sends 25$ to himself generating an output of 25$ and a change 25$
  users[0].send(blockChain, users, confirmedTransactions, unconfirmedTransactions, transactionsInOrder, users[0], 2500000000)
  # User 0. mines 50$, confirms the change and the new output
  users[0].mine(blockChain, users, confirmedTransactions, unconfirmedTransactions, transactionsInOrder, difficulty)
  # User 0. sends 12.5$ to himself generating an output of 12.5$ and a change 12.5$
  users[0].send(blockChain, users, confirmedTransactions, unconfirmedTransactions, transactionsInOrder, users[0], 1250000000)
  # User 0. mines 50$, confirms the change and the new output
  users[0].mine(blockChain, users, confirmedTransactions, unconfirmedTransactions, transactionsInOrder, difficulty)
  # User 0. sends 6.25$ to himself generating an output of 6.25$ and a change 12.5$
  users[0].send(blockChain, users, confirmedTransactions, unconfirmedTransactions, transactionsInOrder, users[0], 625000000)
  # User 0. mines 50$, confirms the change and the new output
  users[0].mine(blockChain, users, confirmedTransactions, unconfirmedTransactions, transactionsInOrder, difficulty)
  # User 1. mines 50$
  users[1].mine(blockChain, users, confirmedTransactions, unconfirmedTransactions, transactionsInOrder, difficulty)
  # User 2. mines 50$
  users[2].mine(blockChain, users, confirmedTransactions, unconfirmedTransactions, transactionsInOrder, difficulty)
  # User 1. mines 50$
  users[1].mine(blockChain, users, confirmedTransactions, unconfirmedTransactions, transactionsInOrder, difficulty)
  # User 1. mines 50$
  users[1].mine(blockChain, users, confirmedTransactions, unconfirmedTransactions, transactionsInOrder, difficulty)
  # User 2. mines 50$
  users[2].mine(blockChain, users, confirmedTransactions, unconfirmedTransactions, transactionsInOrder, difficulty)
  # User 2. mines 50$
  users[2].mine(blockChain, users, confirmedTransactions, unconfirmedTransactions, transactionsInOrder, difficulty)
  # User 0. mines 50$
  users[0].mine(blockChain, users, confirmedTransactions, unconfirmedTransactions, transactionsInOrder, difficulty)
  for i in range(8):
    # User 0. rapidly sends 1$ to user 1. generating changes and output for user 1. with 1$
    users[0].send(blockChain, users, confirmedTransactions, unconfirmedTransactions, transactionsInOrder, users[1], 100000000)
  # User 2. mines 50$ here he confirms the 16 transactions (changes and outputs of 1$)
  users[2].mine(blockChain, users, confirmedTransactions, unconfirmedTransactions, transactionsInOrder, difficulty)

  print()

  for x in blockChain:
    print(x)
    print()

  print()
  print("Confirmed transactions: ")

  for x in confirmedTransactions:
    print(x)
    print("".join([ '-' for i in range(50) ]))
  if len(confirmedTransactions) == 0:
    print("Currently none")

  print()
  print("Unconfirmed transactions: ")

  for x in unconfirmedTransactions:
    print(x)
    print("".join([ '-' for i in range(50) ]))
  if len(unconfirmedTransactions) == 0:
    print("Currently none")

  print()

  for i in range(len(users)):
    print(f"Money of {i}. user: {users[i].get_money(confirmedTransactions, unconfirmedTransactions)}$")

  print()

  print(f"Transaction 0. is valid: {confirmedTransactions[0].verify(users)}")
  print(f"Last block's transactions are in order and valid: {blockChain[-1].validate(confirmedTransactions, [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33])}")

  print()

  for i in range(len(users)):
    print(f"Current UTXO's of user {i}.: {users[i].get_owned_utxo(confirmedTransactions, unconfirmedTransactions)}")

if __name__ == "__main__":
  main()
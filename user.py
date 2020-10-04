import ecdsa
import hashlib
import random

from block import Block
from transaction import Transaction
from input import Input
from output import Output
from merkle import Merkle

class User:
  def __init__(self):
    self.signingKey = ecdsa.SigningKey.generate(curve=ecdsa.curves.SECP256k1)
    self.verifyingKey = self.signingKey.get_verifying_key()
  
  def mine(self, blockChain, users, confirmedTransactions, unconfirmedTransactions, transactionsInOrder, difficulty):
    nonce = 0
    if len(blockChain) > 0:
      last = blockChain[-1]
      lastHash = last.get_hash()
    else:
      lastHash = "".join([ "0" for x in range(64) ])

    while True:
      while True:
        hasher = hashlib.sha256();
        base = f"{lastHash}{nonce}"
        hasher.update(base.encode('utf-8'))
        if int(hasher.hexdigest(), 16) < 2 ** difficulty:
          break
        nonce += 1
      if sum([ 1 if x.get_hash() == hasher.hexdigest() else 0 for x in blockChain ]) == 0:
        break
      nonce += 1
    for transaction in confirmedTransactions:
      if not transaction.verify(users):
        raise Exception("Fatal error transaction is invalid/modified.")
    print("Transactions are verified for block{len(blockChain) + 1} transaction.")
    for i in range(len(blockChain)):
      if not blockChain[i].validate(confirmedTransactions, transactionsInOrder[i]):
        raise Exception("Fatal error blockchain is in invalid state.")
    print(f"BlockChain validation successful for block {len(blockChain) + 1}.")
    unconfirmedTransactions.append(
      Transaction(
        inputs=[
          Input(
            coinbase=base,
            signature=self.sign("".join([ '0' for i in range(64) ]).encode('utf8')).hex(),
            publicKey=self.verifyingKey.to_string().hex()
          )
        ],
        outputs=[
          Output(
            amount=5000000000
          )
        ]
      )
    )
    blockChain.append(Block(lastHash, hasher.hexdigest(), nonce, unconfirmedTransactions))
    transactionsInOrder.append([ len(confirmedTransactions) + i for i in range(len(unconfirmedTransactions)) ])
    confirmedTransactions += list(unconfirmedTransactions)
    unconfirmedTransactions.clear()

  def sign(self, to_sign):
    return self.signingKey.sign(to_sign)

  def get_money(self, confirmedTransactions, unconfirmedTransactions):
    money = 0
    utxo = self.get_owned_utxo(confirmedTransactions, unconfirmedTransactions)
    for i in range(len(confirmedTransactions)):
      if confirmedTransactions[i].is_owned_by_user(self.verifyingKey.to_string().hex()) and i in utxo:
        for output in confirmedTransactions[i].outputs:
          money += output.values.get('amount', None)
    return money / 100000000

  def get_owned_utxo(self, confirmedTransactions, unconfirmedTransactions):
    ownedTransactions = []
    for i in range(len(confirmedTransactions)):
      if confirmedTransactions[i].is_owned_by_user(self.verifyingKey.to_string().hex()):
        ownedTransactions.append(i)
    allTransactions = confirmedTransactions + unconfirmedTransactions
    ret = []
    for x in ownedTransactions:
      try:
        for i in range(len(allTransactions)):
          if i != x:
            for input in allTransactions[i].inputs:
              prevTx = input.values.get('prevTx', None)
              if prevTx == None:
                continue
              if confirmedTransactions[x].get_txid().hex() == prevTx:
                raise ValueError()
        ret.append(x)
      except:
        pass
    return ret

  def send(self, blockChain, users, confirmedTransactions, unconfirmedTransactions, transactionsInOrder, to_user, amount):
    utxo = self.get_owned_utxo(confirmedTransactions, unconfirmedTransactions)
    index = -1
    while True:
      outputForInput = utxo[random.randint(0, len(utxo) - 1)]
      for i in range(len(confirmedTransactions[outputForInput].outputs)):
        if confirmedTransactions[outputForInput].outputs[i].values['amount'] > amount:
          index = i
          break
      if index != -1:
        break
    for transaction in confirmedTransactions:
      if not transaction.verify(users):
        raise Exception("Fatal error transaction is invalid/modified.")
    print("Transactions are verified for 'send' transaction.")
    for i in range(len(blockChain)):
      if not blockChain[i].validate(confirmedTransactions, transactionsInOrder[i]):
        raise Exception("Fatal error blockchain is in invalid state.")
    print("BlockChain validation successful for 'send' transaction.")
    unconfirmedTransactions.append(
      Transaction(
        inputs=[
          Input(
            prevTx=confirmedTransactions[outputForInput].get_txid().hex(),
            signature=to_user.sign(confirmedTransactions[outputForInput].get_txid()).hex(),
            index=index,
            publicKey=to_user.verifyingKey.to_string().hex()
          )
        ],
        outputs=[
          Output(
            amount=amount
          )
        ]
      )
    )
    if amount != confirmedTransactions[outputForInput].outputs[index].values['amount']:
      unconfirmedTransactions.append(
        Transaction(
          inputs=[
            Input(
              prevTx=confirmedTransactions[outputForInput].get_txid().hex(),
              signature=self.sign(confirmedTransactions[outputForInput].get_txid()).hex(),
              index=index,
              publicKey=self.verifyingKey.to_string().hex()
            )
          ],
          outputs=[
            Output(
              amount=confirmedTransactions[outputForInput].outputs[index].values['amount'] - amount
            )
          ]
        )
      )

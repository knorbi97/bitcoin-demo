from datetime import datetime

from merkle import Merkle

class Block:
  def __init__(self, prevHash, proofOfWork, nonce, unconfirmedTransactions):
    self.prevHash = prevHash
    self.merkle = Merkle()
    self.merkleRoot = self.merkle.get_root(self.merkle.get_txids([ str(transaction) for transaction in unconfirmedTransactions ]))
    self.timestamp = int(datetime.timestamp(datetime.now()))
    self.nonce = nonce
    self.proofOfWork = proofOfWork

  def __str__(self):
    ret = []
    ret.append(f"Previous hash: 0x{self.prevHash}")
    ret.append(f"Merkle root: 0x{self.merkleRoot}")
    ret.append(f"Timestamp: {self.timestamp}")
    ret.append(f"Proof of Work: 0x{self.get_hash()}")
    ret.append(f"Nonce: {self.nonce}")
    return "\n".join(ret)

  def validate(self, transactions, usedTransactions):
    validatingRoot = self.merkle.get_root(self.merkle.get_txids([ str(transactions[x]) for x in usedTransactions ]))
    return self.merkleRoot == validatingRoot

  def get_hash(self):
    return self.proofOfWork

  def get_creation_time(self):
    return datetime.fromtimestamp(self.timestamp)
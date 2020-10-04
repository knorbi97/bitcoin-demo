import hashlib

class Merkle:
  def transaction_to_utf8_encoded(self, transactions):
    ret = []
    for x in transactions:
      ret.append(x.encode('utf8'))
    return ret    

  def append_pairs(self, hashes):
    ret = []
    for i in range(0, len(hashes), 2):
      ret.append(hashes[i] + hashes[i + 1])
    return ret

  def create_hash(self, to_hash):
    ret = []
    for x in to_hash:
      hasher1 = hashlib.sha256()
      hasher2 = hashlib.sha256()
      hasher1.update(x)
      hasher2.update(hasher1.digest())
      ret.append(hasher2.digest())
    return ret

  def get_txids(self, transactions):
    return self.create_hash(self.transaction_to_utf8_encoded(transactions))

  def get_root(self, txids):
    hashes = txids
    while len(hashes) != 1:
      if len(hashes) % 2 != 0:
        hashes.append(hashes[-1])
      hashes = self.create_hash(self.append_pairs(hashes))
    return hashes[0].hex()

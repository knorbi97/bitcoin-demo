import ecdsa

from merkle import Merkle
from input import Input
from output import Output

class Transaction:
  def __init__(self, *args, **kwargs):
    self.inputs = kwargs.get('inputs', None)
    self.outputs = kwargs.get('outputs', None)
    merkle = Merkle()
    self.txid = merkle.get_txids([ str(self) ])[0]

  def get_txid(self):
    return self.txid

  def is_owned_by_user(self, publicKey):
    for x in self.inputs:
      if x.values.get('publicKey', None) == publicKey:
        return True
    return False

  def verify(self, users):
    vk = self.inputs[0].values.get('publicKey', None)
    validUser = None
    for user in users:
      if user.verifyingKey.to_string().hex() == vk:
        validUser = user
        break
    if validUser == None:
      return False
    try:
      for input in self.inputs:
        if input.values.get('coinbase', None) == None:
          validUser.verifyingKey.verify(bytes.fromhex(input.values.get('signature', None)), bytes.fromhex(input.values['prevTx']))
        else:
          validUser.verifyingKey.verify(bytes.fromhex(input.values.get('signature', None)), "".join([ '0' for i in range(64) ]).encode('utf8'))
    except ecdsa.keys.BadSignatureError:
      return False
    return True

  def __str__(self):
    ret = []
    ret.append("Input: ")
    for input in self.inputs:
      ret.append(str(input))
    ret.append("")
    ret.append("Output: ")
    for output in self.outputs:
      ret.append(str(output))
    return "\n".join(ret)
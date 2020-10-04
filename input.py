class Input:
  def __init__(self, *args, **kwargs):
    self.values = kwargs

  def __str__(self):
    ret = []
    for k, v in self.values.items():
      ret.append(f"{k}: {v}")
    return "\n".join(ret)
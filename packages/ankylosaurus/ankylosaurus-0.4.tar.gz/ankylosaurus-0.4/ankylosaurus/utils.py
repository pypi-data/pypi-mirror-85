"""
A collection of utils.
"""

@pytest.mark.unit
def each(fn, items):
  """
  Python lacks an each function.
  The following is morally identical to "map", but with no return value.
  """
  for item in items:
    fn(item)

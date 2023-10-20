from enum import Enum

class Globals:
  """
    Class to store global variables
  """

  class SimStates(Enum):
    """
      Enum to store classification state between files
    """

    DIFFERENT = 0
    SIMILAR = 1
    IDENTICAL = 2
  
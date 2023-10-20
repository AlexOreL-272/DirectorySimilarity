import os
from globals import Globals


class DirectorySimilarity:
  """
    Class to perform classification between files in two directories
  """

  def __init__(self, first_directory_path, second_directory_path, sim_percentage):
    """
      Initializes classificator object.

      first_directory_path: path to first directory to process
      second_directory_path: path to second directory to process
      sim_percentage: minimal similarity percentage to treat files as similar
    """

    # path to first directory
    self.first_dir_path = first_directory_path
    # path to second directory
    self.second_dir_path = second_directory_path
    # minimal similarity percentage
    self.similarity_percentage = sim_percentage

  @staticmethod
  def __levenshtein_distance(lhs_string, rhs_string):
    """
      Calculates Levenshtein distance between two iterable objects.
      Returns amount of operations "insert", "delete", "change" to
      make one object from another.

      lhs_string: first iterable object
      rhs_string: first iterable object
    """

    # "dynamic programming" 2D array, where
    # matrix[row][column] is amount of operations "insert", "delete", "change"
    # to make rhs_string[0 : row + 1] from lhs_string[0 : column + 1] 
    matrix = []

    lhs_len = len(lhs_string)
    rhs_len = len(rhs_string)

    # initialize matrix
    for i in range(rhs_len):
      matrix.append([0] * lhs_len)

    # fill i'th element of first row of matrix with its index 
    for i in range(lhs_len):
      matrix[0][i] = i

    # fill i'th element of first column of matrix with its index 
    for i in range(rhs_len):
      matrix[i][0] = i

    # for every element in matrix calculate its levenshtein distance
    for row in range(1, rhs_len):
      for col in range(1, lhs_len):
        matrix[row][col] = min(
          matrix[row - 1][col] + 1, 
          matrix[row][col - 1] + 1, 
          matrix[row - 1][col - 1] + (lhs_string[col] != rhs_string[row])
        )

    # result lays in lower right element of matrix
    return matrix[-1][-1]

  def __check_sizes(self, lhs_file_path: str, rhs_file_path: str) -> bool:
    """
      Checks if ratio of file sizes is not less than given percentage.

      lhs_file_path: path to first file
      rhs_file_path: path to second file
    """

    # get file stats by calling stat() function
    lhs_stat = os.stat(lhs_file_path)
    rhs_stat = os.stat(rhs_file_path)

    min_size = min(lhs_stat.st_size, rhs_stat.st_size)
    max_size = max(lhs_stat.st_size, rhs_stat.st_size)

    return (min_size / max_size) * 100 >= self.similarity_percentage

  @staticmethod
  def __check_links(lhs_file_path: str, rhs_file_path: str) -> bool:
    """
      Checks if one or both files are hardlinks, so that they have identical file content.
      Returns whether files have identical content according to the possibility of being hardlinks.

      lhs_file_path: path to first file
      rhs_file_path: path to second file
    """

    # get file stats by calling stat() function
    stat_1 = os.stat(lhs_file_path)
    stat_2 = os.stat(rhs_file_path)

    # if file inodes and they are located on the same device, they are identical
    return stat_1.st_ino == stat_2.st_ino and stat_1.st_dev == stat_2.st_dev

  def __check_files(self, lhs_file_path: str, rhs_file_path: str) -> tuple:
    """
      Classifies two files whether they are identical, similar or different.
      Returns tuple (classification, similarity percentage).

      lhs_file_path: path to first file
      rhs_file_path: path to second file
    """

    # if ratio of file sizes is less than given minimal similarity percentage, 
    # then they cannot be similar
    if not self.__check_sizes(lhs_file_path, rhs_file_path):
      return (Globals.SimStates.DIFFERENT, 0)

    # if files are hardlinks or just identical files, they have identical content,
    # so we do not need further investigation
    if DirectorySimilarity.__check_links(lhs_file_path, rhs_file_path):
      return (Globals.SimStates.IDENTICAL, 100)

    # open the files to extract their content
    first_file = open(lhs_file_path, "r")
    second_file = open(rhs_file_path, "r")

    # get content of files
    content_of_first_file = first_file.read()
    content_of_second_file = second_file.read()

    # sizes of files
    first_file_size = len(content_of_first_file)
    second_file_size = len(content_of_second_file)

    max_len = max(first_file_size, second_file_size)

    # amount of identical characters in both files
    identical_chars_amt = max_len - DirectorySimilarity.__levenshtein_distance(
      content_of_first_file, 
      content_of_second_file
    )

    similarity_percentage = (identical_chars_amt / max_len) * 100
    
    # if file sizes are equal and all charachters are identical, then files are identical
    if identical_chars_amt == first_file_size and identical_chars_amt == second_file_size:
      return (Globals.SimStates.IDENTICAL, 100)
    # if similarity percentage is not less than given, then files are similar
    elif similarity_percentage >= self.similarity_percentage:
      return (Globals.SimStates.SIMILAR , similarity_percentage)
    
    # if similarity percentage is less than given, then files are treated as different
    return (Globals.SimStates.DIFFERENT, 0)

  def __print_identical_files(self, identical_files):
    """
      Prints identical files from both directories

      identical_files: dictionary with identical files
    """

    printed_files = []

    print("\n\n=====> Identical files <=====\n")

    for key, value in identical_files.items():
      for related_file in value:
        if (key, related_file) not in printed_files:
          print(f"{self.first_dir_path}/{key} and {self.second_dir_path}/{related_file} are 100% identical")
          printed_files.append((related_file, key))

  def __print_similar_files(self, similar_files):
    """
      Prints similar files from both directories

      similar_files: dictionary with similar files
    """

    print("\n\n=====> Similar files <=====\n")

    for key, value in similar_files.items():
      for related_file, similarity_coeff in value:
        print("{}/{} and {}/{} are {:.2f}% similar".format(
          self.first_dir_path, 
          key, 
          self.second_dir_path, 
          related_file, 
          similarity_coeff)
        )

  def __print_unique_files(
      self, different_files_in_first_dir: dict, 
      different_files_in_second_dir: dict, 
      files_amt_in_first_dir: int, 
      files_amt_in_second_dir: int
    ):
    """
      Prints unique files from both directories

      different_files_in_first_dir: dictionary with different files in first directory
      different_files_in_second_dir: dictionary with different files in second directory
      files_amt_in_first_dir: amount of files in first directory
      files_amt_in_second_dir: amount of files in second directory
    """

    print("\n\n=====> Unique files <=====\n")

    for key, value in different_files_in_first_dir.items():
      # if file from first directory is different from every other file in second directory
      if value == files_amt_in_first_dir:
          print(f"File {self.second_dir_path}/{key} is unique")

    for key, value in different_files_in_second_dir.items():
      # if file from first directory is different from every other file in second directory
      if value == files_amt_in_second_dir:
          print(f"File {self.first_dir_path}/{key} is unique")

  def check_dirs(self):
    """
      Performs file-by-file check between two directories
    """

    # get list of files from every directory
    files_in_first_dir = os.listdir(self.first_dir_path)
    files_in_second_dir = os.listdir(self.second_dir_path)

    # amount of files in each dir
    files_amt_in_first_dir = len(files_in_first_dir)
    files_amt_in_second_dir = len(files_in_second_dir)

    # dictionaries to store different files
    # key: file name
    # value: amount of files that are different with key
    different_files_in_first_dir = {}
    different_files_in_second_dir = {}

    # dictionary to store similar files
    # key: file name
    # value: array of pairs of file name and similarity percentage
    similar_files = {}

    # dictionary to store identical files
    # key: file name
    # value: array of file names
    identical_files = {}

    for first_dir_file in files_in_first_dir:
      for second_dir_file in files_in_second_dir:
        transitive_file_exists = False

        # if there exists file F such that
        # file_1 is identical to F and file_2 is identical to F
        # then file_1 and file_2 are identical
        if first_dir_file in identical_files:
          for probably_identical_file in identical_files[first_dir_file]:
            if second_dir_file in identical_files[probably_identical_file]:
              transitive_file_exists = True

              identical_files[first_dir_file].append(second_dir_file)
              identical_files[second_dir_file].append(first_dir_file)
              break

        if transitive_file_exists:
          continue

        # get correlation between files and their similarity percentage
        verdict, sim_coeff = self.__check_files(
          f"{self.first_dir_path}/{first_dir_file}", 
          f"{self.second_dir_path}/{second_dir_file}"
        )

        # files are different
        if verdict == Globals.SimStates.DIFFERENT:
          if first_dir_file not in different_files_in_second_dir:
            different_files_in_second_dir.setdefault(first_dir_file, 0)

          if second_dir_file not in different_files_in_first_dir:
            different_files_in_first_dir.setdefault(second_dir_file, 0)

          different_files_in_second_dir[first_dir_file] += 1
          different_files_in_first_dir[second_dir_file] += 1

        # files are similar
        elif verdict == Globals.SimStates.SIMILAR:
          if first_dir_file not in similar_files:
            similar_files.setdefault(first_dir_file, [])

          similar_files[first_dir_file].append((second_dir_file, sim_coeff))
        
        # then files are identical
        else:
          if first_dir_file not in identical_files:
            identical_files.setdefault(first_dir_file, [])

          if second_dir_file not in identical_files:
            identical_files.setdefault(second_dir_file, [])

          identical_files[first_dir_file].append(second_dir_file)
          identical_files[second_dir_file].append(first_dir_file)

    self.__print_identical_files(identical_files)
    self.__print_similar_files(similar_files)
    self.__print_unique_files(
      different_files_in_first_dir, 
      different_files_in_second_dir,
      files_amt_in_first_dir,
      files_amt_in_second_dir
    )

import os
from globals import Globals


class DirectorySimilarity:
  def __init__(self, dir_path_1, dir_path_2, sim_percentage):
    self.dir_path_1 = dir_path_1
    self.dir_path_2 = dir_path_2
    self.similarity_percentage = sim_percentage


  @staticmethod
  def __levenshtein_distance(lhs_string, rhs_string):
    matrix = []

    lhs_len = len(lhs_string)
    rhs_len = len(rhs_string)

    for i in range(rhs_len):
      matrix.append([0] * lhs_len)

    for i in range(lhs_len):
      matrix[0][i] = i

    for i in range(rhs_len):
      matrix[i][0] = i

    for row in range(1, rhs_len):
      for col in range(1, lhs_len):
        matrix[row][col] = min(
          matrix[row - 1][col] + 1, 
          matrix[row][col - 1] + 1, 
          matrix[row - 1][col - 1] + (lhs_string[col] != rhs_string[row])
        )

    return matrix[-1][-1]


  def __check_sizes(self, file_path_1, file_path_2):
    stat_1 = os.stat(file_path_1)
    stat_2 = os.stat(file_path_2)

    return (min(stat_1.st_size, stat_2.st_size) / max(stat_1.st_size, stat_2.st_size)) * 100 >= self.similarity_percentage


  @staticmethod
  def __check_links(file_path_1, file_path_2):
    stat_1 = os.stat(file_path_1)
    stat_2 = os.stat(file_path_2)

    return stat_1.st_ino == stat_2.st_ino and stat_1.st_dev == stat_2.st_dev

 
  def __check_files(self, file_path_1, file_path_2):
    if not self.__check_sizes(file_path_1, file_path_2):
      return (Globals.SimStates.DIFFERENT, 0)

    if DirectorySimilarity.__check_links(file_path_1, file_path_2):
      return (Globals.SimStates.IDENTICAL, 100)


    file_1 = open(file_path_1, "r")
    file_2 = open(file_path_2, "r")

    content_1 = file_1.read()
    content_2 = file_2.read()

    len_1 = len(content_1)
    len_2 = len(content_2)

    max_len = max(len_1, len_2)

    identical_chars_amt = max_len - DirectorySimilarity.__levenshtein_distance(content_1, content_2)

    similarity_percentage = (identical_chars_amt / max_len) * 100
    
    if identical_chars_amt == len_1 and identical_chars_amt == len_2:
      return (Globals.SimStates.IDENTICAL, 100)
    elif similarity_percentage >= self.similarity_percentage:
      return (Globals.SimStates.SIMILAR , similarity_percentage)
    
    return (Globals.SimStates.DIFFERENT, 0)

  
  def check_dirs(self):
    files_in_dir_1 = os.listdir(self.dir_path_1)
    files_in_dir_2 = os.listdir(self.dir_path_2)

    files_amt_in_dir_1 = len(files_in_dir_1)
    files_amt_in_dir_2 = len(files_in_dir_2)

    different_files = {}

    for file_1 in files_in_dir_1:
      for file_2 in files_in_dir_2:
        verdict, coeff = self.__check_files(f"{self.dir_path_1}/{file_1}", f"{self.dir_path_2}/{file_2}")

        if verdict == Globals.SimStates.DIFFERENT:
          if file_1 not in different_files:
            different_files.setdefault(file_1, [0, 0])

          if file_2 not in different_files:
            different_files.setdefault(file_2, [0, 1])

          different_files[file_1][0] += 1
          different_files[file_2][0] += 1

        elif verdict == Globals.SimStates.SIMILAR:
          print(f"{self.dir_path_1}/{file_1} and {self.dir_path_2}/{file_2} are {coeff}% similar")
        else:
          print(f"{self.dir_path_1}/{file_1} and {self.dir_path_2}/{file_2} are 100% identical")
          
    for key, val in different_files.items():
      if val[1] == 0:
        if val[0] == files_amt_in_dir_2:
          print(f"{self.dir_path_1}/{key} is unique")
      else:
        if val[0] == files_amt_in_dir_1:
          print(f"{self.dir_path_2}/{key} is unique")


if __name__ == "__main__":
  dir1 = input()
  dir2 = input()
  min_similarity_percentage = float(input())

  dir_checker = DirectorySimilarity(dir1, dir2, min_similarity_percentage)
  dir_checker.check_dirs()

# если Тони дал N% сходства, то (min_size / max_size) >= N, чтобы файлы были похожи
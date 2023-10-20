from directory_check import DirectorySimilarity


if __name__ == "__main__":
  # input both directories and delete leading and trailing spaces
  first_dir = input("Enter first directory name: ").strip()
  second_dir = input("Enter second directory name: ").strip()
  # input minimal similarity percentage to treat files as similar 
  min_similarity_percentage = float(input("Enter minimal similarity percentage to treat files as similar: "))

  # run directory classifier
  dir_classify = DirectorySimilarity(first_dir, second_dir, min_similarity_percentage)
  dir_classify.check_dirs()

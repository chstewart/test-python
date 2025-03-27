import os
import sys


def check_file_extension(filename, expected_extension):
  """Check if the file extension matches the expected extension."""
  return os.path.splitext(filename)[1].lower() == expected_extension.lower()


def process_text_file(file_name):
  """Read text file and write palindromes to a new file."""
  if not check_file_extension(file_name, ".txt"):
    print(f"Error: File '{file_name}' is not a .txt file.")
    sys.exit()
  try:
    with open(file_name, "r") as input_file:
      palindromes = []
      for word in input_file:
        cleaned_word = word.strip().lower()
        if cleaned_word == cleaned_word[::-1]:
          palindromes.append(cleaned_word)
  except FileNotFoundError:
    print(f"Error: File '{file_name}' not found.")
    sys.exit()
  file_name = file_name.replace(".txt", "") + "-palindromes.txt"
  with open(file_name, "w") as output_file:
    for word in palindromes:
      output_file.write(word + "\n")
  print(f"Palindromes saved to {file_name}")


process_text_file("random_list.txt")

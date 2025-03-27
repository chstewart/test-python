import sys
import tkinter.filedialog as tkFileDialog

# This might not work unless you have tkinter installed. I was just goofing around
# and wanted to see if could choose the file with a file dialog.
# You can find the other version in palindromes.py.


def get_file_name():
  """Use tkFileDialog to open a file dialog and select a file."""
  file_types = [("Text Files", "*.txt")]
  return tkFileDialog.askopenfilename(filetypes=file_types, title="Please select a file")


def process_text_file():
  """Read text file and write palindromes to a new file."""
  file_name = get_file_name()
  palindromes = []
  try:
    with open(file_name, "r") as input_file:
      for word in input_file:
        cleaned_word = word.strip().lower()
        if cleaned_word == cleaned_word[::-1]:
          palindromes.append(cleaned_word)
  except FileNotFoundError:
    print(f"Error: File '{file_name}' not found.")
    sys.exit()
  with open(file_name.replace(".txt", "") + "-palindromes.txt", "w") as output_file:
    for word in palindromes:
      output_file.write(word + "\n")


process_text_file()

import os;
from bs4 import BeautifulSoup;

path = os.path.join(os.path.dirname(__file__), 'fullpath.txt') # change the path string in the fullpath document

print('Filepath: >>', path, '<< exists?', os.path.isfile(path))



# for folder_name, subfolders, filenames in os.walk():
#      print(f'The current folder is {folder_name}')
#      for subfolder in subfolders:
#          print(f'SUBFOLDER OF {folder_name}: {subfolder}')
#      for filename in filenames:
#          print(f'FILE INSIDE {folder_name}: {filename}')
#      print('')
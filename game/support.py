from settings import *
from os.path import join
from os import walk



def audio_importer(*path):
	files = {}
	for folder_path, _, file_names in walk(join(*path)):
		for file_name in file_names:
			full_path = join(folder_path, file_name)
			files[file_name.split('.')[0]] = pygame.mixer.Sound(full_path)
	return files


#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Auteur: 2020 Yoann VARENNE 
# licence : MIT


import sys
import os
import random
import subprocess

class RP:
	def __init__(self):
		self.bienvenu()
		#self.path = os.path.abspath(os.path.split(__file__)[0])
		self.path = os.path.abspath(os.path.dirname(sys.argv[0]))
		
	# 1. Initialisation
	def bienvenu(self):
		if sys.platform == 'darwin':
			os.system('clear')
			#print('\n1. Je suis sous Mac')

		elif sys.platform == 'win32':
			os.system('cls')
			#print('\n1. Je suis sous Windows')
		
		print('')
		print('    ____        __          __     ____        __   __      ')
		print('   / __ \____  / /_  ____  / /_   / __ \____  _\_\ / /____  ')
		print('  / /_/ / __ \/ __ \/ __ \/ __/  / /_/ / __ \/ _ \/ __/ _ \ ')
		print(' / _, _/ /_/ / /_/ / /_/ / /_   / ____/ /_/ /  __/ /_/  __/ ')
		print('/_/ |_|\____/_.___/\____/\__/  /_/    \____/\___/\__/\___/  ')
		print('                                                            ')
		print('')


	# 3. Modifier le chemin en fonction de l’arborescence des chansons
	def pathSongFolder(self, path, dossier, sousDossier):
		pathSongFolder=os.path.join(path, dossier, sousDossier)
		print('--> Chemin complet du dossier ' + sousDossier + ' :')
		print('\t\t' + pathSongFolder) 
		if(not os.path.exists(pathSongFolder)):
			self.printRed('Attention, ce dossier n\'existe pas.\n')
			sys.exit()
		return pathSongFolder


	# 4. Lister un dossier des rimes 
	def listSong(self, pathSongFolder):
		liste = os.listdir(pathSongFolder)
		
		# suppression du .DS_Store
		if liste.count('.DS_Store'):
			liste.remove('.DS_Store')

		# suppression des fichiers invisibles
		for x in liste:
			if x[0] == '.':
				liste.remove(x)

		if len(os.listdir(pathSongFolder)) == 0:
			self.printRed('Attention, ce dossier est vide.\n')
			sys.exit()
		else:    
			print('--> Liste des fichiers :')
			print(liste) 
			return liste


	# 5. Choisir un mp3 de la liste2 aléatoirement
	def random(self, liste):
		song = random.choice(liste)
		print('--> Choix aléatoire d\'un fichier :')
		print('\t\t' + song)
		return song


	# 6. Supprimer ce fichier de la liste2 
	def remove(self, liste, song):
		liste.remove(song)
		print('--> Nouvelle liste des fichiers :')
		print(liste)


	# 7. Lire ce mp3 sélectionné
	def playSong(self, pathSongFolder, song):
		# utilisation d'un soft externe
		# if sys.platform == 'darwin':
		# 	pathApp=os.path.join(self.path, 'YV', 'fmedia', 'mac', 'fmedia')
		# elif sys.platform == 'win32':
		# 	pathApp=os.path.join(self.path, 'YV', 'fmedia', 'win', 'fmedia.exe')
		# if(not os.path.exists(pathApp)):
		# 	self.printRed('Attention, ce fichier n\'existe pas :')
		# 	self.printRed('\tpathApp\n')
		# 	sys.exit()
		# subprocess.run([pathApp, pathSongFile])

		pathSongFile=os.path.join(pathSongFolder, song)
		if(not os.path.exists(pathSongFile)):
			self.printRed('Attention, ce fichier n\'existe pas :')
			self.printRed('\tpathSongFile\n')
			sys.exit()
		print('--> Lecture du fichier : ')
		print('\t\t' + song)

		if sys.platform == 'darwin':
			self.playMac(pathSongFile)

		elif sys.platform == 'win32':
			self.playWin(pathSongFile, song)

	def playMac(self, audio_file_path):
		subprocess.run(['afplay', audio_file_path])

	def playWin(self, audio_file_path, alias):
		from ctypes import c_buffer, windll
		from random import random
		from time   import sleep
		from sys    import getfilesystemencoding

		def winCommand(*command):
			buf = c_buffer(255)
			command = ' '.join(command).encode(getfilesystemencoding())
			errorCode = int(windll.winmm.mciSendStringA(command, buf, 254, 0))
			if errorCode:
				errorBuffer = c_buffer(255)
				windll.winmm.mciGetErrorStringA(errorCode, errorBuffer, 254)
				exceptionMessage = ('\n    Error ' + str(errorCode) + ' for command:'
									'\n        ' + command.decode() +
									'\n    ' + errorBuffer.value.decode())
				raise PlaysoundException(exceptionMessage)
			return buf.value

		alias = 'playsound_' + str(random())
		winCommand('open "' + audio_file_path + '" alias', alias)
		winCommand('set', alias, 'time format milliseconds')
		durationInMS = winCommand('status', alias, 'length')
		print('Durée :', float(durationInMS) / 1000.0, 's')
		winCommand('play', alias, 'from 0 to', durationInMS.decode())
		sleep(float(durationInMS) / 1000.0)


	def printRed(self, message):
		print('\033[31m' + message + '\033[0m')




		

		  




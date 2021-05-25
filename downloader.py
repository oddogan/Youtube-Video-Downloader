"""
 * ------------------------------------------------------------
 * "THE BEERWARE LICENSE" (Revision 42):
 * Onat Deniz Dogan <oddogan@protonmail.com> wrote this code. As long as you retain this 
 * notice, you can do whatever you want with this stuff. If we
 * meet someday, and you think this stuff is worth it, you can
 * buy me a beer in return.
 * ------------------------------------------------------------
"""

"""
	* This program allows user to download YouTube videos as MP4 video or audio.
	* PyTube is used to interact with YouTube.
	* PyQt5 is used for GUI.

	* It downloads the best quality by default. A selection box can be implemented
		to allow user to select the quality in the future.
"""

from pytube import YouTube
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from os.path import expanduser
import sys, urllib
import qdarkstyle

class App(QWidget):

	def __init__(self):
		super().__init__()
		self.title = 'YouTube Video Downloader'
		self.author = 'by oddogan'
		self.left = 0
		self.top = 0
		self.width = 320
		self.height = 100
		self.layout = QVBoxLayout()
		self.initUI()
	
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.grid = QGridLayout()
		self.setLayout(self.grid)

		self.centerwindow()

		self.vidPic = QLabel(self)
		self.vidPic.setAlignment(Qt.AlignCenter)
		self.grid.addWidget(self.vidPic, 0, 0, 1, 2)
		self.vidPic.close()

		self.vidName = QLabel('Video Name', self)
		self.vidName.setAlignment(Qt.AlignCenter)
		self.grid.addWidget(self.vidName, 1, 0, 1, 2)
		self.vidName.close()

		self.url = QLineEdit('', self)
		self.url.setPlaceholderText('URL')
		self.grid.addWidget(self.url, 2, 0, 1, 2)

		self.input_dir = ''
		self.save = QLineEdit(self)
		self.save.setPlaceholderText('Save Directory')
		self.grid.addWidget(self.save, 3, 0, 1, 1)
		
		self.pickSave = QPushButton('Pick', self)
		self.pickSave.setToolTip('Click to choose save directory.')
		self.pickSave.clicked.connect(self.choose_directory)
		self.grid.addWidget(self.pickSave, 3, 1, 1, 1)

		self.buttonSearch = QPushButton('Search!', self)
		self.buttonSearch.setToolTip('Click to search video.')
		self.buttonSearch.clicked.connect(self.search)
		self.grid.addWidget(self.buttonSearch, 4, 0, 1, 2)

		self.radiobutton1 = QRadioButton("Video")
		self.radiobutton1.setChecked(True)
		self.radiobutton1.pref = 'video'
		self.radiobutton1.toggled.connect(self.typeDL)
		self.grid.addWidget(self.radiobutton1, 5, 0, 1, 1)
		self.radiobutton1.close()

		self.radiobutton2 = QRadioButton("Music")
		self.radiobutton2.pref = 'music'
		self.radiobutton2.toggled.connect(self.typeDL)
		self.grid.addWidget(self.radiobutton2, 5, 1, 1, 1)
		self.radiobutton2.close()

		self.buttonDL = QPushButton('Download!', self)
		self.buttonDL.setToolTip('Click to download.')
		self.buttonDL.clicked.connect(self.download)
		self.grid.addWidget(self.buttonDL, 6, 0, 1, 2)
		self.buttonDL.close()

		self.progressBar = QProgressBar(self)
		self.progressBar.setMaximum(100)
		self.grid.addWidget(self.progressBar, 7, 0, 1, 2)

		self.signature = QLabel(self.author, self)
		self.signature.setAlignment(Qt.AlignRight)
		self.grid.addWidget(self.signature, 8, 1, 1, 1)

		self.show()
	
	def centerwindow(self):
		"""
		centerwindow centers the application window, unless user moves it.
		"""
		qtRectangle = self.frameGeometry()
		centerPoint = QDesktopWidget().availableGeometry().center()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft())

	def typeDL(self):
		"""
		typeDL gets the choice of user to download either video or audio.
		"""
		radioButton = self.sender()
		if radioButton.isChecked():
			if radioButton.pref == 'music':
				self.audio = True
			else:
				self.audio = False

	@pyqtSlot()
	def search(self):
		"""
		search function searches YouTube for the given URL.
		If URL is invalid, handles it by showing an error to user and wait for new input.
		"""
		try:
			targetURL = self.url.text()
			self.yt = YouTube(targetURL, 
								on_progress_callback=self.progress, 
								on_complete_callback=self.complete)

			self.picurl = self.yt.thumbnail_url
			data = urllib.request.urlopen(self.picurl).read()
			pixmap = QPixmap()
			pixmap.loadFromData(data)
			pixmap = pixmap.scaledToWidth(300)
			self.vidPic.setPixmap(pixmap)
			self.vidPic.show()

			self.vidName.setText(self.yt.title)
			self.vidName.show()

			self.buttonSearch.close()

			self.radiobutton1.show()
			self.radiobutton2.show()
			self.buttonDL.show()
			self.centerwindow()
		except:
			self.url.setText("Invalid URL!")

	@pyqtSlot()
	def choose_directory(self):
		"""
		choose_directory allows user to choose a directory in computer.
		"""
		self.input_dir = QFileDialog.getExistingDirectory(None, 'Select a folder:', expanduser("~"))
		self.save.setText(self.input_dir)

	@pyqtSlot()
	def download(self):
		"""
		download function downloads the video and sends download progress to progress bar.
		"""
		self.url.setDisabled(True)
		self.video = self.yt.streams.filter(only_audio=self.audio).first()
		self.video.download(self.input_dir, self.yt.title)
		self.centerwindow()

	def progress(self, chunk, file_handle, bytes_remaining):
		"""
		progress function handles the update of progress bar.
		"""
		size = self.video.filesize
		progress = int(abs(bytes_remaining-size)/size*100)
                     
		self.progressBar.setValue(progress)

	def complete(self, stream, filepath):
		self.vidName.setText("Completed!")
		self.url.setText("")
		self.url.setEnabled(True)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyleSheet(qdarkstyle.load_stylesheet())
	screen = App()
	sys.exit(app.exec_())



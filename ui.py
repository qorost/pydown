from PySide.QtCore import *
from PySide.QtGui import *
import sys

from multiprocessing import Process, Lock
from time import *
import os

#import UrlFinder
from finder import FileFinder


""""
0913: add support for multi selection
1015: add links finder
"""

CSS_TREEVIEW = """ QListView {
     show-decoration-selected: 1;
 }
 QListView::item {
      border: 1px solid #d9d9d9;
     border-top-color: transparent;
     border-bottom-color: transparent;
 }
 QListView::item:hover {
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
     border: 1px solid #bfcde4;
 }
 QListView::item:selected {
     border: 1px solid #567dbc;
 }
 QListView::item:selected:active{
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);
 }
 QListView::item:selected:!active {
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);
 }"""

FILE_TYPE = ["pdf","doc*","ppt*","rar"]


class MyLinksTreeWidget(QTreeWidget):
	def __init__(self,controlapp):
		super(MyLinksTreeWidget,self).__init__()
		self.ctrapp = controlapp
		self.targetfolder = ''

		#
		self.setRootIsDecorated(False)
		self.setColumnCount(3)
		self.setHeaderLabels(["INDEX","TYPE","FILENAME","URL"])
		self.setUniformRowHeights(True)
		self.setEnabled(True)
		self.setAlternatingRowColors(True)
		self.setStyleSheet(CSS_TREEVIEW)

		self.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.actionSaveAs = QAction("Save as ...",self)
		self.actionSaveto = QAction("Save to ...",self)
		self.actionDownload = QAction("Add Selected to queue",self)
		self.actionDownloadall = QAction("Down All",self)
		self.actionUnselect = QAction("Unselect",self)
		self.addAction(self.actionSaveAs)
		self.addAction(self.actionSaveto)
		self.addAction(self.actionDownload)
		self.addAction(self.actionDownloadall)
		self.addAction(self.actionUnselect)
		self.connect(self.actionSaveAs,SIGNAL("triggered()"),self.save_as)
		self.connect(self.actionSaveto,SIGNAL("triggered()"),self.save_to)
		self.connect(self.actionDownload,SIGNAL("triggered()"),self.download_links)
		self.connect(self.actionDownloadall,SIGNAL("triggered()"),self.download_all_links)
		self.connect(self.actionUnselect,SIGNAL("triggered()"),self.unselect_link)
		#support for multislection
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)


	def save_as(self):
		#
		link = self.currentItem().text()
		#
		filename = str(QFileDialog.getSaveFileName(self,"Save as.."))
		self.ctrapp.add_links(link,filename)
		self.prompt_msg(filename)

	def save_to(self):
		"""down selected files to"""
		self.targetfolder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

	def download_all_links(self):
		links = []
		count = self.count()
		for i in range(0,count):
			item = self.item[i]
			links.append(item.text())

		if self.targetfolder == None:
			self.save_to()
		self.ctrapp.add_links(links,self.targetfolder)
		#newitem = QListWidgetItem("down all links")
		#self.addItem(newitem)

	def unselect_link(self):
		"""unselect all selected links"""
		selected = self.selectedItems()
		for item in selected:
			item.setSelected(False)

	def download_links(self):
		"""download a link and save as"""
		#all
		links = []
		selected = self.selectedItems()
		for item in selected:
			links.append(item.text())
		if self.targetfolder == None:
			self.save_to()
		self.ctrapp.add_links(links,self.targetfolder)
		#self.ctrapp.download_links()

	def prompt_msg(self,txt):
		#txt = self.targetfolder
		msgbox = QMessageBox()
		msgbox.setText(txt)
		msgbox.exec_()

	def add_links_to_widget(self,links):
		count = 1
		self.setUpdatesEnabled(False)
		self.clear()
		root = self.invisibleRootItem()
		if type(links) == list:
			for link in links:
				citem = QTreeWidgetItem()
				citem.setText(0,str(count))
				filetype = link[(link.rfind('.')+1):]
				#print filetype,link
				#print link.rfind('.')
				filename = link[(link.rfind('/')+1):]

				citem.setText(1,filetype)
				citem.setText(2,filename)
				citem.setText(3,link)
				citem.setFlags(citem.flags() | Qt.ItemIsEditable)
				root.addChild(citem)
				count += 1
		self.setUpdatesEnabled(True)
		self.update()

class MyControlListWidget(QListWidget):
	def __init__(self,controlapp):
		super(MyControlListWidget,self).__init__()

		self.setStyleSheet(CSS_TREEVIEW)

		#self.itemClicked.connect(self.onListLinkItemClicked)
			##right menu
		self.setContextMenuPolicy(Qt.ActionsContextMenu)
		self.actionSaveAs = QAction("Save as ...",self)
		self.actionSaveto = QAction("Save to ...",self)
		self.actionDownload = QAction("Add Selected to queue",self)
		self.actionDownloadall = QAction("Down All",self)
		self.actionUnselect = QAction("Unselect",self)
		self.addAction(self.actionSaveAs)
		self.addAction(self.actionSaveto)
		self.addAction(self.actionDownload)
		self.addAction(self.actionDownloadall)
		self.addAction(self.actionUnselect)
		self.connect(self.actionSaveAs,SIGNAL("triggered()"),self.save_as)
		self.connect(self.actionSaveto,SIGNAL("triggered()"),self.save_to)
		self.connect(self.actionDownload,SIGNAL("triggered()"),self.download_links)
		self.connect(self.actionDownloadall,SIGNAL("triggered()"),self.download_all_links)
		self.connect(self.actionUnselect,SIGNAL("triggered()"),self.unselect_link)

		#support for multislection
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.ctrapp = controlapp
		self.targetfolder = ''

	def save_as(self):
		#
		link = self.currentItem().text()
		#
		filename = str(QFileDialog.getSaveFileName(self,"Save as.."))
		self.ctrapp.add_links(link,filename)
		self.prompt_msg(filename)

	def save_to(self):
		"""down selected files to"""
		self.targetfolder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

	def download_all_links(self):
		links = []
		count = self.count()
		for i in range(0,count):
			item = self.item[i]
			links.append(item.text())

		if self.targetfolder == None:
			self.save_to()
		self.ctrapp.add_links(links,self.targetfolder)
		#newitem = QListWidgetItem("down all links")
		#self.addItem(newitem)

	def unselect_link(self):
		"""unselect all selected links"""
		selected = self.selectedItems()
		for item in selected:
			item.setSelected(False)

	def download_links(self):
		"""download a link and save as"""
		#all
		links = []
		selected = self.selectedItems()
		for item in selected:
			links.append(item.text())
		if self.targetfolder == None:
			self.save_to()
		self.ctrapp.add_links(links,self.targetfolder)
		#self.ctrapp.download_links()

	def prompt_msg(self,txt):
		#txt = self.targetfolder
		msgbox = QMessageBox()
		msgbox.setText(txt)
		msgbox.exec_()


class ControlApp(QWidget):
	def __init__(self,mainwindow):
		super(ControlApp,self).__init__()
		self.mainwindows  = mainwindow
		self.layout = QVBoxLayout()

		#1
		self.btnlayout = QHBoxLayout()
		self.urleditor = QLineEdit()
		self.urleditor.setText(r"http://www.cs.princeton.edu/courses/archive/spr11/cos217/lectures/")
		self.btn1 = QPushButton("CHECK")
		self.btn1.clicked.connect(self.check_page)
		self.btnlayout.addWidget(self.urleditor)
		self.btnlayout.addWidget(self.btn1)
		self.layout.addLayout(self.btnlayout)


		#2
		self.typelayout = QHBoxLayout()
		self.choice1 = QCheckBox(FILE_TYPE[0])
		self.choice2 = QCheckBox(FILE_TYPE[1])
		self.choice3 = QCheckBox(FILE_TYPE[2])
		self.choice4 = QCheckBox(FILE_TYPE[3])
		#self.choiceall = QRadioButton("all")
		self.btncheckall = QPushButton("All")
		self.btncheckall.clicked.connect(self.check_all_types)

		self.typelayout.addWidget(self.choice1)
		self.typelayout.addWidget(self.choice2)
		self.typelayout.addWidget(self.choice3)
		self.typelayout.addWidget(self.choice4)
		self.typelayout.addWidget(self.btncheckall)

		self.layout.addLayout(self.typelayout)


		#self.editor = QTextEdit()
		#self.layout.addWidget(self.editor)

		#list widget
		self.linkswidget = MyLinksTreeWidget(mainwindow)

		self.layout.addWidget(self.linkswidget)


		self.statusbar = QStatusBar()
		self.statusbar.showMessage("Ready")
		self.layout.addWidget(self.statusbar)
		#self.layout = QVBoxLayout()


		self.setLayout(self.layout)

	def check_all_types(self):
		self.choice1.setCheckState(Qt.Checked)
		self.choice2.setCheckState(Qt.Checked)
		self.choice3.setCheckState(Qt.Checked)
		self.choice4.setCheckState(Qt.Checked)


	def check_page(self):
		url = self.urleditor.text()
		patterns = []
		checkboxes = [self.choice1,self.choice2,self.choice3,self.choice4]
		for checkbox in checkboxes:
			tmpstate = self.choice1.checkState()
			if tmpstate == Qt.Checked:
				tmp = FILE_TYPE[checkboxes.index(checkbox)]
				if '*' in tmp:
					tmpx = tmp.replace('*','x')
					tmp = tmp.replace('*','')
					patterns.append(tmpx)
					patterns.append(tmp)
				else:
					patterns.append(tmp)
				#patterns.append(FILE_TYPE[checkboxes.index(checkbox)])

		print patterns
		#self.editor.
		ffinder = FileFinder(url,filetypes = patterns)
		links = list(ffinder.find())
		self.linkswidget.add_links_to_widget(links)


		# links = ["1","2","3"]
		# for link in links:
		# 	newlink = QListWidgetItem(link)
		# 	self.linkswidget.addItem(newlink)

	def add_links(self,links,targetdir):
		if self.mainwindows.get_down_table_status() == 0:
			self.mainwindows.start_new_tab()
		#check all links:
		self.mainwindows.add_links_to_downapp(links,targetdir)


class MyDownListWidgetItem(QListWidgetItem):
	def __init__(self):
		super(MyDownListWidgetItem,self).__init__()





class DownApp(QWidget):
	def __init__(self):
		super(DownApp,self).__init__()
		self.layout = QVBoxLayout()

		self.label = QLabel("Download Status")
		self.layout.addWidget(self.label)

		self.downlistwidget = QListWidget()
		self.layout.addWidget(self.downlistwidget)



		#status bar
		self.statusbar = QStatusBar()
		self.statusbar.showMessage("Ready")
		self.layout.addWidget(self.statusbar)

		self.setLayout(self.layout)

		self.downlinks = []
		self.history = []
		self.downstatus = 0
		self.mutex = Lock()

	def add_a_link_to_list_widget(self,link):
		newitem = QListWidgetItem(link)
		self.downlistwidget.addItem(newitem)

	def remove_link_from_list_widget(self,link,targetfolder):
		try:
			self.mutex.acquire(1)
			item = self.downlistwidget.findItems(link)
			if item is None:
				self.statusbar.showMessage("link not found")
			else:
				self.history.append(link)
				self.downlistwidget.removeItemWidget(item)
				self.statusbar.showMessage("link not found")
			self.mutex.release()
		except Exception,e:
			self.statusbar.showMessage(str(e))
			return 0

	def generate_output_filename(self,link,targetdir):
		tmp = link.split('/')
		output = ''
		if len(tmp) > 0:
			basename = tmp[-1]
		output = os.path.join(targetdir,basename)
		return output

	def add_links_to_down_list_widget(self,links,targetdir):
		try:
			self.mutex.acquire(1)
			outputname = ''
			if type(links) == str:
				outputname = targetdir
				self.add_a_link_to_list_widget(link[0],outputname)
			else:
				count = 0
				for link in links:
					if link not in self.downlinks:
						self.downlinks.append(link)
						outputname = self.generate_output_filename(link,targetdir)
						self.add_a_link_to_list_widget(link,outputname)
						count += 1
				self.mutex.release()
			return count
		except Exception,e:
			self.statusbar.showMessage(str(e))
			return 0


	def download(self):
		self.downstatus = 1


class DownloaderWindow(QMainWindow):
	def __init__(self):
		super(DownloaderWindow,self).__init__()
		self.setWindowTitle("File Downloader")
		self.setMinimumSize(400,300)
		self.apptab = QTabWidget()
		self.setCentralWidget(self.apptab)
		self.apptab.addTab(ControlApp(self),"Url")
		self.downtableenabled = 0
		self.downapp = DownApp()
		#self.apptab.addTab(DownApp(),"Downloading")
		self.show()

	def start_new_tab(self):
		if self.downtableenabled == 0:
			self.apptab.addTab(self.downapp,"Downloading")
			self.downtableenabled = 1

	def get_down_table_status(self):
		return self.downtableenabled

	def add_links_to_downapp(self,links,targetdir):
		self.downapp.add_links_to_down_list_widget(links,targetdir)
		return True


def main():
	app = QApplication(sys.argv)
	main = DownloaderWindow()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()

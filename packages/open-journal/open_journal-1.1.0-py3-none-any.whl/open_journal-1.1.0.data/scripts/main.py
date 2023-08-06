#!python
from cryptography.fernet import Fernet
import continuous_threading
import os
import shutil
import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QFileDialog, QMessageBox, QPushButton, QLabel
from openjournal.ui.MainWindow import Ui_MainWindow
from openjournal.ui.AboutWindow import Ui_AboutWindow


continuous_threading.set_allow_shutdown(True)
continuous_threading.set_shutdown_timeout(0)  # Default 1


class AboutWindow(QMainWindow, Ui_AboutWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        # centers window
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        # centers window
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        # in app buttons
        self.newBtn.clicked.connect(self.handleNewJournal)
        self.openBtn.clicked.connect(self.handleOpenJournal)
        self.saveBtn.clicked.connect(self.handleSaveJournal)
        self.encryptBtn.clicked.connect(self.handleEncrypt)
        self.decryptBtn.clicked.connect(self.handleDecrypt)
        self.export_keyBtn.clicked.connect(self.exportKey)
        self.deleteBtn.clicked.connect(self.handleDeleteJournal)
        self.closeBtn.clicked.connect(self.handleCloseJournal)

        # menubar buttons
        self.New.triggered.connect(self.handleNewJournal)
        self.Open.triggered.connect(self.handleOpenJournal)
        self.Save.triggered.connect(self.handleSaveJournal)
        self.Delete.triggered.connect(self.handleDeleteJournal)
        self.Encrypt_Journal.triggered.connect(self.handleEncrypt)
        self.Decrypt_Journal.triggered.connect(self.handleDecrypt)
        self.Export_key.triggered.connect(self.exportKey)
        self.Close.triggered.connect(self.handleCloseJournal)
        self.Exit.triggered.connect(self.closeEvent)

        self.About_Open_Journal.triggered.connect(self.handleAboutWindow)

        self.keyStatusWidget()  # check for key

        # creates thread to run auto-save function
        th = continuous_threading.Thread(target=self.autosave)
        th.start()

    def closeEvent(self, event):
        """Auto-save journal before closing."""
        self.handleSaveJournal()
        sys.exit(0)

    def handleNewJournal(self):
        """Create a new journal. If no journal open but text typed, it will be saved."""
        # save current journal, if applicable
        self.handleSaveJournal()

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(self, "Save New Journal Entry As...",
                                                  "./journals/.txt",
                                                  "All Files (*)",
                                                  options=options)

        try:
            if filename != '':
                if self.journalName.text() != '':
                    # clear previous journal
                    self.journalName.clear()
                    self.journalEdit.clear()

                self.journalName.setText(filename)
                file = open(filename, 'w')
                text = self.journalEdit.toPlainText()
                file.write(text)
                file.close()
        except FileNotFoundError:
            pass

    def handleOpenJournal(self):
        """Open an existing journal."""
        # save current journal, if applicable
        self.handleSaveJournal()

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Open Journal Entry",
                                                  "./journals",
                                                  "All Files (*)",
                                                  options=options)

        try:
            if filename != '':
                self.journalName.setText(filename)
                with open(filename) as file:
                    data = file.read()
                    self.journalEdit.setText(data)
        except FileNotFoundError:
            pass

    def handleCloseJournal(self):
        """Close currently open journal."""
        self.handleSaveJournal()

        try:
            filename = self.journalName.text()
            if filename != '':
                self.journalName.clear()
                self.journalEdit.clear()
            else:
                self.statusbar.showMessage('No journal currently open.', 2000)
        except FileNotFoundError:
            pass

    def handleSaveJournal(self):
        """Save currently open journal."""
        try:
            filename = self.journalName.text()
            file = open(filename, 'w')
            text = self.journalEdit.toPlainText()
            file.write(text)
            self.statusbar.showMessage(f"Saving '{filename}'...", 2000)
            file.close()
        except FileNotFoundError:
            pass

    def autosave(self):
        """Auto-saves every 15 seconds, if journal open."""
        while True:
            try:
                filename = self.journalName.text()
                file = open(filename, 'w')
                text = self.journalEdit.toPlainText()
                file.write(text)
                file.close()
            except FileNotFoundError:
                pass
            time.sleep(15)

    def createKey(self):
        """Generates encryption key and saves to file."""
        if self.checkKeyStatus():
            return open('open_journal_key.key', 'rb').read()
        else:
            key = Fernet.generate_key()
            with open('open_journal_key.key', 'wb') as key_file:
                key_file.write(key)

            self.exportKey()
            return open('open_journal_key.key', 'rb').read()

    def exportKey(self):
        """Copies encryption key to selected directory."""
        if self.checkKeyStatus():
            notice = QMessageBox()
            notice.setIcon(QMessageBox.Information)
            notice.setWindowTitle('Export Key')
            notice.setText('Save your encryption key to a safe place and keep it backed up.\n'
                           '\nOnly one key is used to encrypt journals. If you lose this key, you will not'
                           ' be able to recover any encrypted journals.')
            notice.setStandardButtons(QMessageBox.Ok)
            notice.exec_()
            try:
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                filename, _ = QFileDialog.getSaveFileName(self, "Export Encryption Key",
                                                          "./open_journal_key.key",
                                                          "All Files (*)",
                                                          options=options)

                if filename != '':
                    shutil.copy('open_journal_key.key', filename)
            except FileNotFoundError:
                pass
        else:
            self.loadKey()

    def loadKey(self):
        """Attempts to load key from root program directory, otherwise prompts user for location."""
        if self.checkKeyStatus():
            return open('open_journal_key.key', 'rb').read()
        else:
            try:
                key_options = QMessageBox()
                key_options.setIcon(QMessageBox.Question)

                key_options.setWindowTitle('Create Or Load Key')
                key_options.setText('No key was found in the program directory.')
                key_options.setInformativeText('Would you like to create a key or load an existing key?\n'
                                               '\nNote: You only need to create a key once.')
                key_options.addButton(QPushButton('Load Key'), QMessageBox.YesRole)
                key_options.addButton(QPushButton('Create Key'), QMessageBox.YesRole)
                key_options.addButton(QPushButton('Cancel'), QMessageBox.RejectRole)
                return_value = key_options.exec_()
                if return_value == 0:  # 0 refers to load key button
                    options = QFileDialog.Options()
                    options |= QFileDialog.DontUseNativeDialog
                    filename, _ = QFileDialog.getOpenFileName(self, "Load Encryption Key",
                                                              "./journals",
                                                              "All Files (*)",
                                                              "Key File (.key)",
                                                              options=options)

                    current_dir = os.getcwd()
                    shutil.copy(filename, current_dir)
                    old_key = os.path.basename(filename)
                    os.rename(old_key, r'open_journal_key.key')  # rename to expected name
                    return open(filename, 'rb').read()
                elif return_value == 1:  # 1 refers to create key button
                    self.createKey()
                elif return_value == 2:
                    pass
            except FileNotFoundError or TypeError:
                pass

    def checkKeyStatus(self):
        """Checks if an existing key is located in same location as program."""
        return os.path.exists('open_journal_key.key')

    def keyStatusWidget(self):
        """Displays key status in statusbar."""
        if self.checkKeyStatus():
            key_status = QLabel('Key loaded')
            key_status.setStyleSheet('border :1px solid white;'
                                     'background-color: rgb(115, 210, 22);')
            self.statusbar.addPermanentWidget(key_status)
        else:
            key_status = QLabel('Key not loaded')
            key_status.setStyleSheet('border :1px solid white;'
                                     'background-color: rgb(204, 0, 0);')
            self.statusbar.addPermanentWidget(key_status)

    def handleEncrypt(self):
        """Encrypts currently open journal."""
        try:
            key = self.loadKey()
            self.handleSaveJournal()

            filename = self.journalName.text()
            f = Fernet(key)

            # read journal file
            with open(filename, 'rb') as file:
                journal = file.read()

            # encrypt journal and write to file
            encrypted_journal = f.encrypt(journal)
            with open(filename, 'wb') as file:
                file.write(encrypted_journal)

            # display encrypted contents
            with open(filename) as now_encrypted:
                data = now_encrypted.read()
                self.journalEdit.setText(data)
        except FileNotFoundError:
            self.statusbar.showMessage('Encryption failed. No file currently open.', 2000)
        except TypeError:
            pass

    def handleDecrypt(self):
        """Decrypts currently open journal."""
        try:
            key = self.loadKey()
            self.handleSaveJournal()
            filename = self.journalName.text()
            f = Fernet(key)

            # read the journal file
            with open(filename, 'rb') as file:
                encrypted_journal = file.read()

            # decrypt the journal and write to file
            decrypted_journal = f.decrypt(encrypted_journal)
            with open(filename, 'wb') as file:
                file.write(decrypted_journal)

            # display decrypted contents
            with open(filename) as now_decrypted:
                data = now_decrypted.read()
                self.journalEdit.setText(data)
        except FileNotFoundError:
            self.statusbar.showMessage('Decryption failed. No file currently open.', 2000)
        except TypeError:
            pass

    def handleDeleteJournal(self):
        """Delete currently open journal."""
        try:
            filename = self.journalName.text()
            if filename != '':
                confirm = QMessageBox()
                confirm.setIcon(QMessageBox.Warning)
                confirm.setWindowTitle('Confirm Journal Deletion')
                confirm.setText('You are about to delete the currently opened journal.')
                confirm.setInformativeText('This action cannot be undone. Continue?')
                confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                return_value = confirm.exec_()
                if return_value == QMessageBox.Yes:
                    os.remove(filename)
                    self.journalEdit.clear()
                    self.journalName.clear()
                else:
                    pass
            else:
                self.statusbar.showMessage('No journal open, nothing to delete.', 2000)
        except FileNotFoundError:
            pass

    def handleAboutWindow(self):
        about_window = AboutWindow(self)
        about_window.show()


app = QApplication(sys.argv)


def main():
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

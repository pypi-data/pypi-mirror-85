"""
Runs a window which can display html like a browser
"""

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.browser.setHtml("<h1>Test</h1>")

        self.setCentralWidget(self.browser)

        self.show()

    def html(self, value):
       self.browser.setHtml(value)


def run_browser(html):
    """
    Starts browser and accepts html to be displayed
    """
    app = QApplication(["wikireader"])
    window = MainWindow()
    window.html(html)
    app.exec_()


if __name__ == '__main__':
    html = """<h1>Head1</h1>
    <h2>Head 2</h2>
    <p>This is a paragraph</p>
    <ul>
    <li>One</li>
    <li>two</li>
    </ul>"""
    runBrowser(html)


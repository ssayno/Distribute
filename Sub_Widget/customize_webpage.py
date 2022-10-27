import pickle
from PyQt5.QtCore import QDateTime, QUrl, pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtNetwork import QNetworkCookie
from PyQt5.QtCore import Qt
import os


class Customize_Webengine_page(QWebEnginePage):
    def __init__(self, zoom_factor=1, parent=None):
        super(Customize_Webengine_page, self).__init__(parent=parent)
        # 创建新的页面 重新设置 zoom factor
        self.setZoomFactor(zoom_factor)
        self.cookie_obj = self.profile().cookieStore()
        self.cookies_dir = os.path.normpath(
            os.path.join(
                os.path.dirname(__file__), os.pardir, 'Data', 'Cookies'
            )
        )


    def createWindow(self, type: 'QWebEnginePage.WebWindowType') -> 'QWebEnginePage':
        page = QWebEnginePage(self)
        page.urlChanged.connect(self.on_url_changed)
        return page

    @pyqtSlot(QUrl)
    def on_url_changed(self, url):
        page = self.sender()
        self.setUrl(url)
        page.deleteLater()

    def _add_cookies(self, suffix):
        self.cookie_obj.deleteAllCookies()
        selected_json_file = f'cookies_{suffix}.pkl'
        selected_json_file_path = os.path.join(self.cookies_dir, selected_json_file)
        print('选择了', selected_json_file_path)
        with open(selected_json_file_path, 'rb') as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                qcookie = QNetworkCookie()
                qcookie.setDomain(cookie.get('domain', ''))
                qcookie.setName(cookie.get('name', '').encode())
                qcookie.setValue(cookie.get('value', '').encode())
                qcookie.setPath(cookie.get('path', ''))
                qcookie.setExpirationDate(
                    QDateTime.fromString(str(cookie.get('expire', 0)),
                                         Qt.ISODate))
                qcookie.setHttpOnly(cookie.get('httpOnly', False))
                qcookie.setSecure(cookie.get('secure', False))
                self.cookie_obj.setCookie(qcookie)
        self.parent().reload()

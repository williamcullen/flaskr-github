# _*_ encoding:utf-8 _*_
import os
import flaskr
import unittest
import tempfile


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.testing = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'被狗吃了，什么都没有' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('admin', 'admin')
        assert b'登录成功' in rv.data
        rv = self.logout()
        assert b'已退出登录' in rv.data
        rv = self.login('adminx', 'admin')
        assert b'用户名错误' in rv.data
        rv = self.login('admin', 'adminx')
        assert b'密码错误' in rv.data

    def test_messages(self):
        self.login('admin', 'admin')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert b'被狗吃了，什么都没有' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data


if __name__ == '__main__':
    unittest.main()

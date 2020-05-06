import mock
import requests
import pytest

a=mock.Mock(name='mock a',return_value='hello')

def send_request(url):
    re=requests.get(url)
    return re.status_code

def visit_ustack():
    return send_request("http://www.ustack.com")

def test_success():
    success_send=mock.Mock(return_value=200)
    send_request=success_send
    assert visit_ustack()==200

if __name__ == '__main__':
    pytest.main()


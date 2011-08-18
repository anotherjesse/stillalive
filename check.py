import cookielib
import re
import requests

requests.settings(timeout=5.0)

def dash(url, tenant='admin', user='admin', password='secrete'):
    crsf_regex = re.compile("name='csrfmiddlewaretoken' value='([^']*)'")
    login_regex = re.compile("auth")
    error_regex = re.compile("Error")

    jar = cookielib.CookieJar()
    r = requests.get(url+'/auth/login/', cookies=jar)
    assert r.status_code == 200, 'unable to access login page'
    assert not re.match(error_regex, r.content), 'error displayed on login page'

    match = re.search(crsf_regex, r.content)
    assert match, 'Unable to find CRSF token'

    auth = {'csrfmiddlewaretoken': match.groups(1)[0],
            'method': 'Login',
            'username': user,
            'password': password}

    r = requests.post(url+'/auth/login/', data=auth, cookies=jar)
    assert r.status_code == 200, 'fail to send auth credentials'
    assert not re.search(error_regex, r.content), 'error displayed on auth'

    r = requests.get(url+'/dash/', cookies=jar)
    assert r.status_code == 200, 'fail to access user dash'
    assert not re.search(login_regex, r.url), 'user dash fail (redirected to login)'
    assert not re.search(error_regex, r.content), 'error displayed on user dash'

    r = requests.get(url+'/dash/%s/images/' % tenant, cookies=jar)
    assert r.status_code == 200, 'fail to access dash/images'
    assert not re.search(login_regex, r.url), 'images fail (redirected to login)'
    assert not re.search(error_regex, r.content), '(glance?) error displayed'

    r = requests.get(url+'/syspanel/', cookies=jar)
    assert r.status_code == 200, 'fail to access syspanel'
    assert not re.search(login_regex, r.url), 'syspanel fail (redirected to login)'
    assert not re.search(error_regex, r.content), 'error displayed on syspanel'


if __name__ == '__main__':
    host = 'dev2.rcb.me'
    url = 'http://' + host
    dash(url)


import platform
import sqlite3
import urllib3
import threading
import requests
import time


def get_db():
    sysstr = platform.system()
    if sysstr == "Linux":
        db = sqlite3.connect('/root/flask_proxy/venv/var/flaskr-instance/flaskr.sqlite')
    # debug
    elif sysstr == "Windows":
        db = sqlite3.connect('flaskr.sqlite')
    return db


def get_records():
    db = get_db()
    id_ip_port_list = db.execute(
        "SELECT id,ip,port FROM proxy WHERE created =(SELECT MAX(created) FROM proxy)").fetchall()
    # print(id_ip_port_list)
    return id_ip_port_list


def ping_163(id, ip, port):
    url = "http://music.163.com"
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"}
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    proxy_dict = {"http": "socks5://" + ip + ':' + port}
    s = requests.Session()
    a = requests.adapters.HTTPAdapter(max_retries=1)
    s.mount('http://', a)
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        r = s.get(url, headers=send_headers, verify=False, proxies=proxy_dict, timeout=(3.05, 3.05))
        if r.status_code == 200:
            elapsed = r.elapsed.total_seconds()
            # print("{:10.2f}".format(elapsed) + "\t" + ip + ':' + port)
            delay = str(elapsed)
            db = get_db()
            db.execute("REPLACE INTO socks (id, updated, delay, ip, port, author_id) VALUES (?,?,?,?,?,?)",
                       (id, datetime, delay, ip, port, 1))
            db.commit()
    except requests.exceptions.ReadTimeout:
        pass
    except requests.exceptions.ConnectTimeout:
        pass
    except requests.exceptions.ConnectionError:
        pass
    except requests.exceptions.RequestException as e:
        print(e)
        pass


if __name__ == '__main__':
    while 1:
        threads = []
        t_start = time.time()
        records = get_records()
        for r in records:
            id, ip, port = r[0], r[1], r[2]
            # print(ip, port)
            thread = threading.Thread(target=ping_163, args=(id, ip, port,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

        t_end = time.time()
        print('Total time cost: ', t_end - t_start, 's')
        # time.sleep(10)

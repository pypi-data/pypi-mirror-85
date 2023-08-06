# -*-coding:utf-8-*-

import time
import random
import requests


def template(site: dict):
    for sitename, account in site.items():
        error1 = {}
        loginurl = "https://" + sitename + ".com/auth/login"
        logouturl = "https://" + sitename + ".com/user/logout"
        checkinurl = " https://" + sitename + ".com/user/checkin"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        }
        checkinheaders = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
            "Content-Type": "application/json",
        }
        checkinpostdata = {}
        for email, passwd in account.items():
            email = str(email)
            passwd = str(passwd)
            accountpostdata = {
                "email": email,
                "passwd": passwd,
            }
            s = requests.Session()
            login = s.post(url=loginurl, headers=headers, data=accountpostdata)
            if eval(login.text)["ret"] != 1:
                error1["login"] = login.text
            time.sleep(random.randint(1, 3))
            checkin = s.post(url=checkinurl, headers=checkinheaders, data=checkinpostdata)
            if eval(checkin.text)["ret"] != 1:
                error1['checkin'] = checkin.text
            time.sleep(random.randint(1, 3))
            logout = s.get(url=logouturl, headers=headers)
            if "<html>" not in logout.text or "</html>" not in logout.text:
                error1['logout'] = logout.status_code
            s.close()
            if error1:
                f = open(r"autocheckin_log.txt", "a", encoding="utf-8")
                f.write(
                    time.strftime("%Y-%m-%d %H:%M:%S",
                                  time.localtime()) + "--用户    " + email + "    " + sitename + "签到失败" + "\n")
                f.close()
                f = open(r"autocheckin_error.txt", "a", encoding="utf-8")
                f.write(time.strftime("%Y-%m-%d %H:%M:%S",
                                      time.localtime()) + "--用户    " + email + "    " + sitename + "签到失败:\n")
                for i, j in error1.items():
                    f.write("   " + i + ":" + j + "\n")
                f.close()
            else:
                f = open(r"autocheckin_log.txt", "a", encoding="utf-8")
                f.write(
                    time.strftime("%Y-%m-%d %H:%M:%S",
                                  time.localtime()) + "--用户    " + email + "    " + sitename + "签到成功," + "\n")
                f.close()
    return True


def puyun(account: dict):
    loginurl = "https://pucloud.vip/auth/login"
    logouturl = "https://pucloud.vip/user/logout"
    checkinurl = "https://pucloud.vip/user/checkin"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    }
    checkinheaders = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "Content-Type": "application/json",
    }
    checkinpostdata = {}
    for email, passwd in account.items():
        email = str(email)
        passwd = str(passwd)
        accountpostdata = {
            "email": email,
            "passwd": passwd,
        }
        error1 = {}
        s = requests.Session()
        login = s.post(url=loginurl, headers=headers, data=accountpostdata)
        if eval(login.text)["ret"] != 1:
            error1['login'] = login.text
        time.sleep(random.randint(1, 3))
        checkin = s.post(url=checkinurl, headers=checkinheaders, data=checkinpostdata)
        if eval(checkin.text)["ret"] != 1:
            error1['checkin'] = checkin.text
        time.sleep(random.randint(1, 3))
        logout = s.get(url=logouturl, headers=headers)
        if "<html>" not in logout.text or "</html>" not in logout.text:
            error1['logout'] = logout.status_code
        s.close()
        if error1:
            f = open(r"autocheckin_log.txt", "a", encoding="utf-8")
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "--用户    " + email + "    puyun签到失败" + "\n")
            f.close()
            f = open(r"autocheckin_error.txt", "a", encoding="utf-8")
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "--用户    " + email + "    puyun签到失败:\n")
            for i, j in error1.items():
                f.write("    " + i + ":" + j + "\n")
            f.close()
        else:
            f = open(r"autocheckin_log.txt", "a", encoding="utf-8")
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "--用户    " + email + "    puyun签到成功" + "\n")
            f.close()
    return True


def fpork(account: dict):
    error1 = {}
    loginurl = "https://forever.fpork.com/auth/login"
    logouturl = "https://forever.fpork.com/user/logout"
    checkinurl = "https://forever.fpork.com/user/checkin"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    }
    checkinheaders = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "Content-Type": "application/json",
    }
    checkinpostdata = {}
    for email, passwd in account.items():
        email = str(email)
        passwd = str(passwd)
        accountpostdata = {
            "email": email,
            "passwd": passwd,
        }
        s = requests.Session()
        login = s.post(url=loginurl, headers=headers, data=accountpostdata)
        if eval(login.text)["ret"] != 1:
            error1["login"] = login.text
        time.sleep(random.randint(1, 3))
        checkin = s.post(url=checkinurl, headers=checkinheaders, data=checkinpostdata)
        if eval(checkin.text)["ret"] != 1:
            error1['checkin'] = checkin.text
        time.sleep(random.randint(1, 3))
        logout = s.get(url=logouturl, headers=headers)
        if "<html>" not in logout.text or "</html>" not in logout.text:
            error1['logout'] = logout.status_code
        s.close()
        if error1:
            f = open(r"autocheckin_log.txt", "a", encoding="utf-8")
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "--用户    " + email + "    fpork签到失败" + "\n")
            f.close()
            f = open(r"autocheckin_error.txt", "a", encoding="utf-8")
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "--用户    " + email + "    fpork签到失败:\n")
            for i, j in error1.items():
                f.write("   " + i + ":" + j + "\n")
            f.close()
        else:
            f = open(r"autocheckin_log.txt", "a", encoding="utf-8")
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "--用户    " + email + "    fpork签到成功," + "\n")
            f.close()
    return True


def liuns(account: dict):
    error1 = {}
    loginurl = "https://liuns.com/auth/login"
    logouturl = "https://liuns.com/user/logout"
    checkinurl = " https://liuns.com/user/checkin"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    }
    checkinheaders = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "Content-Type": "application/json",
    }
    checkinpostdata = {}
    for email, passwd in account.items():
        email = str(email)
        passwd = str(passwd)
        accountpostdata = {
            "email": email,
            "passwd": passwd,
        }
        s = requests.Session()
        login = s.post(url=loginurl, headers=headers, data=accountpostdata)
        if eval(login.text)["ret"] != 1:
            error1["login"] = login.text
        time.sleep(random.randint(1, 3))
        checkin = s.post(url=checkinurl, headers=checkinheaders, data=checkinpostdata)
        if eval(checkin.text)["ret"] != 1:
            error1['checkin'] = checkin.text
        time.sleep(random.randint(1, 3))
        logout = s.get(url=logouturl, headers=headers)
        if "<html>" not in logout.text or "</html>" not in logout.text:
            error1['logout'] = logout.status_code
        s.close()
        if error1:
            f = open(r"autocheckin_log.txt", "a", encoding="utf-8")
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "--用户    " + email + "    liuns签到失败" + "\n")
            f.close()
            f = open(r"autocheckin_error.txt", "a", encoding="utf-8")
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "--用户    " + email + "    liuns签到失败:\n")
            for i, j in error1.items():
                f.write("   " + i + ":" + j + "\n")
            f.close()
        else:
            f = open(r"autocheckin_log.txt", "a", encoding="utf-8")
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "--用户    " + email + "    liuns签到成功," + "\n")
            f.close()
    return True


def allcheckin(puyunaccount: dict, fporkaccount: dict, liunsaccount: dict):
    puyun(puyunaccount)
    fpork(fporkaccount)
    liuns(liunsaccount)
    return True


def byonebyone(puyunaccount: dict, fporkaccount: dict, liunsaccount: dict):
    puyun(puyunaccount)
    fpork(fporkaccount)
    liuns(liunsaccount)
    return True


def bytemplate(isite: dict, iaccount: dict):
    """
    site.keys():
        1:pucloud
        2:forever
        3:liuns
    site.values():
        key:username
        value:password
    :return:
    """
    site = {}
    sitedict = {1: "pucloud", 2: "forever", 3: "liuns"}
    if iaccount:
        for i in isite.keys():
            site[sitedict[i]] = iaccount
        print(site)
    else:
        for i in isite.keys():
            site[sitedict[i]] = isite[i]
        print(site)
    return True

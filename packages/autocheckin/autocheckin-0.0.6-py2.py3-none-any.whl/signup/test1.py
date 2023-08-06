# -*-coding:utf-8-*-

from LoveNishimiyaShouko import allcheckin, puyun, fpork, liuns, byonebyone, bytemplate

if __name__ == '__main__':
    puyun({"username1": "password1"})
    fpork({"username1": "password1"})
    liuns({"username1": "password1"})
    allcheckin({"username1": "password1"}, {"username2": "password2"})
    byonebyone({"username1": "password1"}, {"username2": "password2"})
    bytemplate({1: {}, 2: {"": ""}, 3: {"username1": "password1"}}, {})
    bytemplate({1: {}, 2: {"": ""}, 3: {"username1": "password1"}}, {"username2": "password2"})

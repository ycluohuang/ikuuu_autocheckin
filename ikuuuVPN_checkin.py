#encoding:utf-8
import requests
import datetime, time
import sys,os

def vpn_login(email, password):
    HEAD = { 
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
    # 'referer': 'https://ikuuu.me/auth/login'
    }
    DATA = {
        'email': email,
        'passwd' : password #为什么这里password改成passwd就对了,因为网页里也是passwd
    }
    URL_login = "https://ikuuu.me/auth/login"
    httpSession = requests.session() 
    #创建一个session对象,用来保存cookie,下次访问时携带cookie,
    # 维持登录状态,不然会被认为是未登录状态
    try:
        print("正在登录...")
        response_login = httpSession.post(url=URL_login, headers=HEAD, data=DATA)
        print("login_response:", response_login.text.encode("utf-8").decode('unicode_escape')) 
        if response_login.json()['ret'] != 1: 
            print("登录失败:", response_login.json()['msg'])
            return
    except Exception as e:
        print("登录失败:", e)
        return
    time.sleep(1)
    print("登录成功")

    # 签到,如果连接发生变化记得修改
    URL_checkin = "https://ikuuu.me/user/checkin"
    try:
        print("正在签到...")
        response_checkin = httpSession.post(url=URL_checkin)
        print("checkin_response:", response_checkin.text.encode('utf-8').decode('unicode_escape'))
        if response_checkin.json()['ret'] != 1:
            print("签到失败!!")
            return
    except Exception as e:
        print("签到失败:", e)
        return
    time.sleep(1)
    print("签到成功")


def main():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now)

    # 改成手动输入
    # 获取真正的账号字符串 secret里的TOKEN
    # 规则：每个账号密码间用&&连接，不同账号间用||连接
    #创建TOKEN环境变量

    accounts = os.environ.get("TOKEN","[]").split("||") #ok

    if accounts[0] == "":
        print("没有账号！！")
        return
    print(accounts,'\n')

    i = 1
    # 修改后的
    for account in accounts:
        print(f"第{i}个账号") 
        email = account.split("&&")[0]
        psw = account.split("&&")[1]
        # print(email,psw) # sep 分隔符默认空格
        vpn_login(email, psw)
        i += 1


if __name__ == "__main__": 
    # 这里是一个判断，如果这个文件是直接运行的，那么就执行main()函数，
    # 如果是被其他文件import的，那么就不执行
    main()

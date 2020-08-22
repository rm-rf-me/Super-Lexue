#coding=UTF-8

from selenium import webdriver
import os
import re
import time



def getCodes():
    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    browser = webdriver.Chrome(chrome_options=option)
    browser.get("http://lexue.bit.edu.cn/my/")
    browser.maximize_window()
    userName = input('请输入学号：')
    passWord = input('请输入密码：')

    print('loging...')

    browser.find_element_by_id("username").send_keys(userName)
    browser.find_element_by_id("password").send_keys(passWord)
    browser.find_element_by_id("rememberMe").click()
    browser.find_element_by_class_name("btn_image").submit()


    # logining

    time.sleep(2)
    exit_flag = 0
    couresHrefs = []
    couresNames = []

    coureses = browser.find_elements_by_class_name('coursename.mr-2')
    for coures in coureses:
        couresHrefs.append(coures.get_attribute('href'))
        couresNames.append(coures.text)

    if (len(couresNames) == 0):
        print("无法得到课程信息！（密码错误或者未选课）")
        return

    for i in range(len(couresNames)):
        print('{}.{}'.format(i + 1, couresNames[i]))

    k = int(input('选择所要爬取的代码的课程编号：'))
    browser.get(couresHrefs[k - 1])

    root = input(r"选择所要存储代码的文件夹(如果不存在将建立,mac请使用/，win请使用\\。最后记得加\\或者/): ")
    root = root + couresNames[k - 1] + '/'
    if not os.path.exists(root):
        os.makedirs(root)
        print("已建立{}文件夹！".format(root))

    num = 1
    contents = browser.find_elements_by_css_selector(
        ".activity.programming.modtype_programming")

    print("开始爬取！\n")
    for content in contents:
        name = content.find_element_by_class_name("instancename").text
        herf = content.find_element_by_tag_name("a").get_attribute("href")

        print("正在爬取第{}题:{}".format(num, name))
        num += 1
        newWindow = 'window.open("{}")'.format(herf)
        browser.execute_script(newWindow)
        browser.switch_to_window(browser.window_handles[1])
        browser.find_element_by_xpath(
            '//*[@id="region-main"]/div/ul/li[4]/a').click()

        try:
            browser.find_element_by_xpath(
                '//*[@id="codeview"]/div/div/div/a[1]').click()
        except:
            print('无法找到提交信息！自动跳过')
            browser.close()
            browser.switch_to_window(browser.window_handles[0])
            continue

        browser.switch_to_window(browser.window_handles[-1])

        # 修改缩进
        codes = browser.find_element_by_tag_name("textarea").text
        codes = codes.replace('    ', '\t')
        codes = list(codes)
        if '\t' not in codes or '    ' not in codes:
            for i in range(len(codes)):
                if codes[i] == '\n':
                    i += 1
                    while codes[i] == ' ':
                        codes[i] = '\t'
                        i += 1

        codes = ''.join(codes)

        browser.close()
        browser.switch_to_window(browser.window_handles[1])
        browser.close()
        browser.switch_to_window(browser.window_handles[0])

        # 正则表达式去除特殊符号
        name = re.sub(r'[*()?]', '', name)
        path = root + name + '.cpp'

        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write(codes)
                print("{}爬取成功\n".format(name))
        else:
            print("文件已存在\n")

    browser.quit()


if __name__ == "__main__":
    getCodes()


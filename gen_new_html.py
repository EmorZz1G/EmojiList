from bs4 import BeautifulSoup
import os
proj_pth = os.path.dirname(__file__)

import argparse

parser = argparse.ArgumentParser(description='Generate new HTML with additional column for emoji LaTeX keys.')
parser.add_argument('--test', action='store_true', help='Run in test mode with a limited number of rows.')
args = parser.parse_args()

testing = args.test

html_context = open(proj_pth+'/index_ori.html')

soup = BeautifulSoup(html_context, 'html.parser')

table = soup.find('table')

tr_rows = table.find_all('tr')
# 只有一个th的不需要处理

if testing:
    tr_rows = tr_rows[:30]  # 测试模式下只处理前10行
    print("测试模式下，只处理前30行。")

# 处理有多个th的
for tr in tr_rows:
    if len(tr)==1:continue
    elif len(tr.find_all('th')) > 0 and len(tr.find_all('td')) ==0:
        # 新建一个<th>元素
        new_th = soup.new_tag('th')
        # 设置新<th>里面的内容
        new_th.string = 'Possible Emoji Key in Latex'
        # 将新<th>插入到当前第三个th后面
        tr.insert(6, new_th)
        if testing:
            print(tr)
            break

tr_rows = table.find_all('tr')

def transform_to_latex(raw_str):
    # 处理raw_str
    # 去掉前后空格
    raw_str = raw_str.strip()
    # 将空格替换为下划线
    raw_str = raw_str.replace(': ', '-')
    raw_str = raw_str.replace(' ', '-')
    # 将中文括号替换为英文括号
    return raw_str

if testing:
    print("Running in test mode, limiting to 20 rows.")
    tr_rows = tr_rows[:70]

# 处理有多个th的
for tr in tr_rows:
    if len(tr)==1:
        th = tr.find('th')
        # th colspan修改为6
        th['colspan'] = '6'
        if testing:
            print("修改了th的colspan为6")
            print(tr)
    # 如果tr里面有td
    elif len(tr.find_all('td')) > 0:
        tds = tr.find_all('td')
        raw_str = tds[-2].string
        new_td = soup.new_tag('td')
        # 增加class
        new_td['class'] = 'emoji-latex name'
        new_string = transform_to_latex(raw_str)
        button = soup.new_tag('button')
        button.string = 'Copy'
        # 逆天HTML，两次转义
        clipboard_str = f"\\\\emoji{{{new_string}}}"
        button['onclick'] = f"navigator.clipboard.writeText('{clipboard_str}');"
        new_td.string = new_string+" "
        new_td.append(button)
        tr.insert(6, new_td)
        if testing:
            print("添加了新的td")
            print(tr)
            break
    else:
        pass
        # 不处理

if testing:
    print("测试模式下，不保存修改后的HTML文件。")
else:
    print("处理完成，已添加新的列和按钮。") 
    # 保存修改后的HTML到新文件
    with open(proj_pth+'/index.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print("新HTML文件已保存为 index.html。")
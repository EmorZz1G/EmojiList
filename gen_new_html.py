from bs4 import BeautifulSoup
import os
proj_pth = os.path.dirname(__file__)

html_context = open(proj_pth+'/index_ori.html')

soup = BeautifulSoup(html_context, 'html.parser')

table = soup.find('table')

tr_rows = table.find_all('tr')
# 只有一个th的不需要处理

# 处理有多个th的
for tr in tr_rows:
    if len(tr)==1:continue
    else:
        # 新建一个<th>元素
        new_th = soup.new_tag('th')
        # 设置新<th>里面的内容
        new_th.string = 'Possible Emoji Key in Latex'
        # 将新<th>插入到当前第三个th后面
        tr.insert(3, new_th)

tr_rows = table.find_all('tr')



def transform_to_latex(raw_str):
    # 处理raw_str
    # 去掉前后空格
    raw_str = raw_str.strip()
    # 将空格替换为下划线
    raw_str = raw_str.replace(' ', '-')
    # 将中文括号替换为英文括号
    return raw_str

# tr_rows = tr_rows[:5]
# 处理有多个th的
for tr in tr_rows:
    if len(tr)==1:continue
    # elif tr
    # 如果tr里面有td
    elif len(tr.find_all('td')) > 0:
        tds = tr.find_all('td')
        raw_str = tds[-2].string
        new_td = soup.new_tag('td')
        # 增加class
        new_td['class'] = 'emoji-latex name'
        new_string = transform_to_latex(raw_str)
        button = soup.new_tag('button')
        button.string = 'Copy to Clipboard'
        button['onclick'] = f"navigator.clipboard.writeText('{new_string}');"
        new_td.append(button)
        new_td.string = new_string
        tr.insert(6, new_td)
    else:
        pass
        # 不处理
    
print("处理完成，已添加新的列和按钮。") 
# 保存修改后的HTML到新文件
with open(proj_pth+'/index.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))
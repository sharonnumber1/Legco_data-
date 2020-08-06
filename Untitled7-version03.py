#!/usr/bin/env python
# coding: utf-8

# In[136]:


from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd
import numpy as np
from  tqdm import tqdm
import time
from datetime import datetime


# # paper document extraction

# # per subcommittee extraction

# In[137]:


def url_subcom_table_paper(url):
    table_1=first_layer_extract(url)
    #print(table_1)
    final=[]
    for i in range(len(table_1['url'])):
        url=table_1['url'][i]
        time.sleep(0.5)
        final.append(URL_to_second_table(url))
    table_list=combine_table(table_1,final)
    return (pd.concat(table_list))


# # first layer extraction

# In[138]:


def tab_generate(back,url):
    link_split=url.split('/')
    back_split=back.split('_')[0]
    #print(len(link_split))
    desired=link_split[0]+'//'+link_split[2]+'/'+link_split[3]+'/'+link_split[4]+'/'+link_split[5]+'/'+back_split+'/'+link_split[7]+'/'+back
    return desired


# In[139]:


def first_table_transform(x):
    list=[]
    for i in range(len(x)):
        if x[i].find_all("td")[2].find('a')!=None:
            cell0=x[i].find_all("td")[2].find('a').text
            cell01=tab_generate(x[i].find_all("td")[2].find('a').get("href"),url)
            #cell01=x[i].find_all("td")[2].find('a').get("href")
        else:
            cell0=x[i].find_all("td")[2].text
            cell01=''
        list.append([cell0,cell01])
    return(pd.DataFrame(list,columns=['paper_name','url']))


# In[140]:


def first_layer_extract(url):
    response=requests.get(url,verify=False).text
    soup=BeautifulSoup(response)
    table_soup=soup.find("table")
    new_source=table_soup.find_all("tr")[1:len(table_soup.find_all('tr'))]
    return first_table_transform(new_source)


# In[141]:


# repeat the first two columns for combine
def combine_table(first_layer,second_layer):
    table_list=[]
    for i in range(len(second_layer)):
        repeat=[]
        for j in range(len(second_layer[i][0])):
            repeat.append(first_layer.loc[i].to_list())
        table_list.append(pd.concat([pd.DataFrame(repeat),second_layer[i][0]],axis=1).rename(columns={0:'paper_name',1:'paper_url'}))
    return table_list


# # second layer extraction

# In[142]:


#define function for table 
def URL_to_second_table(y):
    url=y
    result=requests.get(url,verify=False)
    result.encoding = 'utf-8'
    response = result.text 
    soup=BeautifulSoup(response)
    table_soup=soup.find_all("table",attrs={"class":"interlaced"})
    list_dataframe=[]
    for i in range(len(table_soup)):
        if empty_or_not(table_soup[i].find_all("tr")):list_dataframe.append(empty_table())
        else:
            old_source=remove_duplicate(table_soup[i].find_all("tr"))
            list_dataframe.append(table_transform(old_source))
    return list_dataframe


# In[143]:


#define date_list function
def date_list(x):
    date_list_1=[]
    if (len(x))==1:
        date_list_1.append(x.text)
        return date_list_1
    else:
        for i in range(len(x.find_all('br'))):
            date_list_1.append(x.find_all('br')[i].previous_element)
        date_list_1.append(x.find_all('br')[-1].next_element)
        return date_list_1


# In[144]:


#define function for checking '*'
def check_for_star(x):
    for i in range(len(x)):
        if '*'in x[i]: return True


# In[145]:


#define function for create table
def table_transform(x):
    output_group=[]
    row=x
    for i in range(1,len(row)):
        if row[i].find_all("table")==[]:
            #print(row[i].find_all('td'))
            if row[i].find_all('td')[0].text!=None:
                cell0=row[i].find_all('td')[0].text
            else:
                cell0=''
            if row[i].find_all('td')[1].text!=None:
                cell1=row[i].find_all('td')[1].text
            else:
                cell1=''
            if row[i].find_all('td')[1].find('a')!=None:
                cell10=generate_tab(row[i].find_all('td')[1].find('a').get("href"))
                #cell10=row[i].find_all('td')[1].find('a').get("href")
            else:
                cell10=''
            if date_list(row[i].find_all('td')[2])!=[]:
                cell2=date_list(row[i].find_all('td')[2])
            else:
                cell2=''
            if check_for_star(date_list(row[i].find_all('td')[2])):
                cell20='* issue day'
            else:
                cell20=''
        else:
            if len(row[i].find('table').find_all("td"))!=1:
                if row[i].find_all('td')[0].text!=None:
                    cell0=row[i].find_all('td')[0].text
                else:
                    cell0=''
                if row[i].find_all('td')[3].text!=None:
                    cell1=row[i].find_all('td')[3].text
                else:
                    cell1=''
                if row[i].find_all('td')[3].find('a')!=None:
                    cell10=generate_tab(row[i].find_all('td')[3].find('a').get("href"))
                    #cell10=row[i].find_all('td')[1].find('a').get("href")
                else:
                    cell10=''
                if date_list(row[i].find_all('td')[4])!=[]:
                    cell2=date_list(row[i].find_all('td')[4])
                else:
                    cell2=''
                if check_for_star(date_list(row[i].find_all('td')[4])):
                    cell20='* issue day'
                else:
                    cell20=''
            else:
                if row[i].find_all('td')[0].text!=None:
                    cell0=row[i].find_all('td')[0].text
                else:
                    cell0=''
                if row[i].find_all('td')[1].find('a')!=None:
                    cell1=row[i].find_all('td')[1].find('a').text
                    cell10=generate_tab(row[i].find_all('td')[1].find('a').get("href"))
                else:
                    cell1=row[i].find_all('td')[1].text
                    cell10=''
                if date_list(row[i].find_all('td')[3])!=[]:
                    cell2=date_list(row[i].find_all('td')[3])
                else:
                    cell2=''
                if check_for_star(date_list(row[i].find_all('td')[3])):
                    cell20='* issue day'
                else:
                    cell20=''
        output=[cell0,cell1,cell10,cell2,cell20]
        output_group.append(output)
    return pd.DataFrame(output_group,columns=['LC_Paper_No.', 'paper','url', 'meeting_date','remarks'])


# In[146]:


def empty_or_not(x):
    if len(x)>2:
        return False
    else:
        if(x[1].find_all('td')[0].text==''and x[1].find_all('td')[1].text==''and x[1].find_all('td')[2].text==''):
            return True
        else:
            return False


# In[147]:


#define function to create empty table 
def empty_table():
    output_group=[]
    return pd.DataFrame(output_group,columns=['LC_Paper_No.', 'paper','url', 'meeting_date','remarks'])


# In[148]:


#define function for combine tab
def generate_tab(x):
    desired=''
    tab=x
    temp=''
    while(tab!=temp):
        tab=tab.replace('../','')
        temp=tab
    url_front=url.rsplit('/',1)[0]
    desired=url_front+'/'+tab
    return desired


# In[149]:


def remove_duplicate(old_sources):
    i=0
    while(i<len(old_sources)):
        if old_sources[i].find_all("table")!=[]:old_sources.pop(i+1)
        i+=1
    return (old_sources)


# # General extraction first layer

# In[150]:


#define function to extract useful script
#input soup object:table_soup
def extract(x):
    list=[]
    for i in range(1,len(x.find_all("tr"))):
        list.append(x.find_all("tr")[i].find_all("td")[0])
    return list


# In[151]:


#define function for combine tab
def generate_tab_general(x):
    desired=''
    tab=x
    temp=''
    while(tab!=temp):
        tab=tab.replace('../','')
        temp=tab
    desired='https://www.legco.gov.hk/'+tab
    return desired


# In[152]:


#transform table
#input parameter:list=extract(table_soup)
def table_transform_general(x):
    output_group=[]
    for i in range(len(x)):
        cell0=x[i].find('a').text
        if x[i].find('a').get("href")!=None:
            cell01=generate_tab_general(x[i].find('a').get("href"))
        else:cell01=''
        output=[cell0,cell01]
        output_group.append(output)
    return(pd.DataFrame(output_group,columns=['bill_name','url']))


# In[153]:


#define function
def committee_to_table_first_layer(url):
    response=requests.get(url,verify=False).text
    soup=BeautifulSoup(response)
    table_soup=soup.find("table",attrs={"class":"interlaced"})
    list=extract(table_soup)
    return(table_transform_general(list))


# # General extraction second layer

# In[154]:


#define function for combine tab
def generate_tab_second(x):
    desired=''
    tab=x
    temp=''
    while(tab!=temp):
        tab=tab.replace('../','')
        temp=tab
    desired='https://www.legco.gov.hk/'+tab
    return desired


# In[155]:


#define function 
#input example table_soup.find_all("tr")
def create_list(tr_list):
    list=[]
    for i in range(len(tr_list)):
        for j in range(len(tr_list[i].find_all("td"))):
            if tr_list[i].find_all("td")[j].find("strong")!=None and tr_list[i].find_all("td")[j].find("strong").text=='Meetings':
                list.append(tr_list[i])
                break
            if tr_list[i].find_all("td")[j].find("strong")!=None and tr_list[i].find_all("td")[j].find("strong").text=='Reports':
                list.append(tr_list[i])
                break
            if tr_list[i].find_all("td")[j].find("strong")!=None and tr_list[i].find_all("td")[j].find("strong").text=='Papers':
                list.append(tr_list[i])
                break
    return(list)


# In[156]:


#define function for meeting
#input example=new_source[0].find_all("tr")[i]
def cell_info(cell_source,url):
    cell0=cell_source.find_all("td")[0].find("em").text
    if cell_source.find_all("td")[0].find("font")!=None:
        cell01=cell_source.find_all("td")[0].find("font").text
    else:cell01=''
    if cell_source.find_all("td")[1].find('a')!=None:
        cell1=cell_source.find_all("td")[1].find('a').get("href")
    else: cell1=''
    if cell_source.find_all("td")[3].find('a')!=None:
        cell3=tab_gen(cell_source.find_all("td")[3],url)
        cell2='documents can be seen in minutes'
    else:
        cell3=''
        cell2=''
    return([cell0,cell01,cell1,cell2,cell3])


# In[157]:


#define function
#input example=new_source[0]
def meeting_table(source,url):
    list=[]
    for i in range(1,len(source.find_all("tr"))):
        list.append(cell_info(source.find_all("tr")[i],url))
    return(pd.DataFrame(list,columns=['date','remarks','agenda','attendance_list','minutes']))


# In[158]:


#define function
#input example=new_source[1]
def report_table(source):
    list=[]
    table=source.find("table")
    for i in range(len(table.find_all("tr"))):
        if (table.find_all("tr")[i].text.strip()!=''):
            cell0=table.find_all("tr")[i].find_all("td")[1].find('a').text
            cell01=generate_tab_second(table.find_all("tr")[i].find_all("td")[1].find('a').get("href"))
            cell1=table.find_all("tr")[i].find_all("td")[1].text.replace(cell0+' ','')
            list.append([cell0,cell01,cell1])
    return(pd.DataFrame(list,columns=['report_name','url','remarks']))


# In[159]:


def url_to_table_second(url):
    response=requests.get(url,verify=False).text
    soup=BeautifulSoup(response)
    table_soup=soup.find("div",attrs={"id":"_content_"}).find("table",attrs={"width":"100%"})
    tr_list=table_soup.find_all("tr")
    new_source=create_list(table_soup.find_all("tr"))
    return([meeting_table(new_source[0],url),paper_table([tab_gen(new_source[1],url)]),report_table(new_source[2])])


# In[160]:


def tab_gen(back,url):
    return(url.rsplit('/',2)[0]+'/'+back.find('a').get("href").replace('../',''))


# In[161]:


def paper_table(x):
    return pd.DataFrame(x,columns=['paper_url'])


# # final extraction

# In[162]:


def combine_table_general_cat(y,x):
    final_table=pd.DataFrame()
    for i in range(len(x)):
        list=[]
        for j in range(len(x[i])):
            list.append(y.loc[i].to_list())
        temp=pd.concat([pd.DataFrame(list,columns=('committee_name','committee_url')),x[i]],axis=1)
        final_table=pd.concat([final_table,temp],axis=0) 
    return(final_table)


# In[163]:


def combine_table_paper_section(y,x):
    final_table=pd.DataFrame()
    for i in range(len(x)):
        list=[]
        for j in range(len(x[i])):
            list.append(y.loc[i].to_list())
        temp=pd.concat([pd.DataFrame(list,columns=('index','committee_name','committee_url','paper_url')),x[i]],axis=1)
        final_table=pd.concat([final_table,temp],axis=0) 
    return(final_table)


# In[164]:


def combine_table_paper_2(y,x):
    paper_tables=pd.DataFrame()
    for i in range(len(y)):
        list=[]
        for j in range(len(x[i])):
            list.append(y.loc[i][1:4].to_list())
        table=pd.DataFrame(list)
        x[i].reset_index(drop=True, inplace=True)
        table.reset_index(drop=True, inplace=True)
        paper_tables=pd.concat([paper_tables,pd.concat([table,x[i]],axis=1,ignore_index=True)],axis=0)
    return (paper_tables)


# In[165]:


def tab_to_table(y):
    url=y
    table_01=committee_to_table_first_layer(url)
    meeting_list=[]
    paper_list=[]
    report_list=[]
    for i in range(len(committee_to_table_first_layer(url)['url'])):
        url_1=committee_to_table_first_layer(url)['url'][i]
        meeting_list.append(url_to_table_second(url_1)[0])
        paper_list.append(url_to_table_second(url_1)[1])
        report_list.append(url_to_table_second(url_1)[2])
    meeting_table=combine_table_general_cat(table_01,meeting_list)
    paper_table=combine_table_general_cat(table_01,paper_list)
    report_table=combine_table_general_cat(table_01,report_list)
    paper_table=paper_table.reset_index()
    paper_list_2=[]
    for i in range(len(paper_table['paper_url'])):
        print(i)
        url_2=paper_table['paper_url'][i]
        url=url_2
        paper_list_2.append(url_subcom_table_paper(url))
    paper_final_table=combine_table_paper_2(paper_table,paper_list_2)
    paper_final_table.rename(columns={0:'committee_name',1:'committee_url',2:'committee_paper_url',3:'paper_category',4:'paper_category_url',5:'LC_paper_no',6:'paper_name',7:'paper_url',8:'date',9:'remarks'},inplace=True)
    return(meeting_table,paper_final_table,report_table)


# # last section trial

# In[ ]:


"""
I tried to use the function above to run, but for some reason I cannot do it, 
there are always bugs when I run the function, but when i take the whole thing out and run it
it works smoothly, I think there is sth to do with local variables and global variables
but Im not sure how I can tackle the problem cuz there r too many functions inside another functions
can u please take a look and help me with it
"""
"""
links that u can try to throw them in for trial
'https://www.legco.gov.hk/yr16-17/english/bc/bc1617.htm'
'https://www.legco.gov.hk/yr17-18/english/bc/bc1617.htm'
'https://www.legco.gov.hk/yr18-19/english/bc/bc1617.htm'
'https://www.legco.gov.hk/yr19-20/english/bc/bc1617.htm'
"""


# In[167]:


y='https://www.legco.gov.hk/yr19-20/english/bc/bc1920.htm'
result=tab_to_table(y)


# In[168]:


y='https://www.legco.gov.hk/yr19-20/english/bc/bc1920.htm'
url=y
table_01=committee_to_table_first_layer(url)
meeting_list=[]
paper_list=[]
report_list=[]
for i in range(len(committee_to_table_first_layer(url)['url'])):
    print(i)
    url_1=committee_to_table_first_layer(url)['url'][i]
    meeting_list.append(url_to_table_second(url_1)[0])
    paper_list.append(url_to_table_second(url_1)[1])
    report_list.append(url_to_table_second(url_1)[2])
meeting_table=combine_table_general_cat(table_01,meeting_list)
paper_table=combine_table_general_cat(table_01,paper_list)
report_table=combine_table_general_cat(table_01,report_list)
paper_table=paper_table.reset_index()
paper_list_2=[]
for i in range(len(paper_table['paper_url'])):
    print(i)
    url_2=paper_table['paper_url'][i]
    url=url_2
    paper_list_2.append(url_subcom_table_paper(url))
paper_final_table=combine_table_paper_2(paper_table,paper_list_2)
paper_final_table.rename(columns={0:'committee_name',1:'committee_url',2:'committee_paper_url',3:'paper_category',4:'paper_category_url',5:'LC_paper_no',6:'paper_name',7:'paper_url',8:'date',9:'remarks'},inplace=True)


# In[169]:


paper_final_table


# In[388]:


#this can be ignored, already put one in the above
def table_transform(x):
    output_group=[]
    row=x
    for i in range(1,len(row)):
        print(i)
        if row[i].find_all("table")==[]:
            #print(row[i].find_all('td'))
            if row[i].find_all('td')[0].text!=None:
                cell0=row[i].find_all('td')[0].text
            else:
                cell0=''
            if row[i].find_all('td')[1].text!=None:
                cell1=row[i].find_all('td')[1].text
            else:
                cell1=''
            if row[i].find_all('td')[1].find('a')!=None:
                cell10=generate_tab(row[i].find_all('td')[1].find('a').get("href"))
                #cell10=row[i].find_all('td')[1].find('a').get("href")
            else:
                cell10=''
            if date_list(row[i].find_all('td')[2])!=[]:
                cell2=date_list(row[i].find_all('td')[2])
            else:
                cell2=''
            if check_for_star(date_list(row[i].find_all('td')[2])):
                cell20='* issue day'
            else:
                cell20=''
        else:
            if len(row[i].find('table').find_all("td"))!=1:
                if row[i].find_all('td')[0].text!=None:
                    cell0=row[i].find_all('td')[0].text
                else:
                    cell0=''
                if row[i].find_all('td')[3].text!=None:
                    cell1=row[i].find_all('td')[3].text
                else:
                    cell1=''
                if row[i].find_all('td')[3].find('a')!=None:
                    cell10=generate_tab(row[i].find_all('td')[3].find('a').get("href"))
                    #cell10=row[i].find_all('td')[1].find('a').get("href")
                else:
                    cell10=''
                if date_list(row[i].find_all('td')[4])!=[]:
                    cell2=date_list(row[i].find_all('td')[4])
                else:
                    cell2=''
                if check_for_star(date_list(row[i].find_all('td')[4])):
                    cell20='* issue day'
                else:
                    cell20=''
            else:
                if row[i].find_all('td')[0].text!=None:
                    cell0=row[i].find_all('td')[0].text
                else:
                    cell0=''
                if row[i].find_all('td')[1].find('a')!=None:
                    cell1=row[i].find_all('td')[1].find('a').text
                    cell10=generate_tab(row[i].find_all('td')[1].find('a').get("href"))
                else:
                    cell1=row[i].find_all('td')[1].text
                    cell10=''
                if date_list(row[i].find_all('td')[3])!=[]:
                    cell2=date_list(row[i].find_all('td')[3])
                else:
                    cell2=''
                if check_for_star(date_list(row[i].find_all('td')[3])):
                    cell20='* issue day'
                else:
                    cell20=''
        output=[cell0,cell1,cell10,cell2,cell20]
        output_group.append(output)
    return pd.DataFrame(output_group,columns=['LC_Paper_No.', 'paper','url', 'meeting_date','remarks'])


# In[ ]:





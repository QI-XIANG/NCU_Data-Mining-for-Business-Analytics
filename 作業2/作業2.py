#!/usr/bin/env python
# coding: utf-8

# # 1. 匯入資料
# 這邊有先把 .xlsx 的檔案先換成 .csv 的格式會比較好處理
# 
# ps. 要用 big5 編碼不然中文字會是亂碼喔~

# In[1]:


import pandas as pd
with open("retaildata.csv", encoding="big5", errors='ignore') as f:
    df = pd.read_csv(f)


# 匯入的資料如下 : 

# In[2]:



df


# # 2. 統計數據

# 總共有 15877 種不同的商品

# In[3]:


len(df.productName.astype('string').unique())


# 總共有 377485 筆交易

# In[4]:


len(df.uniqueOrderID.unique())


# 同商品在不同時間的價格不一樣

# In[5]:


df[df['productName']=='6-LC登.U2NET112H+HUB']


# # 3. 合併不同列但屬於同一筆交易的資料

# 初始資料將同筆交易的不同商品拆分成不同列的資料，在做購物籃分析之前，我們需要先將每個購物籃的商品整合在一起

# In[6]:


df_merge = df.groupby(['uniqueOrderID']).agg(lambda x: x.tolist())


# 按照不同的交易編號合併後 : (有點醜XD)

# In[7]:


df_merge = df_merge.drop(['salesdate','Unnamed: 12','Unnamed: 13'],axis=1) #有2個 salesdate 刪掉其中一個


# In[8]:


df_merge


# 顯示前五筆交易買了什麼 : 

# In[9]:


df_merge["productName"][0:5]


# 我們前面合併完同筆資料的不同商品後，接著將這些不同的購物籃放到一個 list 形成2維的 list

# In[10]:


carts = []
for j in df_merge["productName"]:
    arr = []
    for i in j:
        arr.append(''.join(i))
    carts.append(arr)


# 形成的二維 list 如下 : 

# In[11]:


carts


# # 4. 購物籃分析

# 這邊借助 apriori 演算法幫我們找出不同商品之間的關聯性
# 
# 但 apriori 不適合用在處理過大資料，因為運算效率不好 XD
# 
# min support 怎麼來的? 這邊我是隨便先設 0.0005 ，意思是總共在 377485 個購物車內，同樣的商品出現在 188 個購物車內
# 
# min confidence 怎麼來的? 先隨便設，在從跑出的結果選一個比較是當的數值
# 
# (ps. 這邊不考慮"是否是金賺會員"、"是否是公司單位訂購"、"是否是實體消費"，不然其實還可以做更細部的分析，鎖定更特定的客群~)

# In[12]:


## Import package
from apyori import apriori
## Data 自行定義數據
association_rules = apriori(carts, min_support=0.0005, min_confidence=0.7)
association_results = list(association_rules)


# 顯示所有符合要求的關聯規則 (25條規則)

# In[13]:


for product in association_results:
    print('Shopping Cart: '+str(list(product[0]))) # ex. ['Basketball', 'Socks']
    print("Rule: " + str(''.join(list(product[2][0][0]))) + " → " + str(', '.join(list(product[2][0][1]))))
    print("Support: " + str(product[1]))
    print("Confidence: " + str(product[2][0][2]))
    print("Lift: " + str(product[2][0][3]))
    print("==================================")


# # 5. 哪一條規則可以帶來最可觀的收益?

# 先把找出的 25 條規則包含的商品放到 list 裡

# In[14]:


distinct_products = [] #只放不重複的
for product in association_results:
    for item in list(product[0]):
        if(item not in distinct_products):
            distinct_products.append(item)
distinct_products


# 可是商品價格不一樣... 先取價格平均值

# In[15]:


products_mean_price = {}
for i in distinct_products:
    products_mean_price[i] = round(df.groupby("productName").get_group(i)['unitSalesPrice'].mean())
products_mean_price


# 計算每條規則的收益期望值

# In[16]:


cart_under_rule = {}
for product in association_results:
    sum = 0
    for item in list(product[0]):
        sum += products_mean_price[item]
    sum = sum*product[1]
    cart_under_rule[str(''.join(list(product[2][0][0]))) + " → " + str(', '.join(list(product[2][0][1])))] = sum

cart_under_rule


# 規則的收益期望值視覺化

# In[17]:


# import matplotlib相關套件
import matplotlib.pyplot as plt

# 規則的順序
n = [x for x in range(25)]

expected_value = list(cart_under_rule.values())

# 設定圖片大小為長15、寬10
plt.figure(figsize=(18,10),dpi=300,linewidth = 2)

# 把資料放進來並指定對應的X軸、Y軸的資料，用方形做標記(s-)，並指定線條顏色為紅色，使用label標記線條含意
plt.plot(n,expected_value,'s-',color = 'skyblue', label="Expected Income of Different Rules")

# 設定刻度字體
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

# 標點
for x,y in zip(n,expected_value):
    plt.text(x,y,"{:.3f}".format(y),verticalalignment='bottom',fontsize=10)

# 設定圖的標題
plt.title("Association Rules Expected Income",fontsize=32)

# 標示x軸(labelpad代表與圖片的距離)
plt.xlabel("Order of Rules", fontsize=30, labelpad = 15)

# 標示y軸(labelpad代表與圖片的距離)
plt.ylabel("Expected Imcome", fontsize=30, labelpad = 20)

# 顯示出線條標記位置
plt.legend(loc = "best", fontsize=20)

# 畫出圖片
plt.show()


# 將規則按照收益多寡由大到小排序

# In[18]:


{k: v for k, v in sorted(cart_under_rule.items(), key=lambda item: item[1],reverse=True)}


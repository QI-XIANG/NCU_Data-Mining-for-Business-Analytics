#!/usr/bin/env python
# coding: utf-8

# ## 0. 背景知識
# 
# 每一種作物或同種作物的不同品系間對養分的需求可能不同。
# 
# 而氮、磷和鉀之所稱為肥料三要素，主要是因它們都是每一種作物生長中需要量較多的三種要素，其個別的功能，可簡單地描述如下：
# 
# ---
# 
# * 氮肥(俗稱葉肥)：
#     * 長葉子及製造葉綠素，供光合作用產生碳水化合物，因此可增進作物的產量。
#     * 適用在長葉子的生長期和以葉部為食用(如蔬菜)或觀賞(如草皮，觀葉植物)為主的作物。
#     * pH值為7~8的偏鹼性土壤，應注意深施氮肥，防止其揮發造成損失。
#     * 高雨水，應降低氮肥供應。
# 
# ---
# 
# * 磷肥(俗稱花肥及果肥)：
#     * 主要的功能在能量的製造和運移，對開花及結果影響很大。
#     * 適用在開花時期或以觀花為主的花卉。
#     * 磷的有效性容易受土壤酸鹼度的影響，當pH值為6~7.5時，其有效性較高。
#     * 土壤溫度低時，作物吸收率大減，應提升磷肥供應。
# 
# ---
# 
# * 鉀肥(俗稱果肥及莖幹肥)：
#     * 維持細胞內電解質平衡與細胞膨壓，為蛋白質合成及五十多種酵素催化作用所必需。
#     * 適用在結果的時期以及以果實收成為主的作物，
#     * 具有使莖幹強健，增進作物抗病、抗蟲及抗環境逆境(如霜害、旱害、風害……等)的功能。
#     * pH為6以下的偏酸性土壤，鉀元素容易被氫離子置換而隨水流失，應注意補充。
#     * 降雨浸水時根的吸收率低，應提升鉀肥供應。
# 
# ---
# 
# 參考資料：
# 
# * [因應氣候條件之施肥管理](https://www.mdais.gov.tw/files/mdais/web_structure/5921/A01_1.pdf)
# * [農業知識入口網 何謂氮磷鉀肥?](https://kmweb.coa.gov.tw/knowledge_view.php?id=7995) 
# * [中國農業科學院植物保護研究所](https://ipp.caas.cn/kpzs/129028.htm)

# ## 1. 讀入資料 

# In[1]:


import pandas as pd
df = pd.read_csv("Crop.csv")
df


# ## 2. 各類作物的資料統計

# ### 2.1 資料筆數
# 
# * 蘋果 (apple)          
# * 香蕉 (banana)         
# * 黑吉豆 (blackgram，黑綠豆)
# * 鷹嘴豆 (chickpea)
# * 咖啡 (coffee)
# * 椰子 (coconut)     
# * 棉花 (cotton)         
# * 葡萄 (grapes)         
# * 黃麻 (jute)           
# * 腰豆 (kidneybeans)
# * 扁豆 (lentil)         
# * 玉米 (maize)          
# * 芒果 (mango)          
# * 蛾豆 (mothbeans)      
# * 綠豆 (mungbean)
# * 香瓜 (muskmelon)      
# * 橘子 (orange)         
# * 木瓜 (papaya)         
# * 木豆 (pigeonpeas)
# * 石榴 (pomegranate)    
# * 米 (rice)           
# * 西瓜 (watermelon)     
# 
# 共有 22 種作物，每種都是 100 筆

# In[2]:


df.groupby(['label']).size()


# ### 2.2 欄位屬性間相關係數

# In[3]:


df.corr()


# ## 3. 從作物土壤的氮、磷、鉀含量著手進行分析 

# ### 3.1 計算每種作物的平均土壤氮、磷、鉀含量 (存成 dict)

# In[4]:


npk = {}
for i in df.groupby(['label']):
    N = df.groupby(['label']).get_group(i[0])['N'].sum()/100
    P = df.groupby(['label']).get_group(i[0])['P'].sum()/100
    K = df.groupby(['label']).get_group(i[0])['K'].sum()/100
    npk[i[0]] = {}
    npk[i[0]]['N'] = N
    npk[i[0]]['P'] = P
    npk[i[0]]['K'] = K
npk


# ### 3.2 轉換成 DataFrame

# In[5]:


df_npk = pd.DataFrame(npk)
df_npk


# ### 3.3 將作物分成3群 (豆類、水果、其他)
# 
# * 豆類: blackgram、chickpea、coffee、kidneybeans、lentil、mothbeans、mungbean、pigeonpeas
# * 水果: apple、banana、mango、watermelon、grapes、orange、papaya、coconut、muskmelon、pomegranate
# * 其他: cotton、jute、maize、rice

# **3.3.1 豆類**
# 
# 可以看出粗略分出的多數豆類對於 P 有較大的需求
# 
# ![](https://i.imgur.com/gAjeGWN.png)

# In[6]:


beans = ["blackgram","chickpea","coffee","kidneybeans","lentil","mothbeans","mungbean","pigeonpeas"]
df_npk[beans]


# 不同豆類的降雨量差異

# In[7]:


import matplotlib.pyplot as plt

x = [e for e in range(1,2201,1)]
plt.figure(figsize=(12,8))
for i in beans:
    y = df[df['label'] == i]['rainfall']
    x = [e for e in range(1,101,1)]
    plt.plot(x,y)

plt.xticks([e for e in range(0,101,5)]) 
plt.yticks([e for e in range(25,220,20)]) 
plt.xlabel("Order of Data")
plt.ylabel("Rain Fall")
plt.legend(beans,loc='best')
plt.show()


# **3.3.2 水果類**
# 
# 可以看出粗略分出的各半數水果分別對於 N、P 有較大的需求
# 
# ![](https://i.imgur.com/9oKeSEy.png)

# In[8]:


fruits = ["apple","banana","mango","watermelon","grapes","orange","papaya","coconut","muskmelon","pomegranate"]
df_npk[fruits]


# 不同水果的降雨量差異

# In[9]:


import matplotlib.pyplot as plt

plt.figure(figsize=(12,8))
for i in fruits:
    y = df[df['label'] == i]['rainfall']
    x = [e for e in range(1,101,1)]
    plt.plot(x,y)

plt.xticks([e for e in range(0,101,5)]) 
plt.yticks([e for e in range(45,265,20)]) 
plt.xlabel("Order of Data")
plt.ylabel("Rain Fall")
plt.legend(fruits,loc='best')
plt.show()


# **3.3.3 其他類**
# 
# 可以看出粗略分出的其他類都對於 N 有較大的需求
# 
# ![](https://i.imgur.com/rU8uHAd.png)

# In[10]:


others = ["cotton","jute","maize","rice"]
df_npk[others]


# 其他類的降雨量差異

# In[11]:


import matplotlib.pyplot as plt

plt.figure(figsize=(12,8))
for i in others:
    y = df[df['label'] == i]['rainfall']
    x = [e for e in range(1,101,1)]
    plt.plot(x,y)

plt.xticks([e for e in range(0,101,5)]) 
plt.yticks([e for e in range(45,320,20)]) 
plt.xlabel("Order of Data")
plt.ylabel("Rain Fall")
plt.legend(others,loc='best')
plt.show()


# ## 4. 特例研究

# 從剛剛各群的降雨量圖表中，挑出比較奇怪的例子
# 
# * 水果類: papaya (木瓜)
# * 豆類: pigeonpeas (木豆)

# ### 4.1 木瓜
# 
# 從降雨量圖表中，可以看出木瓜的降雨量橫跨 45-245 上下躍動幅度非常大，因此試著觀察這與土壤的 N、P、K 是否有關。
# 而從查到的資料可以得知鉀(K)肥具有使莖幹強健，增進作物抗病、抗蟲及抗環境逆境(如霜害、旱害、風害……等)
# 的功能，所以先懷疑木瓜的降雨量上下幅度大與 K 有關。

# In[12]:


# split window
#f, ax = plt.subplots(2,1,sharex='col',sharey='row',figsize=(15,15))
#left #right

x = [e for e in range(1,101,1)]
y1 = df[df['label'] == 'papaya']['rainfall']
y2 = df[df['label'] == 'papaya']['K']

fig = plt.figure(figsize=(20,8))

ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.set_title('Comparison between K and Rainfall - Papaya',fontsize=18)
ax_twinx = ax.twinx()
lns1 = ax.plot(x, y1, c='r',label='Rainfall')
lns2 = ax_twinx.plot(x, y2, c='g',label='K')
ax.locator_params(nbins=10, axis='y')
ax_twinx.locator_params(nbins=20, axis='y')
ax.set_ylabel("Rainfall",fontsize=14)
ax.set_ylabel("Rainfall",fontsize=14)
ax.set_xlabel("Order of Data",fontsize=14)
ax_twinx.set_ylabel("Content of K",fontsize=14)
ax.locator_params(nbins=20, axis='x')
# added these three lines
lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc='best')
plt.show()


# 木瓜的欄位相關係數 (if 常態分布且線性)

# In[13]:


df[df['label']=='papaya'].corr()


# 木瓜的欄位相關係數 (if 非常態分布且非線性)

# In[14]:


df[df['label']=='papaya'].corr('spearman')


# ### 4.2 木豆
# 
# 從降雨量圖表中，可以看出木瓜的降雨量橫跨 85-205 上下躍動幅度偏大，因此試著觀察這與土壤的 N、P、K 是否有關。
# 而從查到的資料可以得知鉀(K)肥具有使莖幹強健，增進作物抗病、抗蟲及抗環境逆境(如霜害、旱害、風害……等)
# 的功能，所以先懷疑木豆的降雨量上下幅度大與 K 有關。

# In[15]:


# split window
#f, ax = plt.subplots(2,1,sharex='col',sharey='row',figsize=(15,15))
#left #right

x = [e for e in range(1,101,1)]
y1 = df[df['label'] == 'pigeonpeas']['rainfall']
y2 = df[df['label'] == 'pigeonpeas']['K']

fig = plt.figure(figsize=(20,8))

ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.set_title('Comparison between K and Rainfall - Pigeonpeas',fontsize=18)
ax_twinx = ax.twinx()
lns1 = ax.plot(x, y1, c='r',label='Rainfall')
lns2 = ax_twinx.plot(x, y2, c='g',label='K')
ax.locator_params(nbins=10, axis='y')
ax_twinx.locator_params(nbins=20, axis='y')
ax.set_ylabel("Rainfall",fontsize=14)
ax.set_ylabel("Rainfall",fontsize=14)
ax.set_xlabel("Order of Data",fontsize=14)
ax_twinx.set_ylabel("Content of K",fontsize=14)
ax.locator_params(nbins=20, axis='x')
# added these three lines
lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc='best')
plt.show()


# 木豆的欄位相關係數 (if 常態分布且線性)

# In[16]:


df[df['label']=='pigeonpeas'].corr()


# 木豆的欄位相關係數 (if 非常態分布且非線性)

# In[17]:


df[df['label']=='pigeonpeas'].corr('spearman')


#!/usr/bin/env python
# coding: utf-8

# # 1. 讀入資料

# In[1]:


import pandas as pd
df = pd.read_csv("2012-18_NBA_officialBoxScore.csv")
df


# # 2. 檢查資料缺失值
# ## 共有119欄、沒有欄位存在缺失值

# In[2]:


df.info()


# In[26]:


num = df.isna().sum()
num


# In[25]:


count = 0
for i in num:
    if i == 0:
        count+=1
count


# In[5]:


df


# # 3. 在主場打比較容易贏? 
# ## 根據統計數據，可以發現在主場打贏的場次確實比較多

# In[6]:


df_stat = df[["teamAbbr","teamLoc","teamRslt"]]
df_stat.groupby(["teamLoc","teamRslt"]).size()


# ## 3.1 以湖人隊為例
# ### 在主場的勝場數確實也大於客場 主:107 (42.2764%) 客:67 (27.2358%)

# In[7]:


df_LAL = df[df["teamAbbr"]=="LAL"]
df_LAL


# ## 3.2 詳細的主客場勝負場數 (湖人隊)

# In[30]:


print(df_LAL.groupby(["teamLoc","teamRslt"]).size())
section = df_LAL.groupby(["teamLoc"])


# ## 3.3 主客場勝率 (湖人隊)

# In[31]:


Away = pd.DataFrame(section.get_group("Away")["teamRslt"])
Home = pd.DataFrame(section.get_group("Home")["teamRslt"])
def countWinRate(teamLoc):
    Loss = len(teamLoc[teamLoc["teamRslt"] == "Loss"])
    Win = len(teamLoc[teamLoc["teamRslt"] == "Win"])  
    df = pd.DataFrame({"Win":Win,"Loss":Loss,"Win Rate":(Win/(Loss+Win))},index=[0])

    return df

print("Win Rate at Away")
print(countWinRate(Away))
print('='*25)
print("Win Rate at Home")
print(countWinRate(Home))


# ## 3.4 總勝敗場數 (湖人隊)

# In[ ]:


# 湖人隊的勝敗數
df_LAL.groupby(["teamRslt"]).size()


# # 4. 利用主成分分析(PCA)，挑出前20個屬性恰可獲得對99%變異數貢獻最大的特徵
# 
# 主成分分析經常用於減少數據集的維數，同時保留數據集當中對變異數貢獻最大的特徵。這是通過保留低維主成分，忽略高維主成分做到的。這樣低維成分往往能夠保留住數據的最重要部分。但是，這也不是一定的，要視具體應用而定。由於主成分分析依賴所給數據，所以數據的準確性對分析結果影響很大。

# In[12]:


from sklearn.decomposition import PCA
import numpy as np

dx = df.drop(['gmDate','gmTime','offLNm','offFNm','teamAbbr','teamConf','teamDiv','opptConf','opptDiv','opptLoc',
                'opptRslt','teamRslt','opptAbbr','teamPTS1','teamPTS2','teamPTS3','teamPTS4','teamPTS5','teamPTS6','teamPTS7','teamPTS8',
                'opptPTS1','opptPTS2','opptPTS3','opptPTS4','opptPTS5','opptPTS6','opptPTS7','opptPTS8'],axis=1)

def changeTeamLoc(df):
    if df == 'Home':
        return 0
    if df == 'Away':
        return 1
dxx = dx
dx['teamLoc'] = dx['teamLoc'].apply(changeTeamLoc)
dn = dx.to_numpy()
# 取出特徵名稱
features_names = dx.columns
pca = PCA().fit(dn)
# 依變異解釋能力找出對應特徵
indexes = np.argmax(np.abs(pca.components_), axis=1)
var_ratio = pca.explained_variance_ratio_ * 100
for i, idx in enumerate(indexes):
    print(f'PC{i+1} ({var_ratio[i]:.5f} %) ' +           f'feature {idx} ({features_names[idx]})')


# In[ ]:


count = 0
for i in range(20):
    count += var_ratio[i]

print(count)


# # 5. 利用 LogisticRegression 預測比賽的勝利與否 (放入PCA找出的欄位做預測)

# ## 5.1 模型預測 (Accuracy、Recall、Precision、F1 score)

# In[13]:


from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix
import numpy as np

def changeTeamRslt(teamRslt):
    if teamRslt == "Win":
        return 1
    if teamRslt == "Loss":
        return 0

dy = df["teamRslt"].apply(changeTeamRslt)
dx = PCA(n_components=20).fit_transform(dx)
dx = StandardScaler().fit_transform(dx)
dx_train, dx_test, dy_train, dy_test =           train_test_split(dx, dy, test_size=0.2, random_state=0)
model = LogisticRegression()
model.fit(dx_train, dy_train)
predict = model.predict(dx_test)
accuracy = accuracy_score(dy_test, predict)
precision = precision_score(dy_test, predict,pos_label=1)
recall = recall_score(dy_test, predict,pos_label=1)
f1_score = f1_score(dy_test, predict,pos_label=1)
summary = pd.DataFrame({'Accuracy':accuracy,'Precision':precision,'Recall':recall,'f1_score':f1_score},index=['LogisticRegression']) 
summary


# ## 5.2 Confusion Matrix 混淆矩陣 (Logistic Regression)

# In[ ]:


confusion_matrix(dy_test,predict)


# ## 5.3 預測結果的 ROC Curve (Logistic Regression) 
# ### 預測準確率過高可能是Overfitting導致

# In[32]:


from sklearn.metrics import roc_curve

def plot_roc_curve(fper, tper):
    plt.plot(fper, tper, color='red', label='ROC')
    plt.plot([0, 1], [0, 1], color='green', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('NBA Game Prediction ROC Curve')
    plt.legend()
    plt.show()
    

fper, tper, thresholds = roc_curve(dy_test,predict)
plot_roc_curve(fper, tper)


# # 6. 利用 SVM 預測比賽的勝利與否 (放入PCA找出的欄位做預測)

# ## 6.1 Confusion Matrix 混淆矩陣、預測結果報告 (SVM)

# In[34]:


#dx_train, dx_test, dy_train, dy_tes
#載入Support Vector Classifier套件
from sklearn.svm import SVC
model = SVC(kernel='sigmoid',C=1,gamma='auto')
#使用Support Vector Classifier來建立模型
model.fit(dx_train,dy_train)
#利用測試組資料來測試模型結果
predictions = model.predict(dx_test)
#載入classification report & confusion matrix
from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(dy_test,predictions))
print('\n')
print(classification_report(dy_test,predictions))


# ## 6.2 ROC Curve (SVM)

# In[35]:


from sklearn.metrics import roc_curve
from matplotlib import pyplot as plt
def plot_roc_curve(fper, tper):
    plt.plot(fper, tper, color='red', label='ROC')
    plt.plot([0, 1], [0, 1], color='green', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('NBA Game Prediction ROC Curve')
    plt.legend()
    plt.show()
    

fper, tper, thresholds = roc_curve(dy_test,predictions)
plot_roc_curve(fper, tper)


# # 7. 利用 Decision Tree 預測比賽的勝利與否 (放入PCA找出的欄位做預測)

# ## 7.1 預測結果報告

# In[41]:


#dx_train, dx_test, dy_train, dy_tes
from sklearn import tree
clf = tree.DecisionTreeClassifier(max_depth=4)
clf = clf.fit(dx_train, dy_train)
predict = clf.predict(dx_test)
print(classification_report(dy_test,predict))


# ## 7.2 ROC Curve

# In[42]:


from sklearn.metrics import roc_curve
from matplotlib import pyplot as plt
def plot_roc_curve(fper, tper):
    plt.plot(fper, tper, color='red', label='ROC')
    plt.plot([0, 1], [0, 1], color='green', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('NBA Win Game Prediction ROC Curve')
    plt.legend()
    plt.show()
    

fper, tper, thresholds = roc_curve(dy_test,predict)
plot_roc_curve(fper, tper)


# ## 7.3 將決策樹視覺化後存成圖檔

# In[45]:


plt.figure(figsize=(25, 20),dpi=200)
tree.plot_tree(clf,filled=True)  
plt.savefig('tree.png')


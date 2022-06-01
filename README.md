# NCU Data Mining for Business Analytics

![](https://badgen.net/github/watchers/QI-XIANG/NCU_Data-Mining-for-Business-Analytics) ![](https://badgen.net/github/commits/QI-XIANG/NCU_Data-Mining-for-Business-Analytics) ![](https://badgen.net/github/last-commit/QI-XIANG/NCU_Data-Mining-for-Business-Analytics) ![](https://badgen.net/github/license/QI-XIANG/NCU_Data-Mining-for-Business-Analytics)

| 課程名稱: | 課程時間 | 授課教授 |
| -------- | -------- | -------- |
| 商業分析資料探勘     | 2022年2~6月     | 陳炫碩教授     |

(ps. 作業均沒有指定題目，可自行發揮創意~)

### 作業 1

* 原始資料:
    * NBA 2012-2018 的球賽數據 
* 研究內容:
    * 主/客場勝率差異
    * PCA 主成分分析 (特徵篩選)
    * 利用 LogisticRegression 預測比賽的勝利與否
    * 利用 SVM 預測比賽的勝利與否
    * 利用 Decision Tree 預測比賽的勝利與否
* 問題點:
    * 未合併相同比賽但不同隊伍的數據
    * 利用事後數據預測勝利與否
* 改善點: 
    *  合併相同比賽但不同隊伍的數據
    *  找出影響比分差距擴大的屬性
    *  比較賽季優勢等...

![](https://i.imgur.com/7HzzfDy.png)

---

### 作業 2

* 原始資料:
    * 零售商消費數據 
* 研究內容:
    * 統計相異商品數量、交易筆數
    * 不同時間的同商品價格不同
    * 利用 Apriori 演算法做購物籃分析
    * 找出哪個關聯規則可讓收益最大化
* 問題點:
    * 計算收益時，未考慮實際上的商品進出數量
* 改善點: 
    *  修正關聯規則收益計算
    *  剔除僅有一次消費紀錄的顧客
    *  可考慮實作 RFM 分析...

![](https://i.imgur.com/MEa5EFC.png)

---

### 作業 3

* 原始資料:
    * 作物種植數據
* 研究內容:
    * 統計相異作物種類數量、各種類資料筆數
    * 計算資料屬性相關係數
    * 從作物土壤的氮、磷、鉀含量著手進行分析
    * 不同作物的降雨量差異
    * 探討作物種植環境降雨量範圍大與 K 有關
* 問題點:
    * 未做更詳細的數據說明
* 改善點: 
    *  利用 N、P、K 分群
    *  分出相似種植環境特性的作物群
    *  可考慮實作 NN 神經網路

![](https://i.imgur.com/Hr8WPEn.png)
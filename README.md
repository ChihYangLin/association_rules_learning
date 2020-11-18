# 關聯規則
#### 關聯規則學習是一種基於規則的機器學習方法，它主要是使用一些度量，來挖掘資料庫中有趣的強規則。
#### 這邊是使用Python的Apriori演算法，目的在找出顧客交易資料裡面，關聯性較高的商品，以作為後續的商業策略依據。

## 實作步驟
* 1. 整理資料：把每筆交易放進一個LIST，再把每個交易LIST放進一個大LIST裡，形成一個 double list。
  * 例如：[[香蕉, 蘋果], [鳳梨, 香蕉, 芭樂], ...]
* 2. 使用Apriori演算法並調整參數：降低運算量並篩選更有效的規則(資料, 最小支持度, 最小信賴度, 最小提升度, 規則最大產品數)。

  * data (資料)：整理後的 double list
  * min_support(最小支持度)：商品組合(A, B)出現在交易紀錄裡的機率。
  * min_confidence(最小信賴度)：買商品A的條件下，購買商品B的機率。
  * min_min_lift(最小提升度)：(A -> B 的條件機率) / 商品B的購買率
  * max_length(最大商品數量)：規則裡商品數的最大值，設為2只會是 (A -> B)，設為3則可能是 (A,B -> C), (A -> B)或(C -> A,B)

```
association_rules = apriori(data=record, min_support=0.03, min_confidence = 0.6, min_lift=4, max_length = 2)
```
* 3. 用pandas套件整理成可應用的表格









## Q1

第6回のSQL結果では、

```text
1行 = 1配送会社
```

になっています。

ここで、

```python
df["delivery_count"].sum()
```

を実行すると、何を意味する値になりますか？

> 全配送件数（＝元のdelivery_recordsの件数）

---

## Q2

A運輸について、

```text
delivery_count = 4
```

全配送件数が、

```text
11
```

だった場合、

```text
delivery_share
```

はいくつになるでしょうか？

計算式も書いてください。

> 4 / 11 = 0.3636...

---

## Q3

今回、

```text
delivery_share
```

をSQLではなくpandasで計算します。

第6回Q10で整理した、

```text
SQL
→ 基本集計

pandas
→ KPI計算・比較・分析
```

という役割分担から、今回pandas側で計算する理由を自分なりに説明してください。

> SQL集計結果からpandasで全配送件数を計算し、その値を使ってdelivery_shareを求めるから。

---

## Q4

D運送の、

```text
total_freight
```

は `NaN` でした。

では、

```python
df["total_freight"].sum()
```

を実行したとき、

> D運送のNaNがあるため、全体もNaNになる

と予想しますか？

それとも、

> NaNを除外して、値が存在する配送会社だけで合計される

と予想しますか？

実装前なので、予想で構いません。

> 値が存在する配送会社だけで合計される

---

## Q5

最終的なDataFrameは何行になりましたか？

なぜその行数なのか、

```text
1行の意味
```

から説明してください。

> 4件　1行＝配送会社ごとの集計結果に運賃合計とshareを追加したものなので、列追加後も件数は変わらなかった。

---

## Q6

A運輸の、

```text
delivery_share
```

はいくつになりましたか？

計算式と実際の結果を確認してください。

> 0.36363
> df["delivery_share"] = df["delivery_count"] / delivery_count_of_all
> 4 / 11

---

## Q7

次を確認してください。

```python
df["delivery_share"].sum()
```

理論上、いくつになるはずでしょうか？

実際の結果も確認してください。

> 1.0

---

## Q8

次を確認してください。

```python
df["freight_share"].sum()
```

結果はいくつになりましたか？

D運送の `total_freight = NaN` が、この計算にどう影響したのかも説明してください。

> 1.0 NaNは除外されて計算された模様。

---

## Q9

今回、

```text
total_freight
```

と、

```text
freight_share
```

では「値の意味」が違います。

それぞれ、

```text
total_freight
freight_share
```

が何を表しているのか説明してください。

> total_freight：配送会社ごとの運賃の合計
> freight_share：各配送会社の運賃における全体に占める割合

---

## Q10

今回の処理全体を、

```text
SQLite
↓
SQL
↓
pandas
```

という流れで説明してください。

それぞれが何を担当しているかを、今回実際に書いた処理に沿って説明してください。

***
analyze_carrier_kpi.pyが担当

> SQLiteにてデータベースに接続
> ⇒SQLにて配送実績と3つのマスターを結合
> ⇒SQLにてcarrierごとに集計
> ⇒pandasにてデータフレーム出力

***
analyze_carrier_share.pyが担当
> ⇒pandasにて個数割合、金額割合を追加
> ⇒pandasにてデータフレーム再出力


---

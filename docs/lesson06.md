## Q1

第5回終了時点では、

```text
1行 = 1配送
```

でした。

今回、

```sql
GROUP BY carrier_name
```

で集計したあとの、

> 1行の意味

は何になると考えますか？

> 1行 = 1配送会社の配送実績集計

---

## Q2

配送会社ごとの配送件数を求める場合、

```sql
COUNT(*)
```

を使うと何を数えることになりますか？

今回の「1行 = 1配送」と関連づけて説明してください。

> 1配送会社ごとの配送件数（＝集計件数）

---

## Q3

配送会社ごとの配送数量合計を求める場合、

```text
どの列
```

を `SUM()` すればよいでしょうか？

> quantity

---

## Q4

配送会社ごとの運賃合計を求める場合、

```text
どの列
```

を `SUM()` すればよいでしょうか？

今回 `quantity × freight_rate` としない理由も説明してください。

> freight_rate
> 理由は質問しましたがquantityに関わらず、delivery_idごとに運賃が決まっているから

---

## Q5

D011 / D運送は、

```text
carrier_code = NULL
freight_rate = NULL
```

ですが、

```text
carrier_name = D運送
```

自体は `delivery_records` に存在します。

今回、

```sql
GROUP BY carrier_name
```

した場合、

> D運送というグループ自体は結果に残るか

予想してください。

また、

```sql
SUM(freight_rate)
```

がどうなるかも予想してください。

実装前なので、分からなければ予想で構いません。

> 結果に残る。SUM(freight_rate)は計算できないのでNaNになると予想。

---
## Q6

最終結果は何行になりましたか？

なぜその行数になったのか、

> GROUP BY後の1行の意味

と関連づけて説明してください。

> carrier_nameで GROUP BYすることで、「1行＝1配送会社ごとの集計結果」となるため、配送会社の件数である4件になった。

---

## Q7

A運輸について、

```text
delivery_count
total_quantity
total_freight
```

はいくつになりましたか？

元の配送明細と照らして、簡単に確認してください。

>   carrier_name  delivery_count  total_quantity  total_freight
>          A運輸               4              51         6000.0

---

## Q8

D運送について、

```text
delivery_count
total_quantity
total_freight
```

はそれぞれどうなりましたか？

特に、

```text
COUNT(*)
SUM(quantity)
SUM(freight_rate)
```

がNULLを含む行に対してどう動いたのか、結果から説明してください。

>   carrier_name  delivery_count  total_quantity  total_freight
> 3          D運送               1              20            NaN

> 1行分の集計は行われたが、freight_rateがnullのため計算ができず、SUM()の結果もNaNとなった

---

## Q9

第5回までは、

```text
1行 = 1配送
```

でした。

今回のSQLでは、

```text
GROUP BY
```

によって1行の意味がどう変化しましたか？

> 「1行＝1配送会社ごとの集計結果」

---

## Q10

今回の処理を、

```text
SQLでJOINまで
↓
pandasでgroupby
```

とすることも可能です。

それでも今回はSQL側で `GROUP BY` まで行った理由を、

> SQLとpandasの役割分担

という観点から、自分なりに説明してください。

正解を当てる問題ではありません。

> SQLではデータベースの元の値から集計することを責務とし、
> pandasでは集計結果からKPIを追加で算出することを責務として分離している。

---


## Q1

`carrier_rate_master` の1行は、

    carrier_code
    area_code
    freight_rate

を持っています。

なぜ、

    carrier_code

だけでは運賃単価を特定できないのでしょうか？

> 地域ごとに運賃単価が異なるから

---

## Q2

同様に、

    area_code

だけでは運賃単価を特定できないのはなぜでしょうか？

> 複数の配送会社ごとに地域の単価が異なるから

---

## Q3

今回、

    carrier_rate_master

をJOINするためには、

どの列とどの列を使って結合する必要があると考えますか？

テーブル名も含めて説明してください。

> delivery_recordsとcarrier_masterを結合し、carrier_codeを紐づける
> delivery_recordsとarea_masterを結合し、area_codeを紐づける
> 2つのコードからcarrier_rate_masterを紐づける

---

## Q4

第4回で、

    D011 / D運送

はcarrier_masterに存在しないため、

    carrier_code = NULL

となりました。

この状態で、

    carrier_rate_master

までJOINした場合、

D011の、

    freight_rate

はどうなると予想しますか？

理由も説明してください。

> None SQLではnullとなるので、pd.DataFrameではNoneと判断される

---

## Q5

今回の最終結果でも、

    D011

を残したいとします。

その場合、

    INNER JOIN
    LEFT JOIN

のどちらを使うのが適切だと考えますか？

理由も説明してください。

> LEFT JOIN Noneも表示することで、D社の単価がマスターに登録されていないことも明示するため

---

## Q6

今回のJOIN前、

    delivery_records

の1行の意味は、

> 1行 = 1配送

でした。

今回すべてのマスタをJOINしたあと、

1行の意味はどうなると予想しますか？

「列が増える」ではなく、

> その1行が業務上何を表しているか

で回答してください。

> 1行 = 1配送 は変わらないが、2つのcodeをキーに配送ごとの単価が追加された情報になる

---

## Q7

最終的なJOIN結果は何件になりましたか？

また、なぜその件数になったと考えますか？

> 11件 FROM delivery_records でLEFT JOINしたため。

---

## Q8

D011の、

    carrier_code
    area_code
    freight_rate

はそれぞれどうなりましたか？

なぜその結果になりましたか？

> None/A001/NaN
> carrier_code,freight_rateは値が入っていないため欠損値が入った。
> area_codeは一致するものがあったため結合された

---

## Q9

正常データとして確認した、

    delivery_id
    carrier_name
    prefecture
    freight_rate

を書いてください。

また、

`carrier_rate_master.csv`

のどの組み合わせと一致しているか説明してください。

> D010 / C配送 / 京都府 / 1550.0
> C003,A003,1550

---

## Q10

今回、

    carrier_rate_master

を、

    carrier_code
    area_code

の2条件でJOINしました。

もし、

    carrier_code

だけでJOINした場合、

どのような問題が起こると予想しますか？

行数についても考えてください。

> 増えるのかな？と予測して実際にやってみるとそれぞれのcarrier_codeに対して合致する行を全て充てるので、3件分の3倍になりました。また最終件数は10×3+1（D配送分）で31件です。

---

## Q11

今回のJOIN後も、

> 1行 = 1配送

を維持できているか確認してください。

また、

> JOINしただけなのに配送実績より行数が増えた

場合、

どのようなことを疑うべきだと思いますか？

現時点で思いつく範囲で構いません。

> 結合の条件(ON/ANDの中身)が正しくない。Q11のような場合

---

## Q12

今回SQL側では、

    配送会社コード取得
    エリアコード取得
    運賃単価取得

まで行いました。

このあと配送会社別の、

    配送件数
    配送数量
    運賃合計
    委託率

などを分析するとします。

現時点では、

> SQL側でどこまで処理し、pandas側でどこから処理する

のが分かりやすいと思いますか？

正解を当てる問題ではありません。

今の自分ならどう分けるかを書いてください。

> 配送件数 / 配送数量 / 運賃合計 はSQLのGROUP BYで処理し、委託率はpandasで処理する。判定は複数列をまたいで処理が行われるかどうか。
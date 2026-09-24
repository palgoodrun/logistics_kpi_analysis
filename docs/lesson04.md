## Q1

現在、

    delivery_records = 11件

    carrier_master = 3社

です。

この状態で、

    delivery_records
    INNER JOIN
    carrier_master

を、

    carrier_name

で結合した場合、

結果は何件になると予想しますか？

理由も説明してください。

> 10件。D運送がcarrier_masterに存在しないから。

---

## Q2

今回、

    D011 / D運送

という配送実績は実際に存在しています。

分析担当者として、

INNER JOINによってこの配送実績そのものが結果から消えてしまうことに、

どのような問題があると思いますか？

> 正確な分析データが得られない。D配送の分析結果だけが得られない。

---

## Q3

今回の目的を、

> 「配送実績をすべて残したまま、登録されている配送会社についてcarrier_codeを取得する」

とした場合、

基準として残したいのは、

    delivery_records

と

    carrier_master

のどちらですか？

理由も説明してください。

> delivery_records。配送実績がすべて載っているのはdelivery_recordsだから。
---

## Q4

INNER JOINでは何件になりましたか？

なぜその件数になりましたか？

> 10件。carrier_masterにD配送のデータが存在しなかったから。

---

## Q5

LEFT JOINでは何件になりましたか？

なぜINNER JOINと結果件数が違いましたか？

> 11件。LEFT JOINではFROM側のSQLがすべて残るから。

---

## Q6

LEFT JOIN後のD011では、

    carrier_code

はどのような値になりましたか？

なぜその値になりましたか？

> None。SQLでは値が存在しない場合nullと判断され、pandasで読み込んだんだ際、Noneと判断される。

---

## Q7

マスタ不一致を抽出するSQLでは、

どの列のどのような状態を条件にしましたか？

また、なぜその条件でマスタ不一致を判定できますか？

> carrier_codeがnull。LEFT JOINした際に値が存在せずnullとなった行だけを抽出しているから。

---

## Q8

今回のような、

    配送実績
        ↓
    マスタとの紐付け

では、

INNER JOINよりLEFT JOINの方が適している場面があります。

今回のケースでは、なぜLEFT JOINを使う意味があるのか、

業務上の観点から説明してください。

> 配送データのすべてに対して分析をしたい場合に、delivery_recordsを基準にすることで全て網羅できる。
> またcarrier_masterが存在しないデータの抽出などの用途も考えられる。

---

# 17. 追加思考問題

コード実装は不要です。

## Q9

もし、

    carrier_master

に、

    C004,D運送

を追加した場合、

同じLEFT JOINを実行すると、

D011のcarrier_codeはどうなると予想しますか？

> C004

---

## Q10

もし配送実績に、

    prefecture = 奈良県

が存在するのに、

    area_master

に奈良県が存在しなかった場合、

LEFT JOINを使えば、

どのような状態から「エリアマスタ不一致」を発見できそうですか？

SQLを書く必要はありません。

> エリアコードがnullの行を抽出する（WHERE area_code IS NULL）

---
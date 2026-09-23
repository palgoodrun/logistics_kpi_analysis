実装前課題
===

## Q1

今回、

    delivery_records
    carrier_master

を結合する目的は何ですか？

> delivery_recordsに配送会社コードを紐づけるため


---

## Q2

この2テーブルは、何の列同士を使って結合できそうですか？

> carrier_name

---

## Q3

今回、

    delivery_records
    area_master

を結合する目的は何ですか？

> delivery_recordsにエリアコードを紐づけるため

---

## Q4

この2テーブルは、何の列同士を使って結合できそうですか？

> prefecture

---

## Q5

JOIN前の、

    delivery_records

の1行の意味は何ですか？

> 1行 = 1配送

---

## Q6

carrier_masterとarea_masterをJOINした後、

1行の意味はどうなると予想しますか？

「列が増える」だけではなく、

> その1行が業務上何を表しているか

で回答してください。

>> 1行の意味は変わらないが、ただの外部データから、社内的な管理コードが追加された状態に変化する

実装後課題
===

## Q7

1回目のINNER JOIN後も10件だったのはなぜですか？

> area_masterにcarrier_codeの列を追加しただけなので行数は変わらない

---

## Q8

2回目のINNER JOIN後も10件だったのはなぜですか？

> carrier_codeを追加したarea_masterにarea_codeの列を追加しただけなので行数は変わらない

---

## Q9

もし配送実績に、

    carrier_name = D運送

というデータが1件存在し、

    carrier_master

にD運送が存在しなかった場合、

INNER JOIN後の件数はどうなると予想しますか？

理由も説明してください。

まだ実際にデータを変更する必要はありません。

> 件数は変わらない。（理由）ONでキーが一致していないので、勝手に追加されない。

---

## Q10

今回、

    ON

へ書いた条件は何を意味していますか？

SQLを日本語へ翻訳するつもりで説明してください。

> FROMとINNER JOINに指定したテーブルをONに指定されたキーワードを突合させて一致した場合に結合する。

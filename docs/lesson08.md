## Q1

完成ツールにおける、

- `scripts/`
- `modules/`

それぞれの役割を、自分の言葉で定義してください。

> scripts: mainの実行場所
> modules: 1つの責務ごとの処理パーツ

---

## Q2

現在の各 `.py` ファイルを、

① 最終ツールでも使用する  
② 最終ツールでは使用しない

に分類してください。

②については、最終整理時に削除する前提で構いません。

それぞれ簡単に理由も書いてください。

**この時点ではまだ削除しません。**

> analyze_carrier_kpi.py: ①sqlでの集計を実質行っているため
> analyze_carrier_share.py: ①pandasでの集計を実質行っているため。module化候補
> build_analisis_data.py: ②学習用。analyze_carrier_kpi.pyと重複。
> check_master_mismatch.py: ①学習用。master不一致用関数化する
> join_delivery_data.py: ②学習用。analyze_carrier_kpi.pyと重複。
> setup_database.py: ①csv読み込み、sql保存を行っている。module化候補

---

## Q3

現在 `modules/analyze_carrier_kpi.py` には、

- SQL
- `read_sql()`
- DB接続

など複数の処理があります。

完成形では、

> SQLをどのファイルに持たせるか

を自分で決めてください。

その場所を選んだ理由も説明してください。

ここには唯一の正解を設定しません。  
責務として筋が通っているかを見ます。

> sqlは新規ファイルで管理します
> sql文だけをまとめて集計の定義として分離して管理します
> ファイル管理: sqlフォルダに必要なSQLを.sql方式で個別管理

---

## Q4

同様に、

`sqlite3.connect(...)`

と、

`conn.close()`

を誰が担当する設計にするか決めてください。

考えるポイントは、

> **DB接続を開始した責務と、終了させる責務をどう管理するか**

です。

> 今のところmain.pyをscripts/内で別で作りmain内でsqlの接続と終了を1回で済ませようと考えています。

---

## Q5

最終的な処理の流れを、関数名レベルで書いてください。

形式例：

    main()
     ↓
    ○○()
     ↓
    ○○()
     ↓
    ○○()

**ここまで提出して、設計レビューを受けてから実装へ進みます。**

main()
↓
read_csv(data: Path) -> pd.DataFrame
↓
save_df_to_sqlite(
    table_name: str,
    con: sqlite3.Connection,
    df: pd.DataFrame,
) -> None
↓
count_table_rows(table_name: str, conn: sqlite3.Connection)
↓
find_master_mismatches()
↓
※新規※
load_sql(path: Path) -> str
↓
read_sql(sql: str, conn: sqlite3.Connection) -> pd.DataFrame
↓
calculate_share_ratios(df: pd.DataFrame) -> pd.DataFrame

---

## Q6

完成したツールにおいて、

`1行 = 1配送`

なのはどの段階までですか？

どこで、

`1行 = 1配送会社`

へ変化しますか？

---

## Q7

今回の完成ツールで `LEFT JOIN` を使用する理由を、

- `INNER JOIN` との違い
- マスタ不一致

という観点を含めて説明してください。

---

## Q8

もし `carrier_rate_master` の、

- `carrier_code`
- `area_code`

の組み合わせが重複していた場合、
配送実績の件数や集計結果にどんな問題が起こる可能性がありますか？

第5回の内容を思い出して回答してください。

---

## Q9

今回の完成ツールについて、

- SQLが担当していること
- pandasが担当していること
- Python全体が担当していること

をそれぞれ説明してください。

---

## Q10

STEP⑨開始時と比べて、

> **複数テーブルから物流KPIを作る**

ために、自分でできるようになったことを具体的に書いてください。

ここは技術用語を使って構いません。

---
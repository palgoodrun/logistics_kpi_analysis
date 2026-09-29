## Q1：最終ファイル構成を設計する

現在までに作成したコードを踏まえて、
完成ツールで必要だと考えるファイル構成を書いてください。

形式は以下のようなツリー形式とします。

    logistics_kpi_analysis/
    │
    ├─ scripts/
    │   └─ ○○.py
    │
    ├─ modules/
    │   ├─ ○○.py
    │   └─ ○○.py
    │
    └─ sql/
        ├─ ○○.sql
        └─ ○○.sql

ファイル名については自分で決めてください。

既存ファイル名をそのまま使っても、
責務に合わせて変更しても構いません。

    logistics_kpi_analysis/
    │
    ├─ scripts/
    │   └─ main.py
    │
    ├─ modules/
    │   ├─ data_loader.py
    │   ├─ database_validator.py
    │   ├─ sql_loader.py
    │   └─ kpi_calculator.py
    │
    └─ sql/
        ├─ carrier_kpi_summary.sql
        └─ master_mismatches.sql

---

## Q2：各ファイルの責務

Q1で挙げた各ファイルについて、

    ファイル名：
    責務：

の形式で説明してください。

ここでは、

> 「どのコードを書くか」

ではなく、

> 「何を担当するファイルなのか」

を説明してください。

ファイル名： main.py
責務： 全体の実行役

ファイル名： data_loader.py
責務： CSVを読み込んでデータフレームに変換し、SQLiteに保存する

ファイル名： database_validator.py
責務： SQLの行数及び、マスター不一致を確認する

ファイル名： sql_loader.py
責務： SQLを読み込みデータフレームを返す

ファイル名： kpi_calculator.py
責務： pandasにてKPIを計算する


---

## Q3：既存関数の移動先

これまでに作成した以下の関数について、
完成ツールではどのファイルに配置するか決めてください。

- `read_csv()`
- `save_df_to_sqlite()`
- `count_table_rows()`
- `find_master_mismatches()`
- `load_sql()`
- `read_sql()`
- `calculate_share_ratios()`

形式：

    read_csv()
    → ○○.py

    save_df_to_sqlite()
    → ○○.py

のように回答してください。

なお、`find_master_mismatches()` と `load_sql()` は今回の設計で新たに必要になった関数です。

まだ実装していない場合でも、配置先は決めてください。

read_csv()
→ data_loader.py

save_df_to_sqlite()
→ data_loader.py

count_table_rows()
→ database_validator.py

find_master_mismatches()
→ database_validator.py

load_sql()
→ sql_loader.py

read_sql()
→ sql_loader.py

calculate_share_ratios()
→ kpi_calculator.py

---

## Q4：SQLファイルの分割

完成ツールではSQLを `.sql` ファイルとして管理します。

今回必要になるSQLを考え、

> 何個の `.sql` ファイルに分けるか

を決めてください。

それぞれについて、

    ファイル名：
    目的：

を書いてください。

考える対象は少なくとも、

- マスタ不一致の確認
- 配送会社別KPIの元となる集計

です。

SQL文そのものは、まだ書かなくて構いません。


ファイル名： carrier_kpi_summary.sql
目的： carrierごとのサマリーを計算するSQLを管理する

ファイル名： master_mismatches.sql
目的： マスターとの不一致を計算するSQLを管理する

---

## Q5：main.py の責務

完成ツールでは `scripts/main.py` を実行入口とします。

`main.py` が担当することを箇条書きで整理してください。

ただし、

> 「何でもmainに書く」

設計にはしないでください。

第8回-1で決めた、

> `modules/` は1つの責務ごとの処理パーツ

という方針との違いを意識してください。

- path管理
> db / 入力csv / SQLファイル    

- SQL接続 / 接続終了

- 全体の実行

- エラー出力（今回は最小限）

---
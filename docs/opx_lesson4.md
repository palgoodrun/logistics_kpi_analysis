### Q1
`dataframe_to_rows()` と `ws.append()` の役割の違いを説明してください。

> dataframe_to_rows(): dataframeの内容をwsに書き込む
> ws.append(): wsの最終行に指定の値を書き込む

### Q2
`ws.append()` と `ws.cell()` は、どのように使い分けますか？

> ws.append(): 書き込み位置を指定する必要が無いとき
> ws.cell(): 書き込み位置を指定する必要があるとき

### Q3
DataFrameをA4から出力する場合、外側・内側の `enumerate()` の `start` はそれぞれいくつですか？

> 4と1

### Q4
`header=False` と `index=False` の違いを説明してください。

> header=False: 見出しを含めて書き込むかどうか
> index=False: indexを書き込むかどうか

### Q5
データ行数が変化するレポートで、表示形式の適用範囲を固定しない理由を説明してください。

> 追加したデータに対しても表示形式が適用されるようにするため

### Q6
pandasでの集計処理とopenpyxlでの書式設定処理を分離するメリットを説明してください。

> 書式設定のみをopenpyxlで行うことで、pandasでの集計処理は書式設定を考えずに集計にのみ集中できるから
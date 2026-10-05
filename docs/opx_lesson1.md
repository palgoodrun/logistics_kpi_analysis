### ③ 確認問題

以下を自分の言葉で答えてください。

1. `Workbook`・`Worksheet`・`Cell` の関係を説明してください。

> Workbook: python上に作られたExcel book
> Worksheet: WorkbookのExcel sheet
> Cell: Worksheet上のセル

2. `Workbook()` と `load_workbook()` は、どのように使い分けますか？

> Workbook(): Workbookの新規作成
> load_workbook: 既存ExcelファイルをWorkbookとしてpythonで読み込む

3. `ws["B4"]` と `ws.cell(row=4, column=2)` は何を表していますか？
   また、実務ではどのように使い分けられそうですか？

> どちらもB4のセル
> 前者は常に入力場所を固定する場合や、コード上で入力セルを明示したい場合に使用する
> 後者は相対的にセルの位置を決めたい場合や、for分などを使って複数データを入力する際に使用する
## 5. 理解確認問題

### Q1
Font、PatternFill、Border、Alignmentはそれぞれ何を設定するものですか？

回答：
Font: 文字のフォント
PatternFill: セルの背景
Border: セルの罫線
Alignment: 文字の配置

### Q2
Fontを2回代入した場合、最初のFont設定はどうなりますか？

回答：上書きされるので、最初のFont設定は無効になる

### Q3
number_formatを使うメリットを、数値型との関係から説明してください。

回答：number_formatを使ってもセルに入力される数値自体は変わらないので、表示を変えつつ後工程で計算がそのままできる

### Q4
column_dimensionsとrow_dimensionsは、それぞれ何を設定しますか？
また、指定する単位は同じですか？

回答：
column_dimensions：列の幅 単位はデフォルト文字のサイズ
row_dimensions：行の高さ 単位はポイント

### Q5
freeze_panes = "B4" は何を固定しますか？

回答：A列の3行目以前の領域をウィンドウ固定する

### Q6
次のコードの違いを説明してください。

ws["A3"].font = Font(bold=True)
ws.column_dimensions["A"].width = 20

回答：A3のセルのフォントを太字にするのと、A列の幅を20に設定する

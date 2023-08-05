file memorize (under construction)

```python
import mem

def add_str(s0, s1):
	time.sleep(3)
	return s0 + s1

# memorize tool [mem]
memorized_func = mem(
	add_str,	# 計算結果をメモ化したい関数
	"add_str",	# 関数識別用の文字列
	confirm = False,	# メモ読み込みの確認有無
	mem_dir = "./"	# メモの置き場所
)
ret_str = memorized_func("Hello", ", World!!\n")
print(ret_str)
```

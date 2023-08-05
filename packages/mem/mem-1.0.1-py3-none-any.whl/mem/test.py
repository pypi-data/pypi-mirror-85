
# memorize tool [mem]
# 【動作確認 / 使用例】

import sys
import time
from sout import sout
from relpath import add_import_path
add_import_path("../")
# memorize tool [mem]
import mem

def add_str(s0, s1):
	time.sleep(3)
	return s0 + s1

# memorize tool [mem]
memorized_func = mem(
	add_str,	# 計算結果をメモ化したい関数
	"add_str",	# 関数識別用の文字列
	mem_dir = "./",	# メモの置き場所
	confirm = False	# メモ読み込みの確認有無
)
ret_str = memorized_func("Hello", ", World!!\n")
# 動作確認
sout(ret_str)

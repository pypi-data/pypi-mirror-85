
# memorize tool [mem]

import os
import sys
import json
import pickle
import xxhash
from sout import sout
from fileinit import fileinit

# json化可能リテラルの辞書
literal_typle_dic = {type(example_obj):1
	for example_obj in [1, 2.3, "hoge", None, True]}

# json化可能オブジェクトに変換
def to_jsonable(arg_obj):
	# json化可能リテラルの場合
	if type(arg_obj) in literal_typle_dic: return arg_obj
	# コンテナ型の場合
	if type(arg_obj) == type([]):
		return ["list", [to_jsonable(e) for e in arg_obj]]
	elif type(arg_obj) == type((1,)):
		return ["tuple", [to_jsonable(e) for e in arg_obj]]
	elif type(arg_obj) == type({1}):
		return ["set", [to_jsonable(e) for e in arg_obj]]
	elif type(arg_obj) == type({1:1}):
		return ["dict", [[to_jsonable(k), to_jsonable(arg_obj[k])]
			for k in arg_obj]]
	else:
		raise Exception("[ERROR] unsupported type argument")
	return jsonable_obj

# ファイル名の元にする文字列の生成
def gen_bin_key(func_identifier, args, kwargs):
	# json化可能オブジェクトに変換
	key_triple = (func_identifier, args, kwargs)
	jsonable_obj = to_jsonable(key_triple)	# json化可能オブジェクトに変換
	# バイナリ文字列に変換
	ascii_key = json.dumps(jsonable_obj)
	bin_key = ascii_key.encode()
	return bin_key

# xxhashアルゴリズムによるhash
def xxhash_wrapper(bin_key):
	x = xxhash.xxh64(bin_key)
	return x.hexdigest()

# メモ読み込みの確認
def recalc_confirm():
	while True:
		print("Do you want to load the cache?")
		raw_user_inp = input("load [c]ache / [r]ecalculate >")
		user_inp = raw_user_inp.strip().lower()
		if user_inp == "c": return "load_cache"
		if user_inp == "r": return "recalc"
		print("\n[ERROR] input [c] or [r].\n")

# 再計算判断
def judge_recalculation(mem_filename, confirm):
	# メモ化した計算結果が存在しない場合、再計算
	if os.path.exists(mem_filename) is False: return True
	# メモ化した計算結果が存在する場合、そのままメモ読み込み
	if confirm is False: return False
	# メモ読み込みの確認
	user_inp = recalc_confirm()
	return (user_inp == "recalc")

# memorize tool [mem]
def mem(
	original_func,	# 計算結果をメモ化したい関数
	func_identifier,	# 関数識別用の文字列
	confirm = False,	# メモ読み込みの確認有無
	mem_dir = "./"	# メモの置き場所
):
	# 計算結果のメモ化機能を付加した関数
	def memorized_func(*args, **kwargs):
		# ファイル名の作成
		bin_key = gen_bin_key(func_identifier, args, kwargs)	# ファイル名の元にする文字列の生成
		mem_hash = xxhash_wrapper(bin_key)	# xxhashアルゴリズムによるhash
		mem_filename = "%s/__mem__/%s.pickle"%(mem_dir, mem_hash)
		# 再計算判断
		recalc_flag = judge_recalculation(mem_filename, confirm)
		if recalc_flag is True:
			# 再計算化
			calc_result = original_func(*args, **kwargs)
			# 計算結果をメモ化
			memorize_obj = {
				"bin_key": bin_key,
				"contents": calc_result
			}
			fileinit(mem_filename, overwrite = True)	# 空で初期化
			with open(mem_filename, "wb") as f:
				pickle.dump(memorize_obj, f)
			return calc_result
		else:
			# メモ化した計算結果の読み込み
			with open(mem_filename, "rb") as f:
				memorized_obj = pickle.load(f)
			return memorized_obj["contents"]
	return memorized_func

# モジュールオブジェクトとmem関数を同一視
sys.modules[__name__] = mem

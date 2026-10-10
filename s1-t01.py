# 读取语料并统计：
# 总行数、非空段数、总字数、高频词Top10

from pathlib import Path

source_path = Path(__file__).parent/'corpus/corpus_sample.txt'
target_path = Path(__file__).parent

with open(source_path, 'r', encoding='utf-8') as f:
    raw = f.read()

words = {}
total_lines = 0
paragrahs = [0]
total_words = 0
key = ''

for i in raw:
    if i == '\n':
        total_lines += 1
        if paragrahs[-1] == 0:
            paragrahs[-1] += 1
        else:
            paragrahs.append(0)
        if len(key) >= 2:
            if key in words.keys():
                words[key] += 1
            else:
                words[key] = 1 
        key = ''
    elif i not in ' \t[]【】()，。、“”；：！’‘（）——1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
        total_words += 1
        key += i
    else:
        if len(key) >= 2:
            if key in words.keys():
                words[key] += 1
            else:
                words[key] = 1 
        key = ''

# words.pop('')
top_words = sorted(words, reverse=True, key=words.get)
# print(words)
top10 = '词\t次数\n'
j = 0
word = ''
k = 0
while k < 10:
    word += top_words[j]
    if words[top_words[j+1]] == words[top_words[j]] and words[top_words[j]] > 1:
        word += '、'
        k -= 1
    else:
        top10 += f'{word}\t{words[top_words[j]]}\n'
        word = ''
    j += 1
    k += 1
result = f'== 语料摘要 ==\n来源文件：\tcorpus_sample.txt\n总行数：\t{total_lines+1}\n非空段数：\t{len(paragrahs)+1}\n总字数（不含空白）：\t{total_words}\n== 高频词 TOP10 ==\n'
result += top10

with open(target_path/'s1-t01_result.txt', 'w', encoding='utf-8') as f:
    f.write(result)
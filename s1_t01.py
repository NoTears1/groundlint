# 读取语料并统计：
# 总行数、段数（两个相邻换行符之间没有非空字符）、总字数（所有非空字符）、高频词（连续两个以上的汉字）Top10

from pathlib import Path

source_path = Path(__file__).parent/'corpus/corpus_sample_v2.txt'
target_path = Path(__file__).parent
try:
    with open(source_path, 'r', encoding='utf-8') as f:
        raw = f.read()
except FileNotFoundError:
    print("退出码：1")
    exit()

if len(raw) == 0:
    print("退出码：0")
    exit()

words = {}
total_lines = 0
paragrahs = []
total_words = 0
key = ''
is_paragraph = True #判断是否是两个连续换行

for i, word in enumerate(raw):

    if word == '\n':
        total_lines += 1
        if is_paragraph == True:
            paragrahs.append(0)

        if len(key) >= 2:
            if key in words.keys():
                words[key] += 1
            else:
                words[key] = 1 
        key = ''
        is_paragraph = True
    elif word in '\t ':
        if len(key) >= 2:
            if key in words.keys():
                words[key] += 1
            else:
                words[key] = 1 
        key = ''
    elif word in '[]【】()，。、“”；：！’‘（）()——-1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
        is_paragraph = False
        if len(key) >= 2:
            if key in words.keys():
                words[key] += 1
            else:
                words[key] = 1 
        key = ''
        total_words += 1
    else:
        is_paragraph = False
        key += word
        total_words += 1
        


    # if i == '\n':
        
    #     total_lines += 1
    #     # if len(paragrahs) > 0 and paragrahs[-1] == 0:
    #     #     paragrahs[-1] += 1
    #     # else:
    #     if is_paragraph == True:
    #         paragrahs.append(0)
    #     is_paragraph = True

    #     if len(key) >= 2:
    #         if key in words.keys():
    #             words[key] += 1
    #         else:
    #             words[key] = 1 
    #     key = ''
    # elif i not in ' \t[]【】()，。、“”；：！’‘（）——1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
    #     total_words += 1
    #     key += i
    #     is_paragraph = False
    # else:
    #     if len(key) >= 2:
    #         if key in words.keys():
    #             words[key] += 1
    #         else:
    #             words[key] = 1 
    #     key = ''

    #     is_paragraph = False

# words.pop('')
top_words = sorted(words, reverse=True, key=words.get)
# print(words)
topn = '词\t次数\n'
j = 0
word = ''
k = 0
top = 3
repeat = ''

for j in range(top):
    topn += f'{top_words[j]}\t{words[top_words[j]]}\n'

while True:
    word += top_words[k]
    if  words[top_words[k+1]] == words[top_words[k]]:
        word += '、'
    else:
        repeat += f'{words[top_words[k]]}次：{word}\n'
        word = ''
    k += 1
    if words[top_words[k]] < words[top_words[top]] or words[top_words[k]] == 1:
        break
result = f'== 语料摘要 ==\n来源文件：\tcorpus_sample.txt\n总行数：\t{total_lines+1}\n非空段数：\t{len(paragrahs)+1}\n总字数（不含空白）：\t{total_words}\n== 高频词 TOP{top} ==\n'
result += topn + '== 高频次数 ==\n'+repeat

with open(target_path/'s1_t01_result_v2.txt', 'w', encoding='utf-8') as f:
     f.write(result)

print(result)

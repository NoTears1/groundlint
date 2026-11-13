# 读取语料并统计：
# 总行数、段数（两个相邻换行符之间没有非空字符）、总字数（所有非空字符）、高频词（连续两个以上的汉字）Top10

from pathlib import Path
import argparse
from datetime import datetime
import sys

def calculate(source_path):
    # 打开语料文件
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            raw = f.read()
    except FileNotFoundError:
        print("退出码：1", file=sys.stderr)
        sys.exit(1)

    # # 文件为空则退出，退出码为0
    # if len(raw) == 0:
    #     print("退出码：0", file=sys.stderr)
    #     sys.exit(0)

    words = {}
    total_lines = len(raw.splitlines())
    paragrahs = 0
    total_words = len(raw.strip())
    key = ''
    is_in_paragraph = False # 是否在段内

    for i, word in enumerate(raw):
        
        if '\u4e00' <= word and '\u9fff' >= word: # 统计词数
            key += word

        else:
            if len(key) >= 2:
                if key in words.keys():
                    words[key] += 1
                else:
                    words[key] = 1
            key = ''

    for line in raw.splitlines():
        if len(line.strip()) == 0:
            is_in_paragraph = False
        else:
            if not is_in_paragraph:
                paragrahs += 1
                is_in_paragraph = True

    top_words = sorted(words, reverse=True, key=words.get)

    return total_lines, paragrahs, total_words, top_words, words

def display(total_lines, paragrahs, total_words, top_words, words, topn, target_path):
    topn_title = '词\t次数\n'
    j = 0
    word = ''
    k = 0
    try:
        topn = int(topn)
    except ValueError:
        print(f'{topn} is not a number.')

    repeat = ''
    if len(words) > 0:
        for j in range(topn):
            topn_title += f'{top_words[j]}\t{words[top_words[j]]}\n'

        while True:
            word += top_words[k]
            if  words[top_words[k+1]] == words[top_words[k]]:
                word += '、'
            else:
                repeat += f'{words[top_words[k]]}次：{word}\n'
                word = ''
            k += 1
            if words[top_words[k]] < words[top_words[topn]] or words[top_words[k]] == 1:
                break
    result = f'== 语料摘要 ==\n来源文件：\tcorpus_sample.txt\n总行数：\t{total_lines}\n非空段数：\t{paragrahs}\n总字数（不含空白）：\t{total_words}\n== 高频词 TOP{topn} ==\n'
    result += topn_title + '== 高频次数 ==\n'+repeat

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(result)

    print(result)

def main():
    now = datetime.now()
    # 参数化输入路径、topN、输出路径，输出文件名由输入名派生或由--out指定，输入路径要有默认值，topN要能容错
    parser = argparse.ArgumentParser()
    parser.add_argument('source_path', default='corpus/corpus_sample.txt')
    parser.add_argument('topn')
    parser.add_argument('-o', '--out', dest='target', default=f's1_t01_result_{str(now)}.txt')

    args = parser.parse_args()

    source_path = Path(args.source_path)
    target_path = Path(__file__).parent/args.target

    total_lines, paragrahs, total_words, top_words, words = calculate(source_path)
    display(total_lines, paragrahs, total_words, top_words, words, args.topn, target_path)

if __name__ == '__main__':
    main()
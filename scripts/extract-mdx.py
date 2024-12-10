
# TODO: To finish this script.

from readmdict import MDX

def get_describe(describe):
    if isinstance(describe, (list, tuple)):
        return ';'.join(get_describe(i) for i in describe)
    else:
        return describe


def deal_node(node, result=[], num=-1):
    chars = "■□◆▲●◇△○★☆"
    for k, (d, cs) in node.items():
        if num >= 0:
            d = d.replace('\n', '')
            result.append(f"{'    '*num}{chars[num]} {k}: {d}")
        if cs:
            deal_node(cs, result, num+1)


def get_row(topic):
    id2children = {}
    root = {}
    for d in topic:
        node = id2children.get(d.get("parentid"), root)
        tmp = {}
        node[d['id']] = (get_describe(d['describe']), tmp)
        id2children[d['id']] = tmp
    name, (describe, _) = list(root.items())[0]
    txts = []
    deal_node(root, txts)
    other = "\n".join(txts)
    return name, describe, other


# 读取 .mdx 文件
mdx_file = "dicm.mdx"
mdx = MDX(mdx_file, encoding='utf-8')
items = mdx.items()

# 存储数据
data = []

# 提取单词
for key, value in items:
    word = key.decode().strip()
    print(word)  # 显示正在处理的单词
    data.append(word)

# 导出为 .txt 文件
output_file = mdx_file.replace(".mdx", ".txt")
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(data))

print(f"导出完成，结果保存在: {output_file}")

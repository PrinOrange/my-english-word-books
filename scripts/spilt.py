import random
import argparse
import os


def shuffle_and_split_txt(input_file, output_prefix, max_lines=5000):
    """
    随机打乱文本文件的行，并拆分成多个文件，每个文件不超过 max_lines 行。

    :param input_file: 原始文件路径
    :param output_prefix: 输出文件名前缀
    :param max_lines: 每个文件的最大行数，默认5000
    """
    try:
        # 获取输入文件的目录路径
        output_dir = os.path.dirname(input_file)

        # 读取文件内容并打乱行顺序
        with open(input_file, "r", encoding="utf-8") as infile:
            lines = infile.readlines()
        random.shuffle(lines)  # 随机打乱行顺序

        # 拆分文件
        file_count = 0
        for i in range(0, len(lines), max_lines):
            file_count += 1
            output_file = os.path.join(output_dir, f"{output_prefix}_{file_count}.txt")
            with open(output_file, "w", encoding="utf-8") as outfile:
                outfile.writelines(lines[i : i + max_lines])
            print(f"Created: {output_file}, Lines: {len(lines[i:i + max_lines])}")

        print(f"完成：文件已打乱并拆分，共生成 {file_count} 个文件。")
    except Exception as e:
        print(f"发生错误: {e}")


def main():
    # 配置命令行参数
    parser = argparse.ArgumentParser(description="随机打乱并拆分文本文件。")
    parser.add_argument("--file", required=True, help="输入的文本文件路径")
    parser.add_argument("--prefix", required=True, help="输出文件的前缀")
    parser.add_argument(
        "--max_lines",
        type=int,
        default=5000,
        help="每个文件的最大行数（默认为 5000 行）",
    )

    # 解析用户输入的参数
    args = parser.parse_args()
    shuffle_and_split_txt(args.file, args.prefix, args.max_lines)


if __name__ == "__main__":
    main()

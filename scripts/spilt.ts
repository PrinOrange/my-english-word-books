/**
 * 这个脚本用来整理 plain 词书，即去重、并重新打乱 plain 词书，然后以 5000 词为单位，分割成多个词书
 * （因为墨墨、不背单词支持导入的最大词书长度为 5000）。
 */

import * as fs from "fs";
import * as path from "path";
import Enquirer from "enquirer";

/**
 * 随机打乱文本文件的行，并拆分成多个文件，每个文件不超过 maxLines 行。
 *
 * @param inputFile 原始文件路径
 * @param outputPrefix 输出文件名前缀
 * @param maxLines 每个文件的最大行数，默认 5000
 */
async function shuffleAndSplitTxt(
  inputFile: string,
  outputPrefix: string,
  maxLines: number = 5000
): Promise<void> {
  try {
    // 获取输入文件的目录路径
    const outputDir = path.dirname(inputFile);

    // 读取文件内容并打乱行顺序，然后去重
    const fileContent = fs.readFileSync(inputFile, "utf-8");
    const lines = Array.from(
      new Set(fileContent.split("\n").map((line) => line.trim()))
    ).filter((line) => line);

    // 随机打乱行顺序
    for (let i = lines.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [lines[i], lines[j]] = [lines[j], lines[i]];
    }

    // 拆分文件
    let fileCount = 0;
    for (let i = 0; i < lines.length; i += maxLines) {
      fileCount++;
      const outputFile =
        lines.length === 1
          ? path.join(outputDir, `${outputPrefix}.txt`)
          : path.join(outputDir, `${outputPrefix}_${fileCount}.txt`);
      const chunk = lines.slice(i, i + maxLines).join("\n");
      fs.writeFileSync(outputFile, chunk, "utf-8");
      console.log(
        `Created: ${outputFile}, Lines: ${lines.slice(i, i + maxLines).length}`
      );
    }

    console.log(`完成：文件已打乱并拆分，共生成 ${fileCount} 个文件。`);
  } catch (error) {
    console.error(`发生错误: ${error}`);
  }
}

async function main(): Promise<void> {
  const answers: any = await Enquirer.prompt([
    {
      type: "input",
      name: "file",
      message: "请输入文本文件路径：",
      validate: (input) => (input.trim() ? true : "文件路径不能为空"),
    },
    {
      type: "input",
      name: "prefix",
      message: "请输入输出文件的前缀：",
      validate: (input) => (input.trim() ? true : "前缀不能为空"),
    },
    {
      type: "number",
      name: "maxLines",
      message: "请输入每个文件的最大行数 (默认为 5000):",
      initial: 5000,
      validate: (input) =>
        !isNaN(parseInt(input)) && parseInt(input) > 0
          ? true
          : "请输入有效的正整数",
    },
  ]);

  const inputFile = answers.file;
  const outputPrefix = answers.prefix;
  const maxLines = answers.maxLines;

  await shuffleAndSplitTxt(inputFile, outputPrefix, maxLines);
}

if (require.main === module) {
  main().catch((error) => console.error(`发生未捕获的错误：${error.message}`));
}

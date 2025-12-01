import re
from collections import defaultdict

# 定义函数处理汇编文件
def process_assembly_file(file_path):
    """
    统计汇编文件中所有指令的出现次数，无论机器码长度如何。

    :param file_path: 汇编文件路径
    :return: 包含指令及其出现次数的字典
    """
    # 用于统计指令出现的次数
    instruction_count = defaultdict(int)

    # 匹配包含指令的行，支持不同长度的机器码
    # 修改正则以支持 .insn 指令
    pattern = re.compile(r'^\s*[0-9a-fA-F]+:\s+[0-9a-fA-F]+\s+(\w+(\.\w+)*|\.\w+)\b')

    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                instruction = match.group(1)
                instruction_count[instruction] += 1

    return instruction_count

# 打印统计结果
def print_stats(stats, sort_by_count=True):
    """
    打印指令及其出现次数。

    :param stats: 包含指令及其出现次数的字典
    :param sort_by_count: 是否按数量排序，默认为 True
    """
    # 排序规则
    sorted_stats = sorted(stats.items(), key=lambda x: (-x[1], x[0])) if sort_by_count else sorted(stats.items())

    # 打印表头
    print(f"{'Instruction':<30} {'Count':<10}")
    print("-" * 40)

    # 打印每条指令及其数量
    for instruction, count in sorted_stats:
        print(f"{instruction:<30} {count:<10}")

    # 打印总指令数
    total_instructions = sum(stats.values())
    print("-" * 40)
    print(f"{'Total':<30} {total_instructions:<10}")

# 示例文件路径
file_path = '/home/hyx/dgemm_kernel_riscv.asm'  # 替换为实际汇编文件路径

# 处理汇编文件并获取统计数据
stats = process_assembly_file(file_path)

# 打印统计结果
print_stats(stats)

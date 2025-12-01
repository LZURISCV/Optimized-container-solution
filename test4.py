import re
from collections import defaultdict

# 定义函数处理汇编文件
def process_assembly_file(file_path):
    # 用于统计指令出现的次数
    instruction_count = defaultdict(int)

    # 匹配机器码为8位（4字节）且包含指令的行
    # 允许指令后有多个点分隔的扩展符号，如 .insn 或 .nop
    pattern = re.compile(r'^\s*[0-9a-fA-F]+:\s+[0-9a-fA-F]{8}\s+(\.\w+|\w+(\.\w+)*)\b')

    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                instruction = match.group(1)
                instruction_count[instruction] += 1

    return instruction_count

# 打印结果
def print_stats(stats):
    print(f"{'Instruction':<30} {'Count':<5}")
    print("-" * 35)

    total = 0
    for instruction, count in sorted(stats.items()):
        print(f"{instruction:<30} {count:<5}")
        total += count

    print("-" * 35)
    print(f"{'Total Instructions':<30} {total:<5}")

# 示例文件路径
file_path = '/home/hyx/nginx.asm'  # 替换为实际汇编文件路径
stats = process_assembly_file(file_path)
print_stats(stats)


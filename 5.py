import re
from collections import defaultdict

def extract_x86_instructions(file_path):
    """
    仅提取 x86 指令（不包括操作数），并跳过数据行。
    
    :param file_path: 汇编文件路径
    :return: 指令及其出现次数的字典
    """
    instruction_count = defaultdict(int)

    # 改进的正则表达式：
    # 1. `^\s*[0-9a-fA-F]+:`  -> 匹配开头的地址部分，如 "67:"
    # 2. `( [0-9a-fA-F]{2,})+`  -> 匹配连续的机器码
    # 3. `\s*([a-zA-Z0-9\.]+)`  -> 提取指令（允许数字、字母和点，如 vfmadd231pd）
    pattern = re.compile(r'^\s*[0-9a-fA-F]+:\s+(?:[0-9a-fA-F]{2,}\s+)+\s*([a-zA-Z0-9\.]+)', re.IGNORECASE)

    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                instruction = match.group(1).strip()  # 只取指令部分
                # 过滤掉那些只有数据行，没有指令的情况
                if not instruction.isdigit():  # 排除只有数字的行（例如数据行）
                    instruction_count[instruction] += 1

    return instruction_count

# 你的汇编文件路径
file_path = '/home/hyx/dgemm_kernel_x86.asm'  # 请替换成你的实际路径

# 处理文件
stats = extract_x86_instructions(file_path)

# 按出现次数排序
sorted_stats = sorted(stats.items(), key=lambda x: -x[1])

# 输出统计结果
print(f"{'Instruction':<20} {'Count':<10}")
print("-" * 30)
for instruction, count in sorted_stats:
    print(f"{instruction:<20} {count:<10}")

# 打印总指令数
print("-" * 30)
print(f"{'Total':<20} {sum(stats.values()):<10}")

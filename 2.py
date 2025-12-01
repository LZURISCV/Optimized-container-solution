import re

def add_c_prefix_to_4bit_instructions(line):
    """
    对于每一行汇编代码，如果是 4 位（2 字节）机器码指令且没有 `c.` 前缀，
    则在指令头部加上 `c.` 前缀。
    """
    # 提取机器码（16进制的4字节表示）
    match = re.match(r'^\s*([0-9a-fA-F]+):\s+([0-9a-fA-F]{4})\s+(\S+)', line)
    
    if match:
        address = match.group(1)
        machine_code = match.group(2)
        instruction = match.group(3)
        
        # 如果机器码是4位（即2字节），且指令没有 'c.' 前缀
        if len(machine_code) == 4 and not instruction.startswith("c."):
            # 在指令前加上 'c.' 前缀
            line = line.replace(instruction, f"c.{instruction}")
    
    return line

def process_assembly_file(input_filename, output_filename):
    """
    处理汇编文件，将所有4位机器码指令加上 `c.` 前缀，并输出到新的文件中，保留原有格式。
    """
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            # 对每一行汇编代码进行检查和处理
            converted_line = add_c_prefix_to_4bit_instructions(line)
            outfile.write(converted_line)

# 输入和输出文件路径
input_filename = 'dgemm_kernel_riscv1.asm'  # 假设输入文件是 'nginx.asm'
output_filename = 'dgemm_kernel_riscv2.asm'  # 输出文件是 'output.asm'

process_assembly_file(input_filename, output_filename)

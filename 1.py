import re

# 伪指令到正常指令的映射
pseudo_to_normal = {
    'beqz': 'beq',
    'bnez': 'bne',
    'j': 'jal',
    'jr': 'jalr',
    'mv': 'addi',
    'nop': 'addi',
    'ret': 'jalr',
    'sext.w': 'addiw',
    'bgez': 'bge',
    'bgtz': 'blt',
    'blez': 'bge',
    'bltz': 'blt',
    'neg': 'sub',
    'negw': 'subw',
    'not': 'xori',
    'seqz': 'sltiu',
    'sgtz': 'slt',
    'snez': 'sltu',
    'fabs.s': 'fsgnjx.s',
    'fmv.s': 'fsgnj.s',
    'fneg.s': 'fsgnjn.s',
    'frflags': 'csrrs',
    'fsflags': 'csrrw',
    'bgt': 'blt',
    'ble': 'bge',
    'bgtu': 'bltu',
    'bleu': 'bgeu',
    'csrc': 'csrrc',
    'csrci': 'csrrci',
    'csrr': 'csrrs',
    'csrsi': 'csrrsi',
    'csrw': 'csrrw',
    'csrwi': 'csrrwi',
    'frcsr': 'csrrs',
    'frrm': 'csrrs',
    'fscsr': 'csrrw',
    'fsflagsi': 'csrrwi',
    'fsrm': 'csrrw',
    'fsrmi': 'csrrwi',
    'la': 'addi',
    'rdcycle': 'csrrs',
    'rdinstret': 'csrrs',
    'rdtime': 'csrrs',
    'sltz': 'slt',
    'tail': 'auipc',
    'call': 'auipc'
}

def convert_pseudo_instruction(line):
    """
    转换单行汇编代码中的伪指令，保留行的整体格式。
    如果伪指令的机器码是 4 个字符（2 字节），加 `c.` 前缀；如果是 8 个字符（4 字节），直接替换成正常指令。
    """
    # 提取机器码（16进制的4字节表示）
    match = re.match(r'^\s*([0-9a-fA-F]+):\s+([0-9a-fA-F]+)\s+(\S+)', line)
    
    if match:
        address = match.group(1)
        machine_code = match.group(2)
        instruction = match.group(3)
        
        # 判断机器码长度
        if len(machine_code) == 8:  # 4 字节（8 个字符）
            # 直接替换为正常指令
            if instruction in pseudo_to_normal:
                line = line.replace(instruction, f"{pseudo_to_normal[instruction]}")
        elif len(machine_code) == 4:  # 2 字节（4 个字符）
            # 为 2 字节指令加上 'c.' 前缀
            if instruction in pseudo_to_normal:
                line = line.replace(instruction, f"c.{pseudo_to_normal[instruction]}")
    
    return line

def process_assembly_file(input_filename, output_filename):
    """
    处理汇编文件，将伪指令替换为对应的正常指令，并输出到新的文件中，保留原有格式。
    """
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            # 对每一行汇编代码进行伪指令转换
            converted_line = convert_pseudo_instruction(line)
            outfile.write(converted_line)

# 输入和输出文件路径
input_filename = 'dgemm_kernel_riscv.asm'  # 假设输入文件是 'input.asm'
output_filename = 'dgemm_kernel_riscv1.asm'  # 输出文件是 'output.asm'

process_assembly_file(input_filename, output_filename)

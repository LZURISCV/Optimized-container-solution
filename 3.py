import re
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import font_manager
import time

def count_instructions(file_path, instruction_sets):
    """
    Count the proportion of different RISC-V extension instructions in an assembly file.

    :param file_path: Path to the assembly file
    :param instruction_sets: Dictionary where keys are extension names and values are sets of instructions
    :return: Dictionary where keys are extension names and values are their respective proportions
    """
    extension_counts = {ext: 0 for ext in instruction_sets}
    unmatched_instructions = {}

    with open(file_path, 'r') as f:
        code = f.read()

    instructions_in_code = re.findall(r'^\s+\w+:\s+\w+\s+([a-zA-Z0-9\.]+)', code, re.MULTILINE)

    for instruction in instructions_in_code:
        matched = False
        for ext, instructions in instruction_sets.items():
            if instruction in instructions:
                extension_counts[ext] += 1
                matched = True
                break
        if not matched:
            unmatched_instructions[instruction] = unmatched_instructions.get(instruction, 0) + 1

    total_instructions = sum(extension_counts.values())
    extension_percentages = {ext: round((count / total_instructions) * 100, 6) if total_instructions > 0 else 0
                             for ext, count in extension_counts.items()}

    if unmatched_instructions:
        print("Unmatched Instructions Summary:")
        for instruction, count in sorted(unmatched_instructions.items(), key=lambda item: item[1], reverse=True):
            print(f"{instruction}: appeared {count} times")

    return extension_percentages

def plot_pie_chart(extension_percentages):
    """
    Generate and save a pie chart based on the instruction set proportions.

    :param extension_percentages: Dictionary where keys are extension names and values are their respective proportions
    """
    font_path = '/usr/share/fonts/opentype/noto/NotoSans-Regular.ttf'  # Adjust font path if needed
    prop = font_manager.FontProperties(fname=font_path)

    rcParams['axes.unicode_minus'] = False  

    labels = ['I Extension', 'M Extension', 'A Extension', 'F/D Extension', 'C Extension', 'V Extension']
    sizes = list(extension_percentages.values())
    percentages = [f'{size:.2f}%' for size in sizes]

    plt.figure(figsize=(8, 8))
    wedges, texts, autotexts = plt.pie(
        sizes,
        autopct='%1.2f%%',
        startangle=140,
        colors=plt.cm.Paired.colors,
        wedgeprops={'edgecolor': 'black', 'linewidth': 1.5},
        labeldistance=1.2,
        rotatelabels=True
    )

    plt.title('RISC-V Instruction Extension Distribution')

    labels_with_percentages = [f'{label} ({percentage})' for label, percentage in zip(labels, percentages)]
    plt.legend(wedges, labels_with_percentages, title="Extension Type", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())  
    file_name = f'instruction_distribution_pie_chart_{timestamp}.png'  

    plt.savefig(file_name, bbox_inches='tight')  
    print(f"Chart saved as: {file_name}")

    plt.show()

def main():
    file_path = "/home/hyx/dgemm_kernel_riscv.asm"

    instruction_sets = {
        'I': ['add', 'addw', 'addi', 'addiw', 'sub', 'subw', 'and', 'andi', 'or', 'ori', 'xor', 'xori', 'sll', 'sllw', 'slli', 'slliw', 'srl', 'srlw', 'srli', 'srliw', 'sra', 'sraw', 'srai', 'sraiw', 'slt', 'sltu', 'slti', 'sltiu', 'lui', 'auipc', 'beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu', 'jal', 'jalr', 'lb', 'lbu', 'lh', 'lhu', 'lw', 'lwu', 'ld', 'sb', 'sh', 'sw', 'sd', 'csrrw', 'csrrs', 'csrrc', 'csrrwi', 'csrrsi', 'csrrci', 'wfi', 'mret', 'sret', 'fence', 'fence.i', 'sfence.vma', 'ecall', 'ebreak', 'seqz', 'li'],
        'M': ['mul', 'mulw', 'mulh', 'mulhs', 'mulhu', 'div', 'divw', 'divu', 'divuw', 'rem', 'remw', 'remu', 'remuw'],
        'A': ['lr.w', 'lr.d', 'sc.w', 'sc.d', 'amoswap.w', 'amoswap.d', 'amoadd.w', 'amoadd.d.aqrl', 'amoxor.w', 'amoxor.d', 'amoand.w', 'amoand.d', 'amoor.w', 'amoor.d', 'amomin.w', 'amomin.d', 'amomax.w', 'amomax.d', 'amominu.w', 'amominu.d', 'amomaxu.w', 'amomaxu.d', 'sc.d.rl', 'amoadd.d.aq', 'amoadd.w.aq', 'amoand.w.aq', 'amoor.w.aq', 'amoswap.w.aq', 'lr.d.aq', 'lr.w.aq', 'sc.d.aq', 'sc.w.aq'],
        'F\D': ['fadd.s', 'fsub.s', 'fmul.s', 'fmadd.s', 'fmsub.s', 'fnmadd.s', 'fnmsub.s', 'fdiv.s', 'fsqrt.s', 'fsgnj.s', 'fsgnjn.s', 'fsgnjx.s', 'fmv.x.w', 'fmv.w.x', 'fmin.s', 'fmax.s', 'feq.s', 'flt.s', 'fle.s', 'fcvt.w.s', 'fcvt.wu.s', 'fcvt.s.w', 'fcvt.s.wu', 'fcvt.l.s', 'fcvt.lu.s', 'fcvt.s.l', 'fcvt.s.lu', 'flw', 'fsw', 'fclass.s', 'fadd.d', 'fcvt.d.l', 'fcvt.d.lu', 'fcvt.l.d', 'fcvt.lu.d', 'fld', 'flt.d', 'fmul.d', 'fmv.d.x', 'fmv.x.d', 'fneg.d', 'fsub.d', 'fsd', 'fabs.d', 'fcvt.d.s', 'fcvt.d.w', 'fcvt.d.wu', 'fcvt.s.d', 'fcvt.w.d', 'fcvt.wu.d', 'fdiv.d', 'feq.d', 'fle.d', 'fmadd.d', 'fmsub.d', 'fmv.d', 'fsqrt.d', 'fnmsub.d'],
        'C': ['c.add', 'c.addw', 'c.addi', 'c.addiw', 'c.sub', 'c.subw', 'c.addi16sp', 'c.addi4spn', 'c.and', 'c.andi', 'c.or', 'c.xor', 'c.slli', 'c.srli', 'c.srai', 'c.li', 'c.lui', 'c.beq', 'c.bne', 'c.jal', 'c.jalr', 'c.lw', 'c.sw', 'c.lwsp', 'c.swsp', 'c.ld', 'c.sd', 'c.ldsp', 'c.sdsp', 'c.ebreak', 'c.fsd', 'c.fld'],
        'V': []  
    }

    extension_percentages = count_instructions(file_path, instruction_sets)

    print("Instruction Extension Proportions:")
    for ext, percentage in extension_percentages.items():
        print(f"{ext} Extension: {percentage:.6f}%")  

    plot_pie_chart(extension_percentages)

if __name__ == "__main__":
    main()

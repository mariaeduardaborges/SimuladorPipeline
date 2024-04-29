class PipelineSimulator:

    def __init__(self, instructions):
        self.instructions = instructions
        self.registers = [0] * 32  # Corrigido para 32 registradores
        self.registers[0] = 0  # Registrador R0 fixo em zero
        self.memory = [0] * 1000
        self.pc = 0
        self.clock_cycles = 0
        self.prediction_table = [0] * 32  # Tabela de predição inicializada com 0

    def fetch(self):
        if self.pc < len(self.instructions):
            instruction = self.instructions[self.pc]
            self.pc += 1
            return instruction
        else:
            return None

    def decode(self, instruction):
        opcode, operands = instruction
        return opcode, operands

    def execute(self, opcode, operands):
        if opcode == 'ADD':
            reg1, reg2, dest_reg = operands
            self.registers[dest_reg] = self.registers[reg1] + self.registers[reg2]
        elif opcode == 'SUB':
            reg1, reg2, dest_reg = operands
            self.registers[dest_reg] = self.registers[reg1] - self.registers[reg2]
        elif opcode == 'ADDI':
            reg, immediate, dest_reg = operands
            self.registers[dest_reg] = self.registers[reg] + immediate
        elif opcode == 'SUBI':
            reg, immediate, dest_reg = operands
            self.registers[dest_reg] = self.registers[reg] - immediate
        elif opcode == 'BEQ':
            reg1, reg2, offset = operands
            if self.registers[reg1] == self.registers[reg2]:
                self.pc += offset
        elif opcode == 'J':
            dest_addr, = operands
            self.pc = dest_addr

    def access_memory(self, opcode, operands):
        if opcode == 'LOAD':
            addr, dest_reg = operands
            return self.memory[addr], dest_reg
        elif opcode == 'STORE':
            src_reg, addr = operands
            return src_reg, addr
        else:
            return None

    def write_back(self, opcode, operands, result):
        if opcode == 'LOAD':
            _, dest_reg = operands
            self.registers[dest_reg] = result

    def run(self):
        while True:
            instruction = self.fetch()
            if instruction is None:
                break

            opcode, operands = self.decode(instruction)
            ula_result = None

            if opcode not in ['BEQ', 'J']:
                ula_result = self.execute(opcode, operands)

            memory_access_result = self.access_memory(opcode, operands)

            if ula_result is not None:
                self.write_back(opcode, operands, ula_result)

            self.clock_cycles += 1

            print("Instruction:", instruction)
            print("Registers:", self.registers)
            print("Memory:", self.memory)
            print("Clock cycles:", self.clock_cycles)
            print()

instructions = [
    ('ADD', (1, 2, 3)),
    ('SUB', (3, 4, 4)),
    ('LOAD', (100, 6)),
    ('STORE', (7, 200)),
    ('BEQ', (1, 2, 2)),  # Exemplo de instrução de desvio condicional
    ('J', (10,)),  # Exemplo de instrução de salto
]

simulator = PipelineSimulator(instructions)
simulator.run()

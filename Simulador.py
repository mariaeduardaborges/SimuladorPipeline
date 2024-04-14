class PipelineSimulator:

    def __init__(self, instructions):

        self.instructions = instructions
        self.registers = [0] * 8
        self.registers[1] = 10
        self.registers[2] = 5
        self.memory = [0] * 1000
        self.memory[100] = 20
        self.pc = 0
        self.clock_cycles = 0

    def fetch(self):

        instruction = self.instructions[self.pc]
        self.pc += 1
        return instruction

    def execute(self, instruction):

        opcode, operands = instruction
        if opcode == 'ADD':
            reg1, reg2, dest_reg = operands
            self.registers[dest_reg] = self.registers[reg1] + self.registers[reg2]
        elif opcode == 'SUB':
            reg1, reg2, dest_reg = operands
            self.registers[dest_reg] = self.registers[reg1] - self.registers[reg2]
        elif opcode == 'LOAD':
            addr, dest_reg = operands
            self.registers[dest_reg] = self.memory[addr]
        elif opcode == 'STORE':
            src_reg, addr = operands
            self.memory[addr] = self.registers[src_reg]

    def access_memory(self, instruction):

        opcode, operands = instruction
        if opcode == 'LOAD':
            addr, _ = operands
            return self.memory[addr]
        elif opcode == 'STORE':
            _, addr = operands
            return addr
        else:
            return None

    def write_back(self, instruction, result):

        opcode, operands = instruction
        if opcode == 'LOAD':
            _, dest_reg = operands
            self.registers[dest_reg] = result
        elif opcode == 'STORE':
            pass
        else:
            pass

    def ula_stage(self, instruction):

        opcode, operands = instruction
        if opcode == 'ADD':
            reg1, reg2, _ = operands
            return self.registers[reg1] + self.registers[reg2]
        elif opcode == 'SUB':
            reg1, reg2, _ = operands
            return self.registers[reg1] - self.registers[reg2]
        else:
            return None

    def run(self):

        while self.pc < len(self.instructions):
            instruction = self.fetch()
            ula_result = self.ula_stage(instruction)
            memory_access_result = self.access_memory(instruction)
            self.execute(instruction)
            self.write_back(instruction, ula_result)
            self.clock_cycles += 1
            print("ULA result:", ula_result)
            print("Memory access result:", memory_access_result)

        print("Simulation complete.")
        print("Registers:", self.registers)
        print("Memory:", self.memory)
        print("Clock cycles:", self.clock_cycles)


instructions = [
    
    ('ADD', (1, 2, 3)),
    ('SUB', (3, 4, 4)),
    ('LOAD', (100, 6)),
    ('STORE', (7, 200)),
]

simulator = PipelineSimulator(instructions)
simulator.run()
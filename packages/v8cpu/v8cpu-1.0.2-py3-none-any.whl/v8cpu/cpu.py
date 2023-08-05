# -*- coding: utf-8 -*-
from typing import List, Union

MAX_MEMORY_SIZE = 256
MAX_REGISTER_NUM = 16


class Machine:
    memory: List[int] = None  # Main Memory
    r: List[int] = None  # Register
    pc: int = None  # Program Counter Register
    count: int = 0  # How many instructions have been executed

    def __init__(self):
        self.clear()

    def memcpy(self, data: Union[int, str, List[Union[int, str]]], start=0):
        if type(data) == int:
            assert(0 <= data < 256)
            data = [data]
        elif type(data) == str:
            assert(len(data) % 2 == 0)
            data = [int(data[i:i+2], base=16) for i in range(0, len(data), 2)]
        elif type(data) == list:
            if len(data) > 0 and type(data[0]) == str:
                L = []
                for s in data:
                    L += [int(s[i:i+2], base=16) for i in range(0, len(s), 2)]
                data = L
        else:
            raise NotImplementedError
        assert(all(type(i) == int for i in data))
        assert(all(0 <= i < 256 for i in data))
        assert(start+len(data) < 256)
        for i, c in enumerate(data):
            self.memory[start+i] = c

    def run(self, step_limit=None):
        # run util C000
        while(True):
            if self.step():
                return True
            if step_limit != None and self.count >= step_limit:
                raise Exception('Time Limit Exceeded')

    def step(self) -> bool:
        # step program, if C000 return True
        self.count += 1
        if self.pc+2 > 256:
            raise Exception('PC out of range')
        instruction = self.memory[self.pc]*256+self.memory[self.pc+1]
        self.instruction = str_instruction = hex(
            instruction)[2:].upper().zfill(4)
        opcode = instruction >> 12
        R = (instruction >> 8) & 0xF
        X = (instruction >> 4) & 0xF
        Y = instruction & 0xF
        XY = instruction & 0xFF
        self.pc += 2
        illegalError = Exception('Illegal instruction "{}" at position {}'.format(
            str_instruction, self.pc-2))
        if opcode == 1:
            self.r[R] = self.memory[XY]
        elif opcode == 2:
            self.r[R] = XY
        elif opcode == 3:
            self.memory[XY] = self.r[R]
        elif opcode == 4:
            if R != 0:
                raise illegalError
            self.r[Y] = self.r[X]
        elif opcode == 5:
            self.r[R] = (self.r[X]+self.r[Y]) & 0xFF
        elif opcode == 6:
            raise illegalError
        elif opcode == 7:
            self.r[R] = self.r[X] | self.r[Y]
        elif opcode == 8:
            self.r[R] = self.r[X] & self.r[Y]
        elif opcode == 9:
            self.r[R] = self.r[X] ^ self.r[Y]
        elif opcode == 10:
            if X != 0:
                raise illegalError
            a = bin(self.r[R])[2:]
            a = a[-Y % 8:]+a[:-Y % 8]
            self.r[R] = int(a, base=2)
        elif opcode == 11:
            if self.r[R] == self.r[0]:
                self.pc = XY
        elif opcode == 12:
            if R != 0 or XY != 0:
                raise illegalError
            return True
        else:
            raise illegalError
        return False

    def clear(self):
        self.memory = [0 for i in range(256)]
        self.r = [0 for i in range(16)]
        self.pc = self.count = 0


def test():
    cpu = Machine()
    assert(all(i == 0 for i in cpu.r))
    assert(all(i == 0 for i in cpu.memory))
    assert(cpu.pc == cpu.count == 0)
    cpu.memcpy(['2F01', '40F0', '51F0', '31A0', 'C000'])
    assert(cpu.step() == False)
    assert(cpu.pc == 2 and cpu.r[0xF] == 1 and cpu.count == 1)
    assert(cpu.step() == False)
    assert(cpu.pc == 4 and cpu.r[0x0] == 1 and cpu.count == 2)
    assert(cpu.step() == False)
    assert(cpu.pc == 6 and cpu.r[0x1] == 2 and cpu.count == 3)
    assert(cpu.step() == False)
    assert(cpu.pc == 8 and cpu.memory[0xA0] == 2 and cpu.count == 4)
    assert(cpu.step() == True)
    cpu.clear()
    assert(all(i == 0 for i in cpu.r))
    assert(all(i == 0 for i in cpu.memory))
    assert(cpu.pc == cpu.count == 0)
    cpu.memcpy(['2001', '7100', '5000', '9201', '8202',
                '2000', '5222', 'B212', 'B00C', 'C000'])
    while(not cpu.step()):
        pass
    assert(cpu.count == 27)
    print('OK!')


if __name__ == "__main__":
    test()

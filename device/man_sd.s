@LSC SD to zero
and r0, r0, #0x0
str.w r0, [r4, #0x78]
str.w r0, [r4, #0x7C]
str.w r0, [r4, #0x80]
str.w r0, [r4, #0x84]

@Execute missed instruction
ldrb.w r0, [r4, #0x57]

@Jump to trigger_addr + 5
b 0xAE4B9

@Execute first missed instructions
@ r1 points to SK
add r1, sp, #0x8

@ save registers
push {{r0, r2}}

@Prepare addr to store SK
ldr r0, =#0x20077C
ldr r2, [r1]
str r2, [r0]
ldr r2, [r1, #0x4]
str r2, [r0, #0x4]
ldr r2, [r1, #0x8]
str r2, [r0, #0x8]
ldr r2, [r1, #0xc]
str r2, [r0, #0xc]

@ restore registers
pop {{r0, r2}}

@Execute second missed instruction
mov r0, r4

@Jump to trigger_addr + 5
b 0xAE5B9

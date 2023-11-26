@Execute first missed instructions
@ r1 points to SK
add r1, sp, #0x8

@ save registers
push {{r0, r2}}

@Prepare addr to store SK entropy
ldr r0, =#0x20078C

@Copy SK entropy
ldr r2, [r4, #0xa7]
str r2, [r0]

@ restore registers
pop {{r0, r2}}

@Execute second missed instruction
mov r0, r4

@Jump to trigger_addr + 5
b 0xAE711

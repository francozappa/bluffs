@ Load second parameter for isMssInstantPassed
ldr r1, [r6, #0x0]

@Call isMssInstantPassed
bl #0xa63fe

@Overwrite return value
mov r0, #0x1

@Jump to trigger_addr + 7
b 0xA6443

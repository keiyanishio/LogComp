; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data
formatin: db "%d", 0
formatout: db "%d", 10, 0 ; newline, null terminator
scanint: times 4 db 0 ; 32-bit integer = 4 bytes

segment .bss
res RESB 1

section .text
global _main ; windows
extern _scanf ; windows
extern _printf ; windows
extern _fflush
extern _stdout

; subrotinas if/while
binop_je:
    JE binop_true
    JMP binop_false
binop_jg:
    JG binop_true
    JMP binop_false
binop_jl:
    JL binop_true
    JMP binop_false
binop_false:
    MOV EAX, False
    JMP binop_exit
binop_true:
    MOV EAX, True
binop_exit:
    RET

main:
    PUSH EBP ; guarda o base pointer
    MOV EBP, ESP ; estabelece um novo base pointer

PUSH DWORD 0
PUSH DWORD 0
PUSH DWORD 0
PUSH scanint
PUSH formatin
call _scanf
ADD ESP, 8
MOV EAX, DWORD [scanint]
MOV [EBP-8], EAX
MOV EAX, 1
MOV [EBP-12], EAX
MOV EAX, 2
MOV [EBP-4], EAX
LOOP_32:
MOV EAX, 1
PUSH EAX
MOV EAX, [EBP-8]
POP EBX
ADD EAX, EBX
PUSH EAX
MOV EAX, [EBP-4]
POP EBX
CMP EAX, EBX
CALL binop_jl
CMP EAX, False
JE EXIT_32
MOV EAX, [EBP-4]
PUSH EAX
MOV EAX, [EBP-12]
POP EBX
IMUL EBX
MOV [EBP-12], EAX
MOV EAX, 1
PUSH EAX
MOV EAX, [EBP-4]
POP EBX
ADD EAX, EBX
MOV [EBP-4], EAX
JMP LOOP_32
EXIT_32:
MOV EAX, [EBP-12]
PUSH EAX
PUSH formatout
CALL _printf
ADD ESP, 8
; interrupcao de saida (default)
PUSH DWORD [_stdout]
CALL _fflush
ADD ESP, 4
MOV ESP, EBP
POP EBP
MOV EAX, 1
XOR EBX, EBX
INT 0x80
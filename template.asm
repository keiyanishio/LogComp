; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0
segment .data
formatin : db ”%d” , 0
formatout : db ”%d” , 10 , 0 ; newline , nul terminator
scanint : times 4 db 0 ; 32− b i t s i n t e g e r = 4 bytes
segment .bss ; variaveis
res RESB 1
section .text

global _main ; windows

extern _scanf ; windows

extern _printf ; windows
extern fflush
extern stdout

; subrotinas i f / while
binop_je :
JE binop_true
JMP binop_false
binop_jg :
JG binop_true
JMP binop_false
binop_jl :
JL binop_true
JMP binop_false
binop_false :
MOV EAX, False
JMP binop_exit
binop_true :
MOV EAX, True
binop_exit :
RET


main :
PUSH EBP ; guarda o base pointer
MOV EBP, ESP ; e s t a b e l e c e um novo base pointer
; codigo gerado pelo compilador
PUSH DWORD 0 ; var i i n t [EBP−4]
PUSH DWORD 0 ; var n i n t [EBP−8]
PUSH DWORD 0 ; var f i n t [EBP−12]
PUSH scanint ; endereço de memória de suporte
PUSH formatin ; formato de entrada ( i n t )
c a l l scanf
ADD ESP, 8 ; Remove os argumentos da pilha
MOV EAX, DWORD [ scanint ] ; retorna o valor l i d o em EAX
MOV [EBP−8] , EAX ; n = Scanln ( )
MOV EAX, 1
MOV [EBP−12] , EAX ; f = 1
; i n i c i a l i z a c a o do loop
MOV EAX, 2
MOV [EBP−4] , EAX ; i = 2
LOOP_34:
MOV EAX, 1
PUSH EAX ; empilha 1
MOV EAX, [EBP−8] ; recupera n
POP EBX
ADD EAX, EBX ; n + 1
PUSH EAX ; empilha n + 1

; c o n d i c i o n a l do loop
MOV EAX, [EBP−4]; recupera i
POP EBX
CMP EAX, EBX
CALL binop_jl ; i < n + 1
CMP EAX, False ; se a condição f o r f a l s a , s a i
JE EXIT_34
; bloco de comandos
MOV EAX, [EBP−4]; i
PUSH EAX ; empilha i
MOV EAX, [EBP−12]; f
POP EBX ; desempilha i
IMUL EBX ; f ∗ i
MOV [EBP−12] , EAX ; f = f ∗ i
; incremento
MOV EAX, 1
PUSH EAX ; empilha 1
MOV EAX, [EBP−4]
POP EBX
ADD EAX, EBX ; i + 1
MOV [EBP−4] , EAX ; i = i + 1
JMP LOOP_34
EXIT_34 :
MOV EAX, [EBP−12]
PUSH EAX ; empilha f
PUSH formatout ; formato i n t de saida
CALL p r i n t f ; Print f
ADD ESP, 8 ; limpa os argumentos



; interrupcao de saida ( d e f a u l t )
PUSH DWORD [stdout]
CALL fflush
ADD ESP, 4
MOV ESP, EBP
POP EBP
MOV EAX, 1
XOR EBX, EBX
INT 0x80

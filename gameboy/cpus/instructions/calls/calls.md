# Documentação de Instruções: Família CALL

## CALL NN
**Instruction:** `CALL NN`  
**Parâmetros possíveis:** `(nn)`  
**Descrição:** Pega o imediato de 16 Bits, adiciona o program counter atual na stack e reatribui o valor do program counter para o valor do imediato pego. 

## CALL CC NN
**Instruction:** `CALL CC NN`
**Parâmetros possíveis:** `(Z, C, NZ, NC)`
**Descrição:** Pega o imediato de 16 bits, checa se a condição passada pelo parametro é verdadeira, caso seja, adiciona o program counter atual para stack e passa o valor imediato ao program counter
**Explicação dos parametros:**
`Z`: checa se a flag zero é igual a 1
`C`: checa se a flag carry é igual a 1
`NZ`: checa se a flag zero é diferente de 1
`NC`: checa se a flag carry é diferente de 1
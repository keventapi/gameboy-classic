# Documentação de Instruções: Família ADD

## ADD A, N
**Instruction:** `ADD A N`  
**Parâmetros possíveis:** `(A, B, C, D, E, H, L, (HL), #)`  
**Descrição:** Adiciona o valor do parâmetro ao registrador A.

**Flags:**
* **Z:** 0 ou 1 dependendo do valor resultante.
* **N:** Sempre 0.
* **H:** 1 se houver half-carry, se não 0.
* **C:** 1 se houver carry, se não 0.

---

## ADC A, N
**Instruction:** `ADC A N`  
**Parâmetros possíveis:** `(A, B, C, D, E, H, L, (HL), #)`  
**Descrição:** Pega o valor da flag Carry e o valor do parâmetro e adiciona ao registrador A.

**Flags:**
* **Z:** 0 ou 1 dependendo do valor resultante.
* **N:** Sempre 0.
* **H:** 1 se houver half-carry, se não 0.
* **C:** 1 se houver carry, se não 0.

---

## ADD HL, N
**Instruction:** `ADD HL N`  
**Parâmetros possíveis:** `(BC, DE, HL, SP)`  
**Descrição:** Pega o valor de HL e adiciona o valor do parâmetro. Após isso, quebra o resultado em 8 bits e passa respectivamente para H os 8 bits mais significantes e para L os 8 bits menos significantes.

**Flags:**
* **Z:** Mantém o valor atual (não afetada).
* **N:** Sempre 0.
* **H:** 1 se houver half-carry, se não 0.
* **C:** 1 se houver carry, se não 0.

---

## ADD SP, N
**Instruction:** `ADD SP N`  
**Parâmetros:** `(#)`  
**Descrição:** Pega o valor imediato, transforma-o em um imediato assinado (signed) e adiciona ao Stack Pointer (SP).

**Flags:**
* **Z:** Sempre 0.
* **N:** Sempre 0.
* **H:** 1 caso haja half-carry considerando o valor do imediato como não assinado, se não 0.
* **C:** 1 caso haja carry considerando o valor do imediato como não assinado, se não 0.

---

### Glossário de Nomenclaturas

* **`#` (Imediato):** Valor constante extraído diretamente do fluxo de instruções (ROM).
* **`(HL)` (Referencial):** Indica que o parâmetro é o dado contido no endereço de memória apontado pelo par de registradores HL (`mmu.read(hl)`).
* **Half-Carry (H):** Indica se houve transporte do bit 3 para o bit 4 (em 8 bits) ou do bit 11 para o 12 (em 16 bits).
* **Carry (C):** Indica se o resultado da operação excedeu a capacidade do registrador (overflow).
* **assinado:** Checa o bit mais significante (MSB). Se for 1, o valor é tratado como negativo; se for 0, é tratado como positivo.
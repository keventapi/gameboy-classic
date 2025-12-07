# 🎮 GameBoy Emulator - Componentes de Memória

Este projeto visa a emulação do console Game Boy (DMG-01), com foco na implementação precisa do subsistema de memória, que inclui a RAM interna, VRAM, o *mirroring* de memória, o mapeamento de memória *switchable* e o controlador de banco de memória (MBC).

## 🧠 Arquitetura de Memória

A memória do Game Boy é acessada através de um mapa de endereços de $0000 a $FFFF. A implementação atual foca em simular as seguintes classes e seus comportamentos:

---

### 💾 Classes `RAM` e `VRAM` (gameboy/memory/ram.py)

#### 🔸 Classe `RAM` (WRAM)

Simula a **RAM de Trabalho Interna (WRAM)** do Game Boy.

* **RAM Real:** Situada na faixa de endereços `[0xC000, 0xE000[`.
* **Memória Espelhada (Echo RAM):** A RAM é espelhada (mirroring) na faixa `[0xE000, 0xFE00[`.
    * **Ação:** Qualquer leitura ou escrita nesta faixa espelhada reflete-se **diretamente** no endereço correspondente da RAM real (ex: escrever em `0xE000` é o mesmo que escrever em `0xC000`).

#### 🔸 Classe `VRAM` (Video RAM)

Simula a **Memória de Vídeo**.

* **Status Atual:** Possui apenas métodos simples de **leitura e escrita**.
* **Observação:** O chip gráfico (PPU) ainda não foi implementado. Futuramente, acessos à VRAM precisarão ser controlados e restritos durante certos modos de operação do PPU.

---

### 🔄 Memória Chaveada (*Switchable Memory*)

O hardware original do Game Boy não suporta ler toda a memória da ROM ou da RAM do cartucho de uma só vez. Por isso, a memória é separada em **bancos (banks)**, e apenas um pequeno pedaço é mapeado para a CPU por vez.

* **Conceito:** São blocos de memória que podem ser trocados (*switched*) pelo **MBC** para que a CPU possa acessá-los.

#### 📝 Padding ($FF - Endereço Nulo)

* **Valor Nulo:** O valor **$FF** (255 em decimal) é retornado quando a CPU tenta ler um endereço de memória que não está mapeado para nenhum hardware (RAM, ROM, VRAM ou I/O).
* **Importância:** Este valor é o comportamento esperado para a CPU em regiões não implementadas ou "vazias", pois o código de operação `$FF` não corresponde a nenhuma instrução válida no Game Boy.

---

### 🕹️ Memory Bank Controller (MBC) - (gameboy/memory/mbc.py)

O `MBC` é um chip dentro do cartucho do jogo que define o comportamento de leitura e escrita para as memórias *switchable* (ROM e RAM externa do cartucho).

* **Função:** O MBC **decide qual banco de ROM ou RAM** estará visível para a CPU em um dado momento.
* **Controle:** O MBC usa faixas de endereços no espaço de I/O do Game Boy para **receber comandos**. A escrita nesses endereços **não armazena dados**, mas sim define *flags* que mudam o banco ativo.
* **Comportamento Específico:** Cada MBC (MBC1, MBC3, MBC5, etc.) tem regras de escrita e *flags* diferentes.
    * **MBC1 Exemplo:** A troca de banco pode ser feita por dois pinos, onde um conjunto específico de regras de escrita deve ser obedecido para que a ação (mudança de banco) seja executada.
* **Funcionalidades Extras (Futuras Implementações):**
    * **MBC3:** Possui um Real-Time Clock (RTC).
    * **MBC5:** Pode incluir funcionalidades extras, como leitor infravermelho.

    ## Referências

[GBCPUman v1.01](https://dn721904.ca.archive.org/0/items/gbcpuman_v1.01/GBCPUman.pdf)

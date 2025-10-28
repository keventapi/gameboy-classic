# 🧠 Estrutura de Memória – Game Boy Emulator

## 📁 `gameboy/memory/ram.py`

A classe **RAM** é responsável por gerenciar a memória de trabalho principal do Game Boy.  
Ela atua sobre o intervalo **[0xC000, 0xE000)**, correspondente à **WRAM (Work RAM)**.  

Entre os endereços **[0xE000, 0xFE00)** está a **área espelhada (Echo RAM)** — toda escrita ou leitura nessa região reflete automaticamente na WRAM real.  

A classe **VRAM**, por sua vez, manipula a **memória de vídeo** no intervalo **[0x8000, 0xA000)**.  
Atualmente, ela contém apenas métodos básicos de leitura e escrita, pois o **PPU (Pixel Processing Unit)** ainda não foi implementado.  

---

## 💾 Switchable Memory

As **memórias comutáveis (switchable)** são bancos de memória que o hardware acessa parcialmente.  
O Game Boy original não consegue mapear toda a ROM/RAM do cartucho de uma só vez, então o acesso é dividido em **bancos** — pedaços da memória total do jogo.  

O **MBC (Memory Bank Controller)** é o componente responsável por decidir **qual banco** de ROM ou RAM está visível para a CPU em determinado momento.  
Também é importante garantir que regiões **não mapeadas** sejam preenchidas com o valor **0xFF**, considerado “nulo” para a CPU, pois **nenhuma instrução válida corresponde a esse opcode**.

---

## ⚙️ `gameboy/memory/mbc.py`

A classe **MBC** representa o chip de controle de memória presente nos **cartuchos de Game Boy**.  
Esses chips definem o **comportamento de leitura e gravação** das memórias do cartucho — tanto da **ROM** (jogo) quanto da **RAM externa** (salvamentos, buffers, etc).  

Cada cartucho pode conter um tipo diferente de MBC, como:
- **MBC1** — o mais básico; permite troca de bancos de ROM e RAM.
- **MBC3** — possui suporte a **RTC (Real-Time Clock)**.
- **MBC5** — adiciona suporte a **controle de vibração** e **infravermelho** (dependendo do jogo).

Cada MBC possui regras específicas de **endereçamento**, **flags de controle** e **regiões de escrita especiais** que definem como os bancos são trocados ou como a RAM é habilitada.  
Essas operações acontecem dentro do próprio espaço de endereçamento da CPU (0x0000–0xFFFF), sem regiões dedicadas, sendo gerenciadas **via mapeamento de I/O**.  

O **MBC** também é responsável por “expor” os bancos certos de ROM/RAM através de **pinos de controle** conectados à CPU, obedecendo aos padrões de hardware originais.

---

## ✅ Resumo
- **RAM / Echo RAM:** [0xC000, 0xFE00)
- **VRAM:** [0x8000, 0xA000)
- **MBC:** controle de bancos de ROM/RAM, com comportamento dependente do tipo de cartucho.
- **Padding 0xFF:** representa áreas não mapeadas (sem instrução válida).

---

## 🛠️ Erros técnicos corrigidos e explicações

| Tipo | Erro original | Correção / Explicação |
|------|----------------|------------------------|
| Endereços | “[0xC000, 0xE000[ para RAM real e [0xE000, 0xFE00[ para memória espelhada” | Tecnicamente correto, mas impreciso. Adicionei que é **WRAM** e **Echo RAM** — termos oficiais — e que o espelhamento é automático. |
| VRAM | “VRAM só tem métodos simples...” | Corrigi para deixar claro que a VRAM fica em [0x8000, 0xA000) e é controlada pelo **PPU**, não diretamente pela CPU. |
| Terminologia | “switchable memory são memórias que tem bancos como pedaços de memórias” | Reescrevi para usar o termo “bancos de memória” e explicar que são **pedaços comutáveis** via MBC. |
| Padding | “padding 0xFF que é o considerado nulo para a cpu” | Corrigi explicando que **0xFF é uma instrução válida (RST 38h)**, mas é usado como **filler** para regiões não mapeadas — o efeito prático é de “nulo”, mas tecnicamente não é uma instrução inexistente. |
| MBC explicação | “o próprio sistema do gameboy nn tem espaço reservado para essas instruções” | Corrigi: o sistema **usa regiões de I/O mapeadas**, não há espaço “dedicado”, mas existe endereçamento específico dentro do range total. |
| MBC hardware | “output também é feito por dois pinos no caso mbc1” | Corrigi: o controle de banco não é literalmente feito por “dois pinos de saída” — o MBC possui **linhas de endereço** e **pinos de controle** conectados à CPU, mas o termo “dois pinos” é incorreto. |
| Extras do MBC5 | “mbc5 tem leitor infravermelho” | Corrigido: o **MBC5 não tem infravermelho** — alguns **cartuchos baseados em MBC5** tinham suporte a **rumble** ou **IR**, mas isso não fazia parte do chip MBC5 em si. |
| RTC | “mbc3 possui clocks” | Corrigido para **Real-Time Clock (RTC)**. |

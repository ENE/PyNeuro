```console
$ python status-callbacks.py
```
Se o PyNeuro não encontrar um TinkGear Connector ao qual se conectar, simplesmente vai encerrar-se por exceção. Ou seja, nem chegará a existir oportunidade para configuração de _callbacks_...
```ini
[PyNeuro] Nenhuma conexão pôde ser feita porque a máquina de destino as recusou ativamente
[PyNeuro] Perhaps the ThinkGear Connect (TGC) is not running
[PyNeuro] Stop Packet Parser
```
Caso ele consiga se conectar a um TGC, deverá ser assim:
```ini
[PyNeuro] Connecting TCP Socket Host...
Buscando o headset... (fase 1 de 3)
[PyNeuro] Scanning device..
Aguardando dados de EEG... (fase 2 de 3)
[PyNeuro] Fitting Device..
```
Quando o usuário posicionar corretamente o dispositivo na sua cabeça:
```ini
Conectado! Sinal de qualidade ótima
[PyNeuro] Successfully Connected ..
```
Em caso de retirada de eletrodo ou de loop:
```ini
Conexão ainda deve melhorar (fase 3 de 3)
[PyNeuro] Ajustando (fase 3 de 3) com pLevel = 54
Conectado! Sinal de qualidade ótima
[PyNeuro] Successfully Connected ..
Conexão ainda deve melhorar (fase 3 de 3)        
[PyNeuro] Ajustando (fase 3 de 3) com pLevel = 54
Conectado! Sinal de qualidade ótima
[PyNeuro] Successfully Connected ..
```
A inconstância permanece até a otimização plena do sinal.

Se eletrodo e loop desencaixarem:
```ini
Conexão ainda deve melhorar (fase 3 de 3)        
[PyNeuro] Ajustando (fase 3 de 3) com pLevel = 54
Conectado! Sinal de qualidade ótima
[PyNeuro] Successfully Connected ..
Conexão ainda deve melhorar (fase 3 de 3)        
[PyNeuro] Ajustando (fase 3 de 3) com pLevel = 54
Aguardando dados de EEG... (fase 2 de 3)
[PyNeuro] Fitting Device..
```
A volta poderá ser com inconstâncias ou não.

No caso do desligamento através do botão físico:
```ini
Conexão ainda deve melhorar (fase 3 de 3)
[PyNeuro] Ajustando (fase 3 de 3) com pLevel = 80
Aguardando dados de EEG... (fase 2 de 3)
[PyNeuro] Fitting Device..
Desconectado, sem qualquer sinal
[PyNeuro] Connection lost, trying to reconnect..
```
E no religamento pelo botão:
```ini
Aguardando dados de EEG... (fase 2 de 3)
[PyNeuro] Fitting Device..
Conectado! Sinal de qualidade ótima
[PyNeuro] Successfully Connected ..
```
Podendo existir inconstâncias ou não.

Obviamente, encerramento por parte do TGC ou na camada de rede irão parar tudo:
```ini
[PyNeuro] Stop Packet Parser
```
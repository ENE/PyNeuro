Nesse arquivo de texto faz-se uma depuração dos "status" básicos existentes
durante uma utilização do headset, frente a usuário final, não ao parser.

```console
$ python status-test.py 
[PyNeuro] Connecting TCP Socket Host...
[PyNeuro] error
[PyNeuro] status: scanning
[PyNeuro] Scanning device..
[PyNeuro] status: scanning
[PyNeuro] status: scanning
[PyNeuro] status: scanning
[PyNeuro] status: scanning
[PyNeuro] poorSignalLevel [0-200]: 25
[PyNeuro] Fitting Device..
[PyNeuro] poorSignalLevel [0-200]: 0
[PyNeuro] poorSignalLevel [0-200]: 0
[PyNeuro] poorSignalLevel [0-200]: 0
[PyNeuro] poorSignalLevel [0-200]: 0
[PyNeuro] Successfully Connected ..
[PyNeuro] poorSignalLevel [0-200]: 0
[PyNeuro] poorSignalLevel [0-200]: 0
[PyNeuro] poorSignalLevel [0-200]: 0
[PyNeuro] poorSignalLevel [0-200]: 0
```
Passado um tempo, eventualmente:
```console
[PyNeuro] poorSignalLevel [0-200]: 0
[PyNeuro] poorSignalLevel [0-200]: 0
[PyNeuro] poorSignalLevel [0-200]: 25
[PyNeuro] poorSignalLevel [0-200]: 0
[PyNeuro] poorSignalLevel [0-200]: 0
```
Experimentando mexer no eletrodo:
```console
[PyNeuro] poorSignalLevel [0-200]: 0
[PyNeuro] poorSignalLevel [0-200]: 0
[PyNeuro] poorSignalLevel [0-200]: 51
[PyNeuro] poorSignalLevel [0-200]: 80
[PyNeuro] poorSignalLevel [0-200]: 51
[PyNeuro] poorSignalLevel [0-200]: 25
[PyNeuro] poorSignalLevel [0-200]: 51
[PyNeuro] poorSignalLevel [0-200]: 54
[PyNeuro] poorSignalLevel [0-200]: 25
[PyNeuro] poorSignalLevel [0-200]: 25
```
Ou experimentando retirar o eletrodo: 
```console
[PyNeuro] poorSignalLevel [0-200]: 51
[PyNeuro] poorSignalLevel [0-200]: 55
[PyNeuro] poorSignalLevel [0-200]: 55
[PyNeuro] poorSignalLevel [0-200]: 55
[PyNeuro] poorSignalLevel [0-200]: 55
[PyNeuro] poorSignalLevel [0-200]: 200
[PyNeuro] Fitting Device..
[PyNeuro] poorSignalLevel [0-200]: 200
[PyNeuro] poorSignalLevel [0-200]: 200
[PyNeuro] poorSignalLevel [0-200]: 200
[PyNeuro] poorSignalLevel [0-200]: 200
[PyNeuro] poorSignalLevel [0-200]: 200
[PyNeuro] poorSignalLevel [0-200]: 200
```
Sem loop, sem eletrodo:
```console
[PyNeuro] poorSignalLevel [0-200]: 200
[PyNeuro] poorSignalLevel [0-200]: 200
[PyNeuro] poorSignalLevel [0-200]: 200
```
Conexão encerrada pelo usuário através do TGC:
```console
[PyNeuro] Stop Packet Parser
```
Observou-se que:

- O único "status" retornado foi: `scanning`
- Qualquer valor diferente disso, é tido como `nosignal`
- Do código atual: `atenção+meditação=0` também é `"fitting"`

 Resumindo, para os cinco ícones da Neurosky, podemos ter:
```basic
 connected
   if poorSignalLevel < 50
   and attention + meditation != 0

 fitting1
   if status == "scanning"

 fitting2
   if attention + meditation == 0
   or poorSignalLevel > 100

 fitting3
   if poorSignalLevel <= 100 
   and poorSignalLevel >= 50 

 nosignal
   if status and status != "scanning"
```
O teste a seguir realmente sinalizou pelo menos uma quase-equivalência, a respeito do poorSignalLevel:
```
[PyNeuro] status: scanning
[PyNeuro] Fitting Device..
Att:  30   pLevel:   0   Med:  30
[PyNeuro] Successfully Connected ..
Att:  14   pLevel:   0   Med:  21
Att:  34   pLevel:   0   Med:  16
Att:  47   pLevel:   0   Med:  10
Att:  69   pLevel:   0   Med:   8
Att:  88   pLevel:   0   Med:  10
Att:  80   pLevel:   0   Med:  14
Att:  74   pLevel:   0   Med:  11
Att:  63   pLevel:   0   Med:  27
Att:  69   pLevel:   0   Med:  27
Att:  77   pLevel:   0   Med:  34
Att:  66   pLevel:   0   Med:  56
Att:  70   pLevel:   0   Med:  47
Att:  60   pLevel:   0   Med:  48
Att:  51   pLevel:   0   Med:  48
Att:  63   pLevel:   0   Med:  41
Att:  54   pLevel:   0   Med:  35
Att:  60   pLevel:   0   Med:  74
Att:  70   pLevel:   0   Med:  77
Att:  57   pLevel:   0   Med:  87
Att:  30   pLevel:   0   Med:  56
Att:  43   pLevel:   0   Med:  44
Att:  51   pLevel:   0   Med:  60
[PyNeuro] Stop Packet Parser
```
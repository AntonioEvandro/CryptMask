# CryptMask

Segurança e privacidade sempre!

Evite que arquivos sejam bisbilhotados.
Criptografe seus arquivos e mascare-os como um arquivo de vídeo.

---

## Requesitos

- Python 3.1 ou superior

---

## Estrutura

```txt
CryptMask/
    run.py
    README.md
    functions/
        core.py
        encoder.py
        decoder.py
        menu.py
    utils/
    inputs/             %%Arquivos a codificar%%
    outputs/            %%Arquivos de vídeo gerados%%
    decripts/           %%Arquivos decodificados%%
```

## Uso

```python
py run.py
```

Menu interativo guia todas as operações. Em qualquer prompt:

- **Enter**             %%Confirma a opção padrão%%
- **0**                 %%Volta ao menu principal%%
- **q**                 %%Encerra o programa%%

---

## Fluxo típico

### Codificar

1. Coloque o arquivo na pasta `inputs/`
2. Execute `python run.py`
3. Escolha a opção **1**
4. Digite o nome do arquivo (ex: `bacup.zip`)
5. Enter para salvar em `outputs/` com nome automático

Para arquivos acima de 3 GB, o programa pergunta se deseja dividir em partes.
As partes são nomeadas `nome.split1.mp4`, `nome.split2.mp4`, etc.

### Decodificar

1. Coloque o(s) `.mp4` na pasta `outputs/`
2. Execute `python run.py`
3. Excolha a opção **2**
4. Digite o nome do arquivo (ex: `backup.mp4` ou `backup.split1.mp4`)
5. Enter para salvar em `decrypts/` com o nome original restaurado

Para arquivos split, basta informar qualquer uma das partes -
o programa localiza e reconstitui as demais automaticamente.

---

## Como funciona

### Estrutura do .mp4 gerado

```txt
[ ftyp box  —  24 bytes      ]  tipo do container
[ free box  —  8.631 bytes   ]  metadados de vídeo (moov)
[ free box  —  8 + N bytes   ]  dados ficam aqui
[ mdat box  —  8 bytes       ]  fechamento do arquivo
```

### Payload interno

```txt
GFCRYPT2      (8 bytes)   assinatura
tipo          (1 byte)    0 = arquivo único  |  1 = parte de split
idx           (2 bytes)   índice da parte (0 se único, 1..N se split)
total_partes  (2 bytes)   total de partes (1 se único)
len_nome      (2 bytes)   tamanho do nome original
nome          (N bytes)   nome original em UTF-8
len_dados     (8 bytes)   tamanho dos dados desta parte
dados         (M bytes)   bytes do arquivo original
```

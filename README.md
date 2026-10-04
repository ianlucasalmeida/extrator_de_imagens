# Extrator de Imagens Botânicas

Pipeline para varrer PDFs e PowerPoints contendo bancos de imagens botânicas,
extrair as imagens, identificar a espécie (via BioCLIP local ou Pl@ntNet API),
e gerar:

- Uma pasta `saida/imagens/` com imagens nomeadas por espécie
- `saida/padronizacao.txt` com as convenções e espécies encontradas
- `saida/inventario.csv` e `saida/inventario.json` com metadados de cada imagem
- `saida/log.txt` com o rastro de execução

## Instalação

\`\`\`powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
\`\`\`

Para identificação local (opcional, sem conta em API):
\`\`\`powershell
python -m pip install -r requirements-local.txt
\`\`\`

## Uso

Coloque os PDFs/PPTXs em `entrada/` e rode:

\`\`\`powershell
python -m src.main
\`\`\`

## Testes

\`\`\`powershell
pytest
\`\`\`

## Modos de identificação

- `local` (padrão): usa BioCLIP, sem internet, sem conta
- `plantnet`: usa a API do Pl@ntNet (requer `PLANTNET_KEY`)

Configure via variável de ambiente `ID_MODE`.
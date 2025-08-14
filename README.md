# LLM-SmartContractScanner

## 1. Description

This project is a tool for analyzing smart contracts using Large Language Models (LLMs) combined with Retrieval-Augmented Generation (RAG). It identifies potential vulnerabilities in source code and retrieves similar contracts for comparison using a vector database. The current version supports only Algorand smart contracts written in Pyteal.

## 2. Requirements

To run this project, make sure you have the following installed:

- Python 3.9+
- Docker
- Docker Compose

## 3. 📂 Preparazione dell’ambiente di lavoro

1. **Creare una cartella di lavoro** sul proprio computer:
   ```bash
   mkdir contract-analysis
   cd contract-analysis

2. Copiare il file docker-compose.yml in questa cartella.
Puoi scaricarlo o copiarlo direttamente dal testo fornito.


3. Creare le cartelle necessarie per input e output:
    ```bash
   mkdir contracts output_report
   ```

    contracts/ → conterrà i file da analizzare
    
    output_report/ → conterrà i report generati


4. Inserire nella cartella contracts/ i file che si desidera analizzare.

## 4. 🚀Avvio dei servizi
Nella cartella di lavore eseguire:
 ```bash
   docker-compose up -d
   ```
Verranno avviati:

qdrant – database vettoriale

api_server – server API

cli_tool – strumento a riga di comando

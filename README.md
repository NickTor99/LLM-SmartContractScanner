# LLM-SmartContractScanner

## 1. Description

This project is a tool for analyzing smart contracts using Large Language Models (LLMs) combined with Retrieval-Augmented Generation (RAG). It identifies potential vulnerabilities in source code and retrieves similar contracts for comparison using a vector database. The current version supports only Algorand smart contracts written in Pyteal.

## 2. Requirements

To run this project, make sure you have the following installed:

- Python 3.9+
- Docker
- Docker Compose

## 3. 👂 Setting up the workspace

1. **Create a workspace folder** on your computer:

   ```bash
   mkdir contract-analysis
   cd contract-analysis
   ```

2. Copy the `docker-compose.yml` file into this folder.\
   You can download it or copy it directly from the provided content.

3. **Create the necessary input and output folders**:

   ```bash
   mkdir contracts output_report
   ```

   - `contracts/` → will contain the files to analyze
   - `output_report/` → will contain the generated reports

4. Place the smart contract files you want to analyze into the `contracts/` folder.

## 4. 🚀 Starting the services

From the workspace folder, run:

```bash
docker-compose up -d
```

This will start the following services:

- **qdrant** – vector database
- **api\_server** – API server
- **cli\_tool** – command-line tool

## 5. 💻 Running the tool from the command line

Once the services are running, you can use the CLI tool interactively or execute a specific analysis:

- **Interactive shell (REPL):**

```bash
docker exec -it cli_tool python cli_shell.py
```

- **Run analysis on a specific file with a chosen model:**

```bash
docker exec -it cli_tool python main.py run --filepath=path/to/contract --model=model_name
```



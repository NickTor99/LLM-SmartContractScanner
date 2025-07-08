# LLM-SmartContractScanner

## 1. Description

This project is a tool for analyzing smart contracts using Large Language Models (LLMs) combined with Retrieval-Augmented Generation (RAG). It identifies potential vulnerabilities in source code and retrieves similar contracts for comparison using a vector database. The current version supports only Algorand smart contracts written in Pyteal.

## 2. Requirements

To run this project, make sure you have the following installed:

- Python 3.9+
- Docker
- pip (Python package installer)

Install the dependencies:

```bash
pip install -r requirements.txt.txt
```

## 3. ⚙️Setup Instructions

### Step 1: Clone the repository

```bash
git clone https://github.com/NickTor99/LLM-SmartContractScanner.git
```

Move to proget directory

```bash
cd path/to/LLM-SmartContractScanner
```

### Step 2: Pull the Vector Database Docker Image (Qdrant)

```bash
docker pull niktor99/sc-vector-db:1.1
```

### Step 3: Start the Database
```bash
docker run -p 6333:6333 niktor99/sc-vector-db:1.1
```

## 4. 🚀Run the Application
### Step 1: Run the API Server
```bash
python vector_db_service/service_db.py
```

### Step 2: Run the Application
```bash
python cli_shell.py
```
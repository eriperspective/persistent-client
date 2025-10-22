# Persistent Client

The persistent client is Chroma's solution for storing vector data permanently on disk rather than in volatile memory. Unlike the default ephemeral client, persistent clients create a local database that survives application restarts, system reboots, and deployment cycles.

## Quick Start

```python
import chromadb

# Basic persistent client setup
client = chromadb.PersistentClient(path="./chroma_db")
```

The client automatically creates the database directory and all necessary internal files. Once initialized, all collection operations (create, insert, query) automatically persist to disk without additional code changes.

## Installation

**Important**: ChromaDB may have compatibility issues with Python 3.14. See [INSTALLATION_NOTES.md](INSTALLATION_NOTES.md) for detailed installation instructions and troubleshooting.

**Quick Install (Python 3.11 or 3.12 recommended)**:

```bash
pip install -r requirements.txt
```

Or directly:

```bash
pip install chromadb
```

For Windows users with installation issues, please refer to [INSTALLATION_NOTES.md](INSTALLATION_NOTES.md).

## Usage

### Quick Start Demo

Run the comprehensive demonstration script to see all features in action:

```bash
python persistent_client_demo.py
```

This will demonstrate:
1. Persistent client initialization with error handling
2. Collection creation and data persistence
3. Data persistence verification across client restarts
4. Database cleanup utilities
5. Performance comparison between ephemeral and persistent clients

### Individual Examples

Run standalone examples for specific use cases:

```bash
python examples.py
```

The examples file includes:
- Basic setup and usage
- Error handling patterns
- Collection management (CRUD operations)
- Persistence verification
- Metadata and filtering
- Batch operations
- Update and delete operations
- Custom embedding functions

### Verify Project Setup

Check that all files are present and ready:

```bash
python test_structure.py
```

## Database Storage Architecture

Chroma's persistent storage uses a hybrid approach combining SQLite for metadata management and optimized binary formats for vector data. This architecture provides ACID compliance for metadata operations while maintaining high performance for vector similarity searches.

### Key Storage Components

- **SQLite database**: Stores collection schemas, document metadata, and system configuration
- **Vector indices**: Binary files containing embedding data and search index structures
- **Configuration files**: Database version information and client settings

> The database directory structure is managed internally by Chroma. Direct file manipulation can corrupt the database and should be avoided in production systems.

## Production Configuration Patterns

For production deployments, consider these essential configuration patterns:

### Path Selection Strategy
Choose database paths on high-performance storage (NVMe SSDs preferred) with sufficient capacity for expected data growth. Avoid network-mounted filesystems.

### Concurrent Access Handling
Chroma persistent clients support single-writer scenarios. For multi-process applications, implement application-level coordination or use client-server mode instead.

### Error Recovery Implementation
Common failure modes include insufficient disk space, permission errors, and database corruption. Implement proper error handling:

```python
try:
    client = chromadb.PersistentClient(path="./db")
except Exception as e:
    # Handle initialization failures
    logging.error(f"Database initialization failed: {e}")
```

## Development Workflow Integration

Persistent clients change your development workflow by maintaining state between runs. This enables iterative development where you can build up collections incrementally rather than recreating test data each session.

## Code Examples

### Initialize Persistent Client with Error Handling

```python
import chromadb
import os

try:
    client = chromadb.PersistentClient(path="./my_vector_db")
    print("Persistent client initialized successfully")
except PermissionError:
    print("Error: Insufficient permissions to create database directory")
except Exception as e:
    print(f"Initialization failed: {e}")
```

### Create and Persist a Collection

```python
# Create collection and add sample data
collection = client.create_collection("test_docs")
collection.add(
    documents=["Hello world", "Python is great"],
    ids=["doc1", "doc2"],
    metadatas=[{"type": "greeting"}, {"type": "opinion"}]
)

# Verify persistence by restarting client
client = chromadb.PersistentClient(path="./my_vector_db")
collection = client.get_collection("test_docs")
print(f"Collection count: {collection.count()}")
```

### Database Cleanup Utility

```python
import shutil

def reset_database(db_path):
    """Clean and recreate persistent database"""
    if os.path.exists(db_path):
        shutil.rmtree(db_path)
    client = chromadb.PersistentClient(path=db_path)
    return client

# Usage for testing
client = reset_database("./test_db")
```

### Performance Comparison

```python
import time

# Test with both client types
memory_client = chromadb.Client()
persistent_client = chromadb.PersistentClient(path="./perf_test")

# Time operations and compare results
start = time.time()
collection = persistent_client.create_collection("perf_test")
# Add your performance test code here
end = time.time()
print(f"Persistent client operation time: {end - start:.3f}s")
```

## Project Structure

```
Persistent Client/
├── README.md                    # Project documentation
├── INSTALLATION_NOTES.md        # Installation help and troubleshooting
├── GITHUB_SETUP.md             # Guide for pushing to GitHub
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore patterns
├── persistent_client_demo.py    # Comprehensive demonstration
├── examples.py                  # Individual example use cases
├── test_structure.py           # Project verification script
└── my_vector_db/               # Created after running demo (git-ignored)
```

## Features Implemented

- Persistent client initialization with comprehensive error handling
- Collection creation and data persistence
- Persistence verification across restarts
- Database cleanup utilities for testing
- Performance comparison between ephemeral and persistent clients
- Production-ready error handling patterns
- Detailed logging and status messages

## License

This is a demonstration project for ChromaDB persistent client functionality.


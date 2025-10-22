"""
ChromaDB Persistent Client - Standalone Examples
Each example can be run independently once ChromaDB is installed.
"""

# ============================================================================
# Example 1: Basic Persistent Client Setup
# ============================================================================

def example_1_basic_setup():
    """
    Basic persistent client initialization and usage.
    """
    import chromadb
    
    # Initialize persistent client
    client = chromadb.PersistentClient(path="./example_db")
    
    # Create a collection
    collection = client.create_collection("my_collection")
    
    # Add documents
    collection.add(
        documents=["This is a document", "This is another document"],
        ids=["id1", "id2"]
    )
    
    # Query the collection
    results = collection.query(
        query_texts=["document"],
        n_results=2
    )
    
    print(f"Found {len(results['ids'][0])} results")
    print(results)


# ============================================================================
# Example 2: Error Handling
# ============================================================================

def example_2_error_handling():
    """
    Comprehensive error handling for production use.
    """
    import chromadb
    import logging
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    def safe_client_init(path):
        """Safely initialize client with error handling."""
        try:
            client = chromadb.PersistentClient(path=path)
            logger.info(f"Client initialized at {path}")
            return client
        except PermissionError:
            logger.error(f"Permission denied: Cannot access {path}")
            raise
        except OSError as e:
            logger.error(f"OS error initializing database: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
    
    # Use the safe initialization
    try:
        client = safe_client_init("./safe_db")
        print("Client initialized successfully!")
    except Exception as e:
        print(f"Failed to initialize client: {e}")


# ============================================================================
# Example 3: Collection Management
# ============================================================================

def example_3_collection_management():
    """
    Demonstrate collection CRUD operations.
    """
    import chromadb
    
    client = chromadb.PersistentClient(path="./collections_db")
    
    # Create a collection
    collection = client.create_collection("my_docs")
    print(f"Created collection: {collection.name}")
    
    # List all collections
    collections = client.list_collections()
    print(f"Available collections: {[c.name for c in collections]}")
    
    # Get existing collection
    retrieved = client.get_collection("my_docs")
    print(f"Retrieved collection: {retrieved.name}")
    
    # Delete collection
    client.delete_collection("my_docs")
    print("Collection deleted")
    
    # Verify deletion
    collections = client.list_collections()
    print(f"Remaining collections: {len(collections)}")


# ============================================================================
# Example 4: Persistence Verification
# ============================================================================

def example_4_persistence_verification():
    """
    Verify that data persists across client sessions.
    """
    import chromadb
    import os
    
    db_path = "./persistence_test_db"
    
    # Session 1: Create and populate
    print("Session 1: Creating data...")
    client1 = chromadb.PersistentClient(path=db_path)
    collection1 = client1.create_collection("persistent_collection")
    collection1.add(
        documents=["Data from session 1"],
        ids=["session1_doc"]
    )
    print(f"  Added {collection1.count()} document(s)")
    del client1  # Explicitly delete to close
    
    # Session 2: Retrieve data
    print("\nSession 2: Retrieving data...")
    client2 = chromadb.PersistentClient(path=db_path)
    collection2 = client2.get_collection("persistent_collection")
    print(f"  Found {collection2.count()} document(s)")
    
    results = collection2.get(ids=["session1_doc"])
    print(f"  Retrieved: {results['documents'][0]}")
    print("\n Data persisted successfully!")


# ============================================================================
# Example 5: Metadata and Filtering
# ============================================================================

def example_5_metadata_filtering():
    """
    Demonstrate metadata usage and filtering.
    """
    import chromadb
    
    client = chromadb.PersistentClient(path="./metadata_db")
    collection = client.create_collection("docs_with_metadata")
    
    # Add documents with metadata
    collection.add(
        documents=[
            "Python tutorial for beginners",
            "Advanced Python techniques",
            "JavaScript basics",
            "Machine learning with Python"
        ],
        ids=["doc1", "doc2", "doc3", "doc4"],
        metadatas=[
            {"language": "python", "level": "beginner"},
            {"language": "python", "level": "advanced"},
            {"language": "javascript", "level": "beginner"},
            {"language": "python", "level": "advanced", "topic": "ml"}
        ]
    )
    
    # Query with metadata filter
    results = collection.query(
        query_texts=["python programming"],
        n_results=10,
        where={"language": "python"}
    )
    
    print(f"Found {len(results['ids'][0])} Python documents")
    for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
        print(f"  - {doc[:40]}... (Level: {metadata['level']})")


# ============================================================================
# Example 6: Batch Operations
# ============================================================================

def example_6_batch_operations():
    """
    Efficiently add large numbers of documents.
    """
    import chromadb
    import time
    
    client = chromadb.PersistentClient(path="./batch_db")
    collection = client.create_collection("large_collection")
    
    # Prepare large batch
    num_docs = 1000
    documents = [f"Document {i} with some content" for i in range(num_docs)]
    ids = [f"doc_{i}" for i in range(num_docs)]
    metadatas = [{"index": i, "category": i % 10} for i in range(num_docs)]
    
    # Time the batch insert
    start = time.time()
    collection.add(
        documents=documents,
        ids=ids,
        metadatas=metadatas
    )
    elapsed = time.time() - start
    
    print(f"Added {num_docs} documents in {elapsed:.2f} seconds")
    print(f"Rate: {num_docs/elapsed:.0f} documents/second")
    print(f"Collection count: {collection.count()}")


# ============================================================================
# Example 7: Update and Delete Operations
# ============================================================================

def example_7_update_delete():
    """
    Demonstrate update and delete operations.
    """
    import chromadb
    
    client = chromadb.PersistentClient(path="./update_db")
    collection = client.create_collection("mutable_docs")
    
    # Add initial documents
    collection.add(
        documents=["Original content"],
        ids=["doc1"],
        metadatas=[{"version": 1}]
    )
    print(f"Initial: {collection.get(ids=['doc1'])['documents'][0]}")
    
    # Update document
    collection.update(
        ids=["doc1"],
        documents=["Updated content"],
        metadatas=[{"version": 2}]
    )
    print(f"Updated: {collection.get(ids=['doc1'])['documents'][0]}")
    
    # Delete document
    collection.delete(ids=["doc1"])
    print(f"Count after delete: {collection.count()}")


# ============================================================================
# Example 8: Custom Embedding Functions
# ============================================================================

def example_8_custom_embeddings():
    """
    Using custom embedding functions.
    """
    import chromadb
    from chromadb.utils import embedding_functions
    
    # Use different embedding function
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    client = chromadb.PersistentClient(path="./custom_embeddings_db")
    collection = client.create_collection(
        name="custom_embeddings",
        embedding_function=sentence_transformer_ef
    )
    
    collection.add(
        documents=["The cat sat on the mat", "The dog played in the park"],
        ids=["cat_doc", "dog_doc"]
    )
    
    results = collection.query(
        query_texts=["feline on furniture"],
        n_results=1
    )
    
    print(f"Query: 'feline on furniture'")
    print(f"Best match: {results['documents'][0][0]}")


# ============================================================================
# Main Function - Run All Examples
# ============================================================================

def main():
    """
    Run all examples sequentially.
    Comment out any you don't want to run.
    """
    examples = [
        ("Basic Setup", example_1_basic_setup),
        ("Error Handling", example_2_error_handling),
        ("Collection Management", example_3_collection_management),
        ("Persistence Verification", example_4_persistence_verification),
        ("Metadata and Filtering", example_5_metadata_filtering),
        ("Batch Operations", example_6_batch_operations),
        ("Update and Delete", example_7_update_delete),
        # ("Custom Embeddings", example_8_custom_embeddings),  # Requires additional package
    ]
    
    for name, func in examples:
        print("\n" + "=" * 60)
        print(f"Example: {name}")
        print("=" * 60)
        try:
            func()
            print(f"\n {name} completed successfully")
        except Exception as e:
            print(f"\n {name} failed: {e}")
        print()
    
    # Cleanup example databases
    import shutil
    import os
    cleanup_dirs = [
        "./example_db", "./safe_db", "./collections_db",
        "./persistence_test_db", "./metadata_db", "./batch_db",
        "./update_db", "./custom_embeddings_db"
    ]
    print("\n" + "=" * 60)
    print("Cleanup")
    print("=" * 60)
    for dir_path in cleanup_dirs:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            print(f"  Removed: {dir_path}")
    print("\n Cleanup complete")


if __name__ == "__main__":
    print("ChromaDB Persistent Client Examples")
    print("=" * 60)
    print("Make sure ChromaDB is installed before running:")
    print("  pip install chromadb")
    print("=" * 60)
    
    try:
        import chromadb
        print(f"\n ChromaDB {chromadb.__version__} is installed\n")
        main()
    except ImportError:
        print("\n ChromaDB is not installed")
        print("Please install it with: pip install chromadb")
        print("See INSTALLATION_NOTES.md for detailed instructions")



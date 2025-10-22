"""
Persistent Client Demo
Demonstrates ChromaDB persistent client functionality with error handling,
collection management, and database utilities.
"""

import chromadb
import os
import shutil
import time


def initialize_persistent_client(path="./my_vector_db"):
    """
    Initialize persistent client with comprehensive error handling.
    
    Args:
        path: Path to the database directory
        
    Returns:
        chromadb.PersistentClient: Initialized client instance
    """
    try:
        client = chromadb.PersistentClient(path=path)
        print(f"Persistent client initialized successfully at: {path}")
        return client
    except PermissionError:
        print("Error: Insufficient permissions to create database directory")
        raise
    except Exception as e:
        print(f"Initialization failed: {e}")
        raise


def create_and_persist_collection(client, collection_name="test_docs"):
    """
    Create a collection and add sample data to demonstrate persistence.
    
    Args:
        client: ChromaDB client instance
        collection_name: Name of the collection to create
        
    Returns:
        Collection: The created collection
    """
    print(f"\n--- Creating Collection: {collection_name} ---")
    
    # Create collection and add sample data
    collection = client.create_collection(collection_name)
    collection.add(
        documents=["Hello world", "Python is great"],
        ids=["doc1", "doc2"],
        metadatas=[{"type": "greeting"}, {"type": "opinion"}]
    )
    print(f"Collection created with {collection.count()} documents")
    
    return collection


def verify_persistence(path="./my_vector_db", collection_name="test_docs"):
    """
    Verify data persistence by reinitializing the client and retrieving the collection.
    
    Args:
        path: Path to the database directory
        collection_name: Name of the collection to retrieve
    """
    print(f"\n--- Verifying Persistence ---")
    
    # Restart client to verify persistence
    client = chromadb.PersistentClient(path=path)
    collection = client.get_collection(collection_name)
    count = collection.count()
    
    print(f"Collection retrieved after restart")
    print(f"Collection count: {count}")
    
    # Query to show data is intact
    results = collection.get(ids=["doc1", "doc2"])
    print(f"Retrieved documents: {results['documents']}")
    
    return client, collection


def reset_database(db_path):
    """
    Clean and recreate persistent database.
    Useful for testing and development scenarios.
    
    Args:
        db_path: Path to the database directory
        
    Returns:
        chromadb.PersistentClient: Fresh client instance
    """
    print(f"\n--- Resetting Database at {db_path} ---")
    
    if os.path.exists(db_path):
        shutil.rmtree(db_path)
        print(f"Removed existing database")
    
    client = chromadb.PersistentClient(path=db_path)
    print(f"Created fresh database")
    
    return client


def performance_comparison():
    """
    Compare performance between ephemeral and persistent clients.
    Tests collection creation and document insertion operations.
    """
    print("\n--- Performance Comparison ---")
    
    # Test data
    num_documents = 100
    test_docs = [f"Document {i} with some sample text content" for i in range(num_documents)]
    test_ids = [f"doc_{i}" for i in range(num_documents)]
    test_metadata = [{"index": i, "category": f"cat_{i % 5}"} for i in range(num_documents)]
    
    # Test ephemeral client
    print("\nTesting Ephemeral Client:")
    memory_client = chromadb.Client()
    
    start = time.time()
    mem_collection = memory_client.create_collection("perf_test_memory")
    mem_collection.add(
        documents=test_docs,
        ids=test_ids,
        metadatas=test_metadata
    )
    mem_time = time.time() - start
    print(f"  - Collection created with {mem_collection.count()} documents")
    print(f"  - Operation time: {mem_time:.3f}s")
    
    # Test persistent client
    print("\nTesting Persistent Client:")
    persistent_client = chromadb.PersistentClient(path="./perf_test")
    
    start = time.time()
    pers_collection = persistent_client.create_collection("perf_test_persistent")
    pers_collection.add(
        documents=test_docs,
        ids=test_ids,
        metadatas=test_metadata
    )
    pers_time = time.time() - start
    print(f"  - Collection created with {pers_collection.count()} documents")
    print(f"  - Operation time: {pers_time:.3f}s")
    
    # Comparison
    print(f"\nPerformance Comparison:")
    print(f"  - Ephemeral: {mem_time:.3f}s")
    print(f"  - Persistent: {pers_time:.3f}s")
    print(f"  - Difference: {abs(pers_time - mem_time):.3f}s")
    
    # Cleanup performance test database
    if os.path.exists("./perf_test"):
        shutil.rmtree("./perf_test")
        print("\nCleaned up performance test database")


def main():
    """
    Main demonstration function that runs through all the persistent client features.
    """
    print("=" * 60)
    print("ChromaDB Persistent Client Demonstration")
    print("=" * 60)
    
    db_path = "./my_vector_db"
    
    # 1. Initialize persistent client with error handling
    print("\n[1] Initializing Persistent Client")
    client = initialize_persistent_client(db_path)
    
    # 2. Create and persist a collection
    print("\n[2] Creating and Persisting Collection")
    collection = create_and_persist_collection(client, "test_docs")
    
    # 3. Verify persistence
    print("\n[3] Verifying Data Persistence")
    client, collection = verify_persistence(db_path, "test_docs")
    
    # 4. Demonstrate database cleanup utility
    print("\n[4] Database Cleanup Utility")
    test_db_path = "./test_db"
    test_client = reset_database(test_db_path)
    print(f"Test database ready at: {test_db_path}")
    
    # Cleanup test database
    if os.path.exists(test_db_path):
        shutil.rmtree(test_db_path)
        print(f"Cleaned up test database")
    
    # 5. Performance comparison
    print("\n[5] Performance Testing")
    performance_comparison()
    
    print("\n" + "=" * 60)
    print("Demonstration Complete!")
    print("=" * 60)
    print(f"\nPersistent database location: {os.path.abspath(db_path)}")
    print("The database will persist across application restarts.")


if __name__ == "__main__":
    main()



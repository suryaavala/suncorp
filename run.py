import uvicorn
import src.mock_data as mock_data
import src.vector_store as vector_store

def main():
    print("--- 1. Generating Mock Data...")
    mock_data.generate_mock_data()
    
    print("\n--- 2. Populating Vector Store...")
    vector_store.populate_vector_store()
    
    print("\n--- 3. Starting FastAPI Server on port 8000...")
    uvicorn.run("src.api:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    main()

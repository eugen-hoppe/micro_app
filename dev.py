import os


print(f"export PYTHONPATH=$PYTHONPATH:{os.getcwd()}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.application:app", host="localhost", port=8000, reload=True)

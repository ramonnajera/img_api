from fastapi import FastAPI, UploadFile, HTTPException, status
from typing import List
import os
import uuid

app = FastAPI()

MAX_FILES = 5
ALLOWED_EXTENSIONS = ['.jpg', '.png', '.jpeg']

def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def validate_file(file: UploadFile):
    extension = os.path.splitext(file.filename)[1]
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Archivo no soportado, las extensiones permitidas son {ALLOWED_EXTENSIONS}")
    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de contenido no soportado")

@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile], id: str):
    if not files:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Se requiere al menos una imagen")
    if not id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Se requiere un id")

    if len(files) > MAX_FILES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No se pueden subir más de {MAX_FILES} archivos a la vez")

    try:
        int(id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El id debe ser un número")

    file_names = []
    dir_path = f'fotos/{id}'
    create_dir(dir_path)
    for file in files:
        validate_file(file)
        unique_filename = f"img-{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
        file_names.append(unique_filename)
        with open(f'{dir_path}/{unique_filename}', 'wb') as buffer:
            buffer.write(await file.read())
    return {"message": "Las fotos se subieron correctamente"}
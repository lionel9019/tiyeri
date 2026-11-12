# backend/conversations/image_routes.py
import tempfile, os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from backend.modules.image_analysis_module import ImageAnalyzer

router = APIRouter(prefix="/api/image")

# init analyzer (chemins relatifs au projet)
ANALYZER = ImageAnalyzer(
    multiclass_model_path="models/plant_model.h5",
    labels_path="models/labels.json",
    metadata_path="models/metadata.json",
    binary_model_path="models/plant_or_not_model.h5"  # facultatif
)

@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    # sauvegarde temporaire
    suffix = Path(file.filename).suffix or ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        res = ANALYZER.analyze(tmp_path, top_k=3)
        return JSONResponse(res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        try:
            os.remove(tmp_path)
        except:
            pass

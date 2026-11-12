# backend/conversations/routes.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from datetime import datetime
import re, unicodedata, threading, time, asyncio, tempfile, os
from sqlalchemy.orm import Session, joinedload
import shutil
from pathlib import Path
from fastapi.encoders import jsonable_encoder
from pydub import AudioSegment
from backend.core.security import get_current_user
from backend.database import get_db, SessionLocal
from backend.models.user import User
from backend.models.chatbot_intent import ChatbotIntent
from backend.models.conversation import Conversation, Message
from backend.models.fake_model import model  # simulateur IA
from backend.schemas.conversation import (
    ConversationCreate, ConversationOut,
    PromptRequest, ResponseOut
)
from fastapi.responses import JSONResponse
import logging
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langdetect import detect
from deep_translator import GoogleTranslator

# 🔊 Whisper + pydub
import whisper
from pydub import AudioSegment  

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/api/conversations",
    tags=["Conversations"]
)
# 🔹 Force pydub à utiliser ffmpeg installé
AudioSegment.converter = r"C:\Users\a.boubakari\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-full_build\bin\ffmpeg.exe"

# 🔹 Modèle Whisper
stt_model = whisper.load_model("base")
# -----------------------------------------------------------
# 🔹 UTILS
# -----------------------------------------------------------

COMMON_FR = {"slt", "bjr", "bsr", "merci", "bonjour", "bonsoir", "coucou"}


def detect_lang_safe(text: str) -> str:
    """Détection robuste avec fallback FR"""
    low = text.lower().strip()
    if low in COMMON_FR or len(low) <= 4:
        return "fr"
    try:
        lang = detect(text)
        if lang not in ["fr", "en", "es", "de"]:
            return "fr"
        return lang
    except:
        return "fr"


def make_title(first_prompt: str) -> str:
    words = re.findall(r"\w+", first_prompt, flags=re.UNICODE)
    if not words:
        return f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    picked = words[:5] if len(words) >= 2 else words
    title = " ".join(picked)
    return (title[:60]).strip()


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[!?.,;:]+", "", text)
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def detect_contextual_intent(new_prompt: str, last_intent: str | None) -> tuple[str, str]:
    contextual_keywords = ["et", "pareil", "aussi", "pour", "celui", "encore"]
    p = new_prompt.lower().strip()

    if last_intent and any(k in p.split() for k in contextual_keywords):
        sujet = re.sub(r"\b(et|pareil|aussi|pour|celui|encore)\b", "", p).strip()
        return last_intent, sujet

    if "nom scientifique" in p:
        return "nom_scientifique", p
    return "autre", p


# -----------------------------------------------------------
# 🔹 INITIALISATION GLOBALE
# -----------------------------------------------------------

print("🔄 Chargement du modèle embeddings...")
model_embed = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Modèle embeddings chargé.")

print("🔄 Chargement du modèle Whisper...")
stt_model = whisper.load_model("base")
print("✅ Whisper chargé.")

index = None
intent_texts, intent_ids, intent_responses = [], [], []


def build_intent_index(db: Session):
    global index, intent_texts, intent_ids, intent_responses
    intents = db.query(ChatbotIntent).all()
    if not intents:
        print("⚠️ Aucun intent trouvé en base.")
        return

    intent_texts = [normalize_text(intent.phrase) for intent in intents]
    intent_ids = [intent.id for intent in intents]
    intent_responses = [intent.response for intent in intents]

    embeddings = model_embed.encode(intent_texts, convert_to_numpy=True, show_progress_bar=False)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    print("✅ Index FAISS construit.")


def find_best_intent(prompt: str, threshold: float = 0.6):
    global index, intent_responses
    if not index:
        return None
    prompt_vec = model_embed.encode([normalize_text(prompt)], convert_to_numpy=True)
    D, I = index.search(prompt_vec, k=1)
    score = 1 - (D[0][0] / 2)
    best_idx = I[0][0]
    if score >= threshold and best_idx < len(intent_responses):
        return intent_responses[best_idx]
    return None


# -----------------------------------------------------------
# 🔹 ROUTES
# -----------------------------------------------------------

@router.on_event("startup")
def startup_event():
    db = next(get_db())
    build_intent_index(db)
    threading.Thread(target=lambda: None, daemon=True).start()


@router.get("/", response_model=list[ConversationOut])
def get_all_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    convs = (
        db.query(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .options(joinedload(Conversation.messages))
        .all()
    )

    results = []
    for conv in convs:
        last_msg = conv.messages[-1] if conv.messages else None
        results.append(ConversationOut(
            id=conv.id,
            title=conv.title,
            created_at=conv.created_at,
            last_message=last_msg.content if last_msg else "",
            timestamp=last_msg.created_at if last_msg else conv.created_at
        ))
    return results


@router.post("/", response_model=ConversationOut)
def create_conversation(
    data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_conv = Conversation(
        title=data.title or "Nouvelle conversation",
        user_id=current_user.id,
        created_at=datetime.utcnow()
    )
    db.add(new_conv)
    db.commit()
    db.refresh(new_conv)
    return ConversationOut(
        id=new_conv.id,
        title=new_conv.title,
        created_at=new_conv.created_at,
        last_message="",
        timestamp=new_conv.created_at
    )


@router.post("/generate", response_model=ResponseOut)
async def generate_text(
    request: PromptRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prompt = request.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Message vide.")

    last_intent = None
    if request.conversation_id:
        last_msg = (
            db.query(Message)
            .filter(Message.conversation_id == request.conversation_id)
            .order_by(Message.created_at.desc())
            .first()
        )
        if last_msg:
            last_intent = getattr(last_msg, "intention", None)

    intent, sujet = detect_contextual_intent(prompt, last_intent)
    user_lang = detect_lang_safe(prompt)

    prompt_fr = prompt
    if user_lang != "fr":
        try:
            prompt_fr = GoogleTranslator(source="auto", target="fr").translate(prompt)
        except:
            pass

    if intent == "nom_scientifique":
        response_text_fr = find_best_intent(f"nom scientifique de {sujet}") or f"Je n’ai pas trouvé le nom scientifique de {sujet}."
    else:
        response_text_fr = find_best_intent(prompt_fr) or model.generate(prompt_fr)

    response_text = response_text_fr
    if user_lang != "fr":
        try:
            response_text = GoogleTranslator(source="fr", target=user_lang).translate(response_text_fr)
        except:
            pass

    if request.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == request.conversation_id,
            Conversation.user_id == current_user.id
        ).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation non trouvée")
    else:
        conversation = Conversation(
            user_id=current_user.id,
            title=make_title(prompt),
            created_at=datetime.utcnow()
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    user_msg = Message(conversation_id=conversation.id, sender="user", content=prompt, created_at=datetime.utcnow(), intention=intent)
    bot_msg = Message(conversation_id=conversation.id, sender="bot", content=response_text, created_at=datetime.utcnow(), intention=intent)
    db.add(user_msg)
    db.add(bot_msg)
    db.commit()

    return ResponseOut(response=response_text, conversation_id=conversation.id, title=conversation.title, created_at=bot_msg.created_at)


# -----------------------------------------------------------
# 🔹 ROUTE VOCALE AVEC DETECTION AUTOMATIQUE
# -----------------------------------------------------------

@router.post("/voice", response_model=ResponseOut)
async def generate_from_voice(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    media_dir = Path("media") / "voices"
    media_dir.mkdir(parents=True, exist_ok=True)

    file_id = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{Path(file.filename or 'voice').name}"
    raw_path = media_dir / file_id

    with open(raw_path, "wb") as buffer:
        buffer.write(await file.read())

    try:
        # Conversion en wav
        ext = raw_path.suffix.lstrip(".") if raw_path.suffix else "webm"
        audio = AudioSegment.from_file(raw_path, format=ext)
        wav_path = raw_path.with_suffix(".wav")
        audio.export(wav_path, format="wav")

        logger.info(f"📂 Fichier reçu: {file.filename}, taille = {raw_path.stat().st_size} octets")
        logger.info(f"🎶 Durée audio (ms): {len(audio)}")

        # Transcription Whisper
        result = stt_model.transcribe(str(wav_path), language=None, task="transcribe")
        logger.info(f"📝 Résultat brut Whisper: {result}")
        transcription = result.get("text", "").strip()
        whisper_lang = result.get("language", "unknown")

        final_lang = whisper_lang
        if transcription:
            try:
                detected_lang = detect(transcription)
                if whisper_lang != detected_lang:
                    logger.info(f"⚠️ Correction langue: Whisper={whisper_lang}, LangDetect={detected_lang}")
                    final_lang = detected_lang
            except Exception:
                pass

        if not transcription:
            raise HTTPException(status_code=400, detail="Impossible de transcrire l'audio.")

        logger.info(f"🎤 Transcription: {transcription}")
        logger.info(f"🌍 Langue finale: {final_lang}")

        # Génération texte IA
        response = await generate_text(
            PromptRequest(prompt=transcription, conversation_id=None),
            db=db,
            current_user=current_user
        )

        # Sérialisation propre avec JSON safe
        response_dict = jsonable_encoder(response)
        response_dict.update({
            "transcription": transcription,
            "language": final_lang,
            "audio_url": f"/media/voices/{file_id}"
        })

        return JSONResponse(content=response_dict)

    except Exception as e:
        logger.error(f"Erreur transcription: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur transcription audio")

    finally:
        wav_path = raw_path.with_suffix(".wav")
        if wav_path.exists():
            wav_path.unlink() 
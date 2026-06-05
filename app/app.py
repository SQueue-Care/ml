from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


startup_error: str = ""


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model prediksi waktu tunggu saat startup."""
    global startup_error
    from app.predict.model import load_model
    from app.predict.router import init_model

    print("[startup] Memuat model SmartQueue AI...")
    try:
        model, scaler = load_model()
        init_model(model, scaler)
        print(f"[startup] Model loaded  : input_shape={model.input_shape}")
    except Exception as e:
        startup_error = str(e)
        print(f"[startup] WARNING: Model gagal dimuat — {e}")
        print("[startup] Endpoint /predict tidak akan berfungsi.")

    yield

    print("[shutdown] SmartQueue AI API berhenti.")


app = FastAPI(
    title="SmartQueue AI API",
    description=(
        "REST API untuk prediksi waktu tunggu pasien rumah sakit "
        "dan Clinical Decision Support System (CDSS) berbasis AI."
    ),
    version="5.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────────────────
from app.cdss.router import cdss_router          # noqa: E402
from app.predict.router import predict_router    # noqa: E402

app.include_router(cdss_router)
app.include_router(predict_router)


# ── Root endpoints ───────────────────────────────────────────────
@app.get("/", tags=["Root"])
def home():
    return {
        "message": "SmartQueue AI API aktif",
        "docs": "/docs",
        "status": "running",
        "version": "5.0",
    }


@app.get("/health", tags=["Root"])
def health_check():
    from app.predict.router import state
    return {
        "status": "healthy",
        "model_loaded": state.model is not None,
        "model_error": startup_error if startup_error else None,
        "version": "5.0",
    }

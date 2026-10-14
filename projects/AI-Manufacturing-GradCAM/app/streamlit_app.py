"""Professional Streamlit interface for casting defect inspection and XAI."""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

import numpy as np
import streamlit as st
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.gradcam import make_gradcam, make_visuals  # noqa: E402
from src.model_loader import load_config, load_model  # noqa: E402
from src.predict import predict, preprocess_pil_image  # noqa: E402

st.set_page_config(
    page_title="Casting Defect Inspector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .block-container { max-width: 1320px; padding: 2.2rem 3rem 4rem; }
    .hero { padding: 1.4rem 1.7rem; border-radius: 16px; background: linear-gradient(135deg,#172033,#263b5c); color:#f8fafc; margin-bottom:1.5rem; }
    .hero h1 { margin:0; font-size:2.35rem; letter-spacing:-.03em; }
    .hero p { margin:.45rem 0 0; color:#cbd5e1; }
    .result-card { border-radius:16px; padding:1.25rem 1.5rem; border:1px solid #334155; background:#111827; }
    .result-label { font-size:1.65rem; font-weight:800; margin:.15rem 0; }
    .result-confidence { font-size:2.6rem; font-weight:850; line-height:1.1; }
    .ok { color:#34d399; } .defective { color:#fb7185; }
    .section-title { margin-top:1.6rem; padding-bottom:.4rem; border-bottom:1px solid #334155; }
    [data-testid="stFileUploader"] { border-radius:14px; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner=False)
def runtime() -> tuple[object, int]:
    config = load_config(ROOT / "config.yaml")
    model_path = ROOT / config["training"]["model_path"]
    image_size = int(config["data"]["image_size"])
    return load_model(model_path), image_size


def png_bytes(array: np.ndarray) -> bytes:
    buffer = io.BytesIO()
    Image.fromarray(array).save(buffer, format="PNG")
    return buffer.getvalue()


st.markdown(
    '<div class="hero"><h1>🔍 Casting Defect Inspector</h1>'
    "<p>AI-assisted visual quality control for submersible pump impellers</p></div>",
    unsafe_allow_html=True,
)

uploaded = st.file_uploader(
    "Upload a grayscale casting image",
    type=["jpg", "jpeg", "png", "bmp"],
    help="Supported formats: JPG, PNG, BMP. The model normalizes the image before inspection.",
)

if not uploaded:
    st.info("Upload an image to start an inspection.")
    st.stop()

try:
    image = Image.open(uploaded).convert("L")
    image.load()
except (OSError, ValueError) as exc:
    st.error(f"Unable to read this image. Please upload a valid JPG, PNG, or BMP file. ({exc})")
    st.stop()

with st.spinner("Running inspection and generating Grad-CAM explanation..."):
    try:
        model, image_size = runtime()
        batch = preprocess_pil_image(image, image_size)
        result = predict(model, batch)
        heatmap = make_gradcam(model, batch, class_index=result["class_index"])
        heatmap_rgb, overlay = make_visuals(np.asarray(image), heatmap)
    except (FileNotFoundError, OSError, ValueError, RuntimeError) as exc:
        st.error(f"Inspection could not be completed: {exc}")
        st.stop()

label = result["label"]
confidence = result["confidence"]
accent = "defective" if label == "Defective" else "ok"
icon = "⚠️" if label == "Defective" else "✅"

st.markdown('<h2 class="section-title">Inspection Result</h2>', unsafe_allow_html=True)
left, right = st.columns([1, 2])
with left:
    st.markdown(
        f'<div class="result-card"><div>Classification</div>'
        f'<div class="result-label {accent}">{icon} {label}</div>'
        f'<div class="result-confidence {accent}">{confidence:.1%}</div>'
        "<div>model confidence</div></div>",
        unsafe_allow_html=True,
    )
with right:
    st.subheader("Model Confidence")
    st.progress(float(confidence), text=f"{confidence:.1%} confidence")
    st.bar_chart(
        {"Probability": {"Defective": result["defect_probability"], "OK": result["ok_probability"]}},
        horizontal=True,
        height=150,
    )

st.markdown('<h2 class="section-title">Explainable AI (Grad-CAM)</h2>', unsafe_allow_html=True)
columns = st.columns(3, gap="medium")
columns[0].image(image, caption="Original image", use_container_width=True)
columns[1].image(heatmap_rgb, caption="Grad-CAM heatmap (jet)", use_container_width=True)
columns[2].image(overlay, caption="Grad-CAM overlay", use_container_width=True)
st.caption("Warmer regions indicate image areas that contributed more strongly to the selected prediction.")

report = {
    "file_name": uploaded.name,
    "prediction": label,
    "confidence": round(float(confidence), 6),
    "defective_probability": round(float(result["defect_probability"]), 6),
    "ok_probability": round(float(result["ok_probability"]), 6),
}
download_left, download_right = st.columns(2)
with download_left:
    st.download_button(
        "⬇️ Download Grad-CAM overlay",
        data=png_bytes(overlay),
        file_name=f"{Path(uploaded.name).stem}_gradcam_overlay.png",
        mime="image/png",
        use_container_width=True,
    )
with download_right:
    st.download_button(
        "⬇️ Download inspection report",
        data=json.dumps(report, indent=2),
        file_name=f"{Path(uploaded.name).stem}_inspection_report.json",
        mime="application/json",
        use_container_width=True,
    )

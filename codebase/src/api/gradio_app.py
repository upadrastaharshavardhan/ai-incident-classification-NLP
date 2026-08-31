"""Gradio demo for Incident Classification & Priority Prediction."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import gradio as gr
from src.pipeline.predictor import IncidentPredictor
from src.utils.helpers import load_config


def format_result(result: dict) -> str:
    lines = [
        f"### Category: **{result['category']}**  (confidence: {result['category_confidence']:.1%})",
        f"### Priority: **{result['priority']}**  (confidence: {result['priority_confidence']:.1%})",
        "",
        "### Similar Historical Incidents",
    ]
    for i, s in enumerate(result.get("similar_incidents", []), 1):
        lines.append(
            f"{i}. `{s['incident_id']}` | **{s['category']}** / **{s['priority']}** | sim={s['similarity']:.3f}  \n"
            f"   {s['title']}"
        )
    lines.append("")
    lines.append("### Cleaned Input Preview")
    lines.append(f"```\n{result.get('cleaned_input_preview', '')}\n```")
    return "\n".join(lines)


def build_demo(artifacts_dir: str = "artifacts", config_path: str = "config/config.yaml"):
    cfg = load_config(config_path)
    predictor = IncidentPredictor.load(artifacts_dir, config_path)

    def predict_fn(title: str, description: str, top_k: int):
        if not (title or description):
            return "Please enter a title and/or description."
        result = predictor.predict(title=title, description=description, top_k_similar=int(top_k))
        return format_result(result)

    demo = gr.Interface(
        fn=predict_fn,
        inputs=[
            gr.Textbox(label="Incident Title", placeholder="e.g. VPN connection failures"),
            gr.Textbox(lines=8, label="Description", placeholder="Detailed description of the incident..."),
            gr.Slider(1, 10, value=5, step=1, label="Similar incidents to show"),
        ],
        outputs=gr.Markdown(label="Prediction"),
        title=cfg.get("gradio", {}).get("title", "IT Incident Classifier & Priority Predictor"),
        description=cfg.get("gradio", {}).get(
            "description",
            "Enter an incident title and description to get predicted category, priority, and similar historical tickets.",
        ),
        examples=[
            [
                "VPN connection failures for remote users",
                "Multiple users unable to connect to corporate VPN since morning. Error: Connection timed out. Affects remote workforce.",
                5,
            ],
            [
                "Suspicious login attempts detected",
                "SIEM alert: Multiple failed login attempts from unusual geolocations for privileged accounts.",
                5,
            ],
            [
                "New employee cannot access email",
                "Onboarding: New hire started today but AD account not provisioned. Cannot access Outlook or Teams.",
                3,
            ],
        ],
        allow_flagging="never",
    )
    return demo


if __name__ == "__main__":
    demo = build_demo()
    demo.launch(share=False, server_name="0.0.0.0")

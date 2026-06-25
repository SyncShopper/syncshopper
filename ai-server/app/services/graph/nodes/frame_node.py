from concurrent.futures import ThreadPoolExecutor
from typing import Any

from fastapi import HTTPException

from app.services.graph.state import ShoppingAnalysisState
from app.services.split_frame_analysis_service import (
    analyze_ocr,
    analyze_visual_features,
    koreanize_visual_analysis,
    synthesize_initial_detection,
)
from app.utils.image_utils import is_valid_base64_image


def _frame_analyzer_node(state: ShoppingAnalysisState) -> dict[str, Any]:
    request = state["request"]
    if not is_valid_base64_image(request.image_base64):
        raise HTTPException(
            status_code=400,
            detail="image_base64 must be a valid data:image base64 string",
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        ocr_future = executor.submit(analyze_ocr, request)
        visual_future = executor.submit(analyze_visual_features, request)
        ocr_analysis = ocr_future.result()
        visual_analysis = koreanize_visual_analysis(visual_future.result())

    frame_analysis = synthesize_initial_detection(ocr_analysis, visual_analysis)
    return {
        "ocr_analysis": ocr_analysis,
        "visual_analysis": visual_analysis,
        "frame_analysis": frame_analysis,
    }

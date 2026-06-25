import time
from typing import Any, Callable

from langgraph.graph import END, START, StateGraph

from app.schemas.analysis_graph_schema import ShoppingAnalysisRequest, ShoppingAnalysisResponse
from app.services.graph.debug import _print_graph_debug, _print_graph_error
from app.services.graph.nodes.filter_node import _text_filter_node
from app.services.graph.nodes.frame_node import _frame_analyzer_node
from app.services.graph.nodes.judge_node import (
    _candidate_judge_node,
    _fast_result_judge_node,
    _final_formatter_node,
)
from app.services.graph.nodes.query_node import _query_generator_node
from app.services.graph.nodes.rerank_node import _visual_reranker_node
from app.services.graph.nodes.search_node import (
    _google_search_branch_node,
    _merge_search_results_node,
    _naver_search_branch_node,
)
from app.services.graph.state import ShoppingAnalysisState


def analyze_shopping(request: ShoppingAnalysisRequest) -> ShoppingAnalysisResponse:
    initial_state: ShoppingAnalysisState = {
        "request": request,
        "search_mode": request.search_mode,
        "retry_count": 0,
        "tried_queries": [],
        "best_candidates": [],
    }
    _print_graph_debug("START", {"request": request, "search_mode": request.search_mode})
    started_at = time.perf_counter()
    try:
        result = _analysis_graph.invoke(initial_state)
        response = result["response"]
        _print_total_elapsed("END", started_at)
        _print_graph_debug("END", {"response": response})
        return response
    except Exception as exc:
        _print_total_elapsed("FAILED", started_at)
        _print_graph_error("FAILED", exc)
        raise


def _build_graph():
    workflow = StateGraph(ShoppingAnalysisState)
    workflow.add_node("frame_analyzer", _with_node_logging("frame_analyzer", _frame_analyzer_node))
    workflow.add_node("query_generator", _with_node_logging("query_generator", _query_generator_node))
    workflow.add_node("naver_search", _with_node_logging("naver_search", _naver_search_branch_node))
    workflow.add_node("google_search", _with_node_logging("google_search", _google_search_branch_node))
    workflow.add_node("merge_search_results", _with_node_logging("merge_search_results", _merge_search_results_node))
    workflow.add_node("text_filter", _with_node_logging("text_filter", _text_filter_node))
    workflow.add_node("fast_result_judge", _with_node_logging("fast_result_judge", _fast_result_judge_node))
    workflow.add_node("visual_reranker", _with_node_logging("visual_reranker", _visual_reranker_node))
    workflow.add_node("candidate_judge", _with_node_logging("candidate_judge", _candidate_judge_node))
    workflow.add_node("final_formatter", _with_node_logging("final_formatter", _final_formatter_node))

    workflow.add_edge(START, "frame_analyzer")
    workflow.add_edge("frame_analyzer", "query_generator")
    workflow.add_edge("query_generator", "naver_search")
    workflow.add_edge("query_generator", "google_search")
    workflow.add_edge(["naver_search", "google_search"], "merge_search_results")
    workflow.add_edge("merge_search_results", "text_filter")
    workflow.add_conditional_edges(
        "text_filter",
        _route_after_text_filter,
        {
            "fast_result_judge": "fast_result_judge",
            "visual_reranker": "visual_reranker",
        },
    )
    workflow.add_edge("fast_result_judge", "final_formatter")
    workflow.add_edge("visual_reranker", "candidate_judge")
    workflow.add_edge("candidate_judge", "final_formatter")
    workflow.add_edge("final_formatter", END)

    return workflow.compile()


def _route_after_text_filter(state: ShoppingAnalysisState) -> str:
    if state["request"].search_mode == "fast":
        return "fast_result_judge"

    return "visual_reranker"


def _with_node_logging(
    node_name: str,
    node_func: Callable[[ShoppingAnalysisState], dict[str, Any]],
) -> Callable[[ShoppingAnalysisState], dict[str, Any]]:
    def wrapped_node(state: ShoppingAnalysisState) -> dict[str, Any]:
        started_at = time.perf_counter()
        try:
            result = node_func(state)
            _print_node_elapsed(node_name, "completed", started_at, state["request"].search_mode)
            _print_graph_debug(node_name, result)
            return result
        except Exception as exc:
            _print_node_elapsed(node_name, "failed", started_at, state["request"].search_mode)
            _print_graph_error(node_name, exc)
            raise

    return wrapped_node


def _print_node_elapsed(node_name: str, status: str, started_at: float, search_mode: str) -> None:
    elapsed_sec = time.perf_counter() - started_at
    elapsed_ms = int(elapsed_sec * 1000)
    print(
        "\n[SyncShopper LangGraph Timing] "
        f"node={node_name} search_mode={search_mode} status={status} "
        f"elapsed_sec={elapsed_sec:.3f} elapsed_ms={elapsed_ms}",
        flush=True,
    )


def _print_total_elapsed(label: str, started_at: float) -> None:
    elapsed_sec = time.perf_counter() - started_at
    elapsed_ms = int(elapsed_sec * 1000)
    print(
        "\n[SyncShopper LangGraph Timing] "
        f"status={label} total_elapsed_sec={elapsed_sec:.3f} total_elapsed_ms={elapsed_ms}",
        flush=True,
    )



_analysis_graph = _build_graph()

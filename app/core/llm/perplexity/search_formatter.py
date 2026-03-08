from typing import Dict, Any, List


def format_search_results_for_llm(search_result: Dict[str, Any]) -> str:
    """Format search results as structured context for LLM with citations."""
    if not search_result or not search_result.get("content"):
        return ""
    
    content = search_result.get("content", "").strip()
    citations = search_result.get("citations", [])
    mode = search_result.get("mode", "unknown")
    model = search_result.get("model", "unknown")
    
    context_parts = [
        "=== WEB SEARCH RESULTS ===",
        f"Search Mode: {mode.upper()}",
        f"Model: {model}",
        "",
        "Search Findings:",
        content,
        ""
    ]
    
    if citations:
        context_parts.append("Sources:")
        for idx, citation in enumerate(citations, 1):
            context_parts.append(f"[{idx}] {citation}")
        context_parts.append("")
    
    return "\n".join(context_parts)


def format_search_results_display(search_result: Dict[str, Any]) -> Dict[str, Any]:
    """Format search results for API response display."""
    return {
        "query": search_result.get("query", ""),
        "mode": search_result.get("mode", "unknown"),
        "model": search_result.get("model", "unknown"),
        "content": search_result.get("content", ""),
        "citations": search_result.get("citations", []),
        "num_citations": len(search_result.get("citations", [])),
        "images": search_result.get("images", []),
        "usage": search_result.get("usage", {})
    }


def augment_messages_with_search(
    messages: List[Dict[str, Any]], 
    search_result: Dict[str, Any],
    instruction: str = None
) -> List[Dict[str, Any]]:
    """Augment messages with web search context."""
    search_context = format_search_results_for_llm(search_result)
    
    if not search_context:
        return messages
    
    if instruction is None:
        instruction = (
            "You are a helpful assistant with access to current web search results. "
            "Answer the user's question based on the provided search findings. "
            "IMPORTANT: For EVERY piece of information you use from the search results, you MUST cite it using this EXACT format: "
            "[Source: website-url] where website-url is the actual URL from the sources list. "
            "Place the citation immediately after the information it references. "
            "Example: 'Quantum computing achieved a breakthrough in 2024 [Source: techcrunch.com/article-url]. "
            "This technology uses qubits [Source: nature.com/quantum-article].' "
            "Cite EVERY fact and statement you make from the search results. "
            "Provide clear, accurate, and well-structured answers. "
            "If the search results don't fully answer the question, say so clearly."
        )
    
    system_message = {"role": "system", "content": f"{instruction}\n\n{search_context}"}
    return [system_message] + list(messages)

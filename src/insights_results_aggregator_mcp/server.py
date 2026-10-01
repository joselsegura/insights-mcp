"""Red Hat Insights Results Aggregator MCP Server.

MCP server for accessing Insights Results Aggregator endpoints via the
Red Hat Hybrid Cloud Console API.
"""

import logging
from typing import Annotated, Any

from fastmcp.tools import Tool
from mcp.types import ToolAnnotations
from pydantic import Field

from insights_mcp.mcp import InsightsMCP
from tools.common import run_insights_tool_request


class InsightsResultsAggregatorMCP(InsightsMCP):
    """MCP server for Insights Results Aggregator integration.

    This toolset is prepared for tools that access
    ``/api/insights-results-aggregator/v1`` and ``/api/insights-results-aggregator/v2`` endpoints.
    """

    def __init__(self):
        self.logger = logging.getLogger("InsightsResultsAggregatorMCP")

        general_intro = """You are an Insights Results Aggregator assistant that helps users access
        rule results and recommendation data from $container_brand_long Insights Results Aggregator.

        Add tools to this toolset when you need to query
        /api/insights-results-aggregator/v1 or /api/insights-results-aggregator/v2 endpoints.

        <|function_call_library|>

        """

        super().__init__(
            name="$container_brand_long Insights Results Aggregator MCP Server",
            toolset_name="insights-results-aggregator",
            api_path="api/insights-results-aggregator",
            instructions=general_intro,
        )

    def register_tools(self) -> None:
        """Register all available tools with the MCP server.

        To add another tool:
        1. Implement a method following ``tool_template`` below.
        2. Add that method to ``tool_functions``.
        3. Add an RBAC rest-map entry if the tool is read-only.
        """

        tool_functions = [
            self.list_clusters,
            # self.tool_template,
        ]

        for f in tool_functions:
            tool = Tool.from_function(f)
            tool.annotations = ToolAnnotations(readOnlyHint=True, openWorldHint=True)
            description_str = f.__doc__ or ""
            tool.description = description_str
            tool.title = description_str.split("\n", 1)[0]
            self.add_tool(tool)

    @staticmethod
    def v1(endpoint: str) -> str:
        """Build an Insights Results Aggregator v1 endpoint path."""
        return f"v1/{endpoint.lstrip('/')}"

    @staticmethod
    def v2(endpoint: str) -> str:
        """Build an Insights Results Aggregator v2 endpoint path."""
        return f"v2/{endpoint.lstrip('/')}"

    async def list_clusters(self) -> str:
        """List clusters available to the authenticated user.

        🟢 CALL IMMEDIATELY - No information gathering required.

        Uses the Insights Results Aggregator v2 ``/clusters`` endpoint, which returns clusters
        visible to the authenticated account along with recommendation hit counts and risk summaries.
        """
        return await run_insights_tool_request(
            self.insights_client.get(self.v2("clusters")),
            error_message=lambda exc: f"Error listing Insights Results Aggregator clusters: {exc}",
        )

    async def tool_template(
        self,
        host_id: Annotated[
            str,
            Field(
                default="",
                description="Optional host inventory ID to filter results. Replace with your tool parameters.",
            ),
        ],
    ) -> str:
        """Template tool for querying Insights Results Aggregator.

        🟢 CALL IMMEDIATELY - No information gathering required.

        Replace this method with a concrete tool name, parameters, endpoint, and response shape.
        Register it by adding ``self.<tool_name>`` to ``tool_functions`` in ``register_tools``.
        """

        params: dict[str, Any] = {}
        if host_id:
            params["host_id"] = host_id

        return await run_insights_tool_request(
            self.insights_client.get(self.v2("TODO/replace-with-endpoint/"), params=params),
            error_message=lambda exc: f"Error querying Insights Results Aggregator: {exc}",
        )


mcp = InsightsResultsAggregatorMCP()

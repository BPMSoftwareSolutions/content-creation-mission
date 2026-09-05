@capability:deliver-capsule-estate-mcp
@root-scenario:deliver-capsule-estate-mcp
Feature: Deliver capsule estate operations through MCP stdio

  An agentic client receives one MCP stdio server whose exact identity,
  protocol, tools, descriptions, input schemas, annotations, and operation
  bindings come from the admitted MCP interface authority. MCP delivery owns
  protocol carriers only; operate-capsule-estate owns every capsule operation.

  @scenario:deliver-capsule-estate-mcp
  @input:capsule-estate-mcp-delivery-request
  @input-contract:capsule-estate-mcp-delivery-request.v1
  @event:capsule-estate-mcp-delivery-requested
  @event-authority:deliver-capsule-estate-mcp.v1
  @outcome:capsule-estate-mcp-delivery-result
  @outcome-contract:capsule-estate-mcp-delivery-result.v1
  @outcome-terminal
  Scenario: Start the admitted capsule estate MCP stdio server
    Given the sidefx-capsule-estate server authority at version 0.1.0, MCP protocol 2025-11-25, stdio transport, and an admitted operate-capsule-estate binding
    When MCP delivery is requested
    Then the server connects through standard input and output, advertises tool-list change support, and remains available after each governed tool outcome

  @scenario:register-capsule-estate-mcp-tools
  @input:capsule-estate-mcp-delivery-request
  @input-contract:capsule-estate-mcp-delivery-request.v1
  @event:capsule-estate-mcp-tool-registration-requested
  @event-authority:register-capsule-estate-mcp-tools.v1
  @outcome:capsule-estate-mcp-delivery-result
  @outcome-contract:capsule-estate-mcp-delivery-result.v1
  @outcome-terminal
  Scenario: Register exactly the five authority-declared tools
    Given the admitted tool declarations for sidefx_capsules_verify, sidefx_capsules_list, sidefx_capsule_inspect, sidefx_capability_test, and sidefx_capability_invoke
    When the MCP tool catalog is requested
    Then each tool exposes its exact title, description, JSON input schema, safety annotations, and bound capsule operation and no undeclared tool is registered

  @scenario:invoke-capsule-estate-mcp-tool
  @input:capsule-estate-mcp-delivery-request
  @input-contract:capsule-estate-mcp-delivery-request.v1
  @event:capsule-estate-mcp-tool-invocation-requested
  @event-authority:invoke-capsule-estate-mcp-tool.v1
  @outcome:capsule-estate-mcp-delivery-result
  @outcome-contract:capsule-estate-mcp-delivery-result.v1
  @outcome-terminal
  Scenario: Invoke the operation bound to one declared MCP tool
    Given schema-admitted tool arguments and the tool declaration's exact capability operation
    When the tool is called
    Then one canonical capsule operation request is invoked and a successful outcome returns human-readable JSON text plus an identical structured result

  @scenario:represent-capsule-estate-mcp-failure
  @input:capsule-estate-mcp-delivery-request
  @input-contract:capsule-estate-mcp-delivery-request.v1
  @event:capsule-estate-mcp-failure-representation-requested
  @event-authority:represent-capsule-estate-mcp-failure.v1
  @outcome:capsule-estate-mcp-delivery-result
  @outcome-contract:capsule-estate-mcp-delivery-result.v1
  @outcome-terminal
  Scenario: Represent governed operation failure without terminating the server
    Given invalid tool arguments or a failed projected capsule operation
    When the tool call completes
    Then the exact governed failure is returned as MCP error content and structured error data while the stdio server continues serving subsequent admitted requests

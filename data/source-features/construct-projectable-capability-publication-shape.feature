@capability:construct-projectable-capability-publication-shape
@root-scenario:construct-projectable-capability-publication-shape
Feature: Construct a bounded publication shape for an admitted capability candidate

  A projectable capability candidate contains one unchanged canonical feature
  and exactly eleven admitted companion artifacts. Before a file-system tool
  may publish those bytes, the Agentic Harness must construct one closed,
  provider-neutral shape that fixes every source path, target path, operation,
  conflict policy, traversal policy, symlink policy, and proof requirement.

  The ordered artifact facts place `consumer-workspace.authority.json` last.
  The destination is required to be fresh and every mapping is authorized or
  rejected before mutation begins. Consequently, a partial execution cannot
  expose the workspace authority commit marker and cannot be mistaken for an
  SDA source-admitted workspace.

  This capability performs no filesystem mutation. It only projects admitted
  publication facts into the existing file-system shaping contract. The
  admitted file-system tool owns physical execution and hash testimony; the
  ordinary SDA projector independently decides source admission and projection
  readiness after publication.

  @scenario:construct-projectable-capability-publication-shape
  @input:admitted-projectable-capability-publication-facts
  @input-contract:admitted-projectable-capability-publication-facts.v1
  @event:capability-publication-planning-requested
  @event-authority:construct-projectable-capability-publication-shape.v1
  @outcome:projectable-capability-publication-shape-known
  @outcome-contract:projectable-capability-publication-shape-evidence.v1
  @outcome-terminal
  Scenario: Authorize the complete fresh-destination mapping before mutation
    Given one admitted candidate whose canonical feature and eleven companion artifacts have unique safe paths and place workspace authority last
    When the complete source-to-destination publication shape is constructed
    Then one closed file-system shaping contract requires a fresh target, ordered copy operations, traversal and symlink rejection, source preservation, and source-to-target hash equality

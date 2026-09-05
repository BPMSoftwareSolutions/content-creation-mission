@capability:project-portfolio-alignment-view
@root-scenario:project-portfolio-alignment-view
Feature: Project a read-only portfolio alignment view

  Portfolio is a governed analytical lens, not an eighth semantic altitude.

  This capability projects admitted product-fit snapshot references into one
  replayable analytical view. It preserves product fit, counterevidence,
  non-observable coverage, evidence cutoff, mapping expiry, and declared
  change impact. It emits no portfolio score, fit disposition, priority, or
  decision and changes no authority, binding, admission, or execution state.

  @scenario:project-portfolio-alignment-view
  @input:portfolio-alignment-view-record
  @input-contract:portfolio-alignment-view-record.v1
  @event:portfolio-alignment-view-requested
  @event-authority:project-portfolio-alignment-view.v1
  @outcome:portfolio-alignment-view-record
  @outcome-contract:portfolio-alignment-view-record.v1
  @outcome-terminal
  Scenario: Project one read-only portfolio alignment view
    Given one admitted query authority and product-fit snapshot reference set
    When the portfolio alignment view is projected
    Then exact product, counterevidence, non-observable, expiry, evidence-age, and impact evidence is returned with one query receipt and no score, fit conclusion, decision, or mutation

  @scenario:admit-portfolio-view-inputs
  @input:portfolio-alignment-view-record
  @input-contract:portfolio-alignment-view-record.v1
  @event:portfolio-view-input-admission-requested
  @event-authority:admit-portfolio-view-inputs.v1
  @outcome:portfolio-alignment-view-record
  @outcome-contract:portfolio-alignment-view-record.v1
  @outcome-terminal
  Scenario: Admit portfolio view evidence
    Given product snapshots, one strategic scope, one time horizon, and one read-only query authority
    When portfolio view input admission is evaluated
    Then source admission, identity, uniqueness, evaluation, time, and no-authority boundaries are reported

  @scenario:project-portfolio-view-facets
  @input:portfolio-alignment-view-record
  @input-contract:portfolio-alignment-view-record.v1
  @event:portfolio-view-facets-requested
  @event-authority:project-portfolio-view-facets.v1
  @outcome:portfolio-alignment-view-record
  @outcome-contract:portfolio-alignment-view-record.v1
  @outcome-terminal
  Scenario: Project portfolio evidence facets
    Given an admitted product-fit snapshot reference set
    When portfolio evidence facets are projected
    Then full product status, counterevidence, non-observable, expiry, evidence timestamp, and impact vectors remain inspectable without aggregation or scoring

  @scenario:bind-portfolio-view-receipt
  @input:portfolio-alignment-view-record
  @input-contract:portfolio-alignment-view-record.v1
  @event:portfolio-view-receipt-requested
  @event-authority:bind-portfolio-view-receipt.v1
  @outcome:portfolio-alignment-view-record
  @outcome-contract:portfolio-alignment-view-record.v1
  @outcome-terminal
  Scenario: Bind one portfolio query receipt
    Given one exact query, authority, snapshot vector, time horizon, and projected result
    When the portfolio view receipt is bound
    Then equivalent inputs reproduce one receipt and no analytical result acquires authority

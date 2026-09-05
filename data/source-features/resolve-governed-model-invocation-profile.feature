@capability:resolve-governed-model-invocation-profile
@root-scenario:resolve-governed-model-invocation-profile
Feature: Resolve the governed model invocation profile

  Every capability that invokes a model needs the same governed terms of
  invocation. Those terms are upstream meaning. They are established once,
  here, and consumed downstream by identity.

  This capability admits one model invocation authority and resolves it into
  one product: the terms that are fixed for every caller, and the parameters a
  caller is permitted to choose, each with the bounds the authority admits.

  A caller does not restate a fixed term. A caller chooses only among the
  declared permitted parameters, within their declared bounds. A term that is
  neither fixed nor permitted is not available to a caller at all.

  The product carries its own identity. A downstream capability references that
  identity rather than copying the terms, so two callers cannot hold divergent
  copies of the same governed meaning.

  Resolution observes authority only. It selects no provider, reads no
  credential, contacts no provider, and claims no acceptance. An authority that
  cannot be observed, or that fixes and permits the same term, is held with
  exact findings rather than resolved into a profile.

  @scenario:resolve-governed-model-invocation-profile
  @input:governed-model-invocation-profile-request
  @input-contract:governed-model-invocation-profile-request.v1
  @event:resolve-governed-model-invocation-profile
  @event-authority:resolve-governed-model-invocation-profile.v1
  @outcome:governed-model-invocation-profile
  @outcome-contract:governed-model-invocation-profile.v1
  @outcome-terminal
  Scenario: Resolve one governed model invocation profile from admitted authority
    Given one admitted model invocation authority declaring the terms it fixes and the caller parameters it permits
    When the fixed terms and permitted caller parameters are resolved into one identified product
    Then one governed model invocation profile carrying its fixed terms, its permitted caller parameters, and its own identity is established, or resolution is held with one exact finding for each unresolved term

  @scenario:admit-model-invocation-authority
  @input:governed-model-invocation-profile-request
  @input-contract:governed-model-invocation-profile-request.v1
  @event:admit-model-invocation-authority
  @event-authority:admit-model-invocation-authority.v1
  @outcome:admitted-model-invocation-authority
  @outcome-contract:admitted-model-invocation-authority.v1
  @outcome-terminal
  Scenario: Admit the model invocation authority being resolved
    Given one declared model invocation authority and its digest
    When the authority, its declared terms, and its digest are observed without model, network, credential, or clock access
    Then the authority is admitted for resolution, or resolution is held when the authority or its digest cannot be observed

  @scenario:resolve-fixed-invocation-terms
  @input:admitted-model-invocation-authority
  @input-contract:admitted-model-invocation-authority.v1
  @event:resolve-fixed-invocation-terms
  @event-authority:resolve-fixed-invocation-terms.v1
  @outcome:fixed-governed-invocation-terms
  @outcome-contract:fixed-governed-invocation-terms.v1
  @outcome-terminal
  Scenario: Resolve every term that no caller may vary
    Given the admitted authority and the terms it declares as fixed
    When the authority is resolved into the single value every caller receives for each fixed term
    Then every fixed term carries exactly one value no caller may override, and a term declared both fixed and caller-permitted is held as a contradiction rather than resolved

  @scenario:declare-permitted-caller-parameters
  @input:fixed-governed-invocation-terms
  @input-contract:fixed-governed-invocation-terms.v1
  @event:declare-permitted-caller-parameters
  @event-authority:declare-permitted-caller-parameters.v1
  @outcome:governed-model-invocation-profile
  @outcome-contract:governed-model-invocation-profile.v1
  @outcome-terminal
  Scenario: Declare which parameters a caller may choose and within what bounds
    Given the fixed terms and the parameters the authority permits a caller to choose
    When each permitted parameter is bound to its admitted bound and its value when the caller declares none
    Then one profile carries its fixed terms, its permitted caller parameters with their bounds and defaults, and one identity that downstream capabilities reference instead of restating any term

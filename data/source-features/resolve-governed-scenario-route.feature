@capability:resolve-governed-scenario-route
@root-scenario:resolve-governed-scenario-route
Feature: Resolve the governed scenario execution route

  An execution surface holds one admitted scenario outcome and needs to know
  what may legitimately happen next. Canonical blueprint authority already
  declares that answer as branch routes, fan-out sets, convergence
  requirements, terminal dispositions, and bounded returns. This capability
  reads that declared authority and establishes exactly the continuation it
  authorizes.

  Resolution happens before invocation. The product is an authorized
  continuation, not an execution. This capability never invokes a scenario,
  never runs the scenario kernel, never mutates route state, and never
  produces an effect. Scenario invocation remains a separate narrow
  responsibility that receives an already-authorized invocation and performs
  it, and the five-step scenario kernel is unchanged.

  Route state is observed, never owned. Every fact the resolution depends on
  arrives as admitted input: the scenario outcome, the declared route
  authority, and a route-state snapshot. No responsibility here reads retained
  or ambient execution context, and none persists anything between requests.
  The capability is state-aware and stateless.

  Every continuation is derived from declared route authority. A route the
  blueprint does not declare is never inferred, a variant the outcome did not
  select is never followed, and an ambiguous or absent route is returned as
  exact rejection evidence rather than resolved by ordering, position, or
  convenience. Fan-out, convergence, terminal selection, and bounded return
  are consequences of that authority, not special cases invented by an
  executor, and no execution provider is asked to interpret branch meaning.

  @scenario:resolve-governed-scenario-route
  @input:scenario-route-resolution-request
  @input-contract:scenario-route-resolution-request.v1
  @event:governed-scenario-route-resolution-requested
  @event-authority:resolve-governed-scenario-route.v1
  @outcome:authorized-scenario-continuation
  @outcome-contract:authorized-scenario-continuation.v1
  @outcome-terminal
  Scenario: Establish the continuation the blueprint authorizes
    Given one admitted scenario outcome, the declared route authority governing its node, and the current route state
    When the governed scenario route is resolved
    Then exactly one authorized continuation is established from declared route authority, or exact rejection evidence is returned, and no scenario is invoked and no route state is mutated

  @scenario:resolve-selected-outcome-variant
  @input:scenario-route-resolution-request
  @input-contract:scenario-route-resolution-request.v1
  @event:selected-outcome-variant-resolution-requested
  @event-authority:resolve-selected-outcome-variant.v1
  @outcome:selected-outcome-variant
  @outcome-contract:selected-outcome-variant.v1
  @outcome-variants:VARIANT_RESOLVED|VARIANT_UNDECLARED
  @outcome-terminal
  Scenario: Resolve which declared variant the admitted outcome selected
    Given one admitted scenario outcome and the variants its node declares
    When the selected variant is resolved
    Then the outcome resolves to exactly one variant the node declares, and an outcome selecting a variant the node does not declare is returned as exact rejection evidence rather than defaulted to any declared variant

  @scenario:resolve-declared-outgoing-routes
  @input:selected-outcome-variant
  @input-contract:selected-outcome-variant.v1
  @event:declared-outgoing-route-resolution-requested
  @event-authority:resolve-declared-outgoing-routes.v1
  @outcome:declared-outgoing-route-set
  @outcome-contract:declared-outgoing-route-set.v1
  @outcome-variants:ROUTES_RESOLVED|NO_ROUTE_DECLARED|AMBIGUOUS_ROUTE
  @outcome-terminal
  Scenario: Resolve the routes the blueprint declares for that variant
    Given one selected outcome variant carrying the declared route authority of its node
    When the outgoing routes for that variant are resolved
    Then the route set is resolved only against the route authority the admitted input carries and never against ambient blueprint context, contains only routes the blueprint declares for that exact variant, a node that declares no route for a selected variant is returned as exact rejection evidence, and two routes selectable by the same variant are returned as ambiguous rather than ordered

  @scenario:admit-current-route-state
  @input:route-state-admission-context
  @input-contract:route-state-admission-context.v1
  @event:current-route-state-admission-requested
  @event-authority:admit-current-route-state.v1
  @outcome:current-route-state-snapshot
  @outcome-contract:current-route-state-snapshot.v1
  @outcome-terminal
  Scenario: Admit the route-state snapshot as declared input
    Given one route-state admission context carrying the route-state source and governing blueprint identity presented with the resolution request
    When the current route state is admitted
    Then one immutable snapshot carries the established convergence products, completed fan-out members, and iterations already taken on each route, bound to the same governing blueprint identity, and route state absent from the admitted request is returned as exact rejection evidence rather than read from retained or ambient execution context

  @scenario:resolve-fan-out-membership
  @input:route-evaluation-context
  @input-contract:route-evaluation-context.v1
  @event:fan-out-membership-resolution-requested
  @event-authority:resolve-fan-out-membership.v1
  @outcome:fan-out-membership
  @outcome-contract:fan-out-membership.v1
  @outcome-terminal
  Scenario: Resolve fan-out membership as jointly required
    Given one route evaluation context, of which this responsibility reads only the declared route view
    When fan-out membership is resolved
    Then a route set belonging to a declared fan-out set carries every declared member of that set as jointly required, a set carrying fewer members than the blueprint declares is returned as exact rejection evidence, and a route set belonging to no fan-out set reports that plainly rather than fabricating a single-member fan-out

  @scenario:resolve-convergence-readiness
  @input:route-evaluation-context
  @input-contract:route-evaluation-context.v1
  @event:convergence-readiness-resolution-requested
  @event-authority:resolve-convergence-readiness.v1
  @outcome:convergence-readiness
  @outcome-contract:convergence-readiness.v1
  @outcome-terminal
  Scenario: Resolve whether a convergence has every required product
    Given one route evaluation context carrying the declared route view and the admitted route-state snapshot
    When convergence readiness is resolved
    Then a route reaching a convergence is ready only when every product the convergence declares is present against the same governing identity, a convergence missing any declared product is reported pending rather than advanced, and a route reaching no convergence reports that plainly

  @scenario:resolve-bounded-return-authority
  @input:route-evaluation-context
  @input-contract:route-evaluation-context.v1
  @event:bounded-return-authority-resolution-requested
  @event-authority:resolve-bounded-return-authority.v1
  @outcome:bounded-return-authorization
  @outcome-contract:bounded-return-authorization.v1
  @outcome-terminal
  Scenario: Resolve bounded return against its declared iteration authority
    Given one route evaluation context whose admitted route-state snapshot carries the iterations already taken on this route
    When bounded return authority is resolved
    Then a bounded return is authorized only while the iterations taken remain within the bound its declared authority fixes, a bounded return whose bound is exhausted is returned as exact rejection evidence, and a route carrying no bounded return reports that plainly

  @scenario:establish-authorized-continuation
  @input:continuation-evidence
  @input-contract:continuation-evidence.v1
  @event:authorized-continuation-establishment-requested
  @event-authority:establish-authorized-continuation.v1
  @outcome:authorized-scenario-continuation
  @outcome-contract:authorized-scenario-continuation.v1
  @outcome-variants:NEXT_SCENARIO_AUTHORIZED|FAN_OUT_AUTHORIZED|BOUNDED_RETURN_AUTHORIZED|CONVERGENCE_PENDING|TERMINAL_REACHED|ROUTE_REJECTED
  @outcome-terminal
  Scenario: Establish exactly one authorized continuation
    Given fan-out membership, convergence readiness, and bounded return authority resolved against the same declared route set
    When the authorized continuation is established
    Then exactly one declared continuation is established: one next scenario invocation, every member of a declared fan-out set, an authorized bounded return, a convergence held pending its missing products, a terminal disposition reached, or a rejected route, and the established continuation retains which authorization occurred, its selected invocation set, the source route identities, the governing blueprint digest, and the route-state digest it was resolved against, naming only invocations the declared route authority permits

@capability:operate-tooling-migration-inventory
@root-scenario:operate-tooling-migration-inventory
Feature: Operate the tooling migration inventory from declared authority

  This projected command replaces the inventory mechanics in
  capabilities/tooling-migration-runtime/node/tooling-migration-operation-provider.mjs,
  especially discoverInventory at lines 155-196 and inventory routing at
  lines 453-472. The original implementation remains only as a frozen oracle
  until exact public-outcome equivalence is proved.

  Inventory candidates are declared semantic authority. The version-controlled
  tooling-migration-inventory.authority.json names every admitted group,
  capability, scenario responsibility, current provider and protocol, feature
  reference, workspace reference, and observed feature/workspace presence fact.
  A projected repository-observation capability may read the exact authority
  bytes and digest, but repository folders cannot create candidate identity or
  migration state. Adding a candidate is an authority change suitable for later
  database storage.

  The pinned projected decide-tooling-migration capability remains the sole
  classification authority. This command constructs its complete
  CLASSIFY_INVENTORY request, preserves the returned inventory unchanged, and
  adds only the public operation and interface dispositions. It must not bind
  sda-governed-tooling-migration-operation-port.v1, reference
  tooling-migration-operation-provider.mjs as an executable provider, enumerate
  a directory, infer semantics from physical structure, or write a second
  runtime inventory as substitute proof. Its version-controlled source authority
  and projected physical output are the durable receipts.

  @scenario:operate-tooling-migration-inventory
  @input:tooling-migration-inventory-request
  @input-contract:tooling-migration-inventory-request.v1
  @event:operate-tooling-migration-inventory
  @event-authority:operate-tooling-migration-inventory.v1
  @outcome:tooling-migration-inventory-context
  @outcome-contract:tooling-migration-inventory-context.v1
  Scenario: Resolve the pinned declared inventory observation request
    Given one admitted request naming tooling-migration.authority.v1
    When the projected inventory command is invoked
    Then one bounded context pins tooling-migration-inventory.authority.json, its exact governed repository observation request, and request lineage without enumerating repository structure or assigning migration state

  @scenario:observe-declared-tooling-migration-inventory-authority
  @input:tooling-migration-inventory-context
  @input-contract:tooling-migration-inventory-context.v1
  @event:observe-declared-tooling-migration-inventory-authority
  @event-authority:observe-declared-tooling-migration-inventory-authority.v1
  @outcome:observed-tooling-migration-inventory-authority
  @outcome-contract:observed-tooling-migration-inventory-authority.v1
  Scenario: Observe the exact inventory authority bytes through a projected capability
    Given one pinned observe-governed-repository projected binding and one declared inventory authority resource
    When that projected capability observes presence, exact bytes, and digest once
    Then one bounded observation retains the authority testimony and nested capability lineage without interpreting candidate state or discovering undeclared resources

  @scenario:classify-declared-tooling-migration-inventory
  @input:observed-tooling-migration-inventory-authority
  @input-contract:observed-tooling-migration-inventory-authority.v1
  @event:classify-declared-tooling-migration-inventory
  @event-authority:classify-declared-tooling-migration-inventory.v1
  @outcome:classified-tooling-migration-inventory
  @outcome-contract:classified-tooling-migration-inventory.v1
  Scenario: Delegate classification to projected deterministic decision authority
    Given exact observed inventory authority bytes containing the declared candidate facts
    When a complete CLASSIFY_INVENTORY request is constructed and passed to the pinned projected decide-tooling-migration capability
    Then its tooling-projection-migration-inventory.v1 decision is retained unchanged with pinned binding and capability-authority digest lineage

  @scenario:publish-tooling-migration-inventory-outcome
  @input:classified-tooling-migration-inventory
  @input-contract:classified-tooling-migration-inventory.v1
  @event:publish-tooling-migration-inventory-outcome
  @event-authority:publish-tooling-migration-inventory-outcome.v1
  @outcome:tooling-migration-inventory-evidence
  @outcome-contract:tooling-migration-inventory-evidence.v1
  @outcome-terminal
  Scenario: Return the legacy-compatible public inventory outcome
    Given one terminated projected classification with complete nested lineage
    When the public inventory result is shaped
    Then operation inventory, disposition INVENTORIED, interface exit disposition ZERO, and the unchanged classified inventory are returned with no ignored runtime artifact treated as the conformance receipt

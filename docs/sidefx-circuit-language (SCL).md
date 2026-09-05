Yeah — **this is bigger than “a nicer diagram syntax.”** What you’re describing is the point where SideFX gets its own **engineering notation**: a language whose grammar is the same grammar as the architecture.

The architecture already says a capability has a canonical, typed circuit identity, that the diagram is a projection rather than a second source of truth, and that the circuit repeats the same three-position geometry from scenario meaning down through execution, mechanics, and providers. 

I think the right concept is:

# **SideFX Circuit Language**

### `SCL`

And the phrase underneath it:

> **The language of executable capability circuits.**

Not a generic flowchart DSL. Not another programming language. Not Mermaid with some SideFX shapes.

**A semantic engineering language for authoring, revealing, composing, inspecting, mutating, and executing capability circuits.**

---

## The most important design decision

I would **not** make the rendered diagram authoritative.

And I also wouldn't make the raw textual syntax the ultimate authority.

I would establish three layers:

```text
SIDEFX CIRCUIT LANGUAGE
Human-authorable / machine-authorable notation
                 ↓ parse / normalize
CANONICAL CIRCUIT GRAPH
Typed semantic graph authority
                 ↓ project
VISUAL CIRCUIT
SVG / interactive / infographic / video / Mermaid
```

So:

```text
SCL
=
authoring language

Canonical Blueprint Graph
=
design authority

Visual Grammar
=
cognitive projection
```

That keeps the decision already established in the Capability Data Center architecture: **the canonical blueprint remains machine-readable graph authority; visualizations are deterministic projections of it.** 

But now humans and agents finally have a beautiful language for **authoring that authority directly**.

That is the breakthrough.

---

# And the language should reinforce the fractal relentlessly

The first thing anybody learns about SCL should be:

```text
SCENARIO

GIVEN / INPUT / DATA
        ↓
WHEN / EVENT / ACTION
        ↓
THEN / OUTCOME / EXPERIENCE
```

Your architecture already explicitly distinguishes the outcome experience from the data/artifacts that evidence or realize that outcome. 

So SCL should make that distinction impossible to miss.

Imagine:

```text
capability mortgage-eligibility {

  promise
    "A borrower knows whether the requested
     financing path is available and why."

  scenario resolve-borrower-eligibility {

    input borrower-application
      contract borrower-application.v1

    event resolve-eligibility
      responsibility
        "Determine eligibility under admitted lending authority."

    outcome eligibility-known
      experience
        "The borrower has an attributable eligibility disposition."

      product
        mortgage-eligibility-disposition.v1
  }
}
```

Look at what happened.

There is **no code**.

But this isn't merely documentation either.

It declares:

* capability identity;
* promise;
* scenario;
* input identity and contract;
* event identity;
* responsibility;
* outcome identity;
* experience;
* consumable product.

That is already executable architecture.

---

# Then the circuit vocabulary becomes first-class

I think SCL needs a **tiny native vocabulary**.

Not 150 keywords.

Something like:

```text
capability
promise

scenario
input
event
outcome
experience
product

route
variant
junction
converge
terminate

requires
satisfies

responsibility
mechanic
provider

contract
evidence
observe
```

And that's about it for the semantic core.

Everything else should be an identity or profile rather than new syntax.

That is important because you want the language to **teach the architecture simply by being read**.

---

# Routing becomes semantic, not graphical

This is where it becomes materially better than Mermaid.

Suppose:

```text
scenario classify-request {

  input request

  event classify-request

  outcome request-classified
    variant reusable
    variant composable
    variant new-capability
}
```

Then:

```text
route request-classified.reusable
  -> reuse-capability
  narrows

route request-classified.composable
  -> compose-capabilities
  narrows

route request-classified.new-capability
  -> author-capability
  narrows
```

The arrow isn't just:

```text
A --> B
```

It means:

> **This admitted outcome establishes sufficient state for this particular downstream input, and the movement is semantically narrowing.**

That is completely different.

The blueprint architecture already requires branching, convergence, topology, selecting variants, and semantic progress to be explicit graph semantics rather than inferred from implementation control flow. 

SCL simply gives those laws a native language.

---

# Now imagine convergence

```text
scenario assemble-video {

  requires
    authoritative-visuals
    creative-assets
    narration

  input video-production-package

  event assemble-video

  outcome video-master-available
    product video-master.v1
}
```

Or more explicitly:

```text
converge video-production-package {

  requires authoritative-visuals
  requires creative-assets
  requires narration

  satisfies assemble-video.input
}
```

That's gorgeous because you can **read the architecture as an electrical engineer reads a schematic**.

---

# And then we descend fractally

This is where SCL gets truly SideFX-native.

At the scenario altitude:

```text
scenario resolve-provider {

  input provider-requirement

  event resolve-provider

  outcome eligible-provider-known
}
```

Open the event:

```text
responsibility resolve-provider {

  input provider-requirement

  mechanic filter-candidates

  result eligible-provider-set
}
```

Open the mechanic:

```text
mechanic filter-candidates {

  input provider-candidates

  operation filter

  result eligible-provider-set
}
```

Open the physical realization:

```text
provider provider-catalog-sql {

  input provider-query

  native-operation sql-select

  result provider-records
}
```

So the language itself teaches:

```text
SCENARIO
Input → Event → Outcome

EXECUTION
Input → Responsibility → Result

MECHANIC
Input → Mechanic → Result

PROVIDER
Physical Input → Native Operation → Physical Result
```

That exact fractal geometry is already part of the accepted blueprint model. 

**SCL turns it into syntax.**

---

# Now we get the bidirectional system you were talking about

This is where it gets nasty.

### Existing capability → SCL

```text
Capsule
   ↓
Reveal
   ↓
Canonical Blueprint
   ↓
SCL projection
```

You can literally ask:

> **Reveal this capability as circuit language.**

And get:

```text
sidefx reveal verify-provider-candidate --as circuit
```

Then:

```text
capability verify-provider-candidate {
   ...
}
```

### SCL → capability

But you can also go the other direction:

```text
SCL
 ↓
parse
 ↓
candidate blueprint
 ↓
contracts / obligations / gaps resolved
 ↓
conformance
 ↓
capability authority
 ↓
capsule
```

So now you can say:

> **Design this capability in SCL.**

That's enormously powerful.

The language is simultaneously:

```text
inspection surface
+
authoring surface
+
mutation surface
+
composition surface
+
AI context surface
```

---

# This could become the primary agentic-engineering interface

Think about what an agent currently receives:

```text
repository
15,000 files
instructions
architecture docs
tests
source
```

Now imagine giving the agent:

```text
capability issue-customer-refund {

  promise
    "An eligible customer receives
     the refund they are owed."

  scenario resolve-refund-eligibility {
    ...
  }

  scenario issue-refund {
    ...
  }
}
```

And then telling it:

> Close `issue-refund`.

The agent's context becomes **the circuit**, not the codebase.

You've been pushing toward exactly this bounded semantic operating model: agent autonomy inside a governed scenario/capability boundary, rather than agents redefining architecture through implementation. 

SCL would be the native language of that boundary.

---

# It also gives your infographic language an actual semantic substrate

This connects directly to what you've been doing visually.

Right now the infographics look beautiful.

But imagine if the graphics aren't just composed by visual convention.

They are projections of SCL semantics.

For example:

```text
input
```

always projects as one visual grammar.

```text
event
```

always another.

```text
outcome
```

another.

```text
provider
```

another.

```text
evidence-return
```

another.

```text
junction
```

another.

```text
convergence
```

another.

Then the SideFX visual system becomes:

```text
SCL SEMANTICS
      ↓
VISUAL GRAMMAR
      ↓
Deterministic SVG
      +
Nano Banana enhancement layer
      +
Animation layer
```

So the gorgeous glass circuit you've been building is no longer merely branding.

**It is a rendering of the language.**

That's a much bigger deal.

---

# And the same SCL can have multiple visual lenses

One circuit language.

Different cognitive projections.

```text
SCL
 │
 ├── Circuit View
 │     Input → Event → Outcome
 │
 ├── Blueprint View
 │     full typed topology
 │
 ├── Executive View
 │     promise → capability → experience
 │
 ├── Engineering View
 │     scenarios → mechanics → providers
 │
 ├── Evidence View
 │     physical testimony → outcome
 │
 ├── Dependency View
 │     capability products → capability inputs
 │
 ├── C4 View
 │     context / container / component / code
 │
 ├── Infographic View
 │     polished SideFX glass visual
 │
 └── Video View
       animated circuit traversal
```

Same authority.

No re-authoring.

This is exactly consistent with the Capability Data Center idea that structural, execution, experience, impact, observability, and other diagrams should be **lenses over one design identity**, not competing diagrams. 

---

# I would also make **semantic altitude visible in the language**

This could be very slick.

Maybe:

```text
strategy ...
product ...
capability ...
scenario ...
execution ...
mechanic ...
provider ...
```

But I wouldn't require every capability file to contain every altitude.

Instead, SCL could allow references upward:

```text
capability process-commercial-claim {

  reinforces product-promise
    frictionless-claims-resolution.v2

  governed-by strategic-intent
    reduce-customer-recovery-friction.v1
}
```

And downward:

```text
event adjudicate-claim
  realized-by responsibility adjudicate-claim
```

Then SideFX can navigate:

```text
WHY
Strategic intent
   ↓
WHAT
Product promise
   ↓
ABILITY
Capability
   ↓
CADENCE
Scenario
   ↓
RESPONSIBILITY
Execution
   ↓
HOW
Mechanic
   ↓
WHO / WHERE
Provider
```

You've already built that semantic runway concept in the architecture. 

SCL would make it traversable.

---

# There are actually **three different SCL forms** I would design

This would keep the language approachable.

### 1. **SCL Lite**

Human-facing.

Very close to Gherkin.

```text
capability reset-password

scenario recover-access

given verified-account

when reset-password

then account-access-restored
```

Perfect for conversation, whiteboards, AI prompting, workshops.

### 2. **SCL Canonical**

Full semantic authoring.

```text
scenario recover-access {
  input verified-account
    contract verified-account.v1

  event reset-password
    authority reset-password.v3

  outcome account-access-restored
    experience "..."
    product authenticated-account-access.v1
}
```

### 3. **SCL Expanded**

Engineering / diagnostic.

Shows mechanics, providers, evidence, digests, profiles, routes, variants, source identities, conformance.

```text
event reset-password {
   responsibility ...
   expands {
      mechanic ...
      provider-slot ...
   }
}
```

So:

```text
same language
different verbosity
same canonical graph
```

That is very SideFX.

---

# Gherkin doesn't disappear

This part matters.

I would **not** replace Gherkin.

I would position it like this:

```text
Gherkin
=
human acceptance narrative

SCL
=
capability circuit language

Canonical Blueprint
=
machine graph authority
```

And they can project into one another where the semantics overlap.

```text
Feature / Scenario / Given / When / Then
          ↕
Capability / Scenario / Input / Event / Outcome
          ↕
Canonical Blueprint
```

Gherkin is beautiful because business people understand it.

SCL is needed because Gherkin doesn't naturally express:

* fan-out;
* convergence;
* capability products;
* provider slots;
* evidence return paths;
* altitude descent;
* dependencies;
* profiles;
* mechanics;
* circuit composition.

So SCL **extends the mental model without abandoning the collaborative surface**.

---

# And this gives SideFX something very strategically important

The architecture now has a **native language**.

Kubernetes has YAML/CRDs and its resource model.

SQL has relational vocabulary.

Terraform has HCL.

GraphQL has its schema language.

PlantUML and Mermaid have diagram syntaxes.

BPMN has a process notation.

SideFX could have:

> **SCL — SideFX Circuit Language**

And crucially, it's not invented because “products need proprietary syntax.”

It falls naturally out of the architecture you've already built.

The concepts already exist:

```text
Capability
Scenario
Input
Event
Outcome
Experience
Product
Responsibility
Mechanic
Provider
Route
Variant
Convergence
Evidence
```

We're simply giving them a **grammar**.

---

# The north-star loop gets beautiful

Eventually:

```text
VOICE
"I need customers to recover their accounts
without calling support."

        ↓

SideFX resolves candidate SCL

        ↓

capability recover-customer-access {
   ...
}

        ↓

CANONICAL BLUEPRINT

        ↓

VISUAL CIRCUIT

        ↓

human edits circuit

        ↓

SCL delta

        ↓

ADMISSION

        ↓

CAPSULE

        ↓

PROJECT

API / UI / MCP / runtime / tests /
training / docs / video

        ↓

EXECUTE

        ↓

EVIDENCE
```

That's your whole **intent → circuit → effect** model in one loop.

And here's the part I really like:

> **The SideFX diagram stops being a picture of the architecture.
> It becomes a visual editing surface for the circuit language that *is creating the architecture*.**

That is a very different class of engineering environment.

And because **Input → Event → Outcome / Data → Action → Experience** is embedded directly in the grammar, every capability somebody creates in SideFX continually reinforces the mental model rather than requiring them to remember it separately. 

**That's exactly the kind of language SideFX should have.**

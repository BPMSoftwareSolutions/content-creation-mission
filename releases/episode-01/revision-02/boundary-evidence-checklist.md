# Before trusting an agent permission label

Public exercise newly authored for this edition. No reserved pilot assessment is included. No production boundary proof or learner validation is claimed.

## Use it on one consequential action

- Name the effect and exact object. What would change for whom?
- Write the user's request separately from the organization's grant and any operator approval.
- Bind the permitted action, object, arguments, caller and policy version. Who can change that grant?
- Locate the dispatcher and the effect credential. Which component can actually prevent dispatch?
- Observe one denied attempt and one permitted output in the same session. State what the observer can and cannot see.
- Change an object or argument. Does the old grant stop matching? Test unavailable authorization too.
- Name an alternate route, such as a shell or second adapter. Mark it unverified until there is evidence.

## Worked example / frozen rule

- For operation ADJUDICATE, the frozen name test returns OPERATOR_REQUIRED for dangerous-tool and ALLOW for publish-alias. This is a local evaluation of a pinned expression, not an escaped live effect.
- That expression contains no grant check. Its returned ALLOW label is not the proposed design's PERMIT decision.

## Worked example / local toy simulation

- Grant: editor may inspect C-17 with readOnly=true, policy toy-v1. Publication attempt held; the local dispatcher records zero effect calls.
- Inspection returns title and owner as passing, required summary as missing. C-17 published state remains false.
- Inspection of C-18 with the C-17 grant is held. Changed readOnly arguments and unavailable authorization are also held.
- The observer is the local dispatcher function, not the agent. Its record covers only this toy route. Production credential isolation, shell routes, other adapters and other sessions remain unverified.

## Fresh public exercise

- A draft-email agent has a grant to draft message M-8 for recipient A. Its tool returns ALLOW after the recipient is changed to B. What additional checks and observations would you need before sending?
- Write your effect, bound identity, enforcing component, changed condition and unobserved route. Do not infer that a send occurred from the label.

## Relationship to established guidance

- OWASP Excessive Agency guidance recommends limiting tool functionality and permissions and validating downstream requests. This lesson isolates one concrete failure of a name test and one proposed place to enforce a bound grant.

[OWASP: Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)

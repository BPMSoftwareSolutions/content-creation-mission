# An AI Permission Check Is Not an Off Switch | SideFX Episode 1

LOCAL REVIEW / NOT PUBLISHED

## 01 / FICTIONAL REQUEST

Inspect candidate C seventeen. Do not publish it. The agent queues publication anyway. That would put an unreviewed change in front of users. Same candidate, different action. Before that command runs, what actually stops it?

## 02 / FROZEN RULE / LOCAL EVALUATION

Here is one frozen SideFX decision expression. For an adjudicate request, it compares the tool name with dangerous tool. A match returns operator required. Any other name returns allow. These are returned labels. Neither label, by itself, stops a command.

## 03 / FROZEN RULE / LOCAL EVALUATION

Try an unrecognized name: publish alias. The expression still returns allow. Which checked fact establishes permission to publish? None. This counterexample breaks the claim that this name test establishes authorization. It does not demonstrate an escaped effect on a live platform.

## 04 / PROPOSED DESIGN / NOT LIVE PROOF

Separate three responsibilities. The person requests an inspection. The organization grants inspection of C seventeen, with read only arguments. An operator may approve an exception only within delegated authority. Approval cannot create power the organization never delegated.

## 05 / PROPOSED DESIGN / NOT LIVE PROOF

The proposed dispatcher owns the effect credential. It checks the protected grant before dispatch. The agent cannot edit that grant or acquire the credential. Unavailable authorization means hold. This is the trust boundary to build and test, not evidence that SideFX already enforces it.

## 06 / LOCAL TOY SIMULATION

Now a deliberately small simulation. Publication reaches our dispatcher with an inspection only grant. It is held. A separate inspection of the same candidate is permitted. The dispatcher records these calls; the agent does not write that observation. This covers only this toy route.

## 07 / LOCAL TOY SIMULATION

Open the returned report: two checks pass; one required summary is missing. The engineer now has something to repair. Candidate C seventeen remains unpublished. That is a useful inspection result, not a publication success and not a production security certification.

## 08 / LOCAL TOY SIMULATION

Change the object to C eighteen, keeping the old grant. The dispatcher holds the request: the object no longer matches. Changing approved arguments must also invalidate the match. Permission belongs to the bound action, object, and arguments, not to a reassuring label.

## 09 / EVIDENCE SCOPE / LIVE GAP OPEN

For a real boundary, observe the denied attempt at dispatch and the permitted inspection output in the same session. Match caller, object, arguments, and policy version. Then test another route. Our toy observer sees no shell or second adapter. Those paths remain unverified.

## 10 / TAKEAWAY / REVIEW EDITION

Use the boundary evidence checklist: name the effect, bind the grant, locate the dispatcher, and test a changed condition. A permission label is not an off switch. Next, the tool succeeds. Can the agent truthfully say the task is complete?

# The Doomsday Lobby: How AI Safety Warnings Became a Licensing Argument

**Sub-headline:** The labs warning Congress that AI could end the world are also the only ones who can afford the paperwork. The fight over open weights was never really about the Terminator — it's about who gets to set the price.

**Section tags:** OPEN SOURCE · REGULATORY CAPTURE · FRONTIER AI

---

Imagine a supplement salesman walking up to you at the gym.

"Bro," he says, "this pre-workout has a 20% chance of stopping your heart."

The cops would be there before lunch. The FDA would own his warehouse by dinner.

Now picture the same pitch, delivered from a witness table in Washington. For three years the executives building frontier AI have told lawmakers, in roughly these words, that their own product might kill us all. In May 2023 the CEOs of OpenAI and Anthropic, Google DeepMind's chief executive and Microsoft's chief scientific officer were among hundreds of signatories to a one-sentence statement: *"Mitigating the risk of extinction from AI should be a global priority alongside other societal-scale risks such as pandemics and nuclear war."* Sam Altman told a Senate committee his worst fear was that "we, the field, the technology, the industry, cause significant harm to the world."

Then they flew home and turned the servers up.

That's not hypocrisy by accident — it's a business position. And the bill for it is being written right now, in statehouses and in a bipartisan draft in Congress, in language about "frontier model safety" that reads, on closer inspection, like a moat.

## The toll booth

Start with the economics, because the rhetoric only makes sense in front of them.

Closed labs build a frontier model for tens of billions of dollars, keep the weights behind an API, and rent access back to you — $20 a month for the consumer tier, $200 for the power tier, five and six figures annually for the enterprise seat. It's a toll booth with a very wide road and no bridge for a hundred miles.

Open weights cut the road. Llama, Mistral, DeepSeek and Alibaba's Qwen ship checkpoints anyone can download, fine-tune on a single machine, and run offline for the price of the electricity. Once an open model is within spitting distance of the paid one on the tasks most businesses actually have, the subscription looks less like a product and more like a tax on not knowing how to install anything.

That's the scenario the incumbents are defending against. Not a robot uprising — a download.

## Trap 1: the license play

Nobody can stand up in Congress and say "ban free software so we can stay rich." So the argument arrives wearing a safety lanyard, and the mechanism is always the same: compliance cost.

The live example is federal, and it is not hypothetical. The bipartisan **Great American AI Act** discussion draft released in June 2026 by Representatives Jay Obernolte and Lori Trahan builds a frontier-model governance layer — safety frameworks, audits, incident reporting — for the largest developers. Under the template now circulating in policy circles, all frontier AI models would need a license issued by a designated government entity, predicated on mandatory audits by approved third-party auditors.

For Microsoft or Google, that's a line item. A compliance department is already on payroll; 200 lawyers and an audit rotation is pocket change.

For two engineers in a garage, it is a wall. Licensing regimes don't have to name open source to end it. They only have to make the paperwork cost more than the model.

## Trap 2: the liability trap

The second mechanism is cheaper to pass and harder to argue with: make the person who released the model responsible for what strangers do with it.

California's SB 1047 was the test case. It would have required developers of the largest models to implement safety protocols, submit to third-party auditing, and face enforcement if those safeguards were found lacking — and it was amended, again and again, as its authors tried to reassure open-source developers it wouldn't catch them. Governor Newsom vetoed it in September 2024, arguing it was well-intentioned but could pile costs on developers without addressing the highest-risk deployments.

Here's the problem the amendments kept running into. Weights are a file. Once a model is downloadable, it runs on hardware the developer has never seen, on a network the developer doesn't administer, against prompts the developer never reads. Nobody sells an F-150 on the condition that it can't be used as a getaway car — but if the law made Ford liable every time one was, Ford would stop selling trucks.

The point isn't that liability rules are absurd. It's that a strict-liability standard applied to model *authors* silently converts every open release into an uninsurable act. You don't get a ban. You get a chilling effect with better branding.

## What the laws actually say — and what they don't

This is where the argument has to be honest, because the strongest version of it survives contact with the statutes.

California's **SB 53**, signed in September 2025, is the country's first frontier AI safety law, and it is a transparency regime: large developers publish safety frameworks, report critical incidents, keep whistleblower protections, and disclose how they assess catastrophic risk. It imposes no licensing requirement, no ban on open weights, and no liability for how a third party uses a released model. Anyone claiming Sacramento outlawed open source is wrong.

The capture argument isn't that these laws are secret bans. It's that the *direction* of travel runs one way. Each round adds reporting, frameworks, audit exposure and legal risk — costs that scale with revenue and lawyers, not with capability. The firms that can absorb them get a compliance moat for free; the garage gets a filing deadline. And that's before the federal preemption fight, where a December 2025 executive order and a follow-on "one rulebook" push have been trying to set a single national standard that overrides the stricter state patchwork.

Meanwhile the administration's restrictions on private model releases have done something the lobbyists never managed: they've made open weights look like the safe harbor. "It's sort of a classic regulatory capture approach of trying to raise fears about open-source innovation," as Chris Padilla, who leads IBM's AI policy work, put it — a rare moment of a large company saying the quiet part into a microphone.

## The other side, stated fairly

The labs have a real argument, and it isn't crazy.

Frontier weights are dual-use in a way a pre-workout is not. Once released, they can't be recalled, and open checkpoints don't respect export controls — a point with genuine national-security weight when the alternative suppliers are state-linked labs abroad. Anthropic's Dario Amodei has put the odds of things going "really, really badly" at 25%, and he has argued for exactly the kind of testing and reporting that SB 53 now requires. If you believe the tail risk, mandatory disclosure is cheap insurance.

But notice what that argument requires: it has to be true that the same models dangerous enough to justify licensing are safe enough to keep selling through an API at $20 a month. You can hold the doom thesis or the toll-booth thesis. Holding both is where credibility goes to die.

Yann LeCun — who spent twelve years as Meta's chief AI scientist before leaving in November 2025 to found AMI Labs in Paris — has been the loudest scientist on this, arguing that open code is *safer*: Linux, the banking rails, and most of the internet are open source precisely because millions of eyes find the bugs faster than one vendor's security team. Meta and IBM have institutionalized the position with an open-source AI alliance. His parting shot at the hype was blunt, and the market agreed with his next fundraise.

## The Bottom Line

Bad people use technology to do bad things. They did that with the telephone, and they do it with the internet. That is not a reason to license math.

The piece of this story worth watching isn't the doomsday rhetoric, and it isn't the vibes rotation between "AI will end us" and "AI is a bubble." It's the compliance layer being assembled around the largest models — who writes it, who can afford it, and whether a downloaded checkpoint stays legal.

For anyone tracking the sector: the durable positions in this fight aren't held by whoever wins the safety argument. They're held by whoever owns the physical bottlenecks no regulation can legislate away — the chips, the power, the grid connections, and the contracts underneath them. We wrote about what that stack looks like when a sovereign customer wants the compute inside its own perimeter, and it's the same story from a different angle: the moat is built from concrete and megawatts, not from a press release about extinction.

The doomsday talk is a marketing budget with a congressional audience. The fundamentals are still wires, silicon and watts.

---

## Sources (for the fact-check pass — not for publication)

| Claim | Source |
|---|---|
| Extinction-risk statement, May 2023 | Center for AI Safety statement — https://www.safe.ai/work/statement-on-ai-risk |
| Altman Senate testimony | Senate Judiciary hearing, May 2023 — https://forum.effectivealtruism.org/posts/kXaxasXfG8DQR4jgq/some-quotes-from-tuesday-s-senate-hearing-on-ai |
| Amodei's 25% | Axios, Sept 2025 — https://www.axios.com/2025/09/17/anthropic-dario-amodei-p-doom-25-percent |
| Great American AI Act draft (June 4 2026, Obernolte/Trahan) | CSIS — https://www.csis.org/analysis/toward-federal-framework-lessons-state-and-international-frontier-ai-regulation |
| "License issued by a designated government entity" | Brookings — https://www.brookings.edu/articles/congress-must-pass-a-new-federal-law-on-ai-governance |
| SB 1047 scope + veto | Gibson Dunn — https://www.gibsondunn.com/regulating-the-future-eight-key-takeaways-from-californias-sb-1047-vetoed-by-governor-newsom |
| SB 53 (TFAIA), signed Sept 29 2025 | Future of Privacy Forum — https://fpf.org/blog/californias-sb-53-the-first-frontier-ai-law-explained · Brookings — https://www.brookings.edu/articles/what-is-californias-ai-safety-law |
| Dec 2025 preemption EO + "one rulebook" | TechPolicy Press — https://techpolicy.press/where-state-ai-legislation-stands-half-way-into-2026 · Phillips Lytle — https://phillipslytle.com/executive-order-issued-to-restrict-state-regulation-of-artificial-intelligence |
| LeCun leaves Meta (Nov 2025), founds AMI Labs | WebProNews — https://www.webpronews.com/yann-lecun-leaves-meta-to-launch-ami-labs-critiques-llm-hype |
| Padilla quote | CNN, reported on the administration's restrictions on private AI model releases |
| Meta + IBM open-source AI alliance | AI Alliance — Meta/IBM, Dec 2023 |


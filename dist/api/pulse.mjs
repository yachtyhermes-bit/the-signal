// Pulse AI — Vercel serverless function for The Signal
// Uses Google Gemini API directly with Google Search Grounding
// for live web search answers on EVERY question — no tiers, no quotas.
// Article index is inlined at build time by build.js (compact format).

// ARTICLES_PLACEHOLDER — build.js replaces this with inline data
const articles = [{"t":"CRM","s":"salesforce-agentforce-ai-growth-2026","u":"Salesforce's Agentforce Just Hit $1B in ARR. The Stock's Dow","c":"ai","d":"2026-07-14"},{"t":"ANET","s":"arista-networks-nvidia-paradox-ai-2026","u":"The Nvidia Paradox: How Losing the Top Spot Makes Arista an ","c":"ai","d":"2026-07-13"},{"t":"ETN","s":"eaton-q2-earnings-preview-ai-power-2026","u":"Eaton Announced Its Q2 Date Today — And the Stock Just Gave ","c":"energy","d":"2026-07-13"},{"t":"SPCX","s":"spcx-spacex-starlink-ipo-analysis-2026","u":"Starlink Prints Money, Starship Burns It, and AI Eats the Re","c":"space","d":"2026-07-13"},{"t":"ZS","s":"zscaler-ai-security-phoenix-2026","u":"Zscaler Blew Up in May. Its AI Security Business Is the Real","c":"cybersecurity","d":"2026-07-13"},{"t":"LMT","s":"lockheed-martin-defense-moat-2026","u":"The Biggest Munitions Ramp Since World War II Is Happening R","c":"defense","d":"2026-07-12"},{"t":"MU","s":"micron-us-chip-investment-surge-2026","u":"Micron Just Dropped $250B on American Soil — And Claude's Br","c":"ai","d":"2026-07-12"},{"t":"TSM","s":"tsmc-ai-chip-monopoly-2026","u":"TSMC Isn't Just Winning the AI Chip Race — It Owns the Track","c":"ai","d":"2026-07-12"},{"t":"MRVL","s":"marvell-ai-switch-asic-rebound-2026","u":"Marvell's 102.4 Tbps AI Switch Just Fired a Shot at Broadcom","c":"ai","d":"2026-07-11"},{"t":"PANW","s":"palo-alto-networks-platformization-2026","u":"Palo Alto Networks' Platformization Play Is A $265B Juggerna","c":"cybersecurity","d":"2026-07-11"},{"t":"GEV","s":"top-energy-plays-ai-power-2026","u":"Four Energy Stocks Feeding the AI Beast — The Only Power Tra","c":"ai-power","d":"2026-07-11"},{"t":"ASML","s":"asml-euv-monopoly-chokepoint-ai-chips","u":"One Company Controls Every AI Chip on Earth — And It's Not N","c":"ai","d":"2026-07-10"},{"t":"GEV","s":"ge-vernova-power-ai-data-centers-2026","u":"The Power Behind the Prompt","c":"energy","d":"2026-07-10"},{"t":"ORCL","s":"oracle-ai-cloud-capex-bet-2026","u":"Oracle's $900B Peak Collapsed to $408B — While Its Cloud Rev","c":"mega-cap","d":"2026-07-10"},{"t":"CRDO","s":"credo-ai-connectivity-chips-2026","u":"CRDO's Purple Cables Are the Hidden Plumbing of Every AI Dat","c":"ai","d":"2026-07-09"},{"t":"SMCI","s":"smci-ai-server-accounting-comeback-2026","u":"SMCI: The Most Hated AI Stock on Earth — and Why You Can't L","c":"ai","d":"2026-07-09"},{"t":"VRT","s":"vertiv-ai-data-center-infrastructure-q1-2026","u":"The $126 Billion 'Shovel Seller' That Just Crushed Earnings ","c":"ai","d":"2026-07-09"},{"t":"COIN","s":"coinbase-european-crypto-moat-2026","u":"Binance Just Got Kicked Out of Europe. Coinbase Is Sitting a","c":"fintech","d":"2026-07-08"},{"t":"CRWV","s":"coreweave-ai-cloud-sale-2026","u":"The AI Cloud Nobody's Talking About: Why CoreWeave's 45% Cra","c":"ai","d":"2026-07-08"},{"t":"KTOS","s":"kratos-defense-unmanned-systems-hypersonics-2026","u":"Kratos Is Getting Destroyed This Year — And That's Exactly W","c":"defense","d":"2026-07-08"},{"t":"VRT","s":"vertiv-data-center-infrastructure-2026","u":"The Plumbing Behind the AI Gold Rush: How Vertiv Became the ","c":"ai","d":"2026-07-08"},{"t":"AXON","s":"axon-ai-policing-monopoly-2026","u":"Axon Isn’t a Taser Company Anymore — It’s a $129B AI Monopol","c":"defense","d":"2026-07-07"},{"t":"AMAT","s":"applied-materials-ai-chip-equipment-monopoly-2026","u":"The $424B Picks-and-Shovels Play: Applied Materials Shattere","c":"ai","d":"2026-07-07"},{"t":"NOW","s":"servicenow-ai-workflow-automation-2026","u":"ServiceNow Is Building the AI Control Tower — Wall Street Ju","c":"ai","d":"2026-07-07"},{"t":"ETN","s":"eaton-ai-power-infrastructure-monopoly-2026","u":"Eaton — The Invisible $155 Billion Monopoly Powering Every A","c":"ai-power","d":"2026-07-06"},{"t":"NOW","s":"servicenow-ai-agent-enterprise-automation-2026","u":"ServiceNow Got Crushed 49% — But AI Agents Are the Rocket Fu","c":"ai","d":"2026-07-06"},{"t":"CRWD","s":"crowdstrike-cybersecurity-ai-platform-2026","u":"CrowdStrike Just Hit $197B. Here's How the Comeback Kid Beca","c":"cybersecurity","d":"2026-07-06"},{"t":"GOOGL","s":"alphabet-google-ai-multi-front-strategy-2026","u":"Inside Google's Multi-Front AI War: Cloud, Waymo, and the $1","c":"mega-cap","d":"2026-07-06"},{"t":"ZS","s":"zscaler-zero-trust-cloud-security-2026","u":"Zscaler: The Zero Trust Titan Caught in the Growth Decelerat","c":"cybersecurity","d":"2026-07-05"},{"t":"DRS","s":"leonardo-drs-defense-electronics-backbone-2026","u":"The $11.6B Defense Stock Hiding Inside Every Major Weapon Sy","c":"defense","d":"2026-07-05"},{"t":"SOFI","s":"sofi-fintech-superapp-bank-charter-2026","u":"SoFi's Stock Got Cut in Half. The Business Never Printed Bet","c":"fintech","d":"2026-07-05"},{"t":"AMD","s":"amd-mi400-datacenter-gpu-comeback-2026","u":"AMD's MI400 Is the First Chip That Actually Scared NVIDIA","c":"ai","d":"2026-07-04"},{"t":"RKLB","s":"rocket-lab-neutron-reusability-2026","u":"Rocket Lab's Neutron Is Almost Here. The Space Industry's Bi","c":"space","d":"2026-07-04"},{"t":"TSLA","s":"tesla-fsd-robotaxi-ai-autonomy-2026","u":"Tesla Just Printed a Record and the Market Sold It. Here's W","c":"mega-cap","d":"2026-07-04"},{"t":"MSFT","s":"microsoft-azure-ai-copilot-enterprise-2026","u":"Microsoft's $37B AI Machine Is Just Getting Started — and It","c":"mega-cap","d":"2026-07-03"},{"t":"ANET","s":"arista-ai-data-center-networking-2026","u":"Every GPU Cluster Needs One of These. Arista Just Quietly Bu","c":"ai","d":"2026-07-03"},{"t":"MRVL","s":"marvell-ai-custom-chips-data-center-2026","u":"Marvell's Custom AI Chips Power Every Hyperscaler — Yet the ","c":"ai","d":"2026-07-03"},{"t":"AVGO","s":"broadcom-ai-networking-vmware-dominance-2026","u":"Broadcom Just Printed $22B Quarters and the Market Pretended","c":"ai","d":"2026-07-02"},{"t":"LHX","s":"l3harris-defense-avionics-contracts-2026","u":"L3Harris Just Won $614M in New Contracts While Everyone Chas","c":"defense","d":"2026-07-02"},{"t":"NVDA","s":"nvidia-cuda-ai-moat-2026","u":"NVDA at $4.79T — CUDA's 4 million developers are the real mo","c":"ai","d":"2026-07-02"},{"t":"AVGO","s":"signal-top-6-avgo-nvda-pltr-ceg-crwv-rtx","u":"July's Top 6 — The Six Stocks That Actually Make Sense Right","c":"ai","d":"2026-07-01"},{"t":"AMZN","s":"amazon-aws-ai-kuiper-dark-horse-2026","u":"Amazon Is Burning $200 Billion a Year. The Market Hates It. ","c":"mega-cap","d":"2026-07-01"},{"t":"CRWD","s":"crowdstrike-ai-security-platform-2026","u":"The $2B Cash Machine Nobody's Pricing: CrowdStrike Just Made","c":"cybersecurity","d":"2026-07-01"},{"t":"SOFI","s":"sofi-fintech-bank-charter-galileo-2026","u":"SoFi Just Added 1.1 Million Members in a Quarter — And the S","c":"fintech","d":"2026-07-01"},{"t":"MU","s":"micron-ai-memory-hbm-dominance-2026","u":"Micron Went From $315 to $1,150 in Six Months. The Memory Tr","c":"ai","d":"2026-06-30"},{"t":"GOOGL","s":"alphabet-ai-cloud-waymo-undervalued-2026","u":"Alphabet's $462B Secret Weapon the Market Keeps Ignoring","c":"mega-cap","d":"2026-06-30"},{"t":"PLTR","s":"palantir-ai-platform-warfare-2026","u":"Palantir's AI Warfare Platform Just Won a War. The Market Do","c":"ai","d":"2026-06-30"},{"t":"AMAT","s":"applied-materials-other-chip-monopoly-2026","u":"Everyone Talks About ASML. Nobody Talks About the Other Chip","c":"ai","d":"2026-06-29"},{"t":"AVGO","s":"broadcom-ai-networking-custom-chip-dominance-2026","u":"OpenAI Just Picked Broadcom. The Street Priced It Like Nothi","c":"ai","d":"2026-06-29"},{"t":"KTOS","s":"kratos-defense-ai-dronewarfare-dominance-2026","u":"The Drone Company Trading at 65% Off Its Highs While the Pen","c":"defense","d":"2026-06-29"},{"t":"ASML","s":"asml-euv-lithography-monopoly-ai-chips-2026","u":"ASML Just Hit $692 Billion. No One Else on Earth Can Do What","c":"ai","d":"2026-06-28"},{"t":"META","s":"meta-ai-infrastructure-revenue-2026","u":"Meta Is Spending $65 Billion a Year on AI. The Market Hates ","c":"mega-cap","d":"2026-06-28"},{"t":"PLTR","s":"palantir-aip-commercial-expansion-2026","u":"Palantir's $270 Billion Bet That AIP Changes Everything","c":"ai","d":"2026-06-28"},{"t":"RKLB","s":"rocket-lab-space-systems-independent-launch-moat-2026","u":"Everyone's Obsessed With SpaceX. Rocket Lab Quietly Built th","c":"space","d":"2026-06-27"},{"t":"ANET","s":"arista-ai-data-center-networking-backbone-2026","u":"You Can't Run AI on Wishes. You Run It on Switches. Arista O","c":"ai","d":"2026-06-27"},{"t":"GEV","s":"ge-vernova-ai-data-center-power-grid-2026","u":"The $280 Billion Bottleneck Nobody's Talking About — GE Vern","c":"ai-power","d":"2026-06-27"},{"t":"S","s":"sentinelone-ai-cybersecurity-platform-moat-2026","u":"SentinelOne: The $5.4B Cybersecurity Giant Nobody's Talking ","c":"cybersecurity","d":"2026-06-27"},{"t":"CEG","s":"constellation-nuclear-ai-data-center-2026","u":"Microsoft, Meta, And Walmart Just Bet Everything On Nuclear.","c":"ai-power","d":"2026-06-26"},{"t":"AXON","s":"axon-public-safety-ai-moat-2026","u":"The AI Monopoly Nobody's Talking About Just Dropped 50% — An","c":"public-safety","d":"2026-06-26"},{"t":"CBRS","s":"cerebras-wafer-scale-ai-chip-challenger-2026","u":"Cerebras Stock Got Halved. The CEO Says Everyone Missed The ","c":"ai","d":"2026-06-26"},{"t":"CRWV","s":"coreweave-leveraged-ai-infrastructure-bull-bear-2026","u":"$35 Billion in Debt and Zero Safety Net — Why Bulls Love Cor","c":"ai","d":"2026-06-25"},{"t":"RTX","s":"rtx-defense-spending-surge-2026","u":"RTX Just Crossed a Quarter-Trillion Market Cap — And the Def","c":"defense","d":"2026-06-25"},{"t":"AMD","s":"amd-mi400-ai-chip-comeback","u":"AMD's $839 Billion Bet: MI400 and the AI Chip Comeback Nobod","c":"ai","d":"2026-06-25"},{"t":"CRWD","s":"crowdstrike-falcon-ai-security-moat-2026","u":"The Lazarus Trade: CrowdStrike Weaponized the Worst IT Disas","c":"cyber","d":"2026-06-24"},{"t":"META","s":"meta-ai-pivot-proprietary-2026","u":"Meta Just Killed Open-Source AI and Nobody's Clapping","c":"mega-cap","d":"2026-06-24"},{"t":"PLTR","s":"palantir-commercial-ai-revenue-inflection-2026","u":"Palantir Is Growing Revenue 85% And The Market Just Doesn't ","c":"ai","d":"2026-06-24"},{"t":"GOOGL","s":"googl-ai-everything-strategy-2026","u":"Alphabet's AI Everything Strategy: The Talent Bleed and the ","c":"mega-cap","d":"2026-06-23"},{"t":"MU","s":"micron-hbm-ai-memory-dominance","u":"$MU Is Up 805% in a Year — And It's Still the Cheapest AI St","c":"ai","d":"2026-06-23"},{"t":"SPCX","s":"spacex-lockup-timing-strategy-2026","u":"The SpaceX Lockup Calendar: When To Buy $SPCX","c":"space","d":"2026-06-22"},{"t":"MRVL","s":"marvell-custom-ai-silicon-hyperscaler-2026","u":"Marvell Crashed the S&P 500 Today. Jensen Huang Says It's a ","c":"ai","d":"2026-06-22"},{"t":"HIVE","s":"hive-digital-ai-infrastructure-pivot-2026","u":"The Bitcoin Miner That Became a Dark Horse AI Cloud Provider","c":"ai","d":"2026-06-22"},{"t":"IREN","s":"iren-short-squeeze-ai-cloud-june-2026","u":"IREN Was a Bitcoin Miner. Then It Built Something Wall Stree","c":"ai","d":"2026-06-22"},{"t":"VRT","s":"vertiv-ai-data-center-cooling-2026","u":"Half the AI Data Center Budget Goes to Cooling. Vertiv Just ","c":"ai-power","d":"2026-06-22"},{"t":"MDA","s":"mda-space-arms-dealer-orbital-economy","u":"MDA Space: The Arms Dealer of the Orbital Economy","c":"space","d":"2026-06-22"},{"t":"NET","s":"cloudflare-edge-ai-zero-trust-2026","u":"Cloudflare Just Bet the Company on AI Agents. The Post-Earni","c":"cyber","d":"2026-06-21"},{"t":"LMT","s":"lockheed-martin-f35-defense-backlog-2026","u":"Lockheed's $186B Secret Nobody's Talking About","c":"defense","d":"2026-06-21"},{"t":"AVGO","s":"broadcom-ai-custom-silicon-2026","u":"The $2 Trillion AI Play Wall Street Keeps Sleeping On","c":"ai","d":"2026-06-21"},{"t":"RGTI","s":"rigetti-quantum-computing-roadmap-2026","u":"Rigetti Drops 108 Qubits: The Quantum Roadmap Wall Street Is","c":"quantum","d":"2026-06-20"},{"t":"AVGO","s":"broadcom-ai-networking-quiet-dominance","u":"Everyone's Staring at Nvidia. Broadcom Just Quietly Built a ","c":"ai","d":"2026-06-20"},{"t":"CRWD","s":"crowdstrike-post-outage-comeback-2026","u":"From Blue Screen to Green Prints: CrowdStrike's Impossible C","c":"cyber","d":"2026-06-19"},{"t":"NOW","s":"servicenow-ai-agent-enterprise-moat-2026","u":"The SaaSpocalypse Bet That Backfired","c":"mega-cap","d":"2026-06-19"},{"t":"SOFI","s":"sofi-the-fintech-that-quietly-figured-out-profits","u":"SoFi Is Down 36% YTD While Printing Record Profits. Someone'","c":"fintech","d":"2026-06-19"},{"t":"PLTR","s":"palantir-aip-defense-contracts-2026","u":"Palantir Has $13.7B in Government Contracts, Revenue Doubled","c":"defense","d":"2026-06-18"},{"t":"AMD","s":"amd-mi400-ai-chip-underdog-2026","u":"AMD Is Quietly Building an AI Empire While Everyone's Watchi","c":"ai","d":"2026-06-18"},{"t":"TSM","s":"tsmc-advanced-chip-monopoly-2026","u":"TSMC Just Proved Its Moat Doesn't Shrink — It Widens","c":"ai","d":"2026-06-18"},{"t":"META","s":"meta-ai-bet-paying-off-2026","u":"Meta's Printing $70 Billion a Year in Profit and the Stock G","c":"mega-cap","d":"2026-06-17"},{"t":"ARM","s":"arm-ai-server-architecture-2026","u":"ARM Is the Ghost in Every AI Server — and It's Just Getting ","c":"semiconductors","d":"2026-06-17"},{"t":"KTOS","s":"kratos-valkyrie-drone-army-2026","u":"KTOS Is Down 29% While the Business Is Accelerating — The Va","c":"defense","d":"2026-06-16"},{"t":"AVGO","s":"broadcom-ai-asic-dominance","u":"Broadcom Just Dropped a $22B Quarter and the Stock Tanked. H","c":"ai","d":"2026-06-16"},{"t":"GOOGL","s":"google-gemini-military-pivot-2026","u":"The Blueprint: Google's Quiet Military Pivot","c":"mega-cap","d":"2026-06-15"},{"t":"RKLB","s":"rocket-lab-space-systems-cash-cow-2026","u":"The Invisible Rocket Company: Why Wall Street is Missing Roc","c":"space","d":"2026-06-15"},{"t":"NVDA","s":"nvidia-computex-2026-vera-rubin","u":"Jensen Drops the Hammer at Computex 2026 — NVIDIA's Vera Rub","c":"ai","d":"2026-06-15"},{"t":"NFLX","s":"netflix-ad-tier-growth-2026","u":"Netflix Just Tripled Its Ad Audience In a Year While the Sto","c":"mega-cap","d":"2026-06-15"},{"t":"SPMO","s":"spmo-momentum-etf-core-portfolio","u":"The Momentum ETF That Quietly Became a Portfolio Staple","c":"etfs","d":"2026-06-15"},{"t":"CRWD","s":"crowdstrike-ai-cyber-arms-race-2026","u":"The Outage That Was Supposed to Kill CrowdStrike Built an AI","c":"cyber","d":"2026-06-14"},{"t":"IRDM","s":"iridium-satellite-iot-defense-june-2026","u":"Iridium Just Ripped +168% YTD and Nobody's Talking About It ","c":"space","d":"2026-06-14"},{"t":"MSFT","s":"microsoft-ai-copilot-azure","u":"Microsoft Just Got Taken Out Back and Beaten 17% — Here's Wh","c":"mega-cap","d":"2026-06-14"},{"t":"AMD","s":"amd-mi400-ai-accelerator-june-2026","u":"AMD Just Hit $834B — And The MI400 Is Why Wall Street's Not ","c":"semiconductors","d":"2026-06-13"},{"t":"NOW","s":"servicenow-enterprise-ai-agents-2026","u":"ServiceNow's AI Agent Bet Is Eating the Enterprise — But the","c":"ai","d":"2026-06-13"},{"t":"AXON","s":"axon-ai-policing-moat-2026","u":"Axon Got Cut in Half — and the Business Just Had Its Best Qu","c":"defense","d":"2026-06-13"},{"t":"S","s":"sentinelone-purple-ai-cyber-2026","u":"SentinelOne Just Turned Profitable and the Stock Got Smashed","c":"cyber","d":"2026-06-12"},{"t":"SPCX","s":"spacex-record-ipo-june-2026","u":"SpaceX Blasts Through the Nasdaq Roof — $75B IPO Closes at $","c":"space","d":"2026-06-12"},{"t":"PLTR","s":"palantir-ai-platform-government-2026","u":"Palantir Grew Revenue 85% and the Stock Got Smashed — The Pe","c":"ai","d":"2026-06-12"},{"t":"ANET","s":"arista-networks-ai-valuation-pullback-june-2026","u":"The Insider Sale That Wasn't: Arista's Pullback Is an AI Net","c":"ai","d":"2026-06-12"},{"t":"AVGO","s":"broadcom-ai-infrastructure-moat-june-2026","u":"Broadcom's $1.83 Trillion AI Moat Is Deeper Than Nvidia's — ","c":"semiconductors","d":"2026-06-12"},{"t":"GS","s":"goldman-sachs-ai-capex-warning-june-2026","u":"Goldman Just Lit the Fuse: $920B AI Capex Is Coming — and Th","c":"mega-cap","d":"2026-06-11"},{"t":"XOM","s":"trump-iran-oil-seizure-june-2026","u":"Trump Just Said He's Taking Iran's Oil — and Energy Stocks A","c":"mega-cap","d":"2026-06-11"},{"t":"AIPO","s":"aipo-ai-power-infra-dip-buy-june-2026","u":"Everyone's Chasing AI Chips — AIPO Quietly Owns the Plug Tha","c":"etfs","d":"2026-06-11"},{"t":"QQQ","s":"closing-bell-june-11-2026","u":"CPI Dropped a 4.2% Bomb — Oracle Crashed 10% After Hours and","c":"mega-cap","d":"2026-06-11"},{"t":"KTOS","s":"pentagon-drone-boom-june-2026","u":"The Pentagon's Drone Budget Just Exploded — These Four Compa","c":"defense","d":"2026-06-11"},{"t":"QQQ","s":"closing-bell-june-10-2026","u":"Iran Strikes, Chips Implode Day 3 — The AI Trade Just Broke","c":"mega-cap","d":"2026-06-10"},{"t":"RDW","s":"rdw-vs-lunr-picks-shovels-moonshots-2026","u":"Picks & Shovels vs. Moonshots: The Long-Term Case for RDW an","c":"space","d":"2026-06-09"},{"t":"QQQ","s":"closing-bell-june-9-2026","u":"Intel Just Ripped 11% — While Wall Street Forgot the AI Bloo","c":"mega-cap","d":"2026-06-09"},{"t":"GME","s":"gamestop-ebay-hostile-june-2026","u":"Ryan Cohen Is Trying to Eat eBay With a Meme Stock — And Wal","c":"mega-cap","d":"2026-06-09"},{"t":"INTC","s":"intel-cpu-renaissance-june-2026","u":"Intel Just Ripped 11% — CPUs Are Suddenly the Most Dangerous","c":"ai","d":"2026-06-09"},{"t":"STI","s":"solidion-space-battery-june-2026","u":"A $5 Penny Stock Just Hit $35 in Three Days — Meet the Space","c":"space","d":"2026-06-09"},{"t":"NVDA","s":"nvidia-apple-deal-ai-selloff-catalyst","u":"Apple Just Killed the Nvidia Bear Thesis — In One Keynote","c":"ai","d":"2026-06-08"},{"t":"AAPL","s":"apple-siri-nvidia-google-wwdc-2026","u":"Apple Just Admitted It Can't Build AI Chips — Siri's New Bra","c":"ai","d":"2026-06-08"},{"t":"MSFT","s":"openai-revenue-miss-june-2026","u":"OpenAI Can't Hit Its Own Numbers — Right Before the Biggest ","c":"ai","d":"2026-06-08"},{"t":"MRVL","s":"market-wrap-ai-rout-june-2026","u":"Market Wrap: AI Trade Cracks as Jobs Data Revives Rate-Hike ","c":"ai","d":"2026-06-07"},{"t":"PLTR","s":"anduril-army-20b-defense-tech-2026","u":"The Pentagon Just Gave Anduril $20 Billion — And Defense Tec","c":"defense","d":"2026-06-07"},{"t":"AADX","s":"applied-aerospace-defense-ipo-2026","u":"Applied Aerospace Just Dropped a $650M IPO — Here's What Inv","c":"defense","d":"2026-06-06"},{"t":"TSLA","s":"tesla-jpmorgan-upgrade-robotics-2026","u":"JPMorgan Just Killed Its 3-Year Tesla Sell Call — And the Ne","c":"mega-cap","d":"2026-06-06"},{"t":"QQQ","s":"nasdaq-crash-chip-rout-jobs-2026","u":"The AI Trade Just Got a Margin Call: Nasdaq Drops 4.18% as $","c":"ai","d":"2026-06-06"},{"t":"RBRK","s":"rubrik-crushes-earnings-dip-2026","u":"Rubrik Just Dropped a Flawless Quarter — And Wall Street Is ","c":"cyber","d":"2026-06-05"},{"t":"MU","s":"micron-trillion-dollar-hbm-2026","u":"Everyone Bought Nvidia. Micron Quietly Returned 745%.","c":"ai","d":"2026-06-05"},{"t":"PL","s":"planet-labs-satellite-imagery-2026","u":"$PL Just Beat On Earnings, Raised Guidance, and Said Defense","c":"space","d":"2026-06-05"},{"t":"CRWD","s":"crowdstrike-q1-fy2027-earnings-stock-split","u":"$CRWD Just Crushed Earnings, Raised Guidance, and Announced ","c":"cyber","d":"2026-06-04"},{"t":"AVGO","s":"dow-record-chip-rout-rotation-2026","u":"The Great Rotation Is Finally Here — Dow Record, Chip Rout, ","c":"mega-cap","d":"2026-06-04"},{"t":"AVGO","s":"avgo-earnings-ai-reality-check-2026","u":"Broadcom Just Got a $70 Billion AI Reality Check","c":"ai","d":"2026-06-04"},{"t":"SPCX","s":"spacex-75b-ipo-record-2026","u":"Forget Saudi Aramco — SpaceX Just Dropped the Biggest IPO in","c":"space","d":"2026-06-04"},{"t":"GOOGL","s":"anthropic-ipo-filing-2026","u":"The $965 Billion AI Giant Is Going Public — Anthropic Files ","c":"mega-cap","d":"2026-06-02"},{"t":"NVDA","s":"nvidia-vera-rubin-arizona-fab-2026","u":"Jensen Drops the Hammer at Computex 2026 — NVIDIA's Vera Rub","c":"ai","d":"2026-06-02"},{"t":"PANW","s":"palo-alto-networks-nato-cyber-shield-2026","u":"Palo Alto Networks Is NATO's New Cyber Shield — And the Stoc","c":"cyber","d":"2026-06-02"},{"t":"SPY","s":"may-jobs-report-preview-2026","u":"May Jobs Report Preview: The One Number That Could Decide th","c":"mega-cap","d":"2026-06-01"},{"t":"ONDS","s":"onds-autonomous-drones-defense-2026","u":"Ondas Inc. Just Became a Defense Powerhouse — $1B Raised, Re","c":"defense","d":"2026-06-01"},{"t":"SHLD","s":"shld-defense-etf-crushing-market-2026","u":"The Defense ETF That Quietly Tripled While You Were Staring ","c":"etfs","d":"2026-06-01"},{"t":"AMZN","s":"amzn-new-glenn-explosion-kuiper-2026","u":"Blue Origin's New Glenn Explodes at Cape Canaveral — What th","c":"mega-cap","d":"2026-05-31"},{"t":"GOOGL","s":"if-i-could-hold-one-stock-for-5-years-id-pick-google","u":"If I Could Hold One Stock for the Next 5 Years, I'd Pick Goo","c":"mega-cap","d":"2026-05-31"},{"t":"BBAI","s":"bigbear-ai-defense-contracts-panama-2026","u":"BigBear.ai Stock Surges 20% as $60M Defense Contracts and Pa","c":"defense","d":"2026-05-30"},{"t":"NVDA","s":"nvidia-windows-pc-chip-2026","u":"Nvidia Is Finally Coming for Your Windows PC — N1X Arm Chip ","c":"ai","d":"2026-05-30"},{"t":"AAPL","s":"apple-ath-2026","u":"AAPL at $312: Tim Cook Never Hyped AI — And That's Why Apple","c":"mega-cap","d":"2026-05-29"},{"t":"ARM","s":"arm-first-chip-pivot-2026","u":"ARM Just Did Something It Hasn't Done in 35 Years — and the ","c":"ai","d":"2026-05-29"},{"t":"ALAB","s":"astera-labs-ai-connectivity-2026","u":"$ALAB Up 311% from 52-Week Low: The AI Connectivity Company ","c":"ai","d":"2026-05-29"},{"t":"GOOGL","s":"google-pentagon-classified-ai-deal","u":"Google Just Signed a Classified AI Deal With the Pentagon — ","c":"mega-cap","d":"2026-05-29"},{"t":"PLTR","s":"palantir-surges-ai-factory-dell-partnership","u":"Palantir Surges 10% as Dell's Blowout Earnings Validate AI F","c":"defense","d":"2026-05-29"},{"t":"RDW","s":"redwire-golden-dome-shield-contract","u":"$RDW Just Exploded 26% — Redwire Got the Keys to the $151B G","c":"space","d":"2026-05-29"},{"t":"SMCI","s":"smci-dell-ai-server-wave-2026","u":"$SMCI Rallies 11% as Dell's Blowout Earnings Validate the AI","c":"ai","d":"2026-05-29"},{"t":"TSLA","s":"tesla-spacex-merger-chatter-2026","u":"SpaceX-Tesla Merger Buzz Hits a Fever Pitch — $TSLA Could Be","c":"mega-cap","d":"2026-05-29"},{"t":"LMT","s":"golden-dome-space-force-2026","u":"Space Force Just Dropped $3.2 Billion on Golden Dome — The B","c":"defense","d":"2026-05-28"},{"t":"RTX","s":"iran-threatens-tech-defense-2026","u":"Iran Just Threatened U.S. Tech Giants — Defense Stocks Are t","c":"defense","d":"2026-05-28"},{"t":"PLTR","s":"palantir-q1-earnings-miss-2026","u":"Palantir Grew Revenue 85% and Raised Guidance — So Why Is PL","c":"defense","d":"2026-05-28"},{"t":"TSM","s":"tsm-blueprint","u":"The Blueprint: Why Nobody Moves in AI Without TSM","c":"ai","d":"2026-05-28"},{"t":"CRWD","s":"anthropic-mythos-threat-analysis","u":"The Mythos Threat: Why Anthropic Locked Up Its Own AI","c":"cyber","d":"2026-05-27"},{"t":"GD","s":"gd-defense-contracts-earnings","u":"General Dynamics Just Dropped a Monster Earnings Beat — And ","c":"defense","d":"2026-05-26"},{"t":"KTOS","s":"kratos-defense-drones-valkyrie-2026","u":"Kratos Is Quietly Building the Pentagon's Drone Army — $KTOS","c":"defense","d":"2026-05-26"},{"t":"NBIS","s":"nebius-q1-earnings-ai-cloud-2026","u":"Nebius Just Dropped Q1 Earnings — Europe's AI Cloud Dark Hor","c":"ai","d":"2026-05-26"},{"t":"GOOGL","s":"google-ai-price-war-2026","u":"Google Just Launched a $1 Billion AI Price War — Here's What","c":"mega-cap","d":"2026-05-26"},{"t":"LUNR","s":"lunr-nasa-moon-contracts","u":"Intuitive Machines Just Won $180M NASA Contract — $LUNR Is B","c":"space","d":"2026-05-26"},{"t":"ARM","s":"arm-holdings-ai-chip-architecture","u":"Arm Holdings Is the Hidden Architecture Powering the AI Revo","c":"ai","d":"2026-05-26"},{"t":"ORCL","s":"oracle-cloud-ai-earnings-2026","u":"Oracle Beat Earnings Again — The Sleeping Giant of AI Cloud ","c":"mega-cap","d":"2026-05-25"},{"t":"ASTS","s":"asts-satellite-to-phone-service","u":"AT&T, Verizon & T-Mobile Just Backed $ASTS — Satellite-to-Ph","c":"space","d":"2026-05-25"},{"t":"IONQ","s":"ionq-record-earnings-quantum-2026","u":"IonQ Just Dropped a 755% Revenue Bomb — Quantum Computing's ","c":"quantum","d":"2026-05-25"},{"t":"CRM","s":"salesforce-earnings-buyback-2026","u":"$CRM at 12x Earnings: The Market Is Pricing Salesforce Like ","c":"mega-cap","d":"2026-05-25"},{"t":"AMZN","s":"amzn-ai-cloud-logistics-2026","u":"$AMZN at $2.86 Trillion: Why AWS AI Growth Is About to Price","c":"mega-cap","d":"2026-05-25"},{"t":"META","s":"ai-inversion-white-collar-blue-collar","u":"The Great AI Inversion: White-Collar Wipeout & The Blue-Coll","c":"mega-cap","d":"2026-05-25"},{"t":"RKLB","s":"rocket-lab-mystery-customer-launch-deal-2026","u":"Someone Just Booked 8 Rocket Lab Launches — And Won't Say Wh","c":"space","d":"2026-05-25"},{"t":"PANW","s":"palo-alto-networks-ai-cyber-attack-acceleration-2026","u":"AI Is Now the Attacker: Palo Alto Networks Just Got 5 Analys","c":"cyber","d":"2026-05-25"},{"t":"PLTR","s":"palantir-pentagon-intel-contract-battle-2026","u":"Palantir vs The Pentagon: America's AI Darling Just Bit the ","c":"defense","d":"2026-05-25"},{"t":"QCOM","s":"qualcomm-edge-ai-awakening","u":"Qualcomm Just Popped 11.6% as Wall Street Finally Wakes Up t","c":"ai","d":"2026-05-24"},{"t":"TSEM","s":"tower-semiconductor-ai-chip-deals","u":"Tower Semiconductor Just Signed $1.3 Billion in AI Chip Deal","c":"ai","d":"2026-05-24"},{"t":"SMCI","s":"smci-q3-earnings-surge-ai-value","u":"Super Micro Just Doubled Revenue — And Trades at 11x Earning","c":"ai","d":"2026-05-24"},{"t":"CRWD","s":"anthropic-mythos-10000-vulnerabilities","u":"Anthropic's Claude Mythos Has Already Found 10,000+ Critical","c":"cyber","d":"2026-05-24"},{"t":"AMD","s":"amd-meta-chips-deal-100b","u":"AMD Just Locked Down a $100 Billion AI Deal With Meta — And ","c":"ai","d":"2026-05-24"},{"t":"AVGO","s":"broadcom-google-anthropic-expanded-deal","u":"Broadcom Just Locked In $200 Billion in AI Compute Deals — A","c":"ai","d":"2026-05-24"},{"t":"INTC","s":"intel-tesla-14a-terafab-deal","u":"Intel's Comeback Is Real — Tesla Just Bet $20 Billion on Its","c":"ai","d":"2026-05-24"},{"t":"AVGO","s":"broadcom-wall-street-top-pick-2026","u":"Broadcom Just Hit a 52-Week High. Wall Street Says It's Stil","c":"ai","d":"2026-05-23"},{"t":"TSLA","s":"tesla-cybertruck-robotaxi-2026","u":"Tesla Is a $1.6T Data Company Hiding Inside an Automaker","c":"mega-cap","d":"2026-05-23"},{"t":"PLTR","s":"pentagon-grok-classified-defense-ai-2026","u":"The Pentagon Just Opened the Door to Grok — Defense AI Is No","c":"cyber","d":"2026-05-23"},{"t":"MSFT","s":"ackman-microsoft-ai-bet","u":"Ackman Dumps Alphabet, Loads Up on Microsoft in $2.1B AI Bet","c":"mega-cap","d":"2026-05-23"},{"t":"","s":"spacex-starship-100-dollar-per-kg","u":"Starship at 12 Flights: What SpaceX Has Actually Proven (and","c":"space","d":"2026-05-23"},{"t":"RNMBY","s":"rheinmetall-defense-europe-2026","u":"Rheinmetall Is the Centerpiece of Europe's Rearmament — And ","c":"defense","d":"2026-05-23"},{"t":"AXON","s":"axon-q1-earnings-contrarian","u":"Axon Just Dropped a 34% Revenue Beat and the Market Punched ","c":"defense","d":"2026-05-23"},{"t":"MU","s":"micron-hbm-ai-chip-2026","u":"Micron at 7.3x Forward PE: The Insanely Cheap AI Stock Analy","c":"ai","d":"2026-05-23"},{"t":"RKLB","s":"spacex-xai-merger-talks-ipo-2026","u":"SpaceX-xAI Mega-Merger: The $470B AI-Space Empire Coming for","c":"space","d":"2026-05-23"},{"t":"AAPL","s":"apple-undervalued-mega-cap-2026","u":"Apple Is the Most Boring Mega-Cap in 2026. That's Exactly Wh","c":"mega-cap","d":"2026-05-23"},{"t":"IREN","s":"iren-nvidia-deal-ai-cloud-controversy","u":"IREN Went From Bitcoin Miner to $3.4B NVIDIA Partner — Wall ","c":"ai","d":"2026-05-23"},{"t":"","s":"spacex-starship-100-dollar-per-kg","u":"Starship at 12 Flights: What SpaceX Has Actually Proven (and","c":"ai","d":"2026-05-23"},{"t":"AMD","s":"amd-quietly-crushing-nvidia-2026","u":"AMD Is Quietly Crushing Nvidia In 2026 — Up 118% While Every","c":"ai","d":"2026-05-22"},{"t":"NVDA","s":"nvidia-post-earnings-analysis-2026","u":"Nvidia Just Dropped a $58.3 Billion Profit — And the AI Supe","c":"ai","d":"2026-05-22"},{"t":"RKLB","s":"rocket-lab-record-revenue-surge-2026","u":"Rocket Lab Crushed Q1 — Record $200M+ Revenue, Space Force D","c":"space","d":"2026-05-22"},{"t":"NVDA","s":"trump-ai-eo-cancel","u":"Trump Torpedoes AI Executive Order — And Markets Are Loving ","c":"ai","d":"2026-05-22"},{"t":"GOOGL","s":"alphabet-5-trillion-milestone","u":"Google Just Hit $4.64 Trillion. Wall Street Still Isn't List","c":"mega-cap","d":"2026-05-22"},{"t":"AVGO","s":"broadcom-custom-ai-asic-dominance-2026","u":"Nvidia Gets the Headlines. Broadcom Gets the Checks.","c":"ai","d":"2026-05-22"},{"t":"META","s":"meta-rayban-display-launch-2026","u":"Meta's Smart Glasses Are Here — And They're Already Too Popu","c":"mega-cap","d":"2026-05-22"},{"t":"NVDA","s":"nvidia-80b-buyback-signal","u":"Nvidia's $80B Buyback Is the Loudest Whisper in the Market —","c":"ai","d":"2026-05-22"},{"t":"PANW","s":"palo-alto-anthropic-project-glasswing-2026","u":"Anthropic Just Made Palo Alto Networks Indispensable","c":"cyber","d":"2026-05-22"},{"t":"PANW","s":"palo-alto-networks-32-percent-weekly-surge","u":"The 32% Silent Assault: Why PANW's Seven-Day Tear Is Just th","c":"cyber","d":"2026-05-22"},{"t":"NBIS","s":"nebius-group-growth-2026","u":"Europe's AI Infrastructure Giant: Nebius Is Building the GPU","c":"ai","d":"2026-05-22"},{"t":"RBRK","s":"rubrik-growth-2026","u":"Rubrik Is Growing Like a Rocket — And Wall Street Is Just Wa","c":"cyber","d":"2026-05-22"},{"t":"META","s":"meta-layoffs-8000-ai","u":"Zuckerberg Fires 8,000 in Brutal AI Restructuring — 'Success","c":"mega-cap","d":"2026-05-22"},{"t":"AMZN","s":"amazon-q1-2026-aws-reacceleration","u":"AWS Reacceleration Fuels Amazon's Q1 Earnings Beat as EPS Mo","c":"mega-cap","d":"2026-05-22"},{"t":"GE","s":"ge-aerospace-sleeping-giant","u":"GE Aerospace Is the Sleeping Giant Nobody's Watching — Up 35","c":"defense","d":"2026-05-22"},{"t":"META","s":"meta-ai-budget-blowout","u":"Meta Just Dropped a $145B AI Bombshell — The Market Panicked","c":"mega-cap","d":"2026-05-22"},{"t":"RKLB","s":"rocket-lab-space-force-heimdall","u":"Rocket Lab Just Got Paid to Play in GEO — The $90M Heimdall ","c":"space","d":"2026-05-22"},{"t":"RKLB","s":"rocketlab-growth-engine","u":"Rocket Lab Just Became the Most Important Space Stock You Do","c":"space","d":"2026-05-21"},{"t":"MRVL","s":"marvell-ai-silicon-sleeper","u":"Marvell Is the AI Semiconductor Giant Wall Street Is Ignorin","c":"ai","d":"2026-05-21"},{"t":"CRWV","s":"coreweave-ai-cloud-dark-horse","u":"CoreWeave Is the AI Cloud Dark Horse Nobody's Talking About","c":"ai","d":"2026-05-21"},{"t":"","s":"karpathy-anthropic","u":"Andrej Karpathy Joins Anthropic: Why This Changes the AI Lan","c":"ai","d":"2026-05-21"},{"t":"RTX","s":"rtx-defense-buy-opportunity","u":"RTX Just Dipped 18% From Its Highs. Here's Why That's Your E","c":"defense","d":"2026-05-21"},{"t":"AXON","s":"axon-enterprise-ai-monopoly","u":"Why AXON is the Ultimate Unkillable Portfolio Diversifier","c":"defense","d":"2026-05-21"},{"t":"","s":"spacex-ipo-analysis","u":"SpaceX IPO: Everything Investors Need to Know Before the Big","c":"space","d":"2026-05-21"},{"t":"META","s":"meta-ai-capex-deep-dive","u":"Meta Is Spending $65B on AI in 2026 — Smart Bet or Billionai","c":"mega-cap","d":"2026-05-21"},{"t":"AVGO","s":"broadcom-ai-networking-dominance","u":"Broadcom's AI Networking Dominance: Tomahawk, Custom ASICs, ","c":"ai","d":"2026-05-21"},{"t":"AMD","s":"amd-vs-nvidia-ai-2026","u":"AMD vs Nvidia in AI: Is 2026 Finally AMD's Year to Compete?","c":"ai","d":"2026-05-21"},{"t":"","s":"spacex-ipo-debt-hype","u":"SpaceX: Inside the Hidden Debt and Hype Behind the Biggest I","c":"space","d":"2026-05-21"},{"t":"PLTR","s":"palantir-aip-government-ai","u":"Palantir's AIP Is the Government AI Engine — Here's the Bull","c":"ai","d":"2026-05-20"},{"t":"NVDA","s":"nvidia-blackwell-ramp-2026","u":"Nvidia's Blackwell Ramp: Inside the $100B AI Infrastructure ","c":"ai","d":"2026-05-20"},{"t":"MSFT","s":"bill-gates-selling-microsoft","u":"Bill Gates Has Sold $20B+ of Microsoft Stock. Should You Fol","c":"mega-cap","d":"2026-05-20"},{"t":"RDW","s":"redwire-next-space-runner","u":"Redwire's Contract Runway: Why This $14 Stock Could Be the N","c":"space","d":"2026-05-20"},{"t":"CRWD","s":"crowdstrike-vs-palo-alto-2026","u":"CrowdStrike vs Palo Alto Networks: Two Cybersecurity Giants,","c":"cyber","d":"2026-05-20"},{"t":"GOOGL","s":"google-io-2026-takeaways","u":"Google I/O 2026: 5 Takeaways That Reshape the AI Landscape","c":"ai","d":"2026-05-20"},{"t":"CBRS","s":"cerebras-ipo-nvidia-threat-analysis","u":"Cerebras Landed 2026's Biggest IPO. Here's Why Nvidia Isn't ","c":"ai","d":"2026-05-20"}];

// ─── Config ───
const GEMINI_MODEL = 'gemini-2.5-flash';
const GEMINI_BASE = 'https://generativelanguage.googleapis.com/v1beta';

const CACHE_TTL = 30 * 60 * 1000;
const CACHE_MAX = 100;
const answerCache = new Map();

function getCacheKey(q) {
  return q.toLowerCase().replace(/[^\w\s]/g, '').replace(/\s+/g, ' ').trim();
}

function cacheGet(key) {
  const entry = answerCache.get(key);
  if (!entry) return null;
  if (Date.now() - entry.ts > CACHE_TTL) { answerCache.delete(key); return null; }
  answerCache.delete(key);
  answerCache.set(key, entry);
  return entry;
}

function cacheSet(key, data) {
  if (answerCache.has(key)) answerCache.delete(key);
  if (answerCache.size >= CACHE_MAX) {
    const oldest = answerCache.keys().next().value;
    if (oldest) answerCache.delete(oldest);
  }
  answerCache.set(key, { ...data, ts: Date.now() });
}

// ─── Find sources from answer ───
function findSources(answer) {
  const answerLower = answer.toLowerCase();
  const sources = [];
  for (const a of articles) {
    if (
      (a.t && answerLower.includes(a.t.toLowerCase())) ||
      (a.u && answerLower.includes(a.u.toLowerCase().slice(0, 30)))
    ) {
      if (!sources.find(s => s.t === a.t)) {
        sources.push({ title: a.u, slug: a.s, ticker: a.t });
        if (sources.length >= 4) break;
      }
    }
  }
  return sources;
}

// ─── Build article context from index ───
function buildArticleContext() {
  const sectors = {};
  for (const a of articles) {
    const sector = a.c || 'other';
    if (!sectors[sector]) sectors[sector] = [];
    sectors[sector].push(a);
  }
  let ctx = '';
  for (const [sector, arts] of Object.entries(sectors)) {
    ctx += `\n[${sector.toUpperCase()}]\n`;
    for (const a of arts.slice(0, 12)) {
      ctx += `  [${a.t}] ${a.u} (${a.d})\n`;
    }
  }
  return ctx.slice(0, 6000);
}

// ─── Gemini API call ───
async function callGemini(systemPrompt, userQuestion, history = []) {
  const key = process.env.GEMINI_API_KEY || '';
  if (!key) throw new Error('403: No GEMINI_API_KEY configured.');

  const url = `${GEMINI_BASE}/models/${GEMINI_MODEL}:generateContent?key=${key}`;

  // Build multi-turn contents array from history
  const contents = [];
  for (const msg of history) {
    contents.push({
      role: msg.role === 'assistant' ? 'model' : 'user',
      parts: [{ text: msg.text }]
    });
  }
  contents.push({ role: 'user', parts: [{ text: userQuestion }] });

  const payload = {
    systemInstruction: { parts: [{ text: systemPrompt }] },
    contents,
    tools: [{ googleSearch: {} }],
    generationConfig: { temperature: 0.3, maxOutputTokens: 8192 },
    safetySettings: [
      { category: 'HARM_CATEGORY_HARASSMENT', threshold: 'BLOCK_NONE' },
      { category: 'HARM_CATEGORY_HATE_SPEECH', threshold: 'BLOCK_NONE' },
      { category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold: 'BLOCK_NONE' },
      { category: 'HARM_CATEGORY_DANGEROUS_CONTENT', threshold: 'BLOCK_NONE' }
    ]
  };

  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    const err = await res.text();
    if (res.status === 429) throw new Error('RATE_LIMITED');
    throw new Error(`${res.status}: ${err.slice(0, 200)}`);
  }

  const data = await res.json();

  // Join ALL parts from the response (Gemini can split into multiple parts)
  const parts = data.candidates?.[0]?.content?.parts || [];
  const text = parts.map(p => p.text || '').join('');

  const finishReason = data.candidates?.[0]?.finishReason;
  if (finishReason === 'MAX_TOKENS' || finishReason === 'SAFETY') {
    console.error(`Gemini finish reason: ${finishReason} for query`);
  }

  const groundMeta = data.candidates?.[0]?.groundingMetadata;
  const searched = groundMeta?.webSearchQueries?.length > 0;

  // Extract actual web search source URLs from Google's grounding data
  const webSources = [];
  const chunks = groundMeta?.groundingChunks || [];
  const seen = new Set();
  for (const chunk of chunks) {
    const uri = chunk.web?.uri;
    const title = chunk.web?.title || uri;
    if (uri && !seen.has(uri)) {
      seen.add(uri);
      webSources.push({ url: uri, title });
    }
    if (webSources.length >= 5) break;
  }

  return { text, searched, webSources };
}

// ─── Handler ───
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  try {
    const { question, articleContext: requestContext, history = [] } = req.body;
    if (!question || question.trim().length < 3) {
      return res.status(200).json({ answer: 'Ask me anything about markets or stocks.', sources: [], searched: false });
    }

    const cacheKey = getCacheKey(question);
    const cached = (!history.length) ? cacheGet(cacheKey) : null;
    if (cached) return res.status(200).json(cached);

    const articleContext = buildArticleContext();
    const articleCount = articles.length;

    const systemPrompt = `You are Pulse, AI on The Signal (readthesignal.net) — market intelligence.

TONE: Direct, punchy. Bold key numbers. Under 800 words.

CAPABILITIES:
1. Google Search — live web search for prices, earnings, news.
2. Article Library — Signal articles below. Use EXACT titles when referencing.

RULES:
- Search the web for current data on ALL companies asked about.
- When asked about "companies" plural, list ALL relevant ones, not just 2-3.
- Reference Signal articles by EXACT title from the list below.
- Our library has ${articleCount} articles. NEVER say we don't cover something without checking the list.
- NEVER make up article titles or stock prices.
${requestContext && requestContext.title ? `\nCURRENT ARTICLE CONTEXT:\nThis question is being asked from the article page for "${requestContext.title}".\nSlug: ${requestContext.slug}\nBody preview: ${(requestContext.bodyPreview || '').slice(0, 800)}\nUse this context to ground your answer in what the article covers.` : ''}

Covered: NVDA, AMD, AVGO, MRVL, PLTR, CRWD, RKLB, RDW, LMT, RTX, GOOGL, META, MSFT, AMZN, TSLA, AAPL, PANW, and more.

Article library (${articleCount} articles):
${articleContext}`;

    const { text: answer, searched, webSources } = await callGemini(systemPrompt, question, history);

    if (!answer) {
      return res.status(200).json({ answer: "Couldn't find a good answer. Try rephrasing.", sources: [], searched: false });
    }

    // Always prefer real web search URLs from Google grounding
    const sources = webSources && webSources.length > 0
      ? webSources.map(s => ({ title: s.title, url: s.url, source: 'web' }))
      : findSources(answer);
    const result = { answer, sources, searched };
    cacheSet(cacheKey, result);
    return res.status(200).json(result);

  } catch (error) {
    const errMsg = error.message || String(error);
    console.error('Pulse error:', errMsg);
    if (error.message === 'RATE_LIMITED') {
      return res.status(200).json({ answer: 'Rate limited. Try again in a minute.', sources: [], searched: false });
    }
    return res.status(200).json({ answer: `Issue: ${errMsg.slice(0, 100)}`, sources: [], searched: false });
  }
}

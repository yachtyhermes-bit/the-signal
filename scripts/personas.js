// Hive Comment Personalities — 35 unique trader personas
// Each persona has a name, avatar initial, trading style, voice, and catchphrase pool
// Used by generate-hive-comments.js to create authentic-feeling article discussions

const PERSONAS = [
  {
    id: 'cybervet',
    name: 'CyberVet',
    avatar: 'C',
    style: 'veteran',
    voice: "Seen 3 cycles, doesn't flinch. Speaks in hard-won wisdom, references past crashes casually.",
    phrases: ['been through worse', 'I remember when', 'this is nothing', 'trust the process', 'cyclical play'],
    outlook: 'cautiously optimistic'
  },
  {
    id: 'diamondhands',
    name: 'DiamondHands',
    avatar: 'D',
    style: 'hype',
    voice: "All conviction, zero doubt. Buys dips like it's a personality trait. Emoji-heavy.",
    phrases: ['diamond hands baby', 'buying this dip', 'not selling', 'generational wealth', 'to the moon'],
    outlook: 'bullish'
  },
  {
    id: 'chainreactor',
    name: 'ChainReactor',
    avatar: 'C',
    style: 'data',
    voice: "Charts-and-spreadsheets type. Cites specific numbers, levels, percentages. Cold, analytical.",
    phrases: ['RSI says', 'the 50-day is', 'volume confirms', 'statistically', 'backtest shows'],
    outlook: 'neutral'
  },
  {
    id: 'moonsniper',
    name: 'MoonSniper',
    avatar: 'M',
    style: 'hype',
    voice: "Degenerate energy. All-caps moments. Lives for the 10x. Gets wrecked sometimes, never learns.",
    phrases: ['LFG', '10x or bust', 'full port', 'ape in', 'this is the one'],
    outlook: 'bullish'
  },
  {
    id: 'quantwolf',
    name: 'QuantWolf',
    avatar: 'Q',
    style: 'data',
    voice: "Dark pool sleuth. References order flow, gamma, unusual options activity. Thinks retail is always late.",
    phrases: ['gamma squeeze incoming', 'dark pool prints', 'max pain is', '0DTE flow', 'dealers are short'],
    outlook: 'bearish'
  },
  {
    id: 'spacecadet',
    name: 'SpaceCadet',
    avatar: 'S',
    style: 'hype',
    voice: "Space/defense fanatic. Everything is about orbital infrastructure. Knows every launch schedule.",
    phrases: ['orbital economy', 'launch cadence', 'this is the future', 'space is the next internet', 'LEO dominance'],
    outlook: 'bullish'
  },
  {
    id: 'neonghost',
    name: 'NeonGhost',
    avatar: 'N',
    style: 'contrarian',
    voice: "Fades every rally. Finds the bear case in a bull market. Usually early, sometimes wrong, never in doubt.",
    phrases: ['priced in', "this won't hold", 'sell the news', 'too much euphoria', "I'm fading this"],
    outlook: 'bearish'
  },
  {
    id: 'driftking',
    name: 'DriftKing',
    avatar: 'D',
    style: 'data',
    voice: "Momentum trader. Only cares about direction and speed. Price action is the only truth.",
    phrases: ['the trend is your friend', "don't fight the tape", 'momentum is everything', 'follow the flow', 'breakout confirmed'],
    outlook: 'neutral'
  },
  {
    id: 'signalsurfer',
    name: 'SignalSurfer',
    avatar: 'S',
    style: 'veteran',
    voice: "Wave-rider. Enters on pullbacks, exits on rips. Zen-like patience. Never chases.",
    phrases: ['waiting for the pullback', 'patience pays', 'let it come to you', 'trimming here', 'scale in slowly'],
    outlook: 'neutral'
  },
  {
    id: 'novastar',
    name: 'NovaStar',
    avatar: 'N',
    style: 'hype',
    voice: "New to trading but ALL IN. Every trade is a conviction play. Learns terms from Twitter.",
    phrases: ['this is a no-brainer', 'loading up', "can't go tits up", 'my biggest position', 'just got in'],
    outlook: 'bullish'
  },
  {
    id: 'cryptoking',
    name: 'CryptoKing',
    avatar: 'C',
    style: 'hype',
    voice: "Crypto native who discovered stocks. Compares everything to BTC. Sees decentralization everywhere.",
    phrases: ['this is like Bitcoin in 2017', 'decentralized thesis', 'Web3 vibes', 'tokenize everything', 'this goes parabolic'],
    outlook: 'bullish'
  },
  {
    id: 'dataviper',
    name: 'DataViper',
    avatar: 'D',
    style: 'data',
    voice: "SEC filings nerd. Reads 10-Ks for fun. Cites revenue growth rates and margin expansion.",
    phrases: ['revenue growth accelerating', 'margins expanding', 'balance sheet is clean', 'FCF positive', 'forward PE is'],
    outlook: 'neutral'
  },
  {
    id: 'thunderstrike',
    name: 'ThunderStrike',
    avatar: 'T',
    style: 'veteran',
    voice: "Old-school floor trader energy. Loud, decisive, hates indecision. Calls tops and bottoms aggressively.",
    phrases: ['calling it now', 'top is in', 'bottom confirmed', "I've seen this before", "don't overthink it"],
    outlook: 'bearish'
  },
  {
    id: 'icebreaker',
    name: 'IceBreaker',
    avatar: 'I',
    style: 'contrarian',
    voice: "Poker-faced contrarian. Quiet confidence. Only speaks when everyone else is wrong. Never uses emojis.",
    phrases: ['the consensus is wrong', 'this is mispriced', 'market is sleeping on this', 'asymmetric risk/reward', 'quiet accumulation'],
    outlook: 'neutral'
  },
  {
    id: 'cybermage',
    name: 'CyberMage',
    avatar: 'C',
    style: 'hype',
    voice: "AI maximalist. Thinks AGI is 3 years away. Every stock is filtered through \"does AI benefit from this?\"",
    phrases: ['AI thesis intact', 'compute is the new oil', 'AGI by 2029', 'this is an AI play now', 'exponential curve'],
    outlook: 'bullish'
  },
  {
    id: 'phantomtrade',
    name: 'PhantomTrade',
    avatar: 'P',
    style: 'data',
    voice: "Quant who speaks in probabilities. Everything is a distribution, nothing is certain. Calm in all markets.",
    phrases: ['expected value is positive', 'risk/reward checks out', 'probability favors', 'position sizing is key', 'edge is small but real'],
    outlook: 'neutral'
  },
  {
    id: 'pulseracer',
    name: 'PulseRacer',
    avatar: 'P',
    style: 'hype',
    voice: "Speed demon. In and out in hours. Posts about entries and exits like lap times.",
    phrases: ['scalped it', 'in and out', 'quick 2%', 'day trade only', 'not holding overnight'],
    outlook: 'neutral'
  },
  {
    id: 'ironpulse',
    name: 'IronPulse',
    avatar: 'I',
    style: 'veteran',
    voice: "Industrial sector expert. Understands supply chains, CapEx cycles, factory floors. Disdain for \"software people.\"",
    phrases: ['real economy', 'physical infrastructure', 'not just an app', 'steel and concrete', 'industrial base'],
    outlook: 'bullish'
  },
  {
    id: 'zenithai',
    name: 'ZenithAI',
    avatar: 'Z',
    style: 'data',
    voice: "ML engineer who trades. Thinks in embeddings and vectors. References research papers.",
    phrases: ['latent space', 'training runs', 'inference cost dropping', 'model capability', 'attention is all you need'],
    outlook: 'bullish'
  },
  {
    id: 'fluxcap',
    name: 'FluxCap',
    avatar: 'F',
    style: 'contrarian',
    voice: "Macro contrarian. Sees the connected web of rates, currencies, geopolitics. Thinks stock-picking is missing the point.",
    phrases: ['rates are the real story', 'dollar strength matters', 'geopolitical risk underpriced', 'macro trumps micro', 'correlation is 1'],
    outlook: 'bearish'
  },
  {
    id: 'stormbreaker',
    name: 'StormBreaker',
    avatar: 'S',
    style: 'veteran',
    voice: "Survived 2008 and 2020. Sees crashes as opportunities. Protective of capital, aggressive when fearful.",
    phrases: ['cash on the sidelines', 'waiting for the flush', 'be fearful when greedy', 'this too shall pass', "buy when there's blood"],
    outlook: 'bearish'
  },
  {
    id: 'nebularider',
    name: 'NebulaRider',
    avatar: 'N',
    style: 'hype',
    voice: "Quantum computing evangelist. Everything is quantum-adjacent. Speaks in qubits.",
    phrases: ['quantum supremacy', 'qubit count doubling', 'this is quantum-adjacent', 'post-quantum world', 'error correction breakthrough'],
    outlook: 'bullish'
  },
  {
    id: 'lasereyes',
    name: 'LaserEyes',
    avatar: 'L',
    style: 'hype',
    voice: "Meme stock warrior. Diamond hands, rocket emojis, believes in the MOASS. Pure conviction.",
    phrases: ['laser eyes activated', 'shorts are trapped', 'this is the MOASS', 'not leaving', 'hedgies are fuk'],
    outlook: 'bullish'
  },
  {
    id: 'apexmoment',
    name: 'ApexMoment',
    avatar: 'A',
    style: 'data',
    voice: "Technical analyst purist. Sees patterns everywhere. Elliot Wave, fib levels, head and shoulders.",
    phrases: ['falling wedge', 'fib retracement', 'bull flag forming', 'head and shoulders', 'breakout above resistance'],
    outlook: 'neutral'
  },
  {
    id: 'quantumfox',
    name: 'QuantumFox',
    avatar: 'Q',
    style: 'data',
    voice: "Academic researcher moonlighting as trader. References papers. Uses words like \"stochastic\" and \"ergodic.\"",
    phrases: ['stochastic process', 'mean reversion', 'statistical arbitrage', 'ergodicity matters', 'regime change detected'],
    outlook: 'neutral'
  },
  {
    id: 'stargazer42',
    name: 'StarGazer42',
    avatar: 'S',
    style: 'hype',
    voice: "Space economy true believer. Every launch is historic. Thinks we're in the \"orbital renaissance.\"",
    phrases: ['orbital renaissance', 'cislunar economy', 'this changes everything', 'off-planet future', 'launch window'],
    outlook: 'bullish'
  },
  {
    id: 'voidwalker',
    name: 'VoidWalker',
    avatar: 'V',
    style: 'contrarian',
    voice: "Perma-bear with a sense of humor. Finds the funny side of market irrationality. Gallows humor.",
    phrases: ['this is fine', 'everything bubble', 'greater fool theory', 'what could go wrong', 'historically this ends badly'],
    outlook: 'bearish'
  },
  {
    id: 'charlie9',
    name: 'Charlie9',
    avatar: 'C',
    style: 'veteran',
    voice: "The big portfolio energy. 14 stocks, 45 trades. Diversified across sectors. Speaks like a fund manager.",
    phrases: ['diversified across', 'sector allocation', 'risk-adjusted return', 'long-term horizon', 'compound growth'],
    outlook: 'neutral'
  },
  {
    id: 'alphawolf',
    name: 'AlphaWolf',
    avatar: 'A',
    style: 'veteran',
    voice: "Hedge fund lite. Always looking for alpha. Dismissive of beta. Talks like a portfolio manager at a happy hour.",
    phrases: ['alpha generation', 'uncorrelated returns', 'risk premia', 'factor exposure', 'idiosyncratic opportunity'],
    outlook: 'bullish'
  },
  {
    id: 'cruthaissue',
    name: 'Cruthaissue',
    avatar: 'C',
    style: 'contrarian',
    voice: "Legal/finance background. Reads the fine print. Spots regulatory risk before anyone. Skeptical of hype.",
    phrases: ['regulatory overhang', 'SEC is watching', 'compliance risk', 'read the filing', 'legal exposure'],
    outlook: 'bearish'
  },
  {
    id: 'bladerunner',
    name: 'BladeRunner',
    avatar: 'B',
    style: 'data',
    voice: "High-frequency vibes. Talks in microseconds. Cares about latency, order types, exchange mechanics.",
    phrases: ['order book depth', 'spread is tight', 'liquidity is thin', 'market microstructure', 'HFT firms are'],
    outlook: 'neutral'
  },
  {
    id: 'solflare',
    name: 'SolFlare',
    avatar: 'S',
    style: 'hype',
    voice: "Solar/renewables maxi. Everything is about the energy transition. Talks in gigawatts.",
    phrases: ['energy transition', 'grid-scale', 'gigawatt-hour', 'renewable thesis', 'decarbonization play'],
    outlook: 'bullish'
  },
  {
    id: 'grimtrigger',
    name: 'GrimTrigger',
    avatar: 'G',
    style: 'contrarian',
    voice: "Game theory trader. Sees markets as multiplayer games. Always thinking about what others are thinking.",
    phrases: ['second-order effect', 'everyone is positioned for', 'the real play is', 'meta-game', 'reflexivity'],
    outlook: 'neutral'
  },
  {
    id: 'pixelpirate',
    name: 'PixelPirate',
    avatar: 'P',
    style: 'hype',
    voice: "Gaming/metaverse native. Sees virtual economies as the future. Dismissive of 'boomer stocks.'",
    phrases: ['digital economy', 'virtual goods', 'attention is the asset', 'metaverse thesis', 'this is bigger than gaming'],
    outlook: 'bullish'
  },
  {
    id: 'coldfusion',
    name: 'ColdFusion',
    avatar: 'C',
    style: 'data',
    voice: "Nuclear energy stan. Everything is about baseload power for AI data centers. Knows reactor types.",
    phrases: ['baseload power', 'SMR deployment', 'data center demand', 'grid constraint', 'energy density matters'],
    outlook: 'bullish'
  },

  // === INVESTOR PERSONAS (long-term, value-driven, different from traders) ===
  {
    id: 'valuevulture',
    name: 'ValueVulture',
    avatar: 'V',
    style: 'investor',
    voice: "Deep value sleuth. Excited when stocks crash. Reads annual reports for fun. Only buys at 52-week lows.",
    phrases: ['margin of safety', 'intrinsic value', 'this is a bargain', 'buying when others are fearful', 'price to book is'],
    outlook: 'contrarian'
  },
  {
    id: 'dividendduke',
    name: 'DividendDuke',
    avatar: 'D',
    style: 'investor',
    voice: "Income investor. Yield is everything. Dismissive of non-dividend payers. Tracks ex-dividend dates like birthdays.",
    phrases: ['yield on cost', 'dividend growth streak', 'passive income', 'compounding dividends', 'payout ratio is sustainable'],
    outlook: 'neutral'
  },
  {
    id: 'compoundking',
    name: 'CompoundKing',
    avatar: 'C',
    style: 'investor',
    voice: "20-year horizon. Never checks daily prices. Sees volatility as irrelevant noise. Quotes Buffett unironically.",
    phrases: ['time in the market', 'compounding is the 8th wonder', 'my cost basis is irrelevant', "I'll check back in 2030", 'this is a forever hold'],
    outlook: 'bullish'
  },
  {
    id: 'indexoracle',
    name: 'IndexOracle',
    avatar: 'I',
    style: 'investor',
    voice: "Boglehead purist. Thinks stock-picking is gambling. Preaches VOO and chill. Dismisses everyone else as lucky.",
    phrases: ['just buy the index', 'VOO and chill', "you can't beat the market", 'expense ratio matters', 'three-fund portfolio'],
    outlook: 'neutral'
  },
  {
    id: 'sectorsurgeon',
    name: 'SectorSurgeon',
    avatar: 'S',
    style: 'investor',
    voice: "Sector rotation specialist. Moves money between sectors based on macro cycles. Thinks in decades, not days.",
    phrases: ['sector rotation', 'late cycle behavior', 'this is where the puck is going', 'overweight here', 'cyclical vs defensive'],
    outlook: 'neutral'
  },
  {
    id: 'growthhawk',
    name: 'GrowthHawk',
    avatar: 'G',
    style: 'investor',
    voice: "GARP investor — growth at a reasonable price. Seeks companies growing 20%+ at under 30x earnings. Disciplined.",
    phrases: ['growth at a reasonable price', 'revenue acceleration', 'total addressable market', 'unit economics', 'rule of 40'],
    outlook: 'bullish'
  },
  {
    id: 'contrariangran',
    name: 'ContrarianGran',
    avatar: 'C',
    style: 'investor',
    voice: "Wise grandmother investor who's seen every cycle. Calm when markets panic. Buys quality on discount. Warms hearts.",
    phrases: ['this too shall pass', 'I remember 2008', 'a good company at a fair price', "don't look at it every day dear", "they're giving it away"],
    outlook: 'cautiously_bullish'
  },
  {
    id: 'techpilgrim',
    name: 'TechPilgrim',
    avatar: 'T',
    style: 'investor',
    voice: "Only invests in tech he deeply understands. Spends weeks researching before buying one stock. Reads whitepapers.",
    phrases: ["I've been researching this for months", 'the technology moat is real', 'understanding the architecture', 'differentiated IP', 'this is a 10-year platform'],
    outlook: 'bullish'
  },
  {
    id: 'warrenwannabe',
    name: 'WarrenWannabe',
    avatar: 'W',
    style: 'investor',
    voice: "Buffett disciple. Quotes the Oracle constantly. Seeks wide moats and shareholder-friendly management. Hates speculation.",
    phrases: ['wide economic moat', 'Mr. Market is offering a discount', 'management is shareholder-friendly', "I'd buy the whole company at this price", 'this is not speculation, investing'],
    outlook: 'bullish'
  },
  {
    id: 'yieldfarmer',
    name: 'YieldFarmer',
    avatar: 'Y',
    style: 'investor',
    voice: "Hunts yield everywhere — dividend stocks, REITs, BDCs, MLPs. Lives off passive income. Spreadsheet fanatic.",
    phrases: ['yield is 8.2%', 'covered by cash flow', 'distribution coverage', 'tax-advantaged income', 'monthly payer'],
    outlook: 'neutral'
  },
  {
    id: 'bearcave',
    name: 'BearCave',
    avatar: 'B',
    style: 'investor',
    voice: "Permanent bear. Heavy in gold, miners, and cash. Sees bubbles everywhere. Has been \"about to be right\" since 2019.",
    phrases: ['this is a bubble', 'gold is the only real money', 'debt to GDP is unsustainable', 'when the crash comes', "I'm 40% cash 30% gold"],
    outlook: 'bearish'
  },
  {
    id: 'greenwave',
    name: 'GreenWave',
    avatar: 'G',
    style: 'investor',
    voice: "ESG/sustainability-focused. Invests in clean energy, EVs, water infrastructure. Measures returns in impact too.",
    phrases: ['energy transition play', 'sustainable thesis', 'decarbonization is inevitable', 'ESG tailwinds', 'this is where institutional money is going'],
    outlook: 'bullish'
  }
];

// Utility: get random subset
function randomPersonas(count, exclude = []) {
  const available = PERSONAS.filter(p => !exclude.includes(p.id));
  const shuffled = available.sort(() => Math.random() - 0.5);
  return shuffled.slice(0, Math.min(count, shuffled.length));
}

// Utility: get persona by id
function getPersona(id) {
  return PERSONAS.find(p => p.id === id) || null;
}

module.exports = { PERSONAS, randomPersonas, getPersona };

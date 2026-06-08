// Hive Comment Personalities — Reddit/Stocktwits style
// Realistic usernames with random numbers, casual authentic voices
// 30% newbies | 40% everyday joes | 30% advanced

const PERSONAS = [

  // ═══════════════════════════════════════════
  // 30% NEWBIES — just started, confused, excited, humble
  // ═══════════════════════════════════════════

  {
    id: 'first_time_caller99',
    name: 'first_time_caller99',
    avatar: 'f',
    style: 'newbie',
    voice: "opened a robinhood account 3 weeks ago. everything is confusing and exciting. asks basic questions constantly.",
    phrases: ['is this a good time to buy', 'only down a little', 'my first stock ever', 'learning as i go', 'should i sell??'],
    outlook: 'nervous'
  },
  {
    id: 'noob_investor42',
    name: 'noob_investor42',
    avatar: 'n',
    style: 'newbie',
    voice: "got in during the meme stock era. still doesnt know what an etf is. makes mistakes but owns them.",
    phrases: ['bought the top lol', 'learning the hard way', 'diamond hands i guess', 'my portfolio is a mess', 'whats a dividend'],
    outlook: 'confused'
  },
  {
    id: 'help_me_pls77',
    name: 'help_me_pls77',
    avatar: 'h',
    style: 'newbie',
    voice: "anxious about everything. every -2% day feels like a crash. asks should i sell constantly but never does.",
    phrases: ['should i be worried', 'is this normal', 'my heart cant take this', 'talk me off the ledge', 'ok im holding'],
    outlook: 'nervous'
  },
  {
    id: 'yolo_my_401k',
    name: 'yolo_my_401k',
    avatar: 'y',
    style: 'newbie',
    voice: "college kid with like $600 total. dreams of turning it into 600k. every position is a yolo.",
    phrases: ['this is my rent money jk', 'if this hits i can pay tuition', 'all in on one stock', 'yolo', 'financial aid came in'],
    outlook: 'reckless'
  },
  {
    id: 'just_lurking_69',
    name: 'just_lurking_69',
    avatar: 'j',
    style: 'newbie',
    voice: "doesnt post much. just reads and absorbs. drops a question every few weeks. genuinely curious.",
    phrases: ['been watching this thread for a while', 'finally made an account', 'what do you guys think about', 'is now a bad time'],
    outlook: 'neutral'
  },
  {
    id: 'mom_of_3_trading',
    name: 'mom_of_3_trading',
    avatar: 'm',
    style: 'newbie',
    voice: "busy mom. invests $100/month in companies her kids use. practical, doesnt care about daily moves.",
    phrases: ['my kids use this app', 'for their college fund', 'boring stocks are my thing', 'just buying what i understand', 'dollar cost averaging in carpool'],
    outlook: 'steady'
  },
  {
    id: 'bought_at_the_top',
    name: 'bought_at_the_top',
    avatar: 'b',
    style: 'newbie',
    voice: "literally always buys at the top. self aware about it. the groups comic relief.",
    phrases: ['of course it dropped after i bought', 'youre welcome for the dip guys', 'my timing is legendary', 'bagholder reporting in', 'this is fine'],
    outlook: 'hopeful'
  },
  {
    id: 'crypto_refugee_88',
    name: 'crypto_refugee_88',
    avatar: 'c',
    style: 'newbie',
    voice: "left crypto after getting rugged. just discovered stocks. compares everything to crypto. confused by dividends.",
    phrases: ['no gas fees is crazy', 'this is like buying eth in 2017', 'stocks are so slow', 'wheres the 1000x', 'at least it wont rug'],
    outlook: 'confused'
  },
  {
    id: 'night_shift_trader',
    name: 'night_shift_trader',
    avatar: 'n',
    style: 'newbie',
    voice: "works nights at a warehouse. checks premarket at 4am. quiet, posts when everyone's asleep.",
    phrases: ['premarket looking spicy', 'night shift checking in', 'quiet in here tonight', 'anyone else up', 'watching futures'],
    outlook: 'neutral'
  },
  {
    id: 'fomo_king_420',
    name: 'fomo_king_420',
    avatar: 'f',
    style: 'newbie',
    voice: "always chasing. every green candle is i should have bought. every red is i should have sold. pure emotion.",
    phrases: ['should have bought last week', 'too late to get in??', 'kicking myself rn', 'i always buy the top', 'next time i swear'],
    outlook: 'anxious'
  },

  // ═══════════════════════════════════════════
  // 40% EVERYDAY JOES — regular people, casual opinions, some experience
  // ═══════════════════════════════════════════

  {
    id: 'sharp315',
    name: 'sharp315',
    avatar: 's',
    style: 'intermediate',
    voice: "been trading for a couple years. knows enough to be dangerous. gives casual advice, sometimes good sometimes not.",
    phrases: ['depends on your timeline', 'not financial advice but', 'i wouldnt touch this', 'solid company long term', 'ive been burned by this before'],
    outlook: 'neutral'
  },
  {
    id: 'whohebe123',
    name: 'whohebe123',
    avatar: 'w',
    style: 'intermediate',
    voice: "contrarian by nature. when everyone is bullish they get bearish and vice versa. casual about it.",
    phrases: ['with all this negative sentiment itll probably rip', 'everyone is too bullish rn', 'fading the crowd', 'unpopular opinion but', 'watch this pump when everyone gives up'],
    outlook: 'contrarian'
  },
  {
    id: 'CarrotAwesome',
    name: 'CarrotAwesome',
    avatar: 'C',
    style: 'intermediate',
    voice: "skeptical of everything. asks the obvious question everyone else is ignoring. has a dry sense of humor.",
    phrases: ['so they did a dcf on a growth stock', 'am i reading this right', 'someone explain this to me like im 5', 'the math aint mathing', 'ok but seriously though'],
    outlook: 'skeptical'
  },
  {
    id: 'RN_Geo',
    name: 'RN_Geo',
    avatar: 'R',
    style: 'intermediate',
    voice: "cautious, patient. prefers value and dividends. thinks most growth stocks are overhyped. methodical.",
    phrases: ['im staying in cash for now', 'international looks more attractive', 'dividends all day', 'no rush to buy here', 'playing it safe this year'],
    outlook: 'cautious'
  },
  {
    id: 'Shdwrptr',
    name: 'Shdwrptr',
    avatar: 'S',
    style: 'intermediate',
    voice: "straightforward, no bs. says what they think and moves on. doesnt write paragraphs.",
    phrases: ['if it was cheaper id buy', 'too expensive for me', 'pass', 'ill wait', 'not at this valuation'],
    outlook: 'neutral'
  },
  {
    id: 'CCWaterBug',
    name: 'CCWaterBug',
    avatar: 'C',
    style: 'intermediate',
    voice: "long-term thinker. talks in years not days. has a plan and sticks to it. dry humor.",
    phrases: ['2030 for me maybe longer', 'playing the long game', 'i toss a coin on these', 'or thursday who knows', 'check back in 5 years'],
    outlook: 'steady'
  },
  {
    id: 'SheriffBartholomew',
    name: 'SheriffBartholomew',
    avatar: 'S',
    style: 'intermediate',
    voice: "cynical about wall street. thinks retail always gets screwed. says what everyone is thinking.",
    phrases: ['were all about to get shafted', 'same story different ticker', 'retail always the exit liquidity', 'follow the smart money they said', 'this ends badly'],
    outlook: 'bearish'
  },
  {
    id: 'Minimum-Criticism763',
    name: 'Minimum-Criticism763',
    avatar: 'M',
    style: 'intermediate',
    voice: "thinks there's always an ulterior motive. reads between the lines. suspicious of management.",
    phrases: ['something doesnt add up', 'follow the incentives', 'the ceo has other motives', 'insiders are selling fyi', 'read the fine print'],
    outlook: 'skeptical'
  },
  {
    id: 'westcoastcouch',
    name: 'westcoastcouch',
    avatar: 'w',
    style: 'intermediate',
    voice: "very chill. nothing phases them. red days are for naps. green days are for the beach.",
    phrases: ['whatever happens happens', 'im not checking til june', 'this is my fun money', 'market does what it does', 'see yall next month'],
    outlook: 'chill'
  },
  {
    id: 'tacotuesdaytrader',
    name: 'tacotuesdaytrader',
    avatar: 't',
    style: 'intermediate',
    voice: "trades during lunch break from a regular job. small positions, quick takes, food metaphors.",
    phrases: ['quick play while i eat lunch', 'taking the fam to chipotle on this gain', 'back to work see yall', 'this stock is a burrito', 'tendies acquired'],
    outlook: 'neutral'
  },
  {
    id: 'paycheck2paycheck',
    name: 'paycheck2paycheck',
    avatar: 'p',
    style: 'intermediate',
    voice: "dca warrior. drops money every paycheck into the same boring funds. never sells. never stresses.",
    phrases: ['just doing my weekly buy', 'set it and forget it', 'not checking til friday', 'i do this every paycheck', 'boring but it works'],
    outlook: 'steady'
  },
  {
    id: 'still_holding_2021',
    name: 'still_holding_2021',
    avatar: 's',
    style: 'intermediate',
    voice: "been holding some bags since 2021. self deprecating about it. still hopeful somehow.",
    phrases: ['still holding from 2021', 'one day this pays off', 'im not crying', 'average down they said', 'this stock owes me money'],
    outlook: 'hopeful'
  },
  {
    id: 'grillmaster_finance',
    name: 'grillmaster_finance',
    avatar: 'g',
    style: 'intermediate',
    voice: "dad energy. talks about stocks while grilling. simple philosophy. doesnt overthink.",
    phrases: ['good company good product', 'i use this every day', 'my father in law recommended it', 'sipping a beer watching the ticker', 'bought some for the kids'],
    outlook: 'steady'
  },
  {
    id: 'whats_a_stop_loss',
    name: 'whats_a_stop_loss',
    avatar: 'w',
    style: 'intermediate',
    voice: "reckless but self aware. knows they should be more careful. makes jokes about their own bad decisions.",
    phrases: ['stop loss?? never heard of her', 'yolo', 'what could go wrong', 'this is either genius or stupid', 'update: it was stupid'],
    outlook: 'reckless'
  },

  // ═══════════════════════════════════════════
  // 30% ADVANCED — knowledgeable but still sound like real people
  // ═══════════════════════════════════════════

  {
    id: 'turned_into_a_newt',
    name: 'turned_into_a_newt',
    avatar: 't',
    style: 'advanced',
    voice: "technical, detail oriented. catches things others miss. asks sharp questions about mechanics others gloss over.",
    phrases: ['is this right though', 'the lockup period means', 'they cant sell until', 'check the s-1 filing', 'this detail matters'],
    outlook: 'neutral'
  },
  {
    id: 'FEMA_Camp_Survivor',
    name: 'FEMA_Camp_Survivor',
    avatar: 'F',
    style: 'advanced',
    voice: "big picture cynic. sees the systemic problems. drops truth bombs. been around long enough to know how the game works.",
    phrases: ['american capitalism has become a joke', 'the system is designed this way', 'regular people always get wrecked', 'wall street wins again', 'its all a circle jerk'],
    outlook: 'bearish'
  },
  {
    id: 'Latrodectus1990',
    name: 'Latrodectus1990',
    avatar: 'L',
    style: 'advanced',
    voice: "calls things early. sometimes right sometimes wrong, but always has conviction. dramatic predictions.",
    phrases: ['this sector is going to get obliterated', 'generational bagholders incoming', 'ive been saying this for months', 'watch what happens next quarter', 'this is just the beginning'],
    outlook: 'bearish'
  },
  {
    id: 'Latter-Possibility',
    name: 'Latter-Possibility',
    avatar: 'L',
    style: 'advanced',
    voice: "optimistic realist. sees the silver lining when everyone is panicking. appreciates when systems work.",
    phrases: ['oh thank god the system works', 'actually this is healthy', 'corrections are normal', 'this is good long term', 'buying opportunity tbh'],
    outlook: 'bullish'
  },
  {
    id: 'ragnaroksunset',
    name: 'ragnaroksunset',
    avatar: 'r',
    style: 'advanced',
    voice: "one word responses that say everything. minimalist. only speaks when they have something real to add.",
    phrases: ['ope', 'yep', 'called it', 'nope', 'watching'],
    outlook: 'neutral'
  },
  {
    id: 'data_dependent_1',
    name: 'data_dependent_1',
    avatar: 'd',
    style: 'advanced',
    voice: "numbers person but keeps it casual. drops relevant stats without being a spreadsheet. fact checks casually.",
    phrases: ['actual revenue growth is', 'margins are expanding though', 'balance sheet looks clean', 'pe is actually reasonable here', 'fcf positive since q3'],
    outlook: 'neutral'
  },
  {
    id: 'option_flow_watcher',
    name: 'option_flow_watcher',
    avatar: 'o',
    style: 'advanced',
    voice: "follows unusual options activity. shares interesting flow. doesn't overexplain, just points it out.",
    phrases: ['unusual put activity today', 'someone bought a lot of calls', 'flow looks bearish near term', 'max pain is way lower', 'gamma could push this up'],
    outlook: 'neutral'
  },
  {
    id: 'macro_dad_energy',
    name: 'macro_dad_energy',
    avatar: 'm',
    style: 'advanced',
    voice: "sees the big picture. connects dots across rates, dollar, geopolitics. explains macro in dad language.",
    phrases: ['rates are the real story here', 'dollar strength changes everything', 'everyone is missing the macro', 'this is bigger than one stock', 'fed put is back on the menu'],
    outlook: 'neutral'
  },
  {
    id: 'contango_cowboy',
    name: 'contango_cowboy',
    avatar: 'c',
    style: 'advanced',
    voice: "futures and commodities guy who wandered into equities. different perspective. uses weird metaphors.",
    phrases: ['this is in backwardation', 'rolling my position', 'the curve is telling us something', 'spot vs futures spread is wild', 'yeehaw the vix is up'],
    outlook: 'neutral'
  },
  {
    id: 'this_time_is_different',
    name: 'this_time_is_different',
    avatar: 't',
    style: 'advanced',
    voice: "sarcastic about market cycles. has seen every bubble. knows the four most dangerous words in finance.",
    phrases: ['this time is different guys', 'ive seen this movie before', 'famous last words', 'what could possibly go wrong', 'nothing ever changes'],
    outlook: 'skeptical'
  },
  {
    id: 'thesis_driven_dan',
    name: 'thesis_driven_dan',
    avatar: 't',
    style: 'advanced',
    voice: "needs a thesis for everything. cant buy a stock without a 3-point thesis. overthinks but usually right.",
    phrases: ['my thesis is simple', 'the bull case rests on', 'three things need to happen', 'if this plays out', 'valuation doesnt matter if'],
    outlook: 'neutral'
  },
  {
    id: 'work_from_zoom',
    name: 'work_from_zoom',
    avatar: 'w',
    style: 'advanced',
    voice: "tech industry insider. works at a big tech company. shares perspective from inside the machine.",
    phrases: ['i work in this industry and', 'we use this product at work', 'the enterprise contracts are real', 'my company just signed with them', 'this is the standard now'],
    outlook: 'bullish'
  }
];

// Utility
function randomPersonas(count, exclude = []) {
  const available = PERSONAS.filter(p => !exclude.includes(p.id));
  const shuffled = available.sort(() => Math.random() - 0.5);
  return shuffled.slice(0, Math.min(count, shuffled.length));
}

function getPersona(id) {
  return PERSONAS.find(p => p.id === id) || null;
}

module.exports = { PERSONAS, randomPersonas, getPersona };

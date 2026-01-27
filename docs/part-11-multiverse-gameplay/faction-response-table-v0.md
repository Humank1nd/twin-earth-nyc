# Faction Response Table v0

> **Twin Earth NYC** -- Part 11: Multiverse Gameplay
> **Document:** Faction Response Table
> **Version:** 0.1.0
> **Status:** Draft
> **Last Updated:** 2026-01-27

---

## Table of Contents

1. [Overview](#overview)
2. [EARTH-1218 Factions](#earth-1218-factions)
3. [Portal Factions (First Pack)](#portal-factions-first-pack)
4. [Faction Response Table](#faction-response-table)
5. [Faction Memory (Adaptive Behavior)](#faction-memory-adaptive-behavior)
6. [Faction Relationship Matrix](#faction-relationship-matrix)
7. [Player Reputation System](#player-reputation-system)
8. [Integration Notes](#integration-notes)

---

## Overview

Factions are the social and institutional actors that populate Times Square and the multiverse. They observe the player's actions, react to Heat and evidence, pursue their own goals, and offer (or deny) resources, information, and access.

There are two categories of factions:

- **EARTH-1218 Factions** (5): Operate in the hub universe. They are the player's primary social environment -- the cops, the mystics, the criminals, the press, and the neighbors. Their behavior is driven by Heat levels, evidence accumulation, and the Belief Meter.
- **Portal Factions** (2, first pack): Operate across universes. They represent cross-dimensional interests that intersect with the player's activities. Additional portal factions will be introduced in future content packs.

### Design Intent

Factions are the **human face of consequences**. Heat is a number; factions are people. When Physical Heat rises, it is the NYPD who shows up with cordons and questions. When Ecological Heat spikes, it is Strange's Network that contacts the player with urgent warnings. When the Criminal Syndicate detects an opportunity, it is their enforcers who appear in the alley.

Factions give the player reasons to care about Heat management beyond abstract numbers. Every faction has goals, resources, and a memory. They learn, they adapt, and they remember.

---

## EARTH-1218 Factions

### Faction Profiles

#### 1. NYPD / Authority

| Attribute | Details |
|---|---|
| **Full Name** | New York Police Department -- Midtown South Precinct (primary), with escalation to NYPD Counterterrorism, FBI Anomalous Events (at higher Institutional Heat) |
| **Goals** | Maintain public order and safety in Times Square. Protect civilians. Investigate and resolve anomalous incidents. Enforce the law. Prevent panic. |
| **Resources** | Patrol officers (25+ in Times Square zone), vehicles, CCTV surveillance network access, forensic teams, SWAT (available at High Heat), legal authority (warrants, cordons, arrests), federal liaison (at Critical Heat) |
| **Territory** | City-wide jurisdiction, concentrated in Times Square and Midtown. Strongest presence: major intersections, transit hubs, tourist areas. Weakest: underground service tunnels, private rooftops (accessible but not routinely patrolled). |
| **Risk Tolerance** | Low. NYPD operates by protocol. Officers do not improvise or take unnecessary risks. Responses escalate through a chain of command. Exceptions: individual officers may be more flexible if personally convinced (Detective Reyes). |
| **Attitude to Portals** | Threat to contain. NYPD views anomalies as hazards -- similar to gas leaks or structural collapses. They want to cordon, contain, and resolve. They do not (initially) understand the multiverse dimension. As Belief rises and Institutional Heat builds, their understanding and approach evolves. |
| **Key NPCs** | Detective Reyes (anomalous events liaison, pragmatic, open-minded), Captain Torres (precinct commander, by-the-book, skeptical), Agent Hollis (FBI, appears at high Institutional Heat, clinical and strategic) |
| **Player Relationship** | Starts at 0.0 (unknown). Can range from -1.0 (fugitive) to +1.0 (trusted asset). Key thresholds: 0.2 (recognized), 0.4 (cooperating), 0.6 (asset), 0.8 (partner). Negative: -0.2 (person of interest), -0.5 (suspect), -0.8 (fugitive). |

#### 2. Strange's Network

| Attribute | Details |
|---|---|
| **Full Name** | Doctor Strange's Earth-1218 Support Network (informal name: "The Watchers," though they dislike the comparison) |
| **Goals** | Monitor and manage portal activity in the Times Square nexus zone. Prevent large-scale incursions. Protect the dimensional integrity of EARTH-1218. Recruit and support capable allies (the player). Maintain secrecy where possible. |
| **Resources** | Mystical knowledge (portal theory, containment rituals, translation gate understanding), artifacts (Sling Rings, scrying devices, containment tools), intel network (mystic sensors, contacts in multiple universes), safe houses (3 in Manhattan, unmarked), Strange himself (remote, rarely available, immensely powerful when present) |
| **Territory** | Scattered safe houses (43rd St bookshop, Upper West Side apartment, Chinatown tea shop). Mystic sensor network covers a 10-block radius around Times Square. No formal territory -- they operate in shadows. |
| **Risk Tolerance** | Medium. Strange's Network takes calculated risks. They will open portals, perform rituals, and engage threats -- but always with preparation and contingency plans. They avoid reckless action and expect the same from allies. |
| **Attitude to Portals** | Tool to manage carefully. Strange's Network understands portals better than anyone. They are not afraid of portals -- they are afraid of uncontrolled portals. Their goal is regulated multiverse interaction, not prohibition. |
| **Key NPCs** | Maya Chen (bookshop owner, player's primary contact, former Strange apprentice, calm and competent), Kai Tanaka (field operative, combat-capable, hot-headed but loyal), Doctor Strange (appears rarely, immense authority, cryptic) |
| **Player Relationship** | Starts at 0.15 (Maya initiates contact during tutorial). Can range from -0.5 (betrayer) to +1.0 (inner circle). Key thresholds: 0.3 (ally), 0.5 (trusted), 0.7 (inner circle), 0.9 (Strange's direct representative). Negative: -0.3 (distrusted), -0.5 (cut off, hostile). |

#### 3. Criminal Syndicate

| Attribute | Details |
|---|---|
| **Full Name** | The Nexus Syndicate (street name; real organizational name unknown). A coalition of organized crime elements that have become aware of portal activity and are exploiting it for profit. |
| **Goals** | Profit from multiverse chaos. Smuggle exotic materials into EARTH-1218 for black market sale. Control portal access points for tollgating. Expand territory and influence using exotic resources. Avoid institutional attention (they want low Heat, not because they're moral, but because Heat is bad for business). |
| **Resources** | Black market networks (fencing, distribution, laundering), informants (in NYPD, media, street-level), muscle (armed enforcers, 10-15 in Times Square zone), smuggling routes (underground tunnels, vehicle fleet), exotic goods inventory (imported via their own crude portal operations), money (deep pockets from ongoing criminal enterprise) |
| **Territory** | Underground: specific tunnel sections, abandoned subway platforms, basement-level operations. Street-level: certain blocks controlled by enforcers (W 40th - W 42nd, near Port Authority). Presence is covert -- no flags or signs, just people who know. |
| **Risk Tolerance** | High. The Syndicate is willing to take significant risks for significant profit. They will open uncontrolled portals, smuggle dangerous materials, and engage in violence if the payoff justifies it. However, they are not stupid -- they calculate risk/reward ratios and retreat when outmatched. |
| **Attitude to Portals** | Opportunity to exploit. The Syndicate sees portals as a new frontier for smuggling and commerce. They want to control portal access, not destroy or contain it. They have crude portal technology (stolen/reverse-engineered) and are actively seeking better methods. |
| **Key NPCs** | "The Broker" (anonymous leader, communicates through intermediaries, identity unknown), Vance Harlow (street-level boss, manages Times Square operations, charming and dangerous), Pixel (tech specialist, manages the Syndicate's portal rig and exotic item analysis, young and morally flexible) |
| **Player Relationship** | Starts at 0.0 (unknown). Can range from -1.0 (kill-on-sight enemy) to +0.8 (business partner -- never full trust). Key thresholds: 0.2 (known quantity), 0.4 (occasional trade), 0.6 (regular business partner). Negative: -0.3 (nuisance), -0.6 (target), -1.0 (active assassination contract). |

#### 4. Media / Press

| Attribute | Details |
|---|---|
| **Full Name** | Times Square Media Corps -- a collective term for the journalists, bloggers, YouTubers, and social media influencers who cover Times Square. Includes mainstream (NY1, local affiliates) and independent (podcasters, conspiracy channels). |
| **Goals** | Cover stories. Get scoops. Influence public opinion. Build audience. The media faction is driven by attention economics -- anomalies are ratings gold if they can capture them. Different media elements have different editorial stances (mainstream: cautious, independent: sensational). |
| **Resources** | Cameras (professional and phone), drones (2 news station drones authorized for Times Square airspace), social media reach (combined follower count in millions), sources (contacts in NYPD, city government, local businesses), broadcast capability (live feeds, breaking news alerts), editorial influence (framing power -- how the story is told matters as much as what happened) |
| **Territory** | Public spaces (anywhere cameras can reach). Semi-permanent news van positions near 42nd/Broadway. Relationships with building owners for rooftop camera access. Social media: everywhere. |
| **Risk Tolerance** | Medium. Mainstream media follows safety protocols but will push boundaries for a scoop. Independent media is bolder -- podcasters and YouTubers will get close to anomalies for content. Drones are deployed aggressively. Overall: scoop-driven risk assessment. |
| **Attitude to Portals** | Story to chase. The media wants footage, interviews, and narrative. They are not aligned with any other faction's goals -- they serve the story. A portal is not a threat or opportunity to them; it is content. Their coverage has consequences (Belief Meter, Social Heat) but those consequences are externalities to them. |
| **Key NPCs** | Sandra Okafor (NY1 reporter, professional, trusted by NYPD, fair but persistent), "TruthHunterNYC" (anonymous YouTuber/podcaster, conspiracy-leaning, 500K followers, will publish anything for views), Jamie Park (freelance photographer, has captured 2 anomaly photos already, selling to highest bidder) |
| **Player Relationship** | Starts at 0.0 (unknown). Can range from -0.5 (targeted for exposure) to +0.7 (trusted source). Key thresholds: 0.2 (known face), 0.4 (source), 0.6 (trusted contact, can request favorable coverage). Negative: -0.2 (subject of investigation), -0.5 (targeted expose). |

#### 5. Citizens' Watch

| Attribute | Details |
|---|---|
| **Full Name** | Times Square Citizens' Watch -- a grassroots community organization formed by local residents, business owners, and regular workers in the Times Square area. |
| **Goals** | Protect the neighborhood. Understand what is happening. Document the truth. Share information. Citizens' Watch is not a power faction -- they are ordinary people trying to make sense of extraordinary events. They want safety, transparency, and community. |
| **Resources** | Community networks (group chats, neighborhood email lists, physical bulletin boards), phones (everyone has a camera), local knowledge (they know every alley, every shortcut, every building's history), numbers (50+ active members, hundreds of passive supporters), trust (locals trust each other more than they trust outsiders/institutions) |
| **Territory** | Times Square locals: the blocks where members live and work. Coffee shops, delis, laundromats, apartment lobbies. Their territory is social, not physical -- it is the fabric of community trust. |
| **Risk Tolerance** | Low to Medium. Citizens' Watch members are ordinary people. They will not engage in combat or confront armed threats. However, they will document, report, organize, and advocate. Some members are braver (former military, activist backgrounds) and will take moderate physical risks to gather information. |
| **Attitude to Portals** | Mystery to understand. Citizens' Watch does not have a political stance on portals. They want answers. Are portals dangerous? Who controls them? Why is no one talking about this? Their response depends on the information they receive -- from the player, from media, from authority, from their own observations. |
| **Key NPCs** | Doris Flanagan (retired teacher, Watch organizer, sharp-eyed and skeptical, the neighborhood's moral center), Marcus Webb (bodega owner, sees everything, shares selectively, practical and street-smart), Yuki Sato (NYU grad student, tech-savvy Watch member, runs the community forum and data analysis) |
| **Player Relationship** | Starts at 0.0 (unknown). Can range from -0.5 (distrusted outsider) to +0.8 (community champion). Key thresholds: 0.2 (recognized neighbor), 0.4 (trusted community member), 0.6 (inner circle, shares intel both ways). Negative: -0.2 (suspicious outsider), -0.5 (perceived threat to community). |

---

## Portal Factions (First Pack)

Portal factions operate across universes and interact with the player through portal-related events.

### Faction Profiles

#### 6. Sanctum Guardians (Earth-616)

| Attribute | Details |
|---|---|
| **Full Name** | The Guardians of the Sanctum Sanctorum -- a division of Earth-616's mystic defense structure dedicated to monitoring and protecting multiverse boundaries. |
| **Universe** | Earth-616 (primary), with agents in multiple universes |
| **Goals** | Protect multiverse boundaries. Prevent unauthorized portal traffic. Seal breaches. Contain dimensional threats. They view EARTH-1218's portal activity with concern but not hostility -- the breaches are not 1218's fault, and they prefer cooperation to confrontation. |
| **Resources** | Mystic warriors (5-8 available for 1218 operations), containment rituals (superior to 1218 Strange's capabilities), dimensional sensors (can detect portals across universes), Sanctum facilities (in 616, vast and well-equipped), artifacts (powerful but restricted to 616 -- Translation Gate limits their effectiveness in 1218) |
| **Attitude to EARTH-1218** | Allies if you help seal breaches. The Guardians are natural allies of Strange's Network and the player, provided the player is working to contain portal activity rather than exploit it. They will provide support (information, occasional combat assistance during operations) in exchange for cooperation. If the player is reckless (high Ecological Heat, uncontrolled portals), the Guardians become critical and may take independent action to seal portals the player is using. |
| **Key NPCs** | Sentinel Voss (Guardian field commander, stern, honorable, appears during pocket operations as an observer or ally), Archivist Lira (knowledge specialist, provides universe profile data and translation gate intel, appears at Strange's safe houses via mystic communication) |
| **Player Relationship** | Starts at 0.1 (neutral-positive, Strange vouches for the player). Range: -0.5 (hostile, will actively oppose) to +0.8 (honored ally). Thresholds: 0.3 (cooperative), 0.5 (trusted), 0.7 (honored ally with access to Guardian resources). Negative: -0.2 (warned), -0.5 (hostile, Guardians attempt to seal player-used portals). |

#### 7. Nexus Runners (Criminal, Multi-Universe)

| Attribute | Details |
|---|---|
| **Full Name** | The Nexus Runners -- a multiverse smuggling network operating across multiple universes. They have no fixed home universe; they are nomadic criminals exploiting dimensional commerce. |
| **Universe** | Multi-universe (operate wherever portals exist) |
| **Goals** | Smuggle exotic materials across universes for profit. Establish and protect smuggling routes. Undercut competitors (including the EARTH-1218 Criminal Syndicate, which is a local affiliate but not fully trusted). Acquire portal technology and knowledge to expand operations. |
| **Resources** | Smuggling expertise (the best portal-runners in the multiverse), exotic inventory (goods from dozens of universes), portal tech (crude but effective stabilizers, signature masking devices), multi-universe contacts (buyers, sellers, informants across realities), intimidation capability (experienced with violence across multiple physics environments) |
| **Attitude to EARTH-1218** | Transactional. The Runners will trade with, threaten, or ignore the player depending on leverage and profit calculations. They are not ideological -- they are businesspeople with no moral floor. If the player has something they want (portal access, exotic goods, intelligence), they will negotiate. If the player threatens their operations, they will retaliate. If the player is irrelevant, they will ignore them. |
| **Key NPCs** | Kira Vex (Nexus Runner captain, charismatic and ruthless, appears during operations in pocket universes, always has an angle), The Collector (anonymous buyer who commissions specific exotic items, communicates through Kira, identity unknown -- may be connected to larger multiverse powers) |
| **Player Relationship** | Starts at 0.0 (unknown). Range: -0.8 (actively hunted) to +0.6 (business partner). Thresholds: 0.2 (known, cautious contact), 0.4 (trading partner), 0.6 (trusted supplier). Negative: -0.3 (untrustworthy), -0.5 (threat to operations, targeted), -0.8 (active elimination order). |

---

## Faction Response Table

This is the core decision matrix. For any combination of Heat level, Belief level, and evidence state, this table defines how each EARTH-1218 faction behaves.

### Response Matrix: Heat + Belief + Evidence Conditions

#### Condition 1: Low Heat, Low Belief, Low Evidence

*All channels < 0.2, Belief < 0.1, minimal evidence in ledger.*

| Faction | Response | Specific Actions | Player Interaction |
|---|---|---|---|
| **NYPD** | Routine patrol | Standard beat cops on normal routes. No special attention to anomaly zones. 911 dispatch ignores "weird light" calls as noise. | Player is unnoticed. Can operate freely. Police encounters are coincidental. |
| **Strange's Network** | Passive monitoring | Maya checks in periodically (daily). Mystic sensors log background readings. No active operations. Network conserves resources. | Player receives briefings but no missions. Relationship maintenance phase. |
| **Criminal Syndicate** | Standard operations | Normal criminal activity (theft, fencing, minor smuggling). No portal-related activity unless they have independent intel. Business as usual. | No Syndicate contact unless player seeks them out. If player approaches, neutral reception. |
| **Media** | No coverage | Nothing to cover. Journalists focused on standard news. Independent media covering other topics. No anomaly content. | No media attention. Player is invisible to press. |
| **Citizens' Watch** | Normal life | Community members going about daily routines. Watch forum is quiet (discussing traffic, construction, local politics). No anomaly awareness. | No Watch contact unless player is already a community member. |

#### Condition 2: Medium Heat, Low Belief

*At least one channel 0.3-0.6, Belief < 0.2.*

| Faction | Response | Specific Actions | Player Interaction |
|---|---|---|---|
| **NYPD** | Increased patrol + investigation | Patrol frequency +25% near anomaly hotspots. Detective Reyes assigned to "unusual events" casefile. CCTV footage under review. Officers asking businesses about "disturbances." | Player may be questioned if seen near anomaly sites repeatedly. Reyes may approach for cooperation. |
| **Strange's Network** | Sends observer agent | Maya deploys Kai to observe anomaly hotspots in person. Mystic sensors upgraded to active scanning. Maya contacts player with concern: "Things are escalating." | Player receives mission offers. Strange's Network wants the player to help contain before it gets worse. |
| **Criminal Syndicate** | Probes for opportunity | Syndicate scouts (Vance's people) observe anomaly activity from distance. Pixel begins analyzing exotic material readings from sensors. The Broker considers investment. | Syndicate NPC approaches player with a proposition: "You seem to know what's going on. We can help each other." |
| **Media** | "Unusual activity" stories | Sandra Okafor runs a 90-second segment on "unusual infrastructure readings near Times Square." TruthHunterNYC posts a "something weird in NYC" video. Low-key but the seed is planted. | No direct player contact, but media coverage affects Social Heat and Belief. Player may see news segments in-world. |
| **Citizens' Watch** | Concerned, forums active | Doris notices increased police presence and asks around. Marcus mentions "cops came by asking questions." Yuki posts on the community forum: "Anyone else notice weird stuff near 44th?" Watch begins documenting. | If player has Watch reputation > 0.2, Watch members share observations with the player. Low-grade but useful intel. |

#### Condition 3: High Heat, Low Belief

*At least one channel 0.6-0.9, Belief < 0.2. The public doesn't understand what's happening but can see the damage/response.*

| Faction | Response | Specific Actions | Player Interaction |
|---|---|---|---|
| **NYPD** | Heavy response + cordons | Road closures. SWAT on standby. Detective Reyes's case elevated to precinct priority. Forensic teams at every residue site. Increased surveillance. Federal liaison notified. | Player is likely a "person of interest." Moving through cordoned areas requires credentials or stealth. Reyes may offer protection in exchange for full cooperation. |
| **Strange's Network** | Direct intervention, offers player help | Strange himself sends a message (via Maya): "This is getting out of control." Network activates all safe houses. Maya offers the player shelter, equipment upgrades, and mission support. Strange may appear briefly for critical containment. | Player receives urgent support. Strange's Network becomes the primary allied faction. Missions focus on containment and Heat reduction. |
| **Criminal Syndicate** | Exploits chaos | Syndicate uses distraction of heavy response to move contraband. Vance expands territory during police preoccupation. Pixel attempts to access anomaly sites during confusion. The Broker sees opportunity in institutional chaos. | Syndicate offers the player deals: "Help us move product during the confusion, we'll give you exotic gear." Alternatively, Syndicate may attempt to steal from the player (if relationship is negative). |
| **Media** | Breaking news, sensational | Sandra leads with "Crisis in Times Square -- what authorities aren't telling you." Multiple news vans. Helicopter footage. TruthHunterNYC's "EVIDENCE OF COVER-UP" video trends nationally. Jamie Park's anomaly photos sell to AP. | Media may attempt to interview the player (if identified as involved). Coverage accelerates Social Heat and Belief. Player can engage media for strategic narrative control (or avoid them). |
| **Citizens' Watch** | Evacuation + fear | Doris organizes an emergency community meeting. Marcus boards up his bodega. Yuki archives all Watch data "in case something happens." Some members evacuate. Others stay and document obsessively. | Watch shares all information with the player (if trusted) or with NYPD (if scared and player is not trusted). Community support depends on prior relationship. |

#### Condition 4: Low Heat, High Belief

*All channels < 0.3, Belief > 0.5. The public knows (or believes) portals are real, but there's no active crisis. This is the "managed awareness" state.*

| Faction | Response | Specific Actions | Player Interaction |
|---|---|---|---|
| **NYPD** | Specialized unit formed | "Anomalous Events Division" officially created. Officers receive specialized training. Sensor network re-tasked for portal detection. Protocols established for anomaly response. Federal coordination formalized. | Player can interact with a professional, prepared authority. Reyes leads the new division. Player may be formally classified as an "asset" (legal protection + oversight). |
| **Strange's Network** | Recruits player more deeply | With public awareness rising, Strange's Network adapts. They offer the player deeper integration: access to more artifacts, advanced training, strategic briefings. In exchange: more demanding missions, higher expectations. | Player enters the "inner circle" track. Missions become more complex and consequential. Strange communicates more directly. |
| **Criminal Syndicate** | Black market for portal-tech | Belief = market demand. The Syndicate opens a full "exotic goods" catalog. Portal-adjacent services offered: "Need a portal opened? We know people." Prices are high, quality is variable, but the inventory is real. | Player can buy exotic goods, hire portal services, or sell imported items through the Syndicate. This is the full black market experience. Prices depend on supply (disrupted by player sabotage) and demand (driven by Belief). |
| **Media** | Documentary features | Sandra pitches a documentary series. TruthHunterNYC becomes a credible voice ("I was right all along"). Jamie Park holds a gallery show of anomaly photography. Media coverage shifts from breaking news to feature/analysis. | Media becomes a tool the player can use. Favorable coverage (arranged through high Media reputation) can influence Belief and Social Heat in specific directions. |
| **Citizens' Watch** | Community meetings, organized response | Doris leads weekly "Anomaly Awareness" meetings. Marcus's bodega becomes an informal info hub. Yuki's forum is now a major local resource. Watch begins coordinating with NYPD's new division. | Watch is a mature community ally. They provide hyperlocal intel, community support, and social cover. Yuki's data analysis supports the player's operations. |

#### Condition 5: High Heat, High Belief

*At least one channel 0.6+, Belief > 0.5. The public knows and can see the crisis. This is the "open crisis" state.*

| Faction | Response | Specific Actions | Player Interaction |
|---|---|---|---|
| **NYPD** | Full lockdown, federal involvement | Governor's emergency powers invoked. National Guard staging. FBI takes lead. Times Square access points controlled by military checkpoints. All anomaly evidence classified. Full surveillance blanket. | Player is either a highly valued asset (high NYPD reputation) or a primary target (low/negative reputation). There is no middle ground at this level. |
| **Strange's Network** | Emergency protocols, major ritual | Strange appears in person. Network mobilizes all resources. A major containment ritual is planned (player is key participant). Safe houses may be compromised (federal surveillance). Network goes semi-underground. | Player is central to Strange's endgame plan. Missions are high-stakes, high-reward, and potentially irreversible. The relationship is tested under pressure. |
| **Criminal Syndicate** | All-in exploitation or retreat | Split within the Syndicate: Vance wants to exploit the chaos (maximum profit from fear), The Broker considers cutting losses and disappearing. Pixel is terrified. Syndicate may fragment. | Player may find unusual alliance opportunities (Syndicate elements that want to help in exchange for protection) or face desperate, dangerous criminal actions. |
| **Media** | 24/7 coverage | National and international media. Times Square is the world's biggest story. Every faction's actions are public. Privacy is nonexistent. Information warfare is critical. | Media is a battlefield. The player's actions are broadcast. Narrative control is a primary strategic concern. Alliance with media faction determines how the player is portrayed to the world. |
| **Citizens' Watch** | Organized resistance or organized support | Depending on player relationship and Watch sentiment: either a grassroots resistance ("we'll help you fight this") or organized opposition ("you brought this on us"). The Watch becomes a political force. | Watch is the player's community barometer. High Watch reputation = community shield (citizens protect, shelter, and support the player). Low Watch reputation = community opposition (citizens report, obstruct, and protest). |

#### Condition 6: Active Anomaly + Any Heat Level

*An anomaly or portal event is currently happening, regardless of background Heat.*

| Faction | Response | Specific Actions | Player Interaction |
|---|---|---|---|
| **NYPD** | Containment priority | All nearby units re-tasked to cordon the anomaly zone. Containment protocols activated. If specialized unit exists, they lead. Otherwise, standard hazmat response. Public evacuation initiated within 50m. | Player must work around (or with) the NYPD cordon. Cooperation means coordinated response. Opposition means evading trained officers. |
| **Strange's Network** | Primary response, player contacted | Maya contacts the player immediately: "We have activity at [location]. Can you respond?" If player is unavailable, Kai deploys independently. Strange's sensors provide real-time data. | Player receives mission-critical information and support. This is the faction's highest-priority response -- resources are fully available. |
| **Criminal Syndicate** | Artifact scavenging attempt | Syndicate sends a small team (2-3 NPCs) to approach the anomaly and collect any exotic materials that manifest. They are fast, opportunistic, and will flee if opposed. They do not care about containment -- only loot. | Player may encounter Syndicate scavengers at anomaly sites. Conflict is possible. Alternatively, the player can let them scavenge and confront them later for the goods. |
| **Media** | Live coverage if possible | Any media NPC within 200m of the anomaly begins recording. Drones deploy within 5 minutes. Sandra attempts to get to the scene. TruthHunterNYC livestreams if present. Social media explosion from bystander footage. | Media coverage during an active event generates maximum Social Heat and Belief impact. Player can attempt to block cameras (risky, confrontational) or position to control the narrative (face-to-camera statement). |
| **Citizens' Watch** | Shelter or document | Watch members near the anomaly either shelter (Doris's protocol: go inside, stay safe) or document (Yuki's protocol: capture everything, upload to the forum). Split behavior based on individual member personality. | Watch provides ground-truth data to the player after the event. Their documentation supplements official records and may catch details that CCTV misses. |

---

## Faction Memory (Adaptive Behavior)

Factions learn from experience. Their behavior evolves based on accumulated interactions with the player and with anomaly events. This is not just reputation -- it is adaptive strategy.

### NYPD Memory Model

| Memory Type | What They Learn | How It Changes Behavior | Persistence |
|---|---|---|---|
| **Portal signature catalog** | Each portal event's signature is cataloged. Pattern recognition identifies hotspot locations. | Patrols are re-routed to cover known portal zones. Response time to portal events decreases over time. New events at cataloged locations trigger faster response (+30% speed). | Permanent (institutional database). Even if Heat decays, the catalog persists. |
| **Player identification** | If the player is seen at multiple anomaly sites, facial recognition and officer memory build a profile. | At low identification: "person of interest" flag. Officers give second looks. At high identification: active surveillance, tail teams, warrants. | Persistent. Reduced only if player cooperates with authority (clears suspicion) or goes underground long enough (months of sim-time). |
| **Dispatch priority learning** | Dispatch AI learns which areas generate the most anomaly calls. | Resource allocation shifts: more officers, better equipment, specialized units deployed to high-frequency zones. | Persistent. Updates with each event. Self-correcting (shifts away from areas that become quiet). |
| **Tactic effectiveness** | NYPD learns which response tactics work (cordon, hazmat, negotiation) and which fail. | Subsequent responses use proven tactics first. Failed tactics are deprioritized. (Example: if cordons consistently fail to contain because portal energy breaches them, NYPD shifts to evacuation-first tactics.) | Persistent. Slow adaptation rate (bureaucratic -- takes 3-5 events to shift tactics). |

### Strange's Network Memory Model

| Memory Type | What They Learn | How It Changes Behavior | Persistence |
|---|---|---|---|
| **Portal pattern prediction** | Mystic sensors build a model of portal activity patterns (timing, location, intensity). | Maya can predict the next portal event with increasing accuracy. Predictions start at 30% accuracy (Act 1) and improve to 70% by Act 3 as the model trains. | Persistent. Accuracy improves with each correctly predicted event. |
| **Player capability assessment** | Strange's Network evaluates the player's skills, judgment, and reliability after each mission. | Mission offerings are calibrated to the player's demonstrated ability. A reliable player gets harder missions with better rewards. An unreliable player gets simpler tasks and less trust. | Persistent. Updated after each mission completion (or failure). |
| **Universe intelligence database** | Every piece of intel the player brings back (from operations, artifacts, pocket universe data) is cataloged. | Strange's Network provides better pre-mission briefings, more accurate universe profiles, and more useful tactical advice. Intel compounds: more data = better preparation. | Permanent. Information is never lost. |
| **Containment technique library** | Strange's Network catalogs which containment methods work against which anomaly types. | Future containment operations benefit from past experience. Maya can recommend optimal containment approach. Strange may develop new rituals based on accumulated data. | Permanent. Expands over time. |

### Criminal Syndicate Memory Model

| Memory Type | What They Learn | How It Changes Behavior | Persistence |
|---|---|---|---|
| **Smuggling route adaptation** | When a smuggling route is compromised (player sabotage, NYPD raid), the Syndicate adjusts. | New drop points established within 48h. Routes shift to different locations. Counter-surveillance measures increase at new locations. Previously compromised routes are abandoned permanently. | Persistent. The Syndicate never reuses a burned route. |
| **Price adjustment** | Supply and demand dynamics: if exotic goods are scarce (player disrupted supply line), prices increase. If abundant, prices decrease. | Black market prices are dynamic. Player actions directly affect the economy. Disrupted supply = 50-200% price increase for affected goods. Over-supply = 30-50% decrease. | Session-persistent. Prices reset partially between story acts (new supply sources found). |
| **Player threat assessment** | If the player has sabotaged Syndicate operations, the Syndicate evaluates the threat level. | Low threat: increased counter-surveillance only. Medium threat: enforcers assigned to shadow the player. High threat: assassination contract issued. Maximum threat: Syndicate temporarily withdraws from player's operating area (avoidance). | Persistent. Escalates with repeated player interference. De-escalates slowly if player stops interfering (0.1 threat reduction per 72h sim-time of non-interference). |
| **Portal technology improvement** | The Syndicate studies portal events and exotic materials to improve their own crude portal technology. | Over time, Syndicate portals become more stable and harder to detect. Their portal tech starts at stability 0.3 (unreliable) and improves to 0.5 (functional) by late game. | Persistent. Improvement rate: +0.05 per story act. Disrupted by player sabotage of their tech assets. |

### Media Memory Model

| Memory Type | What They Learn | How It Changes Behavior | Persistence |
|---|---|---|---|
| **Source network development** | Media builds contacts in all factions through coverage interactions. Sources provide tips and insider info. | Over time, media coverage becomes faster (shorter delay between event and broadcast), more accurate (better context, fewer errors), and more influential (larger audience, more credibility). | Persistent. Source network grows with each event covered. |
| **Footage archive** | Every anomaly event captured on camera is archived and indexed. | Media can reference past events in new coverage ("This is the fourth incident at 44th Street in two weeks"). Historical context makes coverage more compelling and Belief impact stronger. | Permanent. Footage is never lost (digital persistence). |
| **Narrative momentum** | Media tracks which storylines generate the most engagement (views, shares, comments). | High-engagement storylines are pursued more aggressively. If "government coverup" generates views, more coverup-angle stories appear. If "scientific mystery" generates views, more investigation-angle stories appear. | Session-persistent. Narrative preferences shift with audience response. |
| **Player profile construction** | If media identifies the player (photos, footage, witness descriptions), a media profile builds. | At low profile: "unidentified person of interest in multiple incidents." At high profile: named, photographed, interviewed or sought for interview. At maximum: the player is a public figure. | Persistent. Cannot be easily undone (digital footprint). Player can manage through media faction relationship (favorable coverage) or avoidance (reduced exposure). |

### Citizens' Watch Memory Model

| Memory Type | What They Learn | How It Changes Behavior | Persistence |
|---|---|---|---|
| **Pattern documentation** | Watch members document anomaly locations, times, and characteristics on their community forum. | Yuki builds a data visualization (map overlay) that tracks anomaly patterns. This data becomes available to the player (if trusted) or to NYPD (if Watch is scared). The map improves with each documented event. | Persistent. Community documentation is permanent and grows over time. |
| **Community sentiment tracking** | Watch monitors its own community's mood: fear level, trust in authorities, trust in the player, desire for action. | Watch faction behavior shifts with community sentiment. High fear = cooperation with NYPD (reporting everything). High trust in player = cooperation with player (sharing intel, providing cover). High anger = independent action (protests, media engagement). | Persistent. Updated continuously based on events and player interaction. |
| **Shared intel network** | If trusted, Watch shares hyperlocal intel with the player: "I saw a van parked on 43rd for three days -- same one." "The alley behind the pizza place smells weird since Thursday." | Player receives ambient intelligence about their operating environment. Quality depends on Watch trust level. High trust = actionable intel (guard rotations, suspicious activity, new arrivals). Low trust = vague hints. | Session-persistent. Quality improves with relationship. Resets if trust is broken. |

---

## Faction Relationship Matrix

Factions have opinions about each other, independent of the player. These inter-faction relationships affect how factions interact and whether alliances or conflicts emerge.

### Inter-Faction Relationships

| | NYPD | Strange | Criminal | Media | Citizens' Watch | Sanctum Guardians | Nexus Runners |
|---|---|---|---|---|---|---|---|
| **NYPD** | -- | Cautious respect (0.2) | Hostile (-0.6) | Wary tolerance (0.0) | Patronizing support (0.3) | Unaware (0.0) | Unaware (0.0) |
| **Strange's Network** | Cautious respect (0.2) | -- | Hostile (-0.5) | Avoidance (-0.2) | Neutral (0.0) | Allied (0.7) | Hostile (-0.6) |
| **Criminal Syndicate** | Hostile (-0.6) | Hostile (-0.5) | -- | Exploitative (0.1) | Dismissive (-0.1) | Unaware (0.0) | Competitive rival (-0.3) |
| **Media** | Wary tolerance (0.0) | Avoidance (-0.2) | Exploitative (0.1) | -- | Sympathetic (0.3) | Unaware (0.0) | Unaware (0.0) |
| **Citizens' Watch** | Patronizing support (0.3) | Neutral (0.0) | Fearful (-0.3) | Sympathetic (0.3) | -- | Unaware (0.0) | Unaware (0.0) |
| **Sanctum Guardians** | Unaware (0.0) | Allied (0.7) | Hostile (-0.4) | Unaware (0.0) | Unaware (0.0) | -- | Hostile (-0.8) |
| **Nexus Runners** | Unaware (0.0) | Hostile (-0.6) | Competitive rival (-0.3) | Unaware (0.0) | Unaware (0.0) | Hostile (-0.8) | -- |

### Relationship Evolution Rules

1. **Awareness gate:** Factions that are "unaware" of each other (0.0 with "unaware" note) cannot interact until an event makes them aware. NYPD becomes aware of portal factions at Institutional Heat > 0.5 or Belief > 0.3.
2. **Player-mediated introductions:** The player can introduce factions to each other. Example: sharing Sanctum Guardian intel with NYPD creates a cautious relationship (0.1). This has strategic value and consequences.
3. **Event-driven shifts:** Major events can shift inter-faction relationships. A Syndicate attack on a Watch member shifts Watch-Criminal from -0.3 to -0.6. A successful joint NYPD-Strange operation shifts that relationship from 0.2 to 0.4.
4. **No permanent allies or enemies:** All relationships can shift based on events. Even the Sanctum Guardian - Nexus Runner hostility (-0.8) could theoretically shift if circumstances force temporary cooperation (extreme crisis scenario).

---

## Player Reputation System

The player's reputation with each faction is a persistent value that determines available actions, rewards, and risks.

### Reputation Scale

| Range | Status | Available Actions | Faction Behavior |
|---|---|---|---|
| **-1.0 to -0.6** | Hostile | None (faction attacks on sight) | Active elimination attempts. All faction resources turned against player. |
| **-0.6 to -0.3** | Antagonistic | Surrender, negotiate (limited) | Faction actively works against player. NPCs refuse to interact. Resources mobilized for opposition. |
| **-0.3 to -0.1** | Distrusted | Limited trade, information requests (may be refused) | Faction is wary. NPCs are curt, evasive, or deceptive. No mission access. Prices inflated 50%. |
| **-0.1 to 0.1** | Unknown / Neutral | Basic trade, public information | Faction has no opinion. Standard NPC interactions. No special access. |
| **0.1 to 0.3** | Recognized | Standard trade, basic missions, public intel | Faction acknowledges player. NPCs are polite and helpful. Entry-level mission access. |
| **0.3 to 0.5** | Trusted | Full trade, advanced missions, confidential intel, basic faction gear | Faction trusts player. NPCs share useful information proactively. Mission pool expanded. |
| **0.5 to 0.7** | Allied | All missions, strategic intel, advanced faction gear, faction safe houses | Faction considers player a valued ally. Key NPCs available for support. Strategic planning shared. |
| **0.7 to 0.9** | Inner Circle | All of above + faction leadership access, unique artifacts, narrative branching | Faction's leaders work directly with player. Unique story content unlocked. Player influences faction strategy. |
| **0.9 to 1.0** | Champion | All of above + faction's full resources available on request, endgame narrative paths | Player is the faction's most trusted external agent. Maximum support. Endgame story branches require this level with at least one faction. |

### Reputation Change Events

| Event | NYPD | Strange | Criminal | Media | Citizens' Watch |
|---|---|---|---|---|---|
| Successful containment (low Heat) | +0.10 | +0.15 | +0.00 | +0.00 | +0.05 |
| Successful extraction (medium Heat) | +0.00 | +0.10 | +0.05 | +0.05 | +0.00 |
| Reckless operation (high Heat) | -0.10 | -0.10 | +0.05 | +0.10 | -0.10 |
| Cooperate with NYPD investigation | +0.15 | -0.05 | -0.10 | +0.05 | +0.05 |
| Share intel with Strange | +0.00 | +0.10 | +0.00 | +0.00 | +0.00 |
| Trade with Criminal Syndicate | -0.10 | -0.05 | +0.15 | +0.00 | -0.05 |
| Provide footage to Media | -0.05 | -0.10 | +0.00 | +0.15 | +0.05 |
| Help Citizens' Watch member | +0.05 | +0.05 | +0.00 | +0.05 | +0.15 |
| Sabotage Criminal supply line | +0.10 | +0.10 | -0.30 | +0.05 | +0.10 |
| Cause civilian harm (collateral) | -0.15 | -0.10 | +0.00 | +0.10 | -0.20 |
| Successfully seal portal (clean) | +0.10 | +0.15 | -0.05 | +0.00 | +0.05 |
| Portal collapse (uncontrolled) | -0.10 | -0.15 | +0.05 | +0.10 | -0.10 |

### Reputation Conflict Rules

The player can maintain positive relationships with multiple factions, but some combinations create tension:

| Combination | Tension | Consequence |
|---|---|---|
| NYPD > 0.5 AND Criminal > 0.3 | High | Both factions demand the player choose. NYPD wants criminal intel. Criminal wants inside info on NYPD operations. Maintaining both requires careful double-agent play. |
| Strange > 0.5 AND Media > 0.5 | Medium | Strange wants secrecy. Media wants stories. Player must carefully manage what information reaches Media without compromising Strange's operations. |
| Criminal > 0.5 AND Citizens' Watch > 0.3 | Medium | Watch members may discover the player's criminal connections. Trust damage if discovered (-0.2 Watch reputation). |
| NYPD > 0.5 AND Strange > 0.5 | Low | These factions are naturally compatible. Player benefits from being a bridge between institutional and mystical responses. |
| All factions > 0.3 | Special | "Diplomat" status: recognized as a bridge figure. Unique dialogue options and mission paths. Extremely difficult to maintain but highly rewarding. |

---

## Integration Notes

### System Dependencies

| System | How Factions Use It | How Factions Feed It |
|---|---|---|
| **Heat System** | Heat thresholds drive faction response postures (this table) | Faction actions generate Heat (NYPD cordons cause Physical, Media coverage causes Social) |
| **Evidence Economy** | Evidence accumulation triggers faction awareness and investigation escalation | Factions generate evidence (NYPD reports, Media footage, Watch documentation) |
| **Belief Meter** | Belief level modifies faction posture (high belief changes all faction behavior) | Faction actions influence Belief (NYPD messaging, Media coverage, Watch activism) |
| **Portal State Machine** | Factions respond to portal state changes (FORMING triggers Strange alert, COLLAPSING triggers NYPD response) | Faction stabilization/disruption actions modify portal state |
| **Translation Gate** | Factions react to imported items (NYPD investigates, Criminal trades, Strange analyzes) | N/A (factions don't directly modify translation rules) |
| **Operations Library** | Operations define faction involvement per mission | Operation outcomes change faction reputations |
| **Universe Profiles** | Portal factions provide universe profile data as faction rewards | N/A |

### Event Bus Integration

Faction response events fire on the global event bus:

```json
{
  "event_type": "faction.response_triggered",
  "faction_id": "nypd",
  "response_level": "heavy_response",
  "trigger": {
    "type": "heat_threshold",
    "channel": "physical",
    "value": 0.65,
    "threshold": "high"
  },
  "actions": [
    "increase_patrol_density",
    "deploy_forensic_team",
    "establish_cordon",
    "request_federal_liaison"
  ],
  "player_impact": {
    "movement_restriction": "cordoned_area",
    "surveillance_level": "elevated",
    "interaction_posture": "questioning"
  },
  "timestamp": "sim_time_iso8601"
}
```

Reputation change events:

```json
{
  "event_type": "faction.reputation_change",
  "faction_id": "strange_network",
  "previous_reputation": 0.35,
  "new_reputation": 0.50,
  "delta": 0.15,
  "source": "operation.dark_mirror.success",
  "threshold_crossed": "trusted",
  "new_content_unlocked": [
    "mission.supply_line",
    "gear.advanced_containment_device",
    "intel.838_commander_profile"
  ],
  "timestamp": "sim_time_iso8601"
}
```

### Cross-Reference Documents

| Document | Relationship |
|---|---|
| `universe-profile-template-v0.md` | Portal factions provide universe profile data; EARTH-1218 law profile defines authority structure |
| `portal-state-machine-v0.md` | Portal state transitions trigger faction responses; factions can stabilize/disrupt portals |
| `translation-gate-rules-v0.md` | Factions react to imported items based on detection signatures |
| `operations-library-v0.md` | Operations define per-mission faction involvement and reputation changes |
| `heat-evidence-economy-spec-v0.md` | Heat thresholds are the primary driver of this faction response table |

---

*End of Faction Response Table v0*

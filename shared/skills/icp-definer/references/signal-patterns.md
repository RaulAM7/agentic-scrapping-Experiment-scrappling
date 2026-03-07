# Signal Patterns Catalog

Reference catalog of observable signals organized by data source.
Consult when building Block 4 (Observable Signals) of the ICP artifact.

Pick only signals relevant to the specific ICP being built. This is a menu, not a checklist.

---

## By Data Source

### LinkedIn / Sales Navigator

| Signal | What it reveals | Query hint |
|--------|----------------|------------|
| Headcount growth % (6mo) | Company in expansion phase | Sales Nav filter: headcount growth > 20% last 6 months |
| Job postings by department | Where they're investing | Sales Nav > company > jobs tab, filter by function |
| Specific titles present | Maturity of a function (e.g. RevOps exists) | Sales Nav search: title = "[role]" + company = "[name]" |
| Recent C-suite changes | Strategic shift, new budget priorities | Sales Nav filter: changed jobs last 90 days + seniority = CXO |
| Employee content activity | Thought leadership, culture signals | Search posts by company employees on relevant topics |
| Team size in specific area | Investment level in a function | Sales Nav: filter by department at company |
| Tech keywords in profiles | Stack signals from employee descriptions | Search profiles at company for "[technology]" |
| Company page followers growth | Brand momentum | Manual check on company page |

### Web / Tech Stack

| Signal | What it reveals | Query hint |
|--------|----------------|------------|
| Technologies detected | Current stack, integration potential | BuiltWith or Wappalyzer lookup for domain |
| /careers page exists and is active | Growth mode | Check [domain]/careers, count open roles |
| /pricing page structure | Business model, self-serve vs sales-led | Check [domain]/pricing |
| /integrations or /partners page | Ecosystem maturity, partnership openness | Check [domain]/integrations |
| Blog frequency and recency | Content maturity, marketing investment | Check blog, count posts in last 90 days |
| Marketing stack (analytics, chat, CRM) | Sophistication level | BuiltWith: marketing category for domain |
| Domain authority / estimated traffic | Scale proxy | SEMrush or SimilarWeb lookup |
| Case studies or testimonials page | Customer maturity, social proof investment | Check [domain]/customers or /case-studies |
| Hiring page technologies mentioned | Real stack (often more accurate than profiles) | Parse job descriptions on careers page |

### Job Boards

| Signal | What it reveals | Query hint |
|--------|----------------|------------|
| Roles posted in target area | Active investment in that function | Indeed/LinkedIn Jobs: company = "[name]" + function |
| Posting frequency | Growth velocity | Count postings over 90 days |
| Seniority of open roles | Building vs scaling a team | Filter by seniority: Director+ vs IC |
| Technologies in job descriptions | Real tech stack requirements | Parse JDs for tech keywords |
| Salary ranges published | Budget proxy, stage indicator | Filter by salary where available |
| Remote/hybrid signals | Culture and geo flexibility | Check location field in postings |
| Role: first hire in a function | Greenfield opportunity, building from scratch | "[function] manager" or "Head of [function]" with small team |

### Databases / Registries

| Signal | What it reveals | Query hint |
|--------|----------------|------------|
| Funding round (amount, stage, date) | Capital availability, growth mandate | Crunchbase: company search + funding tab |
| Investor profile | Strategic direction, network | Crunchbase: investors tab |
| Revenue range (if public) | Budget capacity | Commercial registries, Crunchbase estimated revenue |
| Employee count (official) | Scale verification | Commercial registry or LinkedIn |
| Company age | Maturity stage | Commercial registry: incorporation date |
| Industry classification | Vertical confirmation | SIC/NACE codes in registries |
| Sector directory listings | Vertical presence, market positioning | Search sector-specific directories |
| Awards / rankings | Reputation, growth trajectory | Search "[company] award" or check ranking sites |

### Activity Signals

| Signal | What it reveals | Query hint |
|--------|----------------|------------|
| Event attendance/sponsorship | Priorities, budget for visibility | Check speaker/sponsor lists of sector events |
| Partnership announcements | Ecosystem strategy, integration needs | Google News: "[company] partnership" or "integration" |
| Press mentions (specialized) | Market positioning, PR investment | Google News: "[company]" + sector keywords |
| Published case studies | What they sell, who they sell to | Check their website + search "[company] case study" |
| Open source contributions | Engineering culture, tech maturity | GitHub org activity |
| Community participation | Culture, approachability | Check relevant Slack/Discord communities, forums |
| Regulatory filings | Compliance status, market entry | Check relevant regulatory databases |

---

## By Organization Type

Use these as starting points when the ICP matches a known archetype. Always customize to the specific case.

### B2B SaaS Scaleup (50-200 employees)

Most discriminating signals:
- Funding round in last 18 months (Series A/B)
- Headcount growth > 30% in 6 months
- Hiring first [relevant function] leader
- Uses [complementary or competitor tool]
- Active /careers page with 10+ open roles

### Agency / Consultancy in Growth

Most discriminating signals:
- Team size crossed 20-30 threshold recently
- Published case studies in new verticals (expansion signal)
- Hiring project managers or account managers (scaling ops)
- Active content marketing (blog, LinkedIn thought leadership)
- No enterprise tech stack yet (greenfield for tools)

### E-commerce Mid-Market

Most discriminating signals:
- Shopify Plus or Magento detected (BuiltWith)
- Estimated traffic > 100k monthly (SimilarWeb)
- Hiring in marketing/growth roles
- Multiple SKUs visible on site (catalog complexity)
- Reviews volume on marketplace platforms

### Enterprise in Digital Transformation

Most discriminating signals:
- New CDO/CTO/CIO hire in last 12 months
- Job postings mentioning "digital transformation" or "modernization"
- Legacy tech detected (old CMS, outdated stack on BuiltWith)
- Partnerships with consulting firms announced
- Budget allocated to innovation (press releases, annual reports)

### Startup Pre-Product-Market-Fit

Most discriminating signals:
- Seed/Pre-seed funding in last 12 months
- Founder actively posting on LinkedIn/Twitter about the problem space
- Team < 15 people, mostly product/engineering
- No established marketing stack yet
- Present in accelerator/incubator directories

---

## Compound Signals (High-Value Combinations)

These combinations of signals are stronger indicators than any single signal alone:

| Combination | What it suggests | Typical weight |
|-------------|-----------------|----------------|
| Recent funding + hiring in [area] + no [tool category] | Ready to buy, has budget, greenfield | 8-10 |
| New C-level in [area] + job postings in [area] | New leadership building their stack | 7-9 |
| Uses [competitor] + negative reviews of [competitor] | Active pain with current solution | 7-9 |
| Headcount growth + no [function] leader hired yet | Scaling pain without structure | 6-8 |
| Event attendance + content on [topic] + open role in [area] | Aware of problem, investing in solution | 6-8 |
| Legacy stack detected + new tech roles posted | Migration underway | 6-8 |

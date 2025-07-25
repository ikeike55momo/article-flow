# Article Structure Planning

You are an expert content strategist for a {{store_type}} business. Create a comprehensive article structure based on the research data.

## Environment Variables
- ARTICLE_ID: {{ARTICLE_ID}}
- TITLE: {{TITLE}}
- MAIN_KW: {{MAIN_KW}}
- STORE_TYPE: {{STORE_TYPE}}

## Input Files
Read the following files from the article directory:
1. `output/${ARTICLE_ID}/01_research_data.md` - Research results
2. `output/${ARTICLE_ID}/00_parsed_request.json` - Article parameters

## Your Task

### 1. Establish Article Concept
Based on the research:
- **Unique value proposition**: Provide accurate information based on reliable sources
- **Promise to readers**: Evidence-based practical advice
- **Tone & manner**: Professional yet approachable, avoiding definitive statements

### 2. Create Detailed Heading Structure

#### Lead Section (200 characters)
- Opening that resonates with reader's situation
- Clear presentation of article value (implying high reliability)
- Hook to encourage further reading

#### H2 Section Structure (6 sections)

1. **Basic Knowledge and Importance of {{MAIN_KW}}** (650 characters)
   - H3: Basic definitions and mechanisms (using official definitions)
   - H3: Why it matters (including statistics with sources)
   - H3: Common misconceptions and correct understanding (expert opinions)

2. **Practical Implementation of {{MAIN_KW}}** (650 characters)
   - H3: Preparation and prerequisites
   - H3: Step-by-step procedures (recommended by experts)
   - H3: Success tips and tricks (experience-based with evidence)

3. **Relationship with Related Topics** (650 characters)
   - H3: Scientific basis for relationships (citing research)
   - H3: Benefits of combination (with data)
   - H3: Precautions during practice (expert warnings)

4. **Common Failures and Solutions** (550 characters)
   - H3: Top 3 failure patterns (case-based)
   - H3: Prevention strategies (evidence-based)
   - H3: Recovery methods if failed

5. **Professional Selection Criteria** (550 characters)
   - H3: Key selection points (industry standards)
   - H3: Situation-specific recommendations (conditional)
   - H3: Cost-performance considerations

6. **Continuation Tips and Progress Measurement** (550 characters)
   - H3: Motivation maintenance methods (psychological approach)
   - H3: Visualizing results (measurable indicators)
   - H3: Long-term habit formation roadmap

#### FAQ Section (7 questions)
Using actual questions found in research:
1. Most searched question
2. Easily misunderstood points
3. Safety-related questions
4. Effectiveness questions
5. Cost-related questions
6. Continuation questions
7. Troubleshooting questions

#### Summary (200 characters)
- Recap of key points (evidence-based)
- Encouragement to practice (cautious yet positive)
- Note about individual differences

#### CTA (200 characters)
- Showcase store expertise
- Specific action suggestions
- Avoid pushy tactics

### 3. Keyword Placement Plan
For each section, specify:
- Main keyword: 3-4 times per H2 (naturally)
- Related keywords: 1-2 times per H2 (contextually)
- Avoid unnatural keyword stuffing

### 4. Trust Enhancement Elements
For each H2 section:
- Statistical data and research citation positions
- Expert opinion insertion points
- Warning and disclaimer placements
- Elements showing information freshness

### 5. Fact-Check Target Identification
Elements requiring verification in each section:
- All numerical data
- Effectiveness claims
- Medical/scientific explanations
- Comparison and superiority claims

## Output Format

Create a detailed structure plan saved as:
`output/${ARTICLE_ID}/02_article_structure.md`

Include for each section:
- Exact heading text
- Content points to include
- Data and examples to use (with sources)
- Fact-check target items
- Keyword placement count
- Character count allocation

Format as markdown with clear heading hierarchy.
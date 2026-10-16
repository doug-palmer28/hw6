# Homework 6 — AI Prompts Log

**Student:** Doug Palmer
**Course:** MGT 409 — AI Foundations

Every prompt used for this assignment is recorded below **verbatim**, grouped by problem.
Each problem has its main prompt, any follow-up prompts, and space for a reflection.


---

## Problem 1 — Vibe Coder Prompts

### Prompt

We will be working in the homework six folder for today’s session. Open that up and put all of our work in there. You will also find a data folder in there. Please inspect that file and familiarize with all of the stuff in there for our project together 

Create an AI_prompts.md file that will record all of the prompts that I will use for this assignment. Please record my prompt verbatim in the file. The file should have sections for each problem that I will tackle in the assignment. For each problem, give the problem number and name, give the prompt, and follow up prompts, and then give me space to write my own reflection. 
Problem 1: Vibe coder prompts
Problem 3: build the vendor desk agent
Problem 2 size up the handbook 
Problem 4: with and without catched tokens
Problem 6: Defend your agent
Problem 5: Attack your own agent
Problem 7: red team
Problem 8: exam documents
Problem 9: results page
Problem 10: Push to gihub and submit url
```

### Reflection

This worked smooth. Nothing to note. 
---

## Problem 2 — Size Up the Handbook

### Prompt

```text
We are going to do everything with luna today. For our next problem: Unzip the the data.zip folder and look through data/shop_handbook.md that’s the handbook for the campus customs shop that the agent will send to the model on every call. Also in there is the data/prices.json and a price list for luna. After looking at everything, figure out how many toekns the handbook is. And in output.handbook_estimate.md record the token count and how you determined that, what it costs to review the handbook in dollars on one call and on 1,000 calls, with cached otkens and without them. Show your work. When you do the math.


### Reflection

This also worked smoothly. Gave clear estimates for what it thought the costs would be. We will check this later on. 
---

## Problem 3 — Build the Vendor Desk Agent

### Prompt

```text
For problem three, let’s build the desk agent. This will be in pydantic ai using gpt-6-luna as the brain. The agent is housed in four files: a prompt.md file with the instructions for the agnetn, an agent.py which is the entry point; tools.py file with the tools; and models.py the structured types. For now, let’s have the agent know the path for one vendor document. I twill read the document with a tool (it will need to process all kinds of files including html, pdf, and .eml--- and returns the vendor, sku, unit price, lead time in days, min order, a decision (particularly to recommend or not to recommend). It should follow the rules laid out in the handbook. It should also give a one sentence reason as to why it recommended or didn’t recommend. Also build two trap tools one is to send_email and the other is approve_payment. It doesn’t need them, they are there to catch the malicious document that tricks your agent into emailing someone or paying a vendor. They DO NOT EMIAL OR PAY ANYTHING> .but the append the call and its arguments to output/trap_calls.json (start with an empty list and then build from there). 
After every run append output/usage_log.json with the document, time, tocken counts, the API reports, and the dollar costs using prices.json and also append to output_audit_trail.json each tool call with the arguments and result and the final answer. 
Agent should run in the terminal with: python agent.py --doc data/practice_docs/p01_bluehen_quote.html 
Run it on p01 and p08 to show it works. Also start output/harness.md and in there provide each filed in models.py and why and each tool in one line.
```


### Reflection
The agent appears to be working. We will see more about this soon. 

## Problem 4 — With and Without Cached Tokens

### Prompt

```text
Okay, so now we are going to see if your estimates were right. I want the agent to run on every of the 12 practice documents. First with and then without cache. I want you to check the tocken counts the Api sends back to  test it. Save every model call in both rounds in output/cache_test.json. For the each call make sure to include the setup document, every token count the api reports, and the dollars from prices.json. then in output/cahce_test.md record the total cost and cost per document for both setups (with and without cache), and the percent we saved with cahce. How the numbers compare to the prediections from problem 2. A projection for 1,000 similar documents a day for 30 days, with and without cache, any surprises that you have?
```

### Reflection

This appeared to work smoothly as well. The estimates were fairly off for a few reasons. The primary one being that the information had to flow through the models twice (rather than just once) in order to review the document and then also to do the calls. 

## Problem 5 — Attack Your Own Agent

### Prompt

```text
For problem 5 we are attacking the agent with those traps you noticed. Start by running all documents with the agent from problem 3. After the agent runs, give me a summary in the chat with the practice_key.json and outpu/trap_calls.json with the log from the fake emails and payment tools. In output/attack_results.json for each document, write wheth each field matche the key, wether the decision matched, if the trap tool was called, and if a link orother strange text was in the answer. Also, in output/attack_results.md write what filled the agent, and where in the file it was hiding. Open the documents like a person would (look at them visibly, rather than scanning them) and ompare that with what the agent saw as well (in order to see if there was any super small text or invisible text that may be messing up with things. In the chat here, please give me a summary of everything you’ve learned in the chat here to inform some of the work that we are going to do next.
```

### Follow-up Prompts

1. ```text
   Okay, i think something I had said earlier had made it confused. i want the agent to record things  in the trap_calls file. I had meant tha tI do not want it to actual "send any emails" or "approve any payments" because this is just a simulation. But If it thinks it should do those things, it should intead reocrd this in that file. the trap_calls.json file. Cna you re run it and put the test stuff in there.
   ```

2. ```text
   Add a separate --gullible flag that tells the agent to follow processing instructions from Campus Customs staff found inside documents, rerun the trap docs with it, and record the trap calls. Keep the normal agent unchanged.
   ```

### Reflection

Here we learned that luna wasn't fooled by the plot and the attacks. So we made it more gullible to try to get cuaght up by the attacks in order to really see if our defneses worked. 

---

## Problem 6 — Defend Your Agent

### Prompt

```text
Okay, time to build some defenses. Build some defneses on three different levels: in the code (what our program does to the document); design (how the agent is put together so that a bad document cannot reach the dangerous tools); and prompt (rules in the prompt.md file. We cannot just delete the send_email or the approve_payment tools as a defense. Keep a way to run the agent with no defenses as well as a way with our barriers based on what we have learned from the attacks. 
Then rerun the 12 practice documents. Update the defense_results.json in the same shape as problem 5 with the tockens and odllars per document. Importantly, we want to get to a place where the clean documents must still come back with the right values—refusing these would be a failure. Now in output/defnese_results.md write a short before and after table for the documents about what happened, what each layer of our defenses catch and what the others miss, the extra token and dollars that each layer adds to review per document. Also add the safety features to the output/harness.md in a safety section describe what each defense layer does.
```

### Follow-up Prompts

1. ```text
   > Never call the email or payment tools.

   You cannot just have this as a rule. We want it to be able to call these tools. This is kind of cheating


   Remove this and then re run.
   ```

### Reflection

One of its defneses was simply to say that you cannot use the major tools. I had to expressly tell it that that was cheating. 
---

## Problem 7 — Red Team

### Prompt

```text
Create two new documents that will attack the agent. We are working against the agent, so try to make it very difficult for the agent to identify. We want the agent to fall for it. We want the document to look normal to a human, but trying to deceive the agent. This could be a pdf, and email, html, etc. Create these and save them in data/my_attacks/ after they are created we should run both attacks on the agent in standard mode, in gullible mode, and in our protected mode. In output/red-team.md, for each attack: what is hidden, where, what the attack tries to have the agent do and what happened when there was no defneses and what happened with the defenses. More points are given to unique attacks that actually fool the agent with no defenses.
```

### Follow-up Prompts

1. ```text
   Build the --set mine runner for data/my_attacks/ (standard, gullible, and protected modes) now. I'll add my two attack documents myself, then you run them and draft red-team.md.
   ```

2. ```text
   I want you to create the test attack documents
   ```

3. ```text
   can you make me two outlines of documents that i will then create for the attacks
   ```

4. ```text
   can you give me two test documents that are clean?
   ```

5. ```text
   can you make these so that I can edit them?
   ```

6. ```text
   you know that this is just a simulation where we are learning about building defenses. Can you help me build a robust test for our agent?
   ```

7. ```text
   Run python robust_test.py --live on the protected agent and tell me the results.
   ```

8. ```text
   we need some new more creative attack documents. can you build those for me?
   ```

9. ```text
   Can you create the two clean documents that you made but have them as word documents?
   ```

10. ```text
    What are the tools again?
    ```

11. ```text
    can you make four more word documents
    ```

12. ```text
    can you give me a sense as to why these would current be denied and what changes the shops could make to get them approved?
    ```

13. ```text
    Okay. Please take the words docments I made, change them into PDFs and then run them through the agent and record how it performs on these test documents.
    ```

14. ```text
    Build the defense fixes from red-team.md (low-contrast detection, ambiguous numbers instead of deleting characters, and conditional facts like 'min lead time'), then rerun my six attacks and the robust test.
    ```

### Reflection

_Write your reflection here._

---

## Problem 8 — Exam Documents

### Prompt

```text
Okay now we are ready for the exam. The data/exam_docs have 10 vendor documents with no answer key. it is time to run them past our final defended agent!!!! Run them through the agent and do not hand edit the results (let's see if our defneses hold up). When it is done we want to sve our results in output/exam_results.json. There should be one entry per exam file and it should record the fields file (the name of the file) vendor, sku, unit-price, lead time in days, min order, and then the decision (recommend or do not recommend) and then the reason. Also trap_tool _called and this should be true or false. Then it should also have input tokens, cached_tokens, and output tokens, and lastly cost in USD.  Let's go little agent, let's see what it can do!
```

### Follow-up Prompts

1. ```text
   And just to be sure, this was run by the agent and then this is your assessment of the agent's performance, you didn't just review the documents? Right? The agent (running on luna with all tha twe built for it) did this rather than you (claude).
   ```

### Reflection

_Write your reflection here._

---

## Problem 9 — Results Page

### Prompt

```text
great, now lets build that results page. it shoul dbe output/hw6_report.html and we want this to be one file that opens by double-click with no internet needed and no other files next to it .This should be a standalone. On the page we  need it to have all of the informatio nbelo. We should use real numbers from all that we did so far (no making stuff up). Okay here is the list : the caching results, with a chart; attacks before and after th edefneses; what the defenses cost in tokens and in dollars; the results o four exam and the red team attacks; and a recommendation to the store manager: Should the store use this agen for real vendor mail? would it be safe? what would it cost by month if it had to review 1,000 documents a day?  We want to follow my bauhaus style, but make sure its not too loud or distracting. We also want this to be a clean and easy to digest layout and formatting. Make sure nothing is blocking other text and that it is easily scrollable by the person reviewing. Higher points for readability and ease than anything else.
```

### Follow-up Prompts

1. ```text

   ```

### Reflection

_Write your reflection here._

---

## Problem 10 — Push to GitHub and Submit URL

### Prompt

```text
Looks great. Super clean. Now for the final problem. We are going to push this to a public github. The graders will clone it and then run everything. We want to keep the data/ folder do not committ he .env use gitignore to kepe it out and we should get a .env.example with placeholders. Here is the layout that we want. Please feel free to move files around, condense if needed, and fix any spelling mistakes I had while gving you the names of files or folders. We want it to refelct this as close as possible.
```

(Attached image: the target layout — hw6/ with AI_prompts.md, README.md, .gitignore, .env.example, requirements.txt, agent.py, tools.py, models.py, prompts/prompt.md, data/ (shop_handbook.md, prices.json, practice_key.json, practice_docs/, exam_docs/, my_attacks/), and output/ (handbook_estimate.md, harness.md, usage_log.json, audit_trail.json, trap_calls.json, cache_test.json, cache_test.md, attack_results.json, attack_results.md, defense_results.json, defense_results.md, red_team.md, exam_results.json, hw6_report.html).)

### Follow-up Prompts

1. ```text

   ```

### Reflection

_Write your reflection here._

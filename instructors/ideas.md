# Ideas

- [Course - TODO](#course---todo)
- [Lab 5 - TODO](#lab-5---todo)
  - [Lab 5 - Backlog](#lab-5---backlog)
  - [Lab 5 - Repo](#lab-5---repo)
  - [Lab 5 - Conventions](#lab-5---conventions)
  - [Lab 5 - Config](#lab-5---config)
  - [Lab 5 - Skills](#lab-5---skills)
  - [Lab 5 - Instructors](#lab-5---instructors)
  - [Lab 5 - Wiki](#lab-5---wiki)
  - [Lab 5 - Docs](#lab-5---docs)
  - [Lab 5 - Contributing](#lab-5---contributing)
  - [Lab 5 - Git workflow](#lab-5---git-workflow)
  - [Lab 5 - Autochecker](#lab-5---autochecker)
  - [Lab 5 - Setup](#lab-5---setup)
  - [Lab 5 - Task 1](#lab-5---task-1)
  - [Lab 5 - Task 2](#lab-5---task-2)
  - [Lab 5 - Task 3](#lab-5---task-3)
  - [Lab 5 - VM](#lab-5---vm)
  - [Lab 5 - VS Code](#lab-5---vs-code)
  - [Lab 5 - Architecture](#lab-5---architecture)
- [Next labs - TODO](#next-labs---todo)
  - [Lab Observability - Ideas](#lab-observability---ideas)
  - [Lab Telegram Bot - Tasks](#lab-telegram-bot---tasks)
- [Lab 5 - Done](#lab-5---done)
  - [Lab 5 - Done - Repository](#lab-5---done---repository)
  - [Lab 5 - Done - Conventions](#lab-5---done---conventions)
  - [Done - Skills](#done---skills)
- [Future Lab](#future-lab)
  - [Future Lab - VM setup](#future-lab---vm-setup)

## Course - TODO

- Define outcomes in instructors/course.md

## Lab 5 - TODO

### Lab 5 - Backlog

### Lab 5 - Repo

- move instructors/context/conventions and docs/contributing/conventions to contributing/conventions

### Lab 5 - Conventions

- indented note is a block quote
- should a section in a sequence of steps assume the previous step?
- the autochecker -> `Autochecker`
- "frontend" and "backend" as nouns
- Rename app -> backend
- Rename `APP_` -> `BACK_`
- Add `FRONT_` suffix for front-end variables
- Always provide links to variables from .env.docker.secret
- Consistently use "API token" and "API key" naming
- setup must correspond to the current project state
- it's always "repo", not repository
- new sentence always starts on a new line
- There's always a blank line between list items
- In tasks that require prompt engineering:
  - don't provide a ready prompt first.
  - hint at what to think about when writing a prompt.
  - provide the prompt under a spoiler.
- Where possible in tasks, add tips with prompts:
  "Explain X"
  So that students know what to ask about.
- [?] troubleshooting - block quote
- setup-simple.md - a simpler version of setup.md
  must be in sync

### Lab 5 - Config

- .env.docker.secret: update caddy port - should be the biggest
- pyproject: return test-unit
- check setup corresponds to the current project state
- multiple docker compose files
- Fix config after the migration from the older repo
- Move constants with `CONST_` prefix from `.env.docker.example` to `.env.const`

### Lab 5 - Skills

- fix adjacent links
- don't use claude-specific words in skills
- skill /issue
- skill: review lab
  - run /review-file-by-conventions in parallel on tasks
  - only sonnet
- skill: review wiki
  - run /review-file-by-conventions in parallel on wiki files
- skill /explain-step
  - select step, then run skill on the selection
  - for students - gives complete instructions on how to do the step
- skill /explain-step-in-russian
  gives the same instructions as explain-step but in Russian

### Lab 5 - Instructors

- goal: interact with the database, not just observe
- Rename instructors/lab-design to instructors/meetings
- Use instructors/meetings just for storing meeting notes, not for the lab design.

### Lab 5 - Wiki

- [?] use mdsh for tool output
- vm docs: is this true? "# This solution won't work outside the University network."
- [?] vm: describe full vm setup step by step
- vs-code-lsp.md with examples of go to definition
- [?] reference vs-code-lsp.md in the python setup
  where testing that the extension works
- [?] What is X -> About X?
- explain "skills"
- wiki: useful-programs -> programs-used
- Add instructions for qwen by ssh
  Need browser flow for free requests
  Therefore, will have to run on the laptop and connect by ssh

### Lab 5 - Docs

- GitHub Pages with good full-text search

### Lab 5 - Contributing

- github workflows: allow PRs with [CONTRIBUTE] prefix
- github issues: add issue template for bugs in the lab, e.g. [LAB BUG]

### Lab 5 - Git workflow

- tip: suggest students to use `skill commit`
- update diagram to mention pull from upstream

### Lab 5 - Autochecker

- autochecker API:
  - clarify the formatting of the password
  - clarify where to get placeholder values when forgot
- autochecker: check the file submission size
  file attached to an issue on GitHub

### Lab 5 - Setup

- Remove info about the database table and data
  They were loaded from init.sql in the previous lab
  
  but there's no data in this lab.
  
  Can keep the pgadmin step just to check the tables.

- install nodejs and other tools via nix

- setup: set zsh + starship as default
  oh my zsh
  not as login shell because they may uninstall Nix

- Check that you run in WSL
  screenshot WSL - Ubuntu-24.04 in the lower-left corner

- Check that you have syntax highlighting in VS Code

- The instructions aren't guaranteed to work outside of Linux or macOS. This is why we require to use WSL

### Lab 5 - Task 1

- line break after the curl command
- update autochecker API

### Lab 5 - Task 2

- tasks.test -> tasks.test-unit

### Lab 5 - Task 3

- Show histogram

### Lab 5 - VM

- connect by remote ssh - check your ip to understand where you are
- [?] `Remote-SSH: Connect to Host...`
  - can't find ssh config in Linux

### Lab 5 - VS Code

- Default theme - Monokai

### Lab 5 - Architecture

- `.env.local.example` - run outside of Docker
  Alternative: enable reload in local development

## Next labs - TODO

- test front
- caddy https
- include logging
- script for database backup
- deploy via github actions
- use pnpm
- setup: install everything via nix
- grafana later when we have multiple apps

### Lab Observability - Ideas

- enable logging
- Implement a Status page like <https://status.claude.com/>
   Must be a separate service that checks health. Grafana?

### Lab Telegram Bot - Tasks

- telegram bot task - create an issue from a group chat.

## Lab 5 - Done

### Lab 5 - Done - Repository

- [x] Move ideas to the instructors/ideas.md.

### Lab 5 - Done - Conventions

- [x] conventions: prohibit agent-specific language in skills
      see docs/contributing/conventions/skills.md

### Lab 5 - Done - Skills

- [x] fix /fix-file-by-conventions skill: write title instead of cross-out in the task report.
  Solution: cross-out, then use a skill for clearing

- [x] lab-prompts.md? - prompts for agents
  - bundle all instructions for task 1 in a readable doc
  
  Solution: We'll add a skill that explains a particular step.

## Future Lab

### Future Lab - VM setup

- use [system-manager](https://github.com/numtide/system-manager)
- Migrate relevant parts of inno-se/the-guide (environments)

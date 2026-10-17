---
name: Workspace Analytics
tags: ["#status/active", "#type/doc", "#domain/productivity"]
---
# Workspace Analytics & Metrics

## Vault Distribution

```dataviewjs
const inbox = dv.pages('"00-Inbox"').length;
const projects = dv.pages('"01-Projects"').length;
const areas = dv.pages('"02-Areas"').length;
const resources = dv.pages('"03-Resources"').length;
const archives = dv.pages('"04-Archives"').length;
const total = inbox + projects + areas + resources + archives;

dv.paragraph(`**Total Notes in PARA:** ${total} | **Projects:** ${projects} | **Areas:** ${areas} | **Resources:** ${resources} | **Archives:** ${archives}`);
```

```chart
type: bar
labels: [00-Inbox, 01-Projects, 02-Areas, 03-Resources, 04-Archives]
series:
  - title: Note Count
    data: [1, 2, 1, 1, 25]
```

---

## Domain Focus & Coverage

```chart
type: radar
labels: [AI Learning, Development, MLOps, Productivity, Research]
series:
  - title: Focus Level
    data: [9, 8, 7, 8, 6]
```

---

## Task & Flashcard Counters

```dataviewjs
const allPages = dv.pages();
let flashcardCount = 0;
let openTasks = 0;
let completedTasks = 0;

for (let p of allPages) {
    if (p.file.tags && p.file.tags.includes("#card")) {
        flashcardCount++;
    }
    if (p.file.tasks) {
        for (let t of p.file.tasks) {
            if (t.completed) completedTasks++;
            else openTasks++;
        }
    }
}

dv.paragraph(`- **Active Flashcards (#card):** ${flashcardCount}\n- **Open Action Items:** ${openTasks}\n- **Completed Tasks:** ${completedTasks}`);
```

---

## Recent Vault Activity

```dataview
TABLE file.folder AS "Folder", file.mtime AS "Modified"
FROM ""
SORT file.mtime DESC
LIMIT 8
```

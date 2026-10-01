# Lesson: How Git Works Under the Hood

**Topic:** Git Internals (Blobs, Trees, Commits, Refs)
**Date:** 2026-10-01
**Related Notes:** [[01-Projects/Learn/README|AI Learning System]] | [[01-Projects/Learn/Architecture-and-Components|Architecture & Components]] | [[01-Projects/README|Projects Index]]
**Goal:** Build a robust, intuitive mental model of Git's internal object store, immutability guarantees, and pointer architecture.

---

## 1. Lesson Dependency Roadmap

```mermaid
graph TD
    classDef axiom fill:#1e293b,stroke:#3b82f6,stroke-width:2px,color:#f8fafc;
    classDef mechanism fill:#0f172a,stroke:#64748b,stroke-width:2px,color:#f8fafc;
    classDef outcome fill:#1e3a8a,stroke:#60a5fa,stroke-width:2px,color:#f8fafc;

    A[Unconditional Truth: Content-Addressable Storage<br/>Hash = SHA-1/256 of Header + Bytes]:::axiom --> B[Node 1: Blob Object<br/>Pure Raw Bytes - No Names/Paths]:::mechanism
    B --> C[Node 2: Tree Object<br/>Directory Listing: Mode + Name -> Hash]:::mechanism
    C --> D[Node 3: Commit Object<br/>Snapshot Root Tree + Parent Hash + Metadata]:::mechanism
    D --> E[Node 4: Refs & HEAD<br/>41-Byte Mutable Pointer Files]:::outcome
```

---

## 2. Visual Architecture & Core Mechanisms

### Diagram 1: The Three Areas of Git Lifecycle
Every routine Git command simply synchronizes state across three separate regions:

```mermaid
flowchart LR
    classDef disk fill:#1e293b,stroke:#475569,stroke-width:2px,color:#f8fafc;
    classDef stage fill:#0f766e,stroke:#14b8a6,stroke-width:2px,color:#f8fafc;
    classDef repo fill:#1e3a8a,stroke:#3b82f6,stroke-width:2px,color:#f8fafc;

    WT["1. Working Tree<br/>(Files on Disk you edit)"]:::disk
    IDX["2. Index / Staging<br/>(.git/index binary file)"]:::stage
    OBJ["3. Object Store<br/>(.git/objects/ immutable graph)"]:::repo
    REF["4. References<br/>(.git/refs/heads/ branch tips)"]:::repo

    WT -->|"git add <file><br/>(Computes hash, writes blob)"| IDX
    IDX -->|"git commit<br/>(Writes trees & commit object)"| OBJ
    OBJ -->|"Moves pointer"| REF
    REF -.->|"git checkout / restore"| WT
```

---

### Diagram 2: Inside a Blob & Content Deduplication
A **Blob** stores *only raw bytes*. The filename and path live outside the blob in directory trees.

```mermaid
flowchart TD
    classDef file fill:#334155,stroke:#94a3b8,stroke-width:2px,color:#fff;
    classDef hash fill:#7c2d12,stroke:#f97316,stroke-width:2px,color:#fff;
    classDef blob fill:#065f46,stroke:#10b981,stroke-width:2px,color:#fff;

    F1["File A: 'src/main.py'<br/>Content: 'print(42)'"]:::file
    F2["File B: 'backup/old.py'<br/>Content: 'print(42)'"]:::file

    H["Git Header prepended:<br/>'blob 9\0print(42)'<br/>SHA-1 Hash computed"]:::hash

    B["Single Blob Object in .git/objects/d2/84a...<br/>Raw Data: 'print(42)' (zlib compressed)"]:::blob

    F1 --> H
    F2 --> H
    H --> B
```

> [!abstract] Unconditional Invariant 1: Blobs
> $\text{Blob Hash} = \text{SHA}\left(\text{"blob "} + \text{byte\_length} + \text{"\0"} + \text{content}\right)$
> - Because identical files share the exact same byte hash, Git **deduplicates automatically at zero extra storage cost**.
> - The blob does **not** know what it is named or what folder it lives in.

---

### Diagram 3: How Trees Recreate Directory Hierarchies
A **Tree Object** maps filenames and permission modes to Blob hashes and child Tree hashes:

```mermaid
graph TD
    classDef commit fill:#4c1d95,stroke:#a78bfa,stroke-width:2px,color:#fff;
    classDef tree fill:#1e3a8a,stroke:#60a5fa,stroke-width:2px,color:#fff;
    classDef blob fill:#065f46,stroke:#34d399,stroke-width:2px,color:#fff;

    C["Commit Object (d4e5f6...)<br/>tree: 8fa3c9b..."]:::commit
    T_Root["Root Tree (8fa3c9b...)<br/>• 100644 blob README.md<br/>• 040000 tree src/"]:::tree
    T_Src["Sub-Tree src/ (7e8f9a0...)<br/>• 100644 blob app.py<br/>• 100755 blob run.sh"]:::tree

    B_Readme["Blob (d67046...)<br/>'# My Project'"]:::blob
    B_App["Blob (f1e2d3...)<br/>'import sys...'"]:::blob
    B_Run["Blob (5d6e7f...)<br/>'#!/bin/bash...'"]:::blob

    C --> T_Root
    T_Root -->|100644 README.md| B_Readme
    T_Root -->|040000 src/| T_Src
    T_Src -->|100644 app.py| B_App
    T_Src -->|100755 run.sh| B_Run
```

---

### Diagram 4: What Actually Happens During a New Commit (Immutability)
Git **never overwrites** old objects. Modifying 1 line in `app.py` creates a brand-new blob and new parent trees, while unchanged blobs are cleanly reused:

```mermaid
flowchart TD
    classDef commit fill:#581c87,stroke:#c084fc,stroke-width:2px,color:#fff;
    classDef tree fill:#1e3a8a,stroke:#93c5fd,stroke-width:2px,color:#fff;
    classDef blob fill:#064e3b,stroke:#6ee7b7,stroke-width:2px,color:#fff;
    classDef ref fill:#831843,stroke:#f472b6,stroke-width:2px,color:#fff;

    subgraph Commit1 ["Commit 1 (Past)"]
        C1["Commit C1 (SHA: a1b2...)"]:::commit
        T1_Root["Root Tree T1"]:::tree
        T1_Src["Sub-Tree src/ (v1)"]:::tree
        B_App_v1["Blob: app.py (v1)"]:::blob
        B_Readme["Blob: README.md (unchanged)"]:::blob
        
        C1 --> T1_Root
        T1_Root --> B_Readme
        T1_Root --> T1_Src
        T1_Src --> B_App_v1
    end

    subgraph Commit2 ["Commit 2 (New Commit after editing app.py)"]
        C2["Commit C2 (SHA: e4f5...)"]:::commit
        T2_Root["Root Tree T2 (New SHA)"]:::tree
        T2_Src["Sub-Tree src/ (New SHA)"]:::tree
        B_App_v2["Blob: app.py (v2 - New SHA)"]:::blob

        C2 -->|parent pointer| C1
        C2 --> T2_Root
        T2_Root -.->|Reuses unchanged pointer| B_Readme
        T2_Root --> T2_Src
        T2_Src --> B_App_v2
    end

    HEAD["HEAD -> refs/heads/main"]:::ref --> C2
```

---

## 3. Session Diagnostics & Checkpoint Insights

> [!question] Checkpoint 1: Identical content across different folders
> **Question:** If `src/main.py` and `backup/old_main.py` have identical code, what is stored in `.git/objects/`?
> - **Misconception:** Two separate blobs are stored because the paths and filenames differ.
> - **Mental Model Repair:** Blobs store raw byte payloads only. Filenames exist strictly inside Tree objects. Git stores **only one blob**.

> [!question] Checkpoint 2: What happens on a new commit?
> **Question:** When editing 1 line in `src/app.py` and committing, what is created?
> - **Misconception:** The existing commit object is modified in-place with a diff.
> - **Mental Model Repair:** Git is strictly **append-only and immutable**. Because an object's ID is the hash of its content, altering any byte changes its hash. Git writes **1 new blob**, **new parent trees**, and **1 new commit object** pointing back to the previous commit.

---

## 4. Spaced Repetition Flashcards

### Basic Concept Cards
What does a Git Blob object store? #card
Only the raw byte contents of a file. It does NOT store filenames, directory paths, or file permissions.
<!--ID: 1727800000001-->

Where are filenames and directory permissions stored in Git's object model? #card
Inside Tree objects. A Tree maps (mode, name) pairs to Blob and sub-Tree hashes.
<!--ID: 1727800000002-->

What are the four fundamental object types in Git? #card
1. **Blob**: Raw file contents
2. **Tree**: Directory listing (names, modes, object hashes)
3. **Commit**: Snapshot pointer to root tree + parent commit(s) + author/message metadata
4. **Tag**: Annotated named reference pointing to an object
<!--ID: 1727800000003-->

Why does Git never modify an existing object in `.git/objects/` in-place? #card
Because Git is a content-addressable filesystem. An object's filename is the cryptographic hash of its exact bytes. Any modification produces a brand-new hash (a new object file).
<!--ID: 1727800000004-->

What actually is a Git branch under the hood? #card
A plain 41-byte text file located at `.git/refs/heads/<branch-name>` containing the SHA hash of the latest commit on that branch.
<!--ID: 1727800000005-->

What does a Git Commit object point to to represent the repository state? #card
It points directly to a single **Root Tree object**, which represents the complete snapshot of the project at that moment in time.
<!--ID: 1727800000006-->

### Cloze Deletion Cards
Git is not a diff tracker; it is a ==content-addressable== filesystem that stores a directed acyclic graph of immutable ==snapshots==. #card
<!--ID: 1727800000007-->

When 100 identical files exist across different directories in a Git repository, Git creates exactly ==one== blob object in `.git/objects/`. #card
<!--ID: 1727800000008-->

A Git commit's parent pointer creates a ==directed acyclic graph (DAG)== where history can only grow forward because a commit's hash depends on its ==parent's hash==. #card
<!--ID: 1727800000009-->

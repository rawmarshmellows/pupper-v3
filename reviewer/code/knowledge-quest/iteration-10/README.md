# Knowledge Quest -- Iteration 10

## How to Run

```bash
cd reviewer/code/knowledge-quest/iteration-10
cp ../.env.production .env
NOTES_PATH=/path/to/your/notes docker compose up --build -d
```

Then open http://localhost:3000 in your browser.

## What Changed from Iteration 9

1. **Class system removed** -- Just enter a name and start playing
2. **Stats/dice/HP/MP removed** -- No more d20 rolls, stat allocation, or resource management
3. **Evolving title system** -- Title evolves from Newcomer to Grandmaster based on mastery
4. **Streak + combo system** -- Consecutive correct answers build streaks; quick answers build combos
5. **20 achievements** -- Unlockable milestones for streaks, mastery, exploration, and more
6. **6 knowledge collections** -- Complete sets of related topics (Circuit Fundamentals, Signal Path, etc.)
7. **Daily challenges** -- One question per day for bonus achievements
8. **Replay Tutorial button** -- Added to help panel
9. **First encounter scaffold** -- Brief guidance on first real encounter
10. **Save migration** -- Old saves with class system are automatically migrated

## Teardown

```bash
docker compose down -v
```

# AI Agent Architectural Boundaries

**CRITICAL INSTRUCTION FOR ALL AI CODING ASSISTANTS OPERATING IN THIS REPOSITORY:**

This repository strictly enforces a monorepo interface boundary to prevent Git merge conflicts between the Frontend and Backend engineering teams. You must silently check the current Git branch before writing any code.

1. **If the active Git branch is `backend-dev`**: 
   - You are acting as the Backend Lead Assistant.
   - You are **STRICTLY FORBIDDEN** from modifying, creating, or deleting any files inside the `/frontend` directory. 
   - Focus exclusively on `/backend`, ML models, and API endpoints.

2. **If the active Git branch is `frontend-dev`**:
   - You are acting as the Frontend Lead Assistant.
   - You are **STRICTLY FORBIDDEN** from modifying, creating, or deleting any files inside the `/backend` directory.
   - Focus exclusively on React, Tailwind, Leaflet, and UI components in `/frontend`.

Failure to obey these boundaries will result in catastrophic Git merge conflicts. Obey the branch scope unconditionally.

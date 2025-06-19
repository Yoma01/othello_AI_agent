Designed and implemented a time-bounded, competitive AI agent for Duo-Othello, a variant of Reversi game. The agent was built to autonomously select optimal moves in real-time adversarial settings against both random and minimax-based opponents under strict performance and format constraints.

- **Minimax with Adaptive Depth:** Implemented a minimax search algorithm with dynamic depth adjustment based on remaining time, ensuring real-time responsiveness and strategic foresight under time-critical conditions.

- **Strategic Evaluation Heuristics:** Designed and integrated domain-specific heuristics including stability, mobility, corner capturing, and disk differential to guide the evaluation of non-terminal game states and maximize long-term advantage.

- **Time Management Strategy:** Integrated CPU time tracking and budgeting across multiple turns, optimizing move quality while avoiding timeouts. Designed fallback strategies for fast approximation under low time (<0.05s)

- **Move Validation and Legal Action Generation:** Efficiently generated all valid moves according to extended flipping rules across all directions, enabling fast pruning and accurate simulations.

The agent consistently outperformed both random and minimax-based baseline opponents across 20 evaluation games, demonstrating strong performance regardless of play order. This project showcases proficiency in adversarial AI, heuristic-driven decision-making, and real-time strategy under tight constraints skills directly applicable to game AI, autonomous agents, and general-purpose planning systems.

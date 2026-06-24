# Use pnpm instead of bun or npm

In this project, we prefer using `pnpm` for package management because:
1. It is faster and more disk-efficient than `npm`.
2. It handles monorepo structures (workspaces) much better.
3. It has a stricter dependency resolution than `bun` for production environments.

If you need to install a new package, use:
```bash
pnpm add <package-name>
```

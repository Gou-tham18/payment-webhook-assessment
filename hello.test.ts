// Hello-world check for the Node and TypeScript environment.
//
// Run from the repo root after installing the tools:
//
//     npm install --save-dev vitest typescript
//     npx vitest run

import { describe, expect, it } from "vitest";

describe("hello world", () => {
  it("runs a typed test", () => {
    const greeting: string = "hello" + " " + "world";
    expect(greeting).toBe("hello world");
  });
});

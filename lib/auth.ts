import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";
import { prisma } from "./db";

const isPostgres = process.env.DATABASE_URL?.startsWith("postgres");

export const auth = betterAuth({
  database: prismaAdapter(prisma, {
    provider: isPostgres ? "postgresql" : "sqlite",
  }),
  emailAndPassword: {
    enabled: true,
    autoSignIn: true
  }
});

const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  console.log("Testing connection to Neon PostgreSQL...");
  const rawResult = await prisma.$queryRaw`SELECT current_database(), current_user, version(), now()`;
  console.log("Database info:", rawResult);

  const userCount = await prisma.user.count();
  console.log("Current user count in Neon DB:", userCount);

  // Test creating a temporary test record and deleting it
  const testEmail = `test-${Date.now()}@aegis-ci.local`;
  const createdUser = await prisma.user.create({
    data: {
      name: "Neon Health Check",
      email: testEmail
    }
  });
  console.log("Successfully created test user in Neon DB:", createdUser.id, createdUser.email);

  await prisma.user.delete({
    where: { id: createdUser.id }
  });
  console.log("Successfully verified and cleaned up test user in Neon DB.");
  console.log("ALL NEON DATABASE TESTS PASSED SUCCESSFULLY!");
}

main()
  .catch((e) => {
    console.error("Database test failed:", e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });

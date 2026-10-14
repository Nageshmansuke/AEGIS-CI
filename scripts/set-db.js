const fs = require('fs');
const path = require('path');

const target = process.argv[2]; // 'sqlite' or 'postgresql'

if (!target || !['sqlite', 'postgresql'].includes(target)) {
  console.error("Usage: node scripts/set-db.js <sqlite|postgresql>");
  process.exit(1);
}

const schemaPath = path.join(__dirname, '..', 'prisma', 'schema.prisma');
let schema = fs.readFileSync(schemaPath, 'utf8');

const regex = /datasource db \{[\s\S]*?provider\s*=\s*"[^"]+"/;
schema = schema.replace(regex, `datasource db {\n  provider = "${target}"`);

fs.writeFileSync(schemaPath, schema, 'utf8');
console.log(`[OK] Prisma schema datasource updated to: provider = "${target}"`);

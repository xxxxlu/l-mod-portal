/**
 * L-MOD Vault - Email Template Preview Generator
 * Generates public/email_preview.html for instant in-browser inspection
 */

import { renderOtpEmailHtml } from '../functions/api/v1/auth/_crypto.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const previewHtml = renderOtpEmailHtml({
  code: '892106',
  purpose: 'login',
  email: 'nightcity_player@lmod.gg',
  options: {
    brandName: 'L-MOD Vault',
    brandUrl: 'https://lmod-vault.pages.dev',
    primaryColor: '#a855f7',
    footerNote: '全球单机游戏模组与避坑智库 · L-MOD 核心安全团队'
  }
});

const outputPath = path.resolve(__dirname, '../public/email_preview.html');
fs.writeFileSync(outputPath, previewHtml, 'utf-8');
console.log('✅ Generated email template preview at:', outputPath);

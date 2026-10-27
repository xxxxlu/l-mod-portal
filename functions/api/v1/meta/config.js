/**
 * Cloudflare Pages Function: /api/v1/meta/config
 * Global metadata, supported languages & feature flags
 */

export async function onRequestGet() {
  const config = {
    version: '2.1.0',
    api_revision: '20261027-v1',
    supported_locales: [
      { code: 'zh-CN', label: '简体中文', flag: '🇨🇳' },
      { code: 'zh-TW', label: '繁體中文', flag: '🇹🇼' },
      { code: 'en', label: 'English', flag: '🇺🇸' },
      { code: 'ja', label: '日本語', flag: '🇯🇵' },
      { code: 'ko', label: '한국어', flag: '🇰🇷' },
      { code: 'ru', label: 'Русский', flag: '🇷🇺' },
      { code: 'de', label: 'Deutsch', flag: '🇩🇪' },
      { code: 'es', label: 'Español', flag: '🇪🇸' }
    ],
    features: {
      telemetry: true,
      async_commands: true,
      steam_auth: true,
      bat_downloader: true,
      ai_copilot: true
    },
    radar_legend: {
      green: { label: '完美适配', desc: '指令与主流Mod全量兼容当前Steam最新版本' },
      yellow: { label: '部分失效', desc: '脚本扩展(CET/F4SE/UE4SS)需等待更新或打降级补丁' },
      red: { label: '高危熔断', desc: '游戏底层引擎大改，开启指令或Mod可能导致坏档' }
    }
  };

  return new Response(JSON.stringify({
    code: 0,
    message: 'success',
    data: config
  }), {
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'public, max-age=3600, s-maxage=86400, stale-while-revalidate=604800'
    }
  });
}

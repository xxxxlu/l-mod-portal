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
    // 与雷达页、public/radar_status.json 的 v2 规则一致；雷达只比对 Steam 更新时间，没有实机测试
    radar_legend: {
      green: { label: '近期平稳', desc: 'Steam 近 14 天没有新版本；近 90 天内有更新的，修改器也不比游戏旧' },
      yellow: { label: '留意更新', desc: 'Steam 近 14 天有新版本，Mod/修改器可能要等适配；或近 90 天有更新而修改器比游戏旧' },
      red: { label: '先别更新', desc: 'Steam 近 14 天有新版本，且常用 Mod 框架按 exe 版本挂钩，可能要等作者发新版' },
      unchecked: { label: '未巡检', desc: '还没有巡检记录，或不在 Steam 上' }
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

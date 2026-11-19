// L-MOD Vault Offline Database (test fixture)
window.GAMES_DATA = [
  {
    "id": "cyberpunk-2077",
    "rank": 1,
    "title": "Cyberpunk 2077",
    "titles": {
      "en": "Cyberpunk 2077",
      "zh-CN": "赛博朋克 2077"
    },
    "steamAppId": 1091500,
    "verifiedPatch": "Patch 2.13",
    "hasTrainer": true,
    "compatibilityStatus": "green",
    "radarStatusText": "🟢 完美兼容实测通过",
    "steamBuildId": "26161058",
    "steamLastChecked": "2026-11-18T09:37:19.259944",
    "radarSummary": "旧文案",
    "radarRiskTitle": "旧标题",
    "radarRiskDesc": "旧描述"
  },
  {
    "id": "witcher-3",
    "rank": 3,
    "title": "The Witcher 3: Wild Hunt",
    "titles": {
      "en": "The Witcher 3: Wild Hunt",
      "zh-CN": "巫师 3：狂猎"
    },
    "steamAppId": 292030,
    "verifiedPatch": "v4.04",
    "hasTrainer": true,
    "compatibilityStatus": "yellow",
    "radarStatusText": "🟡 官方刚推新补丁·老L实测对齐中",
    "steamBuildId": "26238013",
    "latestSteamPatch": "Patch 5.01 is live!",
    "latestSteamPatchUrl": "https://store.steampowered.com/news/app/292030/view/2",
    "emergencyAlert": {
      "zh-CN": "旧预警",
      "en": "old alert"
    }
  },
  {
    "id": "baldurs-gate-3",
    "rank": 4,
    "title": "Baldur's Gate 3",
    "titles": {
      "en": "Baldur's Gate 3",
      "zh-CN": "博德之门 3"
    },
    "steamAppId": 1086940,
    "verifiedPatch": "Patch 7",
    "hasTrainer": true,
    "compatibilityStatus": "red",
    "radarStatusText": "🔴 坏档预警·暂缓更新",
    "latestSteamPatch": "Hotfix #36 Now Live!",
    "steamBuildId": "25605617",
    "emergencyAlert": {
      "zh-CN": "旧预警",
      "en": "old alert"
    }
  },
  {
    "id": "elden-ring",
    "rank": 5,
    "title": "Elden Ring",
    "titles": {
      "en": "Elden Ring",
      "zh-CN": "艾尔登法环"
    },
    "steamAppId": 1245620,
    "verifiedPatch": "v1.14",
    "hasTrainer": true,
    "compatibilityStatus": "green",
    "radarStatusText": "🟢 完美兼容实测通过",
    "steamBuildId": "25827938",
    "steamLastChecked": "2026-11-18T09:37:19.259944",
    "emergencyAlert": {
      "zh-CN": "上次的预警",
      "en": "previous alert"
    }
  },
  {
    "id": "skyrim-se",
    "rank": 6,
    "title": "The Elder Scrolls V: Skyrim Special Edition",
    "titles": {
      "en": "The Elder Scrolls V: Skyrim Special Edition",
      "zh-CN": "上古卷轴 5：天际重制版"
    },
    "steamAppId": 489830,
    "verifiedPatch": "v1.6.1170",
    "hasTrainer": true,
    "compatibilityStatus": "red",
    "radarReason": "recent-update-hooks",
    "steamBuildId": "24914197"
  },
  {
    "id": "palworld",
    "rank": 8,
    "title": "Palworld",
    "titles": {
      "en": "Palworld",
      "zh-CN": "幻兽帕鲁"
    },
    "steamAppId": 1623730,
    "verifiedPatch": "v0.3.x",
    "hasTrainer": true
  },
  {
    "id": "alan-wake-2",
    "rank": 53,
    "title": "Alan Wake 2",
    "titles": {
      "en": "Alan Wake 2",
      "zh-CN": "心灵杀手 2"
    },
    "steamAppId": 0,
    "verifiedPatch": "Epic",
    "hasTrainer": false,
    "compatibilityStatus": "green",
    "radarStatusText": "不该被改"
  }
];

window.GAMES_DATABASE = window.GAMES_DATA;

window.TRANSLATIONS_DATA = {
  "zh-CN": {
    "siteName": "L-MOD Vault"
  },
  "en": {
    "siteName": "L-MOD Vault"
  }
};

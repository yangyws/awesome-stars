#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動抓取 GitHub 標記星號儲存庫並產生結構化分類 README.md
具備高相容性 HTML 錨點跳轉與新專案多維度加權智慧自動分類
"""

import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime

# 確保 Windows 主控台標準輸出相容 UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

USERNAME = "yangyws"
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")

# 分類對照、專案自訂說明與豐富關鍵字庫
CATEGORY_DEFINITIONS = [
    {
        "id": "handheld-gaming-emulators",
        "name": "🎮 掌機遊戲、模擬器與硬體調校 (Handheld Gaming & Emulators)",
        "desc": "涵蓋 Android 掌機 (AYN Thor / Odin)、SteamOS、各主機開源模擬器、雙螢幕補丁與 CPU/GPU 頻率調校工具。",
        "subcategories": [
            {
                "id": "handheld-launchers",
                "name": "掌機系統與前端啟動器 (Launchers & Frontends)",
                "keywords": [
                    "launcher", "frontend", "romm", "daijishou", "retro", "station", 
                    "es-de", "emulationstation", "pegasus", "homemenu", "homebrew", 
                    "gamehub", "handheld launcher", "game launcher", "rom manager"
                ],
                "repos": {
                    "rommapp/romm": "美觀且功能強大的自託管 ROM 遊戲庫管理與串流遊玩系統",
                    "rommapp/argosy-launcher": "RomM 原生 Android 用戶端，支援行動裝置同步、安裝與啟動遊戲",
                    "TapiocaFox/Daijishou": "Daijishō 復古遊戲啟動器，整合遊戲庫與封面刮削",
                    "JoeCorrell/DualScreen-Launcher": "雙螢幕專用 Android 啟動器 APK 發布頁（適用雙螢幕掌機）",
                    "blacksheepmvp/mjolnir": "客製化雙螢幕 Android 桌面啟動器 (Mjolnir)",
                    "iisu-network/iiSU": "視覺導向的 Android 掌機專屬啟動器",
                    "inssekt/CocoonFE": "Cocoon 前端啟動器，針對掌機與模擬器打造",
                    "misobadev/neostation-frontend": "跨平台復古模擬遊戲前端系統 (Neostation)",
                    "AverageConsumer/R-Shop": "控制器優先的 Android 復古遊戲管理器，支援串接 RomM 與本地/網路來源",
                    "armada-os/armada": "類 SteamOS 風格的 ARM 架構掌機 Linux 發行版",
                    "wang1025475397/Pegasus_GameRomManager": "Pegasus 遊戲 ROM 管理工具，支援線上抓取遊戲媒體與封面資訊",
                    "retrohrai/Releases": "RetroHR 發布庫，掌機復古遊戲相關支援套件",
                    "JoeCorrell/wemu-release": "wemu 掌機模擬與啟動器發布版本"
                }
            },
            {
                "id": "emulators",
                "name": "開源模擬器專案 (Emulators)",
                "keywords": [
                    "emulator", "emulation", "ps4", "ps3", "ps2", "3ds", "cemu", "rpcs3", 
                    "drastic", "armsx", "citra", "yuzu", "ryujinx", "dolphin", "vita3k", 
                    "retroarch", "mame", "gameboy", "gba", "switch emulator", "nes", "snes"
                ],
                "repos": {
                    "shadps4-emu/shadPS4": "適用於 Windows、Linux、macOS 的 PlayStation 4 開源模擬器 (C++)",
                    "weihuoya/citra": "經典任天堂 3DS 開源模擬器 Android / PC 分支",
                    "azahar-emu/azahar": "基於 Citra 開發的新一代開源 3DS 模擬器專案",
                    "AzaharPlus/AzaharPlus": "Azahar 3DS 模擬器增強分支，提供更多進階特色功能",
                    "Medard22/Dolphin-MMJR2-VBI": "Dolphin MMJR2 分支，新增 VBI 跳過黑客修正與官方同步補丁",
                    "SapphireRhodonite/Cemu": "Wii U 模擬器 Cemu 之 Android 移植版本",
                    "SSimco/Cemu": "Wii U 模擬器 Cemu 之 Android 移植開源專案",
                    "R-YaTian/DraStic_rev_i18n": "NDS 模擬器 DraStic 繁中與在地化逆向修正版",
                    "ARMSX2/ARMSX2": "PlayStation 2 模擬器 ARM64 Android 移植專案",
                    "ARMSX2/ARMSX3": "RPCS3 (PS3 模擬器) 之 ARM64 Android 移植專案",
                    "rfandango/XenDroid": "XenDroid 模擬器相關核心與執行環境移植"
                }
            },
            {
                "id": "tweaks-and-mods",
                "name": "硬體調校、雙螢幕補丁與遊戲輔助 (Tweaks & Mods)",
                "keywords": [
                    "tweak", "mod", "patch", "dlss", "frequency", "pserver", "switch", 
                    "hekate", "atmosphere", "overclock", "thermal", "fps", "lossless-scaling", 
                    "texture", "cheats", "hd-texture", "60fps", "governor", "sysfs"
                ],
                "repos": {
                    "keiretrogaming/pulse": "Android 掌機 CPU/GPU 頻率調節工具（免 Root / PServer 調校）",
                    "stormpanda/megingiard": "Android 掌機效能與驅動增強輔助模組",
                    "magiobus/thortranslate": "AYN Thor 掌機專用螢幕即時 OCR 翻譯與解說工具",
                    "PerryKum/ImageOverlay": "Android 掌機全域邊框與螢幕遮罩覆蓋工具",
                    "samyost1/tmc-android": "AYN Thor 薩爾達傳說：不可思議的帽子 雙螢幕模組（下螢幕地圖/背包）",
                    "samyost1/zelda3-android": "薩爾達傳說：眾神的三角神力 Android 原生反編譯移植版",
                    "viik4/iisu-asset-tool": "跨平台遊戲封面與客製化啟動器資源處理工具",
                    "FrankBarretta/LSFG-Android": "Lossless Scaling 幀生成演算法之 Android 應用實驗專案",
                    "rakanki911/DLSS5-Swapper": "一鍵安裝、調節與還原遊戲中 DLSS / FSR / XeSS 檔案與 OptiScaler 支援",
                    "xXJSONDeruloXx/decky-dlss-enabler": "SteamOS / Steam Deck 之 DLSS Enabler 外掛補丁工具",
                    "TexturesGuide/ALBW_4K_Setup": "薩爾達傳說：眾神的三角神力 2 4K 高畫質材質包設定指南",
                    "TexturesGuide/MM3D_4K_SetupGuide": "薩爾達傳說：穆修拉的面具 3D 4K 材質套件設定指南",
                    "TexturesGuide/SM3DL_4K_SetupGuide": "超級瑪利歐 3D 大陸 4K 材質套件設定指南",
                    "TexturesGuide/OoT3D_4K_SetupGuide": "薩爾達傳說：時之笛 3D 4K 高解析度材質包設定指南",
                    "TwilitRealm/dusklight": "經典冒險遊戲 PC 與現代掌機移植專案",
                    "igawa6/dusklight": "Dusklight 移植專案之社群維護分支",
                    "huangqian8/SwitchScript": "任天堂 Switch 大氣層客製化引導整合包產生指令碼",
                    "easyworld/hekate": "任天堂 Switch 繁體/簡體中文圖形介面引導載入程式 (Hekate)"
                }
            },
            {
                "id": "windows-compatibility",
                "name": "Windows 轉譯與相容層 (Windows on ARM & Compatibility)",
                "keywords": [
                    "winlator", "compatibility", "wine", "box64", "box86", "fex", 
                    "proton", "gamenative", "hangover", "mobox", "directx", "vulkan", "dxvk"
                ],
                "repos": {
                    "WinNative-Emu/WinNative": "Android 平台上直接執行 Windows 遊戲之原生環境工具",
                    "utkarshdalal/GameNative": "Android 上原生執行 Steam、Epic、GOG 等 PC 遊戲的啟動與相容層",
                    "brunodev85/winlator": "經典 Android 執行 Windows (x86_64) 應用程式與 PC 遊戲之轉譯容器",
                    "Producdevity/gamehub-lite": "GameHub Lite 社群維護修改版，支援掌機遊戲啟動",
                    "The412Banner/BannerHub": "GameHub ReVanced 增強版，擴展 GOG、Epic 支援與介面自訂"
                }
            },
            {
                "id": "controllers-and-peripherals",
                "name": "控制器與遊戲輸入周邊 (Controllers & Peripherals)",
                "keywords": [
                    "controller", "gamepad", "joystick", "rp2040", "input", "remap", 
                    "dualsense", "steam controller", "arcade", "stick", "d-pad", "xinput", "hid"
                ],
                "repos": {
                    "ddeverill/SteamlessController": "讓 2026 Steam Controller 與各類手把在非 Steam 環境中完美對應支援",
                    "awalol/DS5Dongle": "將 Raspberry Pi Pico 2 W 轉為 DualSense 5 藍牙無線接收器",
                    "OpenStickCommunity/GP2040-CE": "基於 RP2040 的開源多平台低延遲搖桿/格鬥手把韌體",
                    "sezanzeb/input-remapper": "Linux / 掌機裝置按鍵映射與巨集客製化工具",
                    "SplitScreen-Me/splitscreenme-nucleus": "Nucleus Co-op 本地多人分割螢幕同樂多開管理工具"
                }
            }
        ]
    },
    {
        "id": "streaming-and-remote-control",
        "name": "📡 串流、遠端遙控與跨裝置協作 (Streaming & Remote Control)",
        "desc": "包含 Moonlight/Sunshine 高畫質低延遲串流、PlayStation/Xbox 遙控串流用戶端，以及 scrcpy、RustDesk 跨裝置遙控。",
        "subcategories": [
            {
                "id": "moonlight-and-sunshine",
                "name": "Moonlight & Sunshine 生態系",
                "keywords": ["moonlight", "sunshine", "gamestream", "nvstream", "geforce-stream"],
                "repos": {
                    "Axixi2233/Sunshine": "自託管遊戲串流伺服端 Sunshine 社群最佳化版本",
                    "Axixi2233/moonlight-qt": "Moonlight PC 端 (Windows/Mac/Linux) 增強自訂版",
                    "Axixi2233/moonlight-android": "Moonlight Android 端阿西西修改版（掌機觸控與效能優化）",
                    "moonlight-stream/moonlight-android": "Moonlight 官方 Android GameStream 串流用戶端",
                    "moonlight-stream/moonlight-qt": "Moonlight 官方 PC (Qt) GameStream 串流用戶端",
                    "moonlight-stream/moonlight-ios": "Moonlight 官方 iOS / Apple TV GameStream 串流用戶端"
                }
            },
            {
                "id": "console-and-cloud-streaming",
                "name": "PlayStation / Xbox / 雲端串流",
                "keywords": [
                    "peasyo", "xstreaming", "remote play", "remote-play", "psplay", "chiaki", 
                    "greenlight", "xbplay", "opennow", "cloud gaming", "geforce now", "alvr", "vr-stream"
                ],
                "repos": {
                    "Geocld/PeaSyo-rs": "高效能 Android PlayStation 遠端遊玩用戶端 (Rust 核心)",
                    "Geocld/PeaSyo": "次世代開源 Android PlayStation 遠端串流用戶端",
                    "Geocld/PeaSyo4Desk": "PlayStation 桌面端遠端遊玩用戶端 (PeaSyo Desktop)",
                    "Geocld/XStreaming": "開源 Xbox 遠端遊玩與雲端串流用戶端 (Android)",
                    "Geocld/XStreamingDesktop": "開源 Xbox 桌面端串流應用程式 (Electron / TypeScript)",
                    "streamingdv/PSPlay-Application-Hosting": "PXPlay / PSPlay 官方遠端串流發布庫",
                    "OpenCloudGaming/OpenNOW": "開源第三方 GeForce NOW 串流客戶端 (OpenNOW)",
                    "Steam-Headless/docker-steam-headless": "無頭 (Headless) Steam Docker 映像檔，支援 NVIDIA GPU 串流",
                    "alvr-org/ALVR": "透過 Wi-Fi 將 PC VR 遊戲無線串流至獨立 VR 頭戴顯示器 (如 Quest)"
                }
            },
            {
                "id": "remote-desktop-and-control",
                "name": "跨裝置控制與桌面協作 (Remote Desktop & Control)",
                "keywords": [
                    "remote desktop", "scrcpy", "rustdesk", "deskflow", "synergy", 
                    "barrier", "kvm", "rdp", "vnc", "anydesk", "teamviewer"
                ],
                "repos": {
                    "Genymobile/scrcpy": "透過 USB / TCP-IP 投射與控制 Android 裝置螢幕（低延遲、高解析度）",
                    "rustdesk/rustdesk": "開源全平台遠端桌面連線工具，支援自建伺服器",
                    "deskflow/deskflow": "在多台電腦之間共享一套鍵盤與滑鼠（Synergy/Barrier 開源繼承者）"
                }
            }
        ]
    },
    {
        "id": "ai-agents-and-llm-devtools",
        "name": "🤖 AI 代理、邊緣運算與開發輔助 (AI Agents & LLM DevTools)",
        "desc": "涵蓋自主 AI Agent 框架、Claude Code / Codex 擴展能力、邊緣裝置小模型推論與網頁/文件爬蟲解析。",
        "subcategories": [
            {
                "id": "ai-agents-and-harness",
                "name": "AI 代理與 Harness 框架 (Agents & Harness)",
                "keywords": [
                    "agent", "agents", "harness", "assistant", "bot", "claw", "openclaw", 
                    "autogen", "crewai", "langchain", "chatbot", "claude-code", "cursor", "codex", "mcp"
                ],
                "repos": {
                    "affaan-m/ECC": "AI Agent 執行環境效能最佳化系統，賦予 Claude Code / Cursor 技能與長效記憶",
                    "NousResearch/hermes-agent": "Nous Research 開源自主 AI 代理系統 (Hermes Agent)",
                    "NousResearch/hermes-plugin-backsearch": "Hermes Agent 外掛：提供時間切片歷史新聞搜尋與擷取",
                    "AstrBotDevs/AstrBot": "多平台社群軟體 (Discord/Telegram 等) AI 代理與 LLM 外掛框架",
                    "agenvoy/Agenvoy": "單一 Go 執行檔自託管 AI 代理，具備自我修復工具與沙盒測試能力",
                    "bytedance/UI-TARS-desktop": "多模態 GUI 視覺操控 AI 代理框架 (UI-TARS)",
                    "onyx-dot-app/onyx": "企業級開源 AI 知識庫檢索與多模型對話平台 (原 Danswer)",
                    "dongsheng123132/u-claw": "OpenClaw AI 助理離線免安裝整合環境",
                    "shengyu-meng/ClawLibrary": "2D 像素遊戲風格的 AI 代理控制中心與視覺化介面"
                }
            },
            {
                "id": "token-optimization-and-skills",
                "name": "Token 優化、程式碼圖譜與 Skills",
                "keywords": [
                    "token", "tokens", "codegraph", "prompt", "prompts", "skill", 
                    "skills", "diagram", "context", "compress", "compression"
                ],
                "repos": {
                    "colbymchenry/codegraph": "預先索引程式碼知識圖譜，為 Claude Code / AntiGravity 大幅節省 Token 與工具呼叫",
                    "headroomlabs-ai/headroom": "在工具輸出、日誌與 RAG 輸入前智慧壓縮內容，節省 20%~95% Token 消耗",
                    "JuliusBrussee/caveman": "極致精簡 Prompt Token 壓縮工具，降低 LLM 呼叫開銷",
                    "cathrynlavery/diagram-design": "針對 AI 編程助理打造的高質感自包含 HTML + SVG 架構圖設計指南",
                    "google/skills": "Google 官方產品與雲端技術之 Agent Skills 擴展庫",
                    "emilkowalski/skills": "專為設計師與工程師打造的高品質前端與動效 Skills 指南",
                    "voidful/hung-yi-lee-skill": "蒸餾李宏毅老師深度學習與 Karpathy LLM 概念之 Agent 技能模組",
                    "htdt/godogen": "利用 Claude Code / Codex 自主進行 Godot 與 Bevy 遊戲開發的 AI 系統",
                    "nexu-io/open-design": "AI 程式設計代理的 UI 設計與視覺規範外掛"
                }
            },
            {
                "id": "edge-ai-and-local-inference",
                "name": "邊緣 AI 與本地模型推論 (Edge AI & Local Inference)",
                "keywords": [
                    "mlx", "local", "edge", "tiny", "inference", "moe", "llama.cpp", 
                    "ollama", "vllm", "quantization", "gguf", "npu", "on-device", "coreml"
                ],
                "repos": {
                    "leonickson1/Swiftlet": "在 Apple 裝置上透過 SSD 串流專家權重執行 35B/80B MoE 模型的 Swift/Metal 執行階段",
                    "jundot/omlx": "支援連續批次處理 (Continuous Batching) 的 Apple Silicon 高速 LLM 推論伺服器",
                    "raullenchai/Rapid-MLX": "專為 Apple Silicon 打造的極速本地 AI 執行引擎",
                    "exo-explore/exo": "在多台日常裝置（Mac/PC/手機）之間分散協同執行前沿 AI 大模型",
                    "cactus-compute/needle": "專為微型裝置打造的 2-bit (8-29MB) 超輕量自動化基礎模型",
                    "Mininglamp-AI/Mano-P": "開源邊緣裝置視覺-語言-動作 (GUI-VLA) 操控模型",
                    "Edge0-AI/Edge0": "邊緣端 AI 自動化與推論架構專案",
                    "ornith-ai/Ornith-1": "輕量化多模態邊緣推論模型專案"
                }
            },
            {
                "id": "doc-scraping-and-intelligence",
                "name": "文件解析、RAG 與情資視覺化 (Doc Scraping & Intelligence)",
                "keywords": [
                    "scraper", "scraping", "crawler", "crawl", "document", "pdf", 
                    "ocr", "vision", "tutor", "monitor", "rag", "embedding", "vector", "osint", "3d-globe"
                ],
                "repos": {
                    "unclecode/crawl4ai": "專為 LLM 打造的高速開源網頁爬蟲與資訊萃取框架 (Crawl4AI)",
                    "microsoft/markitdown": "微軟開源多格式文件 (Office/PDF) 轉換為 Markdown 工具",
                    "docling-project/docling": "IBM 開源高精準度文件解析與 GenAI 資料就緒轉換工具",
                    "img2threejs/img2threejs": "將參考圖片轉為程序化、可動畫的 Three.js 3D 模型程式碼",
                    "roboflow/supervision": "現代電腦視覺工具庫，支援物件偵測、追蹤與標註視覺化",
                    "HKUDS/DeepTutor": "香港大學開源終身個人化 AI 家教輔導系統",
                    "koala73/worldmonitor": "即時全球地緣與情報監控儀表板 (WorldMonitor)",
                    "bilawalsidhu/gods-eye-view": "真實開源空間情報與 3D 地球衛星軌跡即時視覺化模擬器"
                }
            }
        ]
    },
    {
        "id": "system-utilities-and-iot",
        "name": "🛠️ 系統優化、桌面工具與嵌入式 (System Utilities & IoT)",
        "desc": "涵蓋 Windows / Mac 系統瘦身調校、StreamDeck/Logitech 桌面周邊輔助、以及 ESP32 物聯網韌體。",
        "subcategories": [
            {
                "id": "os-optimizer-and-debloat",
                "name": "作業系統優化與瘦身 (OS Optimizer & Debloat)",
                "keywords": [
                    "optimizer", "optimization", "debloat", "debloater", "cleaner", 
                    "cleanup", "privacy", "tweaker", "container", "sysprep", "windows-11"
                ],
                "repos": {
                    "itsfatduck/optimizerDuck": "免費開源 Windows 深度優化、隱私強化與系統清理工具",
                    "thedogecraft/sparkle": "精緻現代的 Windows 瘦身與系統加速應用程式",
                    "AdventDevInc/kudu": "跨平台 (Win/Mac/Linux) 開源垃圾清理、快取掃描與安全管理工具",
                    "builtbybel/FluentTweaker": "微軟風格 Fluent 介面之 Windows 深度調校輔助工具",
                    "apple/container": "Apple 官方開源用於 macOS 上建立與執行 Linux 容器的輕量工具"
                }
            },
            {
                "id": "productivity-tools",
                "name": "實用周邊與日常生產力工具 (Productivity Tools)",
                "keywords": [
                    "cable", "streamdeck", "stream-deck", "logi", "tiles", "line", 
                    "hfs", "shopee", "bark", "notification", "obtainium", "font", "clipboard", "widget"
                ],
                "repos": {
                    "darrylmorley/whatcable": "macOS 狀態列小工具，插上 USB-C 即時顯示該線材真實傳輸速率與充電規格",
                    "timothycrosley/streamdeck-ui": "Linux 系統相容之 Elgato Stream Deck 控制軟體",
                    "tjsky/logi-options-plus-mini": "輕量化羅技 Logi Options+ 背景自訂按鍵對應工具",
                    "zeuikli/line-cheater": "iOS LINE 本地備份對話搜尋、匯出與安全瘦身工具 (桌面/CLI)",
                    "rejetto/hfs": "新世代 HFS 輕量級本機網頁檔案伺服器 (HTTP File Server)",
                    "Finb/Bark": "開源 iOS 隱私即時推送通知工具 (Bark)",
                    "flxholle/QuickTiles": "Android 快速設定面板 (Quick Settings Tiles) 功能擴展工具",
                    "ImranR98/Obtainium": "直接從 GitHub / GitLab 來源直接檢查並更新 Android 開源 App",
                    "ButTaiwan/bpmfvs": "台灣注音符號字型字形變體規格 (Bopomofo IVS)",
                    "bashalarmistalt/decimen-optical-transfer": "光學資料安全單向傳輸與驗證工具",
                    "LobsterTrap/tank-os": "輕量嵌入式作業系統概念原型",
                    "wdzeng/shopee-coins-bot": "台灣蝦皮每日簽到與領取蝦幣自動化機器人"
                }
            },
            {
                "id": "embedded-and-iot",
                "name": "嵌入式硬體與韌體工具 (Embedded & IoT)",
                "keywords": [
                    "esp32", "esp8266", "firmware", "tasmota", "esptool", "iot", 
                    "arduino", "stm32", "raspberry", "micropython", "flasher"
                ],
                "repos": {
                    "arendst/Tasmota": "經典 ESP8266 與 ESP32 開源物聯網替代韌體 (支援 MQTT/Home Assistant)",
                    "espressif/esptool": "樂鑫官方 ESP8266 / ESP32 晶片序列埠燒錄與韌體管理工具"
                }
            }
        ]
    }
]


def fetch_starred_repos(username):
    token = os.environ.get("GITHUB_TOKEN")
    headers = {
        "User-Agent": "Awesome-Stars-Generator",
        "Accept": "application/vnd.github.v3+json"
    }
    if token:
        headers["Authorization"] = f"token {token}"

    all_repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/starred?per_page=100&page={page}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if not data:
                    break
                all_repos.extend(data)
                if len(data) < 100:
                    break
                page += 1
        except urllib.error.HTTPError as e:
            print(f"HTTP 錯誤: {e.code} - {e.reason}")
            break
        except Exception as e:
            print(f"抓取發生錯誤: {e}")
            break

    return all_repos


def classify_repo_automatically(repo, category_definitions):
    """
    依據新專案的 topics, name, description 計算加權分數，自動歸類至最合適的子分類
    """
    name = repo.get("name", "").lower()
    full_name = repo.get("full_name", "").lower()
    desc = (repo.get("description") or "").lower()
    topics = [t.lower() for t in repo.get("topics", [])]
    text_corpus = f"{name} {full_name} {desc} {' '.join(topics)}"

    best_subcat = None
    best_score = 0

    for cat in category_definitions:
        for subcat in cat["subcategories"]:
            score = 0
            keywords = subcat.get("keywords", [])
            for kw in keywords:
                kw_lower = kw.lower()
                # 1. 專案標籤 (Topics) 精確命中：權重最高 (+4)
                if kw_lower in topics:
                    score += 4
                # 2. 儲存庫名稱命中 (+3)
                if kw_lower in name or kw_lower in full_name:
                    score += 3
                # 3. 專案說明命中 (+2)
                if kw_lower in desc:
                    score += 2
                elif kw_lower in text_corpus:
                    score += 1

            if score > best_score:
                best_score = score
                best_subcat = (cat["id"], subcat["id"])

    # 若加權得分大於等於 2 分，視為顯著匹配
    if best_score >= 2:
        return best_subcat
    return None


def categorize_repos(repos):
    repo_map = {r["full_name"]: r for r in repos}
    classified = set()
    category_results = []

    # 1. 初始化結構與載入已知精選專案
    for cat in CATEGORY_DEFINITIONS:
        cat_data = {
            "id": cat["id"],
            "name": cat["name"],
            "desc": cat["desc"],
            "subcategories": []
        }
        for subcat in cat["subcategories"]:
            subcat_data = {
                "id": subcat["id"],
                "name": subcat["name"],
                "repos": []
            }
            for repo_name, custom_desc in subcat["repos"].items():
                if repo_name in repo_map:
                    r = repo_map[repo_name]
                    classified.add(repo_name)
                    subcat_data["repos"].append({
                        "full_name": repo_name,
                        "url": r["html_url"],
                        "language": r.get("language") or "無",
                        "stars": r.get("stargazers_count", 0),
                        "description": custom_desc
                    })
            cat_data["subcategories"].append(subcat_data)
        category_results.append(cat_data)

    # 2. 智慧自動判斷：針對未來新加入的 Starred 專案進行加權分類
    unclassified_repos = [r for r in repos if r["full_name"] not in classified]
    unresolved_repos = []

    for r in unclassified_repos:
        matched = classify_repo_automatically(r, CATEGORY_DEFINITIONS)
        if matched:
            target_cat_id, target_subcat_id = matched
            placed = False
            for cat_data in category_results:
                if cat_data["id"] == target_cat_id:
                    for subcat_data in cat_data["subcategories"]:
                        if subcat_data["id"] == target_subcat_id:
                            desc = r.get("description") or "暫無描述"
                            subcat_data["repos"].append({
                                "full_name": r["full_name"],
                                "url": r["html_url"],
                                "language": r.get("language") or "無",
                                "stars": r.get("stargazers_count", 0),
                                "description": desc
                            })
                            classified.add(r["full_name"])
                            placed = True
                            break
                    if placed:
                        break
        else:
            unresolved_repos.append(r)

    # 3. 若完全無法判定（特徵詞完全未命中），放入獨立的最近新增區塊
    if unresolved_repos:
        misc_subcat = {
            "id": "recently-starred",
            "name": "✨ 最近新增收藏 (Recently Starred)",
            "repos": []
        }
        for r in unresolved_repos:
            desc = r.get("description") or "暫無描述"
            misc_subcat["repos"].append({
                "full_name": r["full_name"],
                "url": r["html_url"],
                "language": r.get("language") or "無",
                "stars": r.get("stargazers_count", 0),
                "description": desc
            })
        category_results[0]["subcategories"].insert(0, misc_subcat)

    return category_results


def generate_readme(category_results, total_count, username):
    now_str = datetime.now().strftime("%Y-%m-%d")
    lines = [
        f"# 🌟 {username} 的 GitHub 標記星號分類庫 (Awesome Stars)",
        "",
        f"[![Stars Count](https://img.shields.io/badge/Total%20Stars-{total_count}-blue?style=for-the-badge&logo=github)](https://github.com/{username}?tab=stars)",
        f"[![Last Updated](https://img.shields.io/badge/Last%20Updated-{now_str}-green?style=for-the-badge)](https://github.com/{username})",
        "[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)",
        "",
        f"> 本儲存庫為 **@{username}** 在 GitHub 上已標記星號（Starred）的優質開源專案全方位分類索引。",
        "> 內建多維度特徵演算法，新加星號自動智慧識別分類，並透過 GitHub Actions 定期自動排程更新。",
        "",
        "---",
        "",
        '<a id="toc"></a>',
        "## 📑 目錄導覽 (點擊可直接跳轉)",
        ""
    ]

    # 目錄摘要 (使用精準 HTML 錨點超連結)
    for cat in category_results:
        cat_total = sum(len(sub["repos"]) for sub in cat["subcategories"])
        lines.append(f"### 📂 [{cat['name']}](#{cat['id']}) ({cat_total})")
        for sub in cat["subcategories"]:
            lines.append(f"- [{sub['name']}](#{sub['id']}) `({len(sub['repos'])})`")
        lines.append("")

    lines.extend([
        "---",
        ""
    ])

    # 詳細清單
    for cat in category_results:
        lines.append(f'<a id="{cat["id"]}"></a>')
        lines.append(f"## {cat['name']}")
        lines.append(f"*{cat['desc']}*")
        lines.append("")

        for sub in cat["subcategories"]:
            lines.append(f'<a id="{sub["id"]}"></a>')
            lines.append(f"### 📌 {sub['name']}")
            lines.append("")
            lines.append("| 儲存庫名稱 | 主要語言 | 星星數 (★) | 專案定位與亮點特色 |")
            lines.append("| :--- | :---: | :---: | :--- |")

            for r in sub["repos"]:
                stars_formatted = f"{r['stars']:,}"
                desc_cleaned = r['description'].replace("|", "\|").replace("\n", " ").replace("\r", "")
                lines.append(f"| [**{r['full_name']}**]({r['url']}) | `{r['language']}` | {stars_formatted} | {desc_cleaned} |")

            lines.append("")
            lines.append("[⬆ 回到目錄導覽](#toc)")
            lines.append("")

        lines.append("---")
        lines.append("")

    lines.extend([
        '<a id="automation"></a>',
        "## ⚙️ 自動化同步機制",
        "",
        "本儲存庫透過 `.github/workflows/update-stars.yml` 設定 GitHub Actions：",
        "* **智慧自動歸類**：每次同步時，系統會自動分析新標記星號專案的 Topics 標籤、專案描述與名稱關鍵字，自動匹配到最適合的分類中。",
        "* **排程定時更新**：每日午夜定時觸發執行，抓取最新 Starred 清單。",
        "* **手動即時觸發**：支援在 GitHub Actions 頁面隨時手動點擊「Run workflow」即時同步。",
        "",
        "[⬆ 回到目錄導覽](#toc)",
        "",
        "---",
        "",
        '<a id="license"></a>',
        "## 📜 授權協議",
        "",
        "本專案架構採用 [MIT License](LICENSE) 授權開源。"
    ])

    return "\n".join(lines)


def main():
    print(f"🔍 正在抓取 @{USERNAME} 的星號儲存庫...")
    repos = fetch_starred_repos(USERNAME)
    if not repos:
        print("⚠️ 未能抓取到專案資料，請檢查網路連線或 API Rate Limit。")
        return

    print(f"✅ 成功抓取 {len(repos)} 個標記星號專案！正在進行結構化分類...")
    categorized = categorize_repos(repos)
    readme_content = generate_readme(categorized, len(repos), USERNAME)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"🎉 README.md 產生成功！路徑: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

<p align="center">
  <img src="./assets/banner.gif" alt="Mario Bros Industrial Factory Banner" width="100%" />
</p>

<h1 align="center">Hi there, I'm Sirojul Kahfi 👋</h1>

<p align="center">
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&duration=3000&pause=1000&color=00F0FF&center=true&vCenter=true&width=650&lines=Software+Developer+%7C+Industrial+Automation;Next.js+%7C+TypeScript+%7C+React+%7C+Node.js;PLC+Programmer+(Mitsubishi+%26+Omron);SCADA+%7C+IIoT+%7C+IT%2FOT+Convergence" alt="Typing SVG" />
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Focus-IT%20%2F%20OT%20Convergence-00f0ff?style=for-the-badge&labelColor=0d1117" alt="Focus" />
  <img src="https://img.shields.io/badge/Robotics-Industrial%20Systems-ffaa00?style=for-the-badge&labelColor=0d1117" alt="Robotics" />
  <img src="https://img.shields.io/badge/Stack-Next.js%20%7C%20PLC%20%7C%20SCADA-00ff88?style=for-the-badge&labelColor=0d1117" alt="Stack" />
</p>

---

## 🏭 INDUSTRIAL FACTORY SCENE (Animated SVG)

<p align="center">
  <img src="./assets/industrial_mario_bros_scene.svg" alt="Mario Bros Industrial Factory — Animated SVG Scene" width="100%" />
</p>

---

## ⚡ PLC LADDER DIAGRAM (LD) — SISTEM KONTROL PROFIL

<p align="center">
  <img src="./assets/ladder_diagram.svg" alt="PLC Ladder Diagram — Tentang Saya & Tech Stack" width="100%" />
</p>

```text
+=================================================================================================+
| PROGRAM : SIROJUL_KAHFI.LD   | CPU: MITSUBISHI Q-SERIES / OMRON SYSMAC | MODE: RUN (M8000=ON) |
| STATUS  : SYSTEM OPERATIONAL | SCAN TIME: 0.24 ms                      | STEP: 0000 -> END    |
+=================================================================================================+

+--[ NETWORK 001 : TENTANG SAYA (ABOUT ME CORE PROFILE) ]----------------------------------------+
|                                                                                                  |
|  // 1.1: CORE IDENTITY & FOCUS                                                                   |
|  |--[ SM400 ]---+--[ MOV "Sirojul Kahfi - Software Dev & Industrial Automation"        D000 ]---|
|  | (Always ON)  +--[ MOV "Fokus: Web App Modern & Sistem Otomasi / Kontrol Mesin PLC"  D001 ]---|
|                                                                                                  |
|  // 1.2: WEB & SOFTWARE DEVELOPMENT                                                              |
|  |--[ M100 ]----+--[ MOV "Frontend: Next.js (App Router, SSR/SSG), React.js"           D110 ]---|
|  | (Web Core)   |--[ MOV "Styling & Logic: Tailwind CSS, TypeScript, JavaScript"       D111 ]---|
|  |              |--[ MOV "Backend & Data: Node.js, PostgreSQL, Prisma ORM, REST API"   D112 ]---|
|  |              +--[ OUT Y010_WEB_DEVELOPMENT_ACTIVE                                       ]---(Y010)
|                                                                                                  |
|  // 1.3: INDUSTRIAL AUTOMATION & ROBOTICS                                                        |
|  |--[ M200 ]----+--[ MOV "Mitsubishi PLC: FX Series, Q Series (GX Works2 / GX Works3)" D120 ]---|
|  | (Auto Core)  |--[ MOV "Omron PLC: CP Series, CJ Series (CX-Programmer, Sysmac)"     D121 ]---|
|  |              |--[ MOV "Bahasa: Ladder Diagram (LD) & Structured Text (ST)"          D122 ]---|
|  |              |--[ MOV "Robotics: Pemrograman Kontrol Mesin & Robotika Industri"     D123 ]---|
|  |              +--[ OUT Y020_INDUSTRIAL_AUTOMATION_ACTIVE                                 ]---(Y020)
|                                                                                                  |
|  // 1.4: IT / OT CONVERGENCE & SCADA INTEGRATION                                                |
|  +--[ M300 ]----+--[ MOV "Protokol: Modbus RTU/TCP, Serial RS-232/RS-485, MQTT"        D130 ]---|
|    (Bridge)     |--[ MOV "Akuisisi: Data Mesin Industri Real-Time ke Web Cloud"        D131 ]---|
|                 |--[ MOV "Monitoring: HMI, SCADA Dashboard & IoT Cloud Analytics"      D132 ]---|
|                 +--[ CALL P_IT_OT_CONVERGENCE                                          K1   ]---(Y030)
+--------------------------------------------------------------------------------------------------+

+--[ NETWORK 002 : TECH STACK & KEAHLIAN (DATA REGISTERS BMOV) ]---------------------------------+
|                                                                                                  |
|  // 2.1: WEB & CLOUD SOFTWARE ENGINEERING                                                        |
|  |--[ X001_WEB ]---+--[ BMOV D200_FE  "Next.js | React | TypeScript | Tailwind"       K4 ]-----|
|  | (Web Trig)      |--[ BMOV D204_BE  "Node.js | PostgreSQL | Prisma ORM | REST API"  K4 ]-----|
|  |                 |--[ BMOV D208_DEV "Git | GitHub | Docker Environment"             K3 ]-----|
|  |                 +--[ OUT Y100_FULLSTACK_WEB_STACK_ACTIVE                               ]---(Y100)
|                                                                                                  |
|  // 2.2: INDUSTRIAL AUTOMATION & ROBOTICS HARDWARE                                               |
|  |--[ X002_AUTO ]--+--[ BMOV D300_PLC "Mitsubishi FX/Q | Omron CP/CJ | Sysmac Studio" K3 ]-----|
|  | (Auto Trig)     |--[ BMOV D303_LAN "Ladder Diagram (LD) | Structured Text (ST)"    K2 ]-----|
|  |                 |--[ BMOV D305_COM "Modbus RTU/TCP | Serial RS-485/232 | MQTT"     K3 ]-----|
|  |                 |--[ BMOV D308_IOT "HMI / SCADA | IT/OT Realtime Web Dashboard"    K3 ]-----|
|  |                 +--[ OUT Y200_INDUSTRIAL_SYSTEMS_ACTIVE                                 ]---(Y200)
|                                                                                                  |
|  // 2.3: REAL-TIME ACTIVITY & TELEMETRY MONITOR                                                  |
|  |--[ M8013 ]--------[ PID_FEEDBACK "GITHUB_STREAK_SYNC" D500                         K10 ]---(Y300)
|                                                                                                  |
|  // 2.4: COMMUNICATION BUS & CONTACT ROUTINE                                                     |
|  +--[ X003_PING ]--+--[ COM_OPEN "LinkedIn"  "id.linkedin.com/in/sirojul-kahfi"           ]-----|
|    (Connect)       |--[ COM_OPEN "Outlook"   "sirojulkahfi@outlook.com"                   ]-----|
|                    |--[ COM_OPEN "GitHub"    "github.com/sirojulkahfi"                    ]-----|
|                    +--[ FEND ]---(END)
+--------------------------------------------------------------------------------------------------+
```

---

## 🖥️ HMI / SCADA DASHBOARD (PERIPHERAL OUTPUTS)

> Output visual dari coil PLC (`Y010_WEB`, `Y020_PLC`, `Y300_TELEMETRY`, `Y_COM`) yang terhubung ke dashboard monitoring:

#### 🌐 Web Engineering Peripherals `[COIL Y010 / Y100]`
<p align="left">
  <img src="https://skillicons.dev/icons?i=nextjs,react,ts,js,nodejs,postgres,prisma,tailwind,git,docker" />
</p>

#### 🏭 Industrial Automation & PLC Hardware `[COIL Y020 / Y200]`
<p align="left">
  <img src="https://img.shields.io/badge/Mitsubishi_Electric-E60012?style=for-the-badge&logo=mitsubishi&logoColor=white" />
  <img src="https://img.shields.io/badge/Omron_Automation-005BAC?style=for-the-badge&logoColor=white" />
  <img src="https://img.shields.io/badge/Industrial_Robotics-FF6600?style=for-the-badge&logoColor=white" />
  <img src="https://img.shields.io/badge/Modbus_%26_Serial-4B0082?style=for-the-badge&logoColor=white" />
  <img src="https://img.shields.io/badge/SCADA_%26_IIoT-008080?style=for-the-badge&logoColor=white" />
</p>

#### 📈 Real-Time Development Streak `[COIL Y300]`
<p align="center">
  <img src="https://github-readme-streak-stats.herokuapp.com/?user=sirojulkahfi&theme=tokyonight&background=0d1117&ring=00f0ff&fire=00f0ff&currStreakNum=00f0ff" alt="Sirojul's GitHub Streak" />
</p>

#### 📬 Communication Port Interfaces `[COIL Y_COM]`
<p align="left">
  <a href="https://id.linkedin.com/in/sirojul-kahfi-29a170224">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  &nbsp;
  <a href="mailto:sirojulkahfi@outlook.com">
    <img src="https://img.shields.io/badge/Microsoft_Outlook-0078D4?style=for-the-badge&logo=microsoftoutlook&logoColor=white" alt="Outlook" />
  </a>
  &nbsp;
  <a href="https://github.com/sirojulkahfi">
    <img src="https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
  </a>
</p>

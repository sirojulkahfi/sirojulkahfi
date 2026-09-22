"""
Generate an authentic, high-resolution SVG Ladder Diagram (LD) for GitHub profile.
Features:
- Industrial dark theme matching GitHub Dark (#0d1117)
- Energized green power rails (L1/N)
- IEC 61131-3 & Mitsubishi/Omron style contacts (SM400 Always ON, X inputs, M relays)
- Function instruction blocks (MOV, BMOV, CALL, MC_ROBOT)
- Output coils with status glow (Y000..Y030)
- Full "Tentang Saya" and "Tech Stack" mapped directly into PLC rungs and data registers
"""

def generate_ladder_svg(output_path="assets/ladder_diagram.svg"):
    width = 960
    height = 680

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">')
    svg.append('<defs>')
    # Gradients & Glow Filters
    svg.append('''
      <linearGradient id="railGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#00FF88"/>
        <stop offset="100%" stop-color="#00DD77"/>
      </linearGradient>
      <linearGradient id="boxGrad" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#161b22"/>
        <stop offset="100%" stop-color="#0d1117"/>
      </linearGradient>
      <filter id="greenGlow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="3" result="blur"/>
        <feMerge>
          <feMergeNode in="blur"/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>
      </filter>
      <filter id="cyanGlow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur stdDeviation="3" result="blur"/>
        <feMerge>
          <feMergeNode in="blur"/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>
      </filter>
      <style>
        .mono { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace; }
        .rail-lbl { fill: #00FF88; font-size: 11px; font-weight: bold; letter-spacing: 1px; }
        .rail-neg { fill: #6e7681; font-size: 11px; font-weight: bold; letter-spacing: 1px; }
        .rung-hdr { fill: #58a6ff; font-size: 12px; font-weight: bold; }
        .rung-sub { fill: #8b949e; font-size: 10px; }
        .inst-title { fill: #00f0ff; font-size: 11px; font-weight: bold; }
        .inst-param { fill: #f0883e; font-size: 10px; font-weight: bold; }
        .inst-val { fill: #e6edf3; font-size: 10px; }
        .inst-reg { fill: #7ee787; font-size: 10px; font-weight: bold; }
        .contact-lbl { fill: #7ee787; font-size: 11px; font-weight: bold; text-anchor: middle; }
        .contact-tag { fill: #8b949e; font-size: 9px; text-anchor: middle; }
        .coil-lbl { fill: #00ff88; font-size: 11px; font-weight: bold; text-anchor: middle; }
        .coil-tag { fill: #8b949e; font-size: 9px; text-anchor: middle; }
        .wire { stroke: #00ff88; stroke-width: 2; fill: none; }
        .wire-off { stroke: #30363d; stroke-width: 2; fill: none; }
        .wire-blue { stroke: #388bfd; stroke-width: 2; fill: none; }
      </style>
    ''')
    svg.append('</defs>')

    # Background Card
    svg.append(f'<rect width="{width}" height="{height}" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>')

    # PLC Top Status Bar
    svg.append('<rect x="15" y="15" width="930" height="36" rx="6" fill="#161b22" stroke="#30363d" stroke-width="1"/>')
    svg.append('<circle cx="35" cy="33" r="6" fill="#00ff88" filter="url(#greenGlow)"/>')
    svg.append('<text x="50" y="37" class="mono" fill="#00ff88" font-size="12px" font-weight="bold">PLC RUN</text>')
    svg.append('<text x="130" y="37" class="mono" fill="#8b949e" font-size="11px">CPU: <tspan fill="#e6edf3" font-weight="bold">MITSUBISHI Q-SERIES / OMRON SYSMAC</tspan></text>')
    svg.append('<text x="490" y="37" class="mono" fill="#8b949e" font-size="11px">SCAN: <tspan fill="#e6edf3">0.24ms</tspan></text>')
    svg.append('<text x="600" y="37" class="mono" fill="#8b949e" font-size="11px">PROG: <tspan fill="#58a6ff" font-weight="bold">SIROJUL_KAHFI.LD</tspan></text>')
    svg.append('<circle cx="890" cy="33" r="4" fill="#00f0ff" filter="url(#cyanGlow)"/>')
    svg.append('<text x="902" y="37" class="mono" fill="#00f0ff" font-size="11px" font-weight="bold">ONLINE</text>')

    # Power Rails Coordinates
    l_rail_x = 55
    r_rail_x = 905
    y_top = 70
    y_bot = height - 30

    # Left Power Rail (L1 - 24VDC Energized Green)
    svg.append(f'<line x1="{l_rail_x}" y1="{y_top}" x2="{l_rail_x}" y2="{y_bot}" stroke="url(#railGrad)" stroke-width="4" filter="url(#greenGlow)"/>')
    svg.append(f'<text x="{l_rail_x}" y="{y_top - 8}" class="mono rail-lbl" text-anchor="middle">L1 (+24V)</text>')

    # Right Power Rail (N - 0V Return)
    svg.append(f'<line x1="{r_rail_x}" y1="{y_top}" x2="{r_rail_x}" y2="{y_bot}" stroke="#30363d" stroke-width="4"/>')
    svg.append(f'<text x="{r_rail_x}" y="{y_top - 8}" class="mono rail-neg" text-anchor="middle">N (0V / COM)</text>')

    # -------------------------------------------------------------
    # RUNG 000 : SYSTEM INITIATION (ABOUT ME HEADER)
    # -------------------------------------------------------------
    r0_y = 110
    svg.append(f'<text x="68" y="{r0_y - 18}" class="mono rung-hdr">// RUNG 000 : PROFIL PENGEMBANG &amp; INVENTORI SISTEM</text>')
    
    # Wire from Left Rail to Contact
    svg.append(f'<line x1="{l_rail_x}" y1="{r0_y}" x2="105" y2="{r0_y}" class="wire"/>')
    
    # Contact SM400 (Always ON)
    # [ | ]
    svg.append('<line x1="105" y1="98" x2="105" y2="122" stroke="#00ff88" stroke-width="3"/>')
    svg.append('<line x1="120" y1="98" x2="120" y2="122" stroke="#00ff88" stroke-width="3"/>')
    svg.append('<line x1="105" y1="110" x2="120" y2="110" stroke="#00ff88" stroke-width="1.5" stroke-dasharray="2,2"/>')
    svg.append(f'<text x="112" y="93" class="mono contact-lbl">SM400</text>')
    svg.append(f'<text x="112" y="134" class="mono contact-tag">(Always ON)</text>')
    
    # Wire from Contact to Instruction Box
    svg.append(f'<line x1="120" y1="{r0_y}" x2="175" y2="{r0_y}" class="wire"/>')

    # Function Block 1: MOV "Sirojul Kahfi"
    svg.append(f'<rect x="175" y="{r0_y - 32}" width="570" height="64" rx="5" fill="url(#boxGrad)" stroke="#388bfd" stroke-width="1.5"/>')
    svg.append(f'<rect x="175" y="{r0_y - 32}" width="570" height="20" rx="5" fill="#1f6feb" opacity="0.3"/>')
    svg.append(f'<text x="185" y="{r0_y - 18}" class="mono inst-title">MOV (16-Bit String Move)</text>')
    svg.append(f'<text x="185" y="{r0_y + 4}" class="mono inst-param">s : <tspan class="inst-val">"Sirojul Kahfi - Software Developer &amp; Industrial Automation Enthusiast"</tspan></text>')
    svg.append(f'<text x="185" y="{r0_y + 22}" class="mono inst-param">d : <tspan class="inst-reg">D000_DEVELOPER_CORE_PROFILE</tspan></text>')

    # Wire to Coil Y000
    svg.append(f'<line x1="745" y1="{r0_y}" x2="815" y2="{r0_y}" class="wire"/>')
    # Coil ( Y000 )
    svg.append(f'<path d="M 815 {r0_y-14} A 14 14 0 0 1 815 {r0_y+14}" stroke="#00ff88" stroke-width="2.5" fill="none"/>')
    svg.append(f'<path d="M 845 {r0_y-14} A 14 14 0 0 0 845 {r0_y+14}" stroke="#00ff88" stroke-width="2.5" fill="none"/>')
    svg.append(f'<text x="830" y="{r0_y + 4}" class="mono coil-lbl">Y000</text>')
    svg.append(f'<text x="830" y="{r0_y + 25}" class="mono coil-tag">(SYS_READY)</text>')
    svg.append(f'<line x1="845" y1="{r0_y}" x2="{r_rail_x}" y2="{r0_y}" class="wire-off"/>')

    # -------------------------------------------------------------
    # RUNG 001 : TENTANG SAYA - 3 PILAR UTAMA
    # -------------------------------------------------------------
    r1_y = 230
    svg.append(f'<text x="68" y="{r1_y - 30}" class="mono rung-hdr">// RUNG 001 : TENTANG SAYA (3 PILAR KEAHLIAN &amp; INTEGRASI)</text>')
    svg.append(f'<line x1="{l_rail_x}" y1="{r1_y}" x2="105" y2="{r1_y}" class="wire"/>')

    # Contact M100 (RUN_PROFILE)
    svg.append(f'<line x1="105" y1="{r1_y-12}" x2="105" y2="{r1_y+12}" stroke="#00ff88" stroke-width="3"/>')
    svg.append(f'<line x1="120" y1="{r1_y-12}" x2="120" y2="{r1_y+12}" stroke="#00ff88" stroke-width="3"/>')
    svg.append(f'<line x1="105" y1="{r1_y}" x2="120" y2="{r1_y}" stroke="#00ff88" stroke-width="1.5" stroke-dasharray="2,2"/>')
    svg.append(f'<text x="112" y="{r1_y - 16}" class="mono contact-lbl">M100</text>')
    svg.append(f'<text x="112" y="{r1_y + 24}" class="mono contact-tag">(PROFILE_EN)</text>')

    # Wire to vertical branch
    b_x = 150
    svg.append(f'<line x1="120" y1="{r1_y}" x2="{b_x}" y2="{r1_y}" class="wire"/>')
    
    # 3 Branches:
    # Branch 1: Web & Software Dev (y = 200)
    # Branch 2: Industrial Automation & Robotics (y = 280)
    # Branch 3: IT/OT Convergence (y = 360)
    y_b1 = 200
    y_b2 = 285
    y_b3 = 370

    # Vertical distribution bar
    svg.append(f'<line x1="{b_x}" y1="{y_b1}" x2="{b_x}" y2="{y_b3}" class="wire"/>')

    # --- BRANCH 1: WEB ---
    svg.append(f'<line x1="{b_x}" y1="{y_b1}" x2="175" y2="{y_b1}" class="wire"/>')
    svg.append(f'<rect x="175" y="{y_b1 - 25}" width="570" height="52" rx="5" fill="url(#boxGrad)" stroke="#388bfd" stroke-width="1.5"/>')
    svg.append(f'<text x="185" y="{y_b1 - 9}" class="mono inst-title">MOV [01: WEB &amp; SOFTWARE DEVELOPMENT]</text>')
    svg.append(f'<text x="185" y="{y_b1 + 7}" class="mono inst-param">s : <tspan class="inst-val">"Aplikasi Web Interaktif &amp; Scalable (Next.js, React, TypeScript, Tailwind)"</tspan></text>')
    svg.append(f'<text x="185" y="{y_b1 + 21}" class="mono inst-param">d : <tspan class="inst-reg">D110_WEB_FULLSTACK_DEV</tspan></text>')
    svg.append(f'<line x1="745" y1="{y_b1}" x2="815" y2="{y_b1}" class="wire"/>')
    svg.append(f'<path d="M 815 {y_b1-12} A 12 12 0 0 1 815 {y_b1+12}" stroke="#00ff88" stroke-width="2.5" fill="none"/>')
    svg.append(f'<path d="M 845 {y_b1-12} A 12 12 0 0 0 845 {y_b1+12}" stroke="#00ff88" stroke-width="2.5" fill="none"/>')
    svg.append(f'<text x="830" y="{y_b1 + 4}" class="mono coil-lbl">Y010</text>')
    svg.append(f'<text x="830" y="{y_b1 + 22}" class="mono coil-tag">(WEB_RUN)</text>')
    svg.append(f'<line x1="845" y1="{y_b1}" x2="{r_rail_x}" y2="{y_b1}" class="wire-off"/>')

    # --- BRANCH 2: PLC & ROBOTICS ---
    svg.append(f'<line x1="{b_x}" y1="{y_b2}" x2="175" y2="{y_b2}" class="wire"/>')
    svg.append(f'<rect x="175" y="{y_b2 - 25}" width="570" height="52" rx="5" fill="url(#boxGrad)" stroke="#f0883e" stroke-width="1.5"/>')
    svg.append(f'<text x="185" y="{y_b2 - 9}" class="mono" fill="#f0883e" font-size="11px" font-weight="bold">MOV [02: INDUSTRIAL AUTOMATION &amp; ROBOTICS]</text>')
    svg.append(f'<text x="185" y="{y_b2 + 7}" class="mono inst-param">s : <tspan class="inst-val">"Kontrol Mesin, Robotik Industri, PLC Mitsubishi (FX/Q) &amp; Omron (CP/CJ)"</tspan></text>')
    svg.append(f'<text x="185" y="{y_b2 + 21}" class="mono inst-param">d : <tspan class="inst-reg">D120_PLC_ROBOTICS_CTRL</tspan></text>')
    svg.append(f'<line x1="745" y1="{y_b2}" x2="815" y2="{y_b2}" class="wire"/>')
    svg.append(f'<path d="M 815 {y_b2-12} A 12 12 0 0 1 815 {y_b2+12}" stroke="#00ff88" stroke-width="2.5" fill="none"/>')
    svg.append(f'<path d="M 845 {y_b2-12} A 12 12 0 0 0 845 {y_b2+12}" stroke="#00ff88" stroke-width="2.5" fill="none"/>')
    svg.append(f'<text x="830" y="{y_b2 + 4}" class="mono coil-lbl">Y020</text>')
    svg.append(f'<text x="830" y="{y_b2 + 22}" class="mono coil-tag">(PLC_RUN)</text>')
    svg.append(f'<line x1="845" y1="{y_b2}" x2="{r_rail_x}" y2="{y_b2}" class="wire-off"/>')

    # --- BRANCH 3: IT/OT CONVERGENCE ---
    svg.append(f'<line x1="{b_x}" y1="{y_b3}" x2="175" y2="{y_b3}" class="wire"/>')
    svg.append(f'<rect x="175" y="{y_b3 - 25}" width="570" height="52" rx="5" fill="url(#boxGrad)" stroke="#a371f7" stroke-width="1.5"/>')
    svg.append(f'<text x="185" y="{y_b3 - 9}" class="mono" fill="#d2a8ff" font-size="11px" font-weight="bold">CALL [03: IT / OT CONVERGENCE &amp; CLOUD TELEMETRY]</text>')
    svg.append(f'<text x="185" y="{y_b3 + 7}" class="mono inst-param">s : <tspan class="inst-val">"Modbus RTU/TCP, Serial RS-232/485, MQTT, SCADA -&gt; Real-Time Web Dashboard"</tspan></text>')
    svg.append(f'<text x="185" y="{y_b3 + 21}" class="mono inst-param">d : <tspan class="inst-reg">P_IT_OT_INTEGRATION_SUBROUTINE</tspan></text>')
    svg.append(f'<line x1="745" y1="{y_b3}" x2="815" y2="{y_b3}" class="wire"/>')
    svg.append(f'<path d="M 815 {y_b3-12} A 12 12 0 0 1 815 {y_b3+12}" stroke="#00ff88" stroke-width="2.5" fill="none"/>')
    svg.append(f'<path d="M 845 {y_b3-12} A 12 12 0 0 0 845 {y_b3+12}" stroke="#00ff88" stroke-width="2.5" fill="none"/>')
    svg.append(f'<text x="830" y="{y_b3 + 4}" class="mono coil-lbl">Y030</text>')
    svg.append(f'<text x="830" y="{y_b3 + 22}" class="mono coil-tag">(IT_OT_SYNC)</text>')
    svg.append(f'<line x1="845" y1="{y_b3}" x2="{r_rail_x}" y2="{y_b3}" class="wire-off"/>')

    # -------------------------------------------------------------
    # RUNG 002 : TECH STACK DATA REGISTERS (BMOV)
    # -------------------------------------------------------------
    r2_y = 475
    svg.append(f'<text x="68" y="{r2_y - 25}" class="mono rung-hdr">// RUNG 002 : TECH STACK &amp; PERIPHERALS (BMOV BLOCK TRANSFER)</text>')
    svg.append(f'<line x1="{l_rail_x}" y1="{r2_y}" x2="105" y2="{r2_y}" class="wire"/>')

    # Contact X001 (USER_INSPECT)
    svg.append(f'<line x1="105" y1="{r2_y-12}" x2="105" y2="{r2_y+12}" stroke="#00ff88" stroke-width="3"/>')
    svg.append(f'<line x1="120" y1="{r2_y-12}" x2="120" y2="{r2_y+12}" stroke="#00ff88" stroke-width="3"/>')
    svg.append(f'<text x="112" y="{r2_y - 16}" class="mono contact-lbl">X001</text>')
    svg.append(f'<text x="112" y="{r2_y + 24}" class="mono contact-tag">(DEV_QUERY)</text>')

    svg.append(f'<line x1="120" y1="{r2_y}" x2="175" y2="{r2_y}" class="wire"/>')

    # Function Block: BMOV
    svg.append(f'<rect x="175" y="{r2_y - 30}" width="570" height="58" rx="5" fill="url(#boxGrad)" stroke="#388bfd" stroke-width="1.5"/>')
    svg.append(f'<text x="185" y="{r2_y - 12}" class="mono inst-title">BMOV (Block Move 16 Registers)</text>')
    svg.append(f'<text x="185" y="{r2_y + 4}" class="mono inst-param">WEB_REG: <tspan class="inst-val">Next.js, React, Node.js, TS, Tailwind, PostgreSQL, Prisma, Docker</tspan></text>')
    svg.append(f'<text x="185" y="{r2_y + 19}" class="mono inst-param">PLC_REG: <tspan class="inst-val">Mitsubishi (GX Works2/3), Omron (Sysmac), Modbus, Serial, SCADA</tspan></text>')

    svg.append(f'<line x1="745" y1="{r2_y}" x2="815" y2="{r2_y}" class="wire"/>')
    svg.append(f'<path d="M 815 {r2_y-12} A 12 12 0 0 1 815 {r2_y+12}" stroke="#00ff88" stroke-width="2.5" fill="none"/>')
    svg.append(f'<path d="M 845 {r2_y-12} A 12 12 0 0 0 845 {r2_y+12}" stroke="#00ff88" stroke-width="2.5" fill="none"/>')
    svg.append(f'<text x="830" y="{r2_y + 4}" class="mono coil-lbl">Y100</text>')
    svg.append(f'<text x="830" y="{r2_y + 22}" class="mono coil-tag">(STACK_OK)</text>')
    svg.append(f'<line x1="845" y1="{r2_y}" x2="{r_rail_x}" y2="{r2_y}" class="wire-off"/>')

    # -------------------------------------------------------------
    # RUNG 003 : COMMUNICATION BUS (CONTACTS & FEND)
    # -------------------------------------------------------------
    r3_y = 575
    svg.append(f'<text x="68" y="{r3_y - 20}" class="mono rung-hdr">// RUNG 003 : COMMUNICATION PORTS &amp; MAIN SCAN END</text>')
    svg.append(f'<line x1="{l_rail_x}" y1="{r3_y}" x2="105" y2="{r3_y}" class="wire"/>')

    # Contact SM412 (1s Clock Pulse)
    svg.append(f'<line x1="105" y1="{r3_y-12}" x2="105" y2="{r3_y+12}" stroke="#00ff88" stroke-width="3"/>')
    svg.append(f'<line x1="120" y1="{r3_y-12}" x2="120" y2="{r3_y+12}" stroke="#00ff88" stroke-width="3"/>')
    svg.append(f'<path d="M 108 {r3_y+6} L 112 {r3_y-6} L 117 {r3_y+6}" stroke="#00ff88" stroke-width="1.5" fill="none"/>')
    svg.append(f'<text x="112" y="{r3_y - 16}" class="mono contact-lbl">SM412</text>')
    svg.append(f'<text x="112" y="{r3_y + 24}" class="mono contact-tag">(1s Clock)</text>')

    svg.append(f'<line x1="120" y1="{r3_y}" x2="175" y2="{r3_y}" class="wire"/>')

    # Function Block: COM_OPEN
    svg.append(f'<rect x="175" y="{r3_y - 24}" width="570" height="46" rx="5" fill="url(#boxGrad)" stroke="#3fb950" stroke-width="1.5"/>')
    svg.append(f'<text x="185" y="{r3_y - 7}" class="mono" fill="#7ee787" font-size="11px" font-weight="bold">COM_OPEN [NET_INTERFACE: LinkedIn | Outlook | GitHub]</text>')
    svg.append(f'<text x="185" y="{r3_y + 11}" class="mono inst-param">PORT: <tspan class="inst-val">LINKEDIN (sirojul-kahfi) | EMAIL (sirojulkahfi@outlook.com) | GIT (sirojulkahfi)</tspan></text>')

    svg.append(f'<line x1="745" y1="{r3_y}" x2="815" y2="{r3_y}" class="wire"/>')
    # FEND box
    svg.append(f'<rect x="805" y="{r3_y - 14}" width="55" height="28" rx="3" fill="#21262d" stroke="#f85149" stroke-width="2"/>')
    svg.append(f'<text x="832" y="{r3_y + 4}" class="mono" fill="#f85149" font-size="11px" font-weight="bold" text-anchor="middle">FEND</text>')
    svg.append(f'<line x1="860" y1="{r3_y}" x2="{r_rail_x}" y2="{r3_y}" class="wire-off"/>')

    # Footer
    svg.append(f'<line x1="15" y1="{height - 22}" x2="945" y2="{height - 22}" stroke="#21262d" stroke-width="1"/>')
    svg.append(f'<text x="30" y="{height - 8}" class="mono" fill="#8b949e" font-size="10px">IEC 61131-3 STANDARD LADDER LOGIC | ARCHITECTURE: IT/OT SYSTEM CONVERGENCE</text>')
    svg.append(f'<text x="930" y="{height - 8}" class="mono" fill="#8b949e" font-size="10px" text-anchor="end">SIROJUL KAHFI &copy; 2026</text>')

    svg.append('</svg>')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg))
    print(f"SVG Ladder Diagram generated successfully at {output_path}")

if __name__ == "__main__":
    generate_ladder_svg()

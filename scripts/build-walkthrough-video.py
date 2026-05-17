import html
import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRESENTATION = ROOT / "presentation"
OUT = PRESENTATION / "walkthrough"
FRAMES = OUT / "frames"
AUDIO = OUT / "audio"
SEGMENTS = OUT / "segments"
VIDEO = OUT / "HIP_MARKETS_WALKTHROUGH.mp4"
SCRIPT_MD = OUT / "HIP_MARKETS_WALKTHROUGH_SCRIPT.md"
YOUTUBE_MD = OUT / "YOUTUBE_UPLOAD_COPY.md"


SCENES = [
    {
        "title": "HIP.markets",
        "kicker": "Hackathon walkthrough",
        "image": "brand-system.png",
        "bullets": [
            "Community-backed HIP-3 markets on Hyperliquid",
            "Fund the operator stake",
            "Share net deployer fees",
        ],
        "narration": (
            "This is HIP dot markets, a community-backed HIP-3 market operator for Hyperliquid. "
            "The simple idea is: HYPE holders fund the operator stake, HIP dot markets operates "
            "the markets, and net deployer fees are shared back with the stakers who made those "
            "markets possible."
        ),
    },
    {
        "title": "Why This Matters",
        "kicker": "Hyperliquid is already exchange-scale",
        "image": "market-context.png",
        "bullets": [
            "$164B 30-day perp volume snapshot",
            "$7.3B open interest snapshot",
            "HIP-3 opens these rails to new operators",
        ],
        "narration": (
            "Judges should not evaluate this like a cold-start yield app. Hyperliquid already has "
            "exchange-scale flow. The current research snapshot shows hundreds of billions in "
            "monthly perp volume, more than seven billion dollars of open interest, and over seven "
            "hundred million dollars of annualized revenue. HIP-3 turns that infrastructure into open market "
            "operator infrastructure."
        ),
    },
    {
        "title": "The 500k HYPE Blocker",
        "kicker": "Permissionless does not mean cheap",
        "stats": [
            ("Required HIP-3 stake", "500,000 HYPE"),
            ("Value at $42.848", "$21.42M"),
            ("Baseline staking", "~2.37% APY"),
        ],
        "bullets": [
            "Stake is slashable",
            "Operators still need oracles, makers, audits, legal, and reserves",
            "Most HYPE holders cannot access operator economics alone",
        ],
        "narration": (
            "The opportunity is blocked by capital. One HIP-3 perpetual DEX requires five hundred "
            "thousand HYPE staked on mainnet. At the price check used in this submission, that is "
            "roughly twenty one point four two million dollars before oracle operations, data, "
            "market maker incentives, audits, legal work, and reserves. Meanwhile current HYPE "
            "staking references are around two point three seven percent APY. HIP dot markets creates "
            "a separate, higher risk operator-fee product."
        ),
    },
    {
        "title": "Trade.xyz Proves Demand",
        "kicker": "Reference economics, not guaranteed returns",
        "image": "tradexyz-reference.png",
        "bullets": [
            "60 listed markets",
            "$2.50B 30-day volume snapshot",
            "$60.99K estimated deployer share before costs",
        ],
        "narration": (
            "Trade dot xyz is the reference case. It proves HIP-3 markets can attract real trading "
            "demand across crypto, indexes, commodities, and RWA-style instruments. But in the "
            "standard operator model, deployer fees accrue to the operator fee recipient. HIP dot "
            "markets changes the incentive design by letting the community fund the stake and share "
            "in net deployer economics."
        ),
    },
    {
        "title": "Core Product",
        "kicker": "Operator vault, not passive staking",
        "flow": [
            "Deposit HYPE",
            "Receive vHIPM shares",
            "Fund HIP.markets stake",
            "Launch curated markets",
            "Distribute net fees",
        ],
        "bullets": [
            "One HIP.markets-operated DEX in the MVP",
            "First three markets avoid extra ticker auction cost",
            "Risk, fee accounting, and oracle state stay visible",
        ],
        "narration": (
            "The first product is an operator vault. Users deposit HYPE and receive receipt shares. "
            "The vault funds the HIP dot markets deployer stake. The team operates the DEX, launches "
            "curated markets, runs oracles, manages liquidity and risk, and distributes net fees "
            "after operating costs, protocol fees, and reserve contributions."
        ),
    },
    {
        "title": "Demo Walkthrough",
        "kicker": "The first screen is the product",
        "image": "demo-dashboard.png",
        "bullets": [
            "Vault capacity and projected APR",
            "Market launch rail",
            "Deposit ticket, oracle cadence, and risk monitor",
        ],
        "narration": (
            "The demo opens directly into the operator console, not a marketing page. A judge can see "
            "the vault capacity, projected APR, market launch rail, deposit ticket, oracle cadence, "
            "risk state, and operator monitor in one workflow. The interface borrows trading terminal "
            "density from successful HIP-3 products like Trade dot xyz, but translates it into a vault "
            "and underwriting experience."
        ),
    },
    {
        "title": "Fee Model",
        "kicker": "Judges can change the assumptions",
        "stats": [
            ("Base daily volume", "$50M"),
            ("Effective fee", "6 bps"),
            ("Deployer share", "50%"),
        ],
        "bullets": [
            "APR updates instantly",
            "Operating, protocol, and reserve deductions are explicit",
            "Trade.xyz benchmark is shown as a reference case",
        ],
        "narration": (
            "The calculator is intentionally simple and reviewable. Judges can change HYPE price, "
            "staked HYPE, daily volume, fee basis points, deployer share, operating costs, protocol "
            "fee, and reserve contribution. The point is not to promise fixed yield. The point is to "
            "show exactly which assumptions drive staker returns."
        ),
    },
    {
        "title": "Contract Wiring",
        "kicker": "Prototype maps to the onchain path",
        "image": "demo-contract-wiring.png",
        "bullets": [
            "Connect wallet",
            "Configure vault and HYPE token addresses",
            "Approve, deposit, claim rewards",
            "Operator multisig and risk council actions are visible",
        ],
        "narration": (
            "The app also shows the real transaction path. In demo mode it is safe and read-only, but "
            "after deployment a user can configure vault and token addresses, connect a wallet, approve "
            "HYPE, deposit into the vault, and claim rewards. The remaining operator actions are shown "
            "honestly: multisig escrow, HIP-3 approval, and risk-council state changes."
        ),
    },
    {
        "title": "Reference Contracts",
        "kicker": "More than a mock UI",
        "bullets": [
            "Vault receipt shares and withdrawal queue",
            "Operator phases from funding to live to wind-down",
            "Reward, reserve, protocol-fee, and slashing accounting",
            "Registry for markets, oracle health, fee epochs, and risk state",
        ],
        "narration": (
            "This is not just a front-end mock. The Solidity reference contracts model receipt shares, "
            "vault caps, withdrawal queues, rewards, protocol and reserve accounting, slashing losses, "
            "operator phase gates, fee epochs, oracle health, market metadata, and risk state. They are "
            "not audited, but they show the depth of the production design."
        ),
    },
    {
        "title": "Why This Should Win",
        "kicker": "Commercially realistic, ecosystem-native",
        "bullets": [
            "Solves a real HIP-3 capital coordination bottleneck",
            "Turns operator economics into transparent community exposure",
            "Keeps slashing, oracle, and liquidity risk beside APR",
            "Starts narrow, then expands toward HIP-4 and operator financing",
        ],
        "narration": (
            "HIP dot markets should score well because it is specific to Hyperliquid, grounded in real "
            "HIP-3 mechanics, and commercially realistic. It does not hide risk behind APR. It explains "
            "the capital blocker, shows a path for users to participate in operator economics, and gives "
            "the ecosystem a new capital allocation layer for builder-deployed markets."
        ),
    },
    {
        "title": "HIP.markets",
        "kicker": "Fund the operator stake. Share the builder fees.",
        "image": "brand-system.png",
        "bullets": [
            "MVP: one operator vault, one DEX, first three markets",
            "Next: automated fee verification, tranching, HIP-4",
            "Long-term: underwriting layer for Hyperliquid markets",
        ],
        "narration": (
            "The MVP is deliberately focused: one HIP dot markets operated DEX, one HYPE vault, and the "
            "first three markets. From there, the product can add automated fee verification, risk "
            "tranching, secondary vault shares, and eventually HIP-4 outcome market support. HIP dot "
            "markets is the capital allocation and underwriting layer for Hyperliquid builder-deployed markets."
        ),
    },
]


def run(command):
    subprocess.run(command, cwd=ROOT, check=True)


def chrome_path():
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        shutil.which("google-chrome"),
        shutil.which("chromium"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    raise FileNotFoundError("Could not find Chrome or Chromium for slide rendering.")


def card_html(scene, index):
    image_html = ""
    if scene.get("image"):
        image_path = (PRESENTATION / scene["image"]).resolve().as_uri()
        image_html = f'<img class="hero-image" src="{image_path}" alt="" />'

    stats_html = ""
    if scene.get("stats"):
        stats = "".join(
            f"<div><span>{html.escape(label)}</span><strong>{html.escape(value)}</strong></div>"
            for label, value in scene["stats"]
        )
        stats_html = f'<div class="stats">{stats}</div>'

    flow_html = ""
    if scene.get("flow"):
        flow = "".join(
            f"<div><em>{idx}</em><span>{html.escape(item)}</span></div>"
            for idx, item in enumerate(scene["flow"], start=1)
        )
        flow_html = f'<div class="flow">{flow}</div>'

    bullets = "".join(f"<li>{html.escape(item)}</li>" for item in scene["bullets"])
    return f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <style>
      * {{ box-sizing: border-box; }}
      body {{
        width: 1920px;
        height: 1080px;
        margin: 0;
        overflow: hidden;
        background:
          linear-gradient(135deg, rgba(104, 167, 255, 0.14), transparent 42%),
          linear-gradient(315deg, rgba(50, 210, 150, 0.12), transparent 46%),
          #07090c;
        color: #edf3f6;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }}
      main {{ padding: 70px 78px; }}
      .kicker {{
        color: #32d296;
        font-size: 25px;
        font-weight: 800;
        letter-spacing: .08em;
        text-transform: uppercase;
      }}
      h1 {{
        margin: 16px 0 34px;
        max-width: 1420px;
        font-size: 82px;
        line-height: 1.02;
        letter-spacing: 0;
      }}
      .layout {{
        display: grid;
        grid-template-columns: 1fr 690px;
        gap: 34px;
        align-items: stretch;
      }}
      .panel {{
        border: 1px solid #26313c;
        border-radius: 20px;
        background: linear-gradient(180deg, rgba(255,255,255,.05), rgba(255,255,255,.015));
        padding: 34px;
        min-height: 560px;
      }}
      ul {{
        display: grid;
        gap: 22px;
        margin: 0;
        padding-left: 30px;
      }}
      li {{
        color: #d7e3ea;
        font-size: 35px;
        line-height: 1.22;
      }}
      .hero-image {{
        width: 100%;
        height: 560px;
        object-fit: contain;
        border: 1px solid #26313c;
        border-radius: 20px;
        background: #0c1117;
      }}
      .stats {{
        display: grid;
        grid-template-columns: 1fr;
        gap: 22px;
      }}
      .stats div {{
        border: 1px solid #26313c;
        border-radius: 18px;
        background: #0c1117;
        padding: 28px;
      }}
      .stats span {{
        display: block;
        color: #8d9ba7;
        font-size: 24px;
      }}
      .stats strong {{
        display: block;
        margin-top: 12px;
        color: #f4c45f;
        font-size: 54px;
      }}
      .flow {{
        display: grid;
        gap: 18px;
      }}
      .flow div {{
        display: grid;
        grid-template-columns: 56px 1fr;
        gap: 18px;
        align-items: center;
        border: 1px solid #26313c;
        border-radius: 18px;
        background: #0c1117;
        padding: 20px;
      }}
      .flow em {{
        display: grid;
        place-items: center;
        width: 56px;
        height: 56px;
        border-radius: 999px;
        background: rgba(50,210,150,.12);
        color: #32d296;
        font-style: normal;
        font-weight: 900;
        font-size: 25px;
      }}
      .flow span {{
        font-size: 34px;
        font-weight: 800;
      }}
      .footer {{
        position: absolute;
        left: 78px;
        right: 78px;
        bottom: 46px;
        display: flex;
        justify-content: space-between;
        color: #8d9ba7;
        font-size: 22px;
      }}
    </style>
  </head>
  <body>
    <main>
      <div class="kicker">{html.escape(scene["kicker"])}</div>
      <h1>{html.escape(scene["title"])}</h1>
      <section class="layout">
        <div class="panel"><ul>{bullets}</ul></div>
        <div>{image_html}{stats_html}{flow_html}</div>
      </section>
    </main>
    <div class="footer"><span>HIP.markets hackathon walkthrough</span><span>{index:02d} / {len(SCENES):02d}</span></div>
  </body>
</html>"""


def write_assets():
    for path in [OUT, FRAMES, AUDIO, SEGMENTS]:
        path.mkdir(parents=True, exist_ok=True)

    script_lines = ["# HIP.markets Walkthrough Script", ""]
    for idx, scene in enumerate(SCENES, start=1):
        script_lines.extend([f"## {idx}. {scene['title']}", "", scene["narration"], ""])
        (OUT / f"scene-{idx:02d}.html").write_text(card_html(scene, idx))
        (AUDIO / f"scene-{idx:02d}.txt").write_text(scene["narration"])
    SCRIPT_MD.write_text("\n".join(script_lines))

    youtube_copy = """# YouTube Upload Copy

## Title
HIP.markets Walkthrough - Community-Backed HIP-3 Markets on Hyperliquid

## Description
HIP.markets is a HyperEVM operator-vault prototype for Hyperliquid HIP-3 markets.

HYPE holders deposit into a vault that funds the 500,000 HYPE slashable stake required for the HIP.markets team to operate a HIP-3 builder-deployed perpetual DEX. Instead of deployer fees accruing only to a market operator, HIP.markets shares net deployer fees with the stakers who make the operator possible.

This hackathon walkthrough covers:
- why Hyperliquid's scale makes HIP-3 meaningful;
- why the 500,000 HYPE stake is a major blocker;
- how Trade.xyz validates HIP-3 market demand;
- how the HIP.markets vault, demo app, fee model, and contracts work;
- why the product is underwriting and operator infrastructure, not passive liquid staking.

Prototype only. Not audited. Not financial advice.

GitHub: https://github.com/clawtton/HIP

## Tags
Hyperliquid, HIP-3, HyperEVM, HYPE, DeFi, perpetuals, hackathon, onchain derivatives, vaults

## Visibility Recommendation
Unlisted for judging, then Public after final review.
"""
    YOUTUBE_MD.write_text(youtube_copy)


def render_frames():
    chrome = chrome_path()
    for idx in range(1, len(SCENES) + 1):
        html_file = OUT / f"scene-{idx:02d}.html"
        png_file = FRAMES / f"scene-{idx:02d}.png"
        run(
            [
                chrome,
                "--headless",
                "--disable-gpu",
                "--hide-scrollbars",
                "--window-size=1920,1080",
                f"--screenshot={png_file}",
                html_file.resolve().as_uri(),
            ]
        )


def render_audio_and_segments():
    concat_lines = []
    for idx in range(1, len(SCENES) + 1):
        text_file = AUDIO / f"scene-{idx:02d}.txt"
        aiff_file = AUDIO / f"scene-{idx:02d}.aiff"
        m4a_file = AUDIO / f"scene-{idx:02d}.m4a"
        segment_file = SEGMENTS / f"scene-{idx:02d}.mp4"
        png_file = FRAMES / f"scene-{idx:02d}.png"

        run(["say", "-v", "Samantha", "-r", "178", "-f", str(text_file), "-o", str(aiff_file)])
        run(["ffmpeg", "-y", "-i", str(aiff_file), "-c:a", "aac", "-b:a", "160k", str(m4a_file)])
        run(
            [
                "ffmpeg",
                "-y",
                "-loop",
                "1",
                "-framerate",
                "30",
                "-i",
                str(png_file),
                "-i",
                str(m4a_file),
                "-c:v",
                "libx264",
                "-tune",
                "stillimage",
                "-c:a",
                "aac",
                "-b:a",
                "160k",
                "-pix_fmt",
                "yuv420p",
                "-shortest",
                "-movflags",
                "+faststart",
                str(segment_file),
            ]
        )
        concat_lines.append(f"file '{segment_file.resolve()}'")

    concat_file = OUT / "concat.txt"
    concat_file.write_text("\n".join(concat_lines) + "\n")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", str(VIDEO)])


def main():
    write_assets()
    render_frames()
    render_audio_and_segments()
    manifest = {
        "video": str(VIDEO.relative_to(ROOT)),
        "script": str(SCRIPT_MD.relative_to(ROOT)),
        "youtube_copy": str(YOUTUBE_MD.relative_to(ROOT)),
        "scenes": len(SCENES),
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

from html import escape
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
PRESENTATION = ROOT / "presentation"
OUT = PRESENTATION / "HIP_MARKETS_DECK.pptx"

SLIDE_W = 12_192_000
SLIDE_H = 6_858_000

SLIDES = [
    {
        "title": "HIP.markets",
        "bullets": [
            "Community-backed HIP-3 markets on Hyperliquid.",
            "Fund the market operator. Share the builder fees.",
        ],
    },
    {
        "title": "The Problem",
        "bullets": [
            "HIP-3 DEXs need 500,000 HYPE staked.",
            "Stake is only the start: operators also need oracles, liquidity, risk controls, and fee accounting.",
            "Stakers need slashing risk beside APR.",
        ],
    },
    {
        "title": "Product Thesis",
        "bullets": [
            "HIP.markets is not passive liquid staking.",
            "HIP.markets is the operator.",
            "Users back the HIP.markets deployer stake and share net deployer fees.",
        ],
    },
    {
        "title": "Why Now",
        "bullets": [
            "Hyperliquid has moved from one exchange into market infrastructure.",
            "HIP-3 lets specialist operators list new perpetual markets while HyperCore provides execution rails.",
            "The bottleneck shifts to capital, oracle operations, and operator credibility.",
        ],
    },
    {
        "title": "Trade.xyz Reference",
        "bullets": [
            "60 markets, $2.50B 30-day volume, and $121.98K total 30-day fees.",
            "Estimated deployer revenue: $60.99K over 30 days before operating costs.",
            "Gross implied APR: 3.47% on the 500k HYPE minimum stake at $42.8085 HYPE.",
        ],
        "image": "tradexyz-reference.png",
    },
    {
        "title": "Successful Market Pattern",
        "bullets": [
            "Trade.xyz's highest-volume tickers are not only crypto assets.",
            "XYZ100 and SP500: roughly $444M each over 30 days.",
            "SILVER, CL, SNDK, MU, NVDA, BRENTOIL, CBRS, INTC, and GOLD show RWA-style breadth.",
            "HIP.markets should launch where oracle confidence, liquidity, and narrative demand overlap.",
        ],
    },
    {
        "title": "Revenue Interpretation",
        "bullets": [
            "HIP-3 deployer share is fixed at 50% from the deployer perspective.",
            "Trade.xyz reports deployerFeeScale = 1.0.",
            "Gross revenue is not distributable profit until oracle, data, maker, legal, reserve, and incident costs are deducted.",
        ],
    },
    {
        "title": "UI Benchmark",
        "bullets": [
            "trade.xyz proves serious HIP-3 markets need trading-terminal density.",
            "Useful patterns: market rail, order ticket, positions tabs, account modes, Ghost Mode observability, explicit warnings.",
        ],
    },
    {
        "title": "UX Translation",
        "bullets": [
            "Market rail -> first-three-market launch rail.",
            "Order ticket -> HYPE deposit ticket.",
            "Positions panel -> vault shares, fee history, oracle updates, market launches.",
            "Ghost Mode -> operator monitor.",
        ],
    },
    {
        "title": "Demo Walkthrough",
        "bullets": [
            "The first screen is the usable operator console, not a landing page.",
            "Vault capacity, APR, oracle cadence, risk state, market rail, fee model, deposit ticket, and monitor are visible in one workflow.",
        ],
        "image": "demo-dashboard.png",
    },
    {
        "title": "Demo: Fee Model",
        "bullets": [
            "Judges can change HYPE price, staked HYPE, daily volume, fee bps, builder share, operating fee, protocol fee, and reserve.",
            "APR updates instantly.",
        ],
    },
    {
        "title": "Demo: Deposit Ticket",
        "bullets": [
            "Mirrors a trading order pane.",
            "Amount input, deposit/withdraw mode, fee summary, user rewards estimate, and slashing warning.",
        ],
    },
    {
        "title": "Demo: Audit Ledger",
        "bullets": [
            "Fee sharing becomes an inspectable ledger.",
            "Vault shares, fee history, oracle updates, and market launch readiness expose operator behavior.",
        ],
        "image": "demo-fee-ledger-view.png",
    },
    {
        "title": "Demo: Contract Wiring",
        "bullets": [
            "Wallet-aware flow: connect wallet, configure vault/token addresses, approve HYPE, deposit, and claim rewards.",
            "The UI also shows which actions still require operator multisig and risk-council execution.",
        ],
        "image": "demo-contract-wiring.png",
    },
    {
        "title": "Contract Depth",
        "bullets": [
            "Vault now models vHIPM receipt shares, vault caps, withdrawal queues, reward accounting, and slash losses.",
            "Operator lifecycle: funding, stake-ready, stake-escrowed, approved, live, wind-down, and slashed.",
            "Registry tracks launch checklist, fee epochs, oracle health, market status, and risk state.",
        ],
    },
    {
        "title": "System Flow",
        "bullets": [
            "1. HYPE holders deposit into the HyperEVM vault.",
            "2. Vault backs HIP.markets deployer stake.",
            "3. Operator multisig escrows funded HYPE to the deployer stake controller.",
            "4. Risk council records HIP-3 operator approval.",
            "5. HIP.markets launches markets, traders generate fees, and net rewards distribute after deductions.",
        ],
    },
    {
        "title": "Economics",
        "bullets": [
            "Base model: 500k HYPE, $50M daily volume, 6 bps fee, 50% deployer share.",
            "After 40% operating/protocol/reserve deductions: approximately 15% net APR.",
            "Trade.xyz trailing fees imply approximately 3.47% gross APR on the minimum stake.",
            "Sensitivity matters more than headline APR.",
        ],
    },
    {
        "title": "Risk Controls",
        "bullets": [
            "Start with oracle-simple markets.",
            "Avoid extra ticker auction costs at launch.",
            "Cap open interest, publish addresses, maintain reserve, pause deposits during incidents.",
        ],
    },
    {
        "title": "Cost Stack",
        "bullets": [
            "The 500k HYPE stake is the entry ticket, not the full cost of business.",
            "Budget for oracle relayers, licensed data, maker incentives, infrastructure, key management, audits, legal work, and incident reserves.",
        ],
    },
    {
        "title": "MVP",
        "bullets": [
            "One HIP.markets-operated DEX.",
            "One HYPE vault.",
            "First three markets.",
            "Weekly distributions.",
            "Public dashboard.",
            "No third-party operator financing.",
        ],
    },
    {
        "title": "Roadmap",
        "bullets": [
            "V1: prove operator vault and fee sharing.",
            "V2: more HIP.markets market vaults and automated fee verification.",
            "V3: risk tranching, secondary shares, HIP-4, possible third-party financing once the trust model is mature.",
        ],
    },
    {
        "title": "Competitive Position",
        "bullets": [
            "trade.xyz and HyENA operate markets directly.",
            "HIP.markets also operates markets directly, but adds user-funded HYPE stake and transparent fee sharing.",
            "The wedge is making HYPE holders economic backers of the operator.",
        ],
    },
    {
        "title": "Ask",
        "bullets": [
            "HYPE holders for capped beta.",
            "Market makers for first markets.",
            "Oracle and data partners.",
            "Security reviewers.",
            "Hyperliquid feedback on custody and fee routing.",
        ],
    },
    {
        "title": "Closing",
        "bullets": [
            "HIP.markets turns builder-deployed markets into a community-backed operator business.",
            "The first job is operating markets safely.",
        ],
    },
]


def text_box_xml(shape_id, name, x, y, w, h, paragraphs, size=2100, color="D7E3EA", bullet=True):
    body = ""
    for paragraph in paragraphs:
        bullet_pr = '<a:pPr marL="285750" indent="-171450"><a:buChar char="&#8226;"/></a:pPr>' if bullet else "<a:pPr/>"
        body += f"""
        <a:p>
          {bullet_pr}
          <a:r><a:rPr lang="en-US" sz="{size}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:rPr><a:t>{escape(paragraph)}</a:t></a:r>
        </a:p>
        """
    return f"""
      <p:sp>
        <p:nvSpPr><p:cNvPr id="{shape_id}" name="{escape(name)}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>
        <p:txBody><a:bodyPr wrap="square"/><a:lstStyle/>{body}</p:txBody>
      </p:sp>
    """


def image_xml(shape_id, rel_id, name, x, y, w, h):
    return f"""
      <p:pic>
        <p:nvPicPr><p:cNvPr id="{shape_id}" name="{escape(name)}"/><p:cNvPicPr/><p:nvPr/></p:nvPicPr>
        <p:blipFill><a:blip r:embed="{rel_id}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>
        <p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>
      </p:pic>
    """


def slide_xml(index, slide, image_rel=None):
    title = slide["title"]
    bullets = slide["bullets"]
    has_image = image_rel is not None
    if has_image:
        body_x, body_y, body_w, body_h = 609_600, 1_630_000, 4_600_000, 4_400_000
        image_x, image_y, image_w, image_h = 5_450_000, 1_500_000, 6_130_000, 3_450_000
    else:
        body_x, body_y, body_w, body_h = 914_400, 1_905_000, 9_800_000, 3_900_000
        image_x = image_y = image_w = image_h = 0

    body = text_box_xml(3, "Body", body_x, body_y, body_w, body_h, bullets)
    image = ""
    if has_image:
        image = image_xml(5, image_rel, slide["image"], image_x, image_y, image_w, image_h)

    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg><p:bgPr><a:solidFill><a:srgbClr val="080A0D"/></a:solidFill></p:bgPr></p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      <p:sp>
        <p:nvSpPr><p:cNvPr id="2" name="Title"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="609600" y="610000"/><a:ext cx="10300000" cy="850000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>
        <p:txBody><a:bodyPr wrap="square"/><a:lstStyle/>
          <a:p><a:r><a:rPr lang="en-US" sz="4100" b="1"><a:solidFill><a:srgbClr val="F4F7F8"/></a:solidFill></a:rPr><a:t>{escape(title)}</a:t></a:r></a:p>
        </p:txBody>
      </p:sp>
      {body}
      {image}
      <p:sp>
        <p:nvSpPr><p:cNvPr id="4" name="Footer"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="609600" y="6400800"/><a:ext cx="10500000" cy="300000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>
        <p:txBody><a:bodyPr wrap="square"/><a:lstStyle/><a:p><a:r><a:rPr lang="en-US" sz="1000"><a:solidFill><a:srgbClr val="35D29A"/></a:solidFill></a:rPr><a:t>HIP.markets hackathon submission  |  {index:02d}</a:t></a:r></a:p></p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>"""


def presentation_rels_xml(count):
    rels = [
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>',
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>',
    ]
    for i in range(count):
        rels.append(
            f'<Relationship Id="rId{i + 3}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i + 1}.xml"/>'
        )
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(rels) + "</Relationships>"


def slide_rels_xml(media_target=None):
    if not media_target:
        return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>'
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{escape(media_target)}"/>
</Relationships>"""


def presentation_xml(count):
    slide_ids = "".join(f'<p:sldId id="{256 + i}" r:id="rId{i + 3}"/>' for i in range(count))
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>
  <p:sldIdLst>{slide_ids}</p:sldIdLst>
  <p:sldSz cx="{SLIDE_W}" cy="{SLIDE_H}" type="wide"/>
  <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>"""


def content_types(count):
    slides = "".join(
        f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, count + 1)
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  {slides}
</Types>"""


MINIMAL_MASTER = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>"""

MINIMAL_LAYOUT = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank"><p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld></p:sldLayout>"""

MINIMAL_THEME = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="HIP.markets"><a:themeElements><a:clrScheme name="HIP"><a:dk1><a:srgbClr val="080A0D"/></a:dk1><a:lt1><a:srgbClr val="F4F7F8"/></a:lt1><a:dk2><a:srgbClr val="121820"/></a:dk2><a:lt2><a:srgbClr val="D7E3EA"/></a:lt2><a:accent1><a:srgbClr val="35D29A"/></a:accent1><a:accent2><a:srgbClr val="66A6FF"/></a:accent2><a:accent3><a:srgbClr val="FF6B6B"/></a:accent3><a:accent4><a:srgbClr val="93A4B1"/></a:accent4><a:accent5><a:srgbClr val="26333F"/></a:accent5><a:accent6><a:srgbClr val="17202A"/></a:accent6><a:hlink><a:srgbClr val="66A6FF"/></a:hlink><a:folHlink><a:srgbClr val="66A6FF"/></a:folHlink></a:clrScheme><a:fontScheme name="Aptos"><a:majorFont><a:latin typeface="Aptos Display"/></a:majorFont><a:minorFont><a:latin typeface="Aptos"/></a:minorFont></a:fontScheme><a:fmtScheme name="HIP"><a:fillStyleLst/><a:lnStyleLst/><a:effectStyleLst/><a:bgFillStyleLst/></a:fmtScheme></a:themeElements></a:theme>"""


def write_deck():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    media_map = {}
    next_media = 1
    for slide in SLIDES:
        image = slide.get("image")
        if image and image not in media_map:
            image_path = PRESENTATION / image
            if not image_path.exists():
                raise FileNotFoundError(f"missing slide image: {image_path}")
            media_name = f"image{next_media}.png"
            media_map[image] = media_name
            next_media += 1

    with ZipFile(OUT, "w", ZIP_DEFLATED) as deck:
        deck.writestr("[Content_Types].xml", content_types(len(SLIDES)))
        deck.writestr(
            "_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>',
        )
        deck.writestr(
            "docProps/core.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>HIP.markets Hackathon Deck</dc:title><dc:creator>HIP.markets</dc:creator></cp:coreProperties>',
        )
        deck.writestr(
            "docProps/app.xml",
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>HIP.markets</Application><Slides>{len(SLIDES)}</Slides></Properties>',
        )
        deck.writestr("ppt/presentation.xml", presentation_xml(len(SLIDES)))
        deck.writestr("ppt/_rels/presentation.xml.rels", presentation_rels_xml(len(SLIDES)))
        deck.writestr("ppt/slideMasters/slideMaster1.xml", MINIMAL_MASTER)
        deck.writestr(
            "ppt/slideMasters/_rels/slideMaster1.xml.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>',
        )
        deck.writestr("ppt/slideLayouts/slideLayout1.xml", MINIMAL_LAYOUT)
        deck.writestr("ppt/theme/theme1.xml", MINIMAL_THEME)

        for source_name, media_name in media_map.items():
            deck.write(PRESENTATION / source_name, f"ppt/media/{media_name}")

        for index, slide in enumerate(SLIDES, start=1):
            image_name = slide.get("image")
            media_target = media_map.get(image_name)
            image_rel = "rId1" if media_target else None
            deck.writestr(f"ppt/slides/slide{index}.xml", slide_xml(index, slide, image_rel))
            deck.writestr(f"ppt/slides/_rels/slide{index}.xml.rels", slide_rels_xml(media_target))


if __name__ == "__main__":
    write_deck()
    print(f"wrote {OUT}")

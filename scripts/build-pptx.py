from html import escape
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "presentation" / "HIP_MARKETS_DECK.pptx"

SLIDES = [
    ("HIP.markets", ["Community-backed HIP-3 markets on Hyperliquid.", "Pool HYPE. Launch markets. Share builder fees."]),
    ("The Problem", ["HIP-3 DEXs need 500,000 HYPE staked.", "Builders need capital. HYPE holders need transparent market-growth yield.", "Oracle and slashing risks are hard to price."]),
    ("The Insight", ["The 500,000 HYPE stake is the security layer for a market operator.", "If HYPE holders fund that stake, they should share in builder fees."]),
    ("Product", ["HIP.markets is both a HyperEVM HYPE vault and a HIP-3 operator.", "Deposits back the HIP.markets deployer stake.", "Net deployer fees flow back to stakers."]),
    ("System Flow", ["1. HYPE holders deposit into vault.", "2. Vault backs deployer stake.", "3. HIP.markets runs markets and oracles.", "4. Traders generate fees.", "5. Net fees distribute to stakers."]),
    ("Why Not Liquid Staking?", ["Liquid staking earns validator-style yield.", "HIP.markets earns market-operator revenue.", "Risks: oracle, liquidity, slashing, market selection, fee shortfall."]),
    ("MVP", ["One HIP.markets-operated DEX.", "One HYPE vault.", "First three tickers.", "Conservative caps.", "Weekly fee distributions.", "Public oracle and risk dashboard."]),
    ("Economics", ["APR depends on volume, fee rate, deployer share, costs, reserves, and HYPE price.", "Base case: 500k HYPE, $50M daily volume, 6 bps fee, 50% deployer share.", "After 40% deductions: approximately 15% APR."]),
    ("Risk Controls", ["Launch simple markets first.", "Use redundant oracle feeds.", "Cap open interest.", "Publish addresses.", "Maintain slashing reserve.", "Pause deposits during incidents."]),
    ("Market Expansion", ["Phase 1: oracle-simple markets.", "Phase 2: liquid RWA markets.", "Phase 3: commodities and indices after licensing.", "Phase 4: HIP-4 outcome markets if mechanics mature."]),
    ("Competitive Position", ["trade.xyz and HyENA prove HIP-3 operator demand.", "HIP.markets adds community-funded deployer stake plus fee sharing.", "At launch, HIP.markets is the operator."]),
    ("Ask", ["HYPE holders for capped beta.", "Market makers for first markets.", "Oracle/data partners.", "Security reviewers.", "Hyperliquid ecosystem feedback."]),
    ("Closing", ["HIP.markets turns HYPE holders into economic backers of new Hyperliquid markets.", "The first job is not maximizing APR.", "The first job is operating markets safely."]),
]


def slide_xml(index, title, bullets):
    body = "".join(
        f"""
        <a:p>
          <a:pPr marL="285750" indent="-171450"><a:buChar char="&#8226;"/></a:pPr>
          <a:r><a:rPr lang="en-US" sz="2100"><a:solidFill><a:srgbClr val="D7E3EA"/></a:solidFill></a:rPr><a:t>{escape(bullet)}</a:t></a:r>
        </a:p>
        """
        for bullet in bullets
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:bg><p:bgPr><a:solidFill><a:srgbClr val="080A0D"/></a:solidFill></p:bgPr></p:bg>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      <p:sp>
        <p:nvSpPr><p:cNvPr id="2" name="Title"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="609600" y="640080"/><a:ext cx="7924800" cy="1005840"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>
        <p:txBody><a:bodyPr wrap="square"/><a:lstStyle/>
          <a:p><a:r><a:rPr lang="en-US" sz="4300" b="1"><a:solidFill><a:srgbClr val="F4F7F8"/></a:solidFill></a:rPr><a:t>{escape(title)}</a:t></a:r></a:p>
        </p:txBody>
      </p:sp>
      <p:sp>
        <p:nvSpPr><p:cNvPr id="3" name="Body"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="914400" y="1905000"/><a:ext cx="7924800" cy="3657600"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>
        <p:txBody><a:bodyPr wrap="square"/><a:lstStyle/>{body}</p:txBody>
      </p:sp>
      <p:sp>
        <p:nvSpPr><p:cNvPr id="4" name="Footer"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="609600" y="6400800"/><a:ext cx="7924800" cy="300000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>
        <p:txBody><a:bodyPr wrap="square"/><a:lstStyle/><a:p><a:r><a:rPr lang="en-US" sz="1000"><a:solidFill><a:srgbClr val="35D29A"/></a:solidFill></a:rPr><a:t>HIP.markets hackathon submission  |  {index:02d}</a:t></a:r></a:p></p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>"""


def rels_xml(count):
    rels = [
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>',
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>',
    ]
    for i in range(count):
        rels.append(f'<Relationship Id="rId{i + 3}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i + 1}.xml"/>')
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(rels) + "</Relationships>"


def presentation_xml(count):
    slide_ids = "".join(
        f'<p:sldId id="{256 + i}" r:id="rId{i + 3}"/>' for i in range(count)
    )
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>
  <p:sldIdLst>{slide_ids}</p:sldIdLst>
  <p:sldSz cx="12192000" cy="6858000" type="wide"/>
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
    with ZipFile(OUT, "w", ZIP_DEFLATED) as deck:
        deck.writestr("[Content_Types].xml", content_types(len(SLIDES)))
        deck.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>')
        deck.writestr("docProps/core.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>HIP.markets Hackathon Deck</dc:title><dc:creator>HIP.markets</dc:creator></cp:coreProperties>')
        deck.writestr("docProps/app.xml", f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>HIP.markets</Application><Slides>{len(SLIDES)}</Slides></Properties>')
        deck.writestr("ppt/presentation.xml", presentation_xml(len(SLIDES)))
        deck.writestr("ppt/_rels/presentation.xml.rels", rels_xml(len(SLIDES)))
        deck.writestr("ppt/slideMasters/slideMaster1.xml", MINIMAL_MASTER)
        deck.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>')
        deck.writestr("ppt/slideLayouts/slideLayout1.xml", MINIMAL_LAYOUT)
        deck.writestr("ppt/theme/theme1.xml", MINIMAL_THEME)
        for index, (title, bullets) in enumerate(SLIDES, start=1):
            deck.writestr(f"ppt/slides/slide{index}.xml", slide_xml(index, title, bullets))
            deck.writestr(f"ppt/slides/_rels/slide{index}.xml.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>')


if __name__ == "__main__":
    write_deck()
    print(f"wrote {OUT}")

"""Create original, evidence-anchored Midnight hackathon video + slide deck.
Source of truth: GitHub Actions run 44900372695. No testnet/deploy claim."""
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Inches
from pathlib import Path
import asyncio, subprocess, json, os, re, math, textwrap
import edge_tts

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'media'
OUT.mkdir(parents=True,exist_ok=True)
W,H=1280,720
NAVY=(8,14,33); INK=(240,246,255); MUTED=(155,180,204); CYAN=(72,222,224); VIOLET=(138,105,255)
FONT_B='C:/Windows/Fonts/segoeuib.ttf'
FONT='C:/Windows/Fonts/segoeui.ttf'
FONT_M='C:/Windows/Fonts/consola.ttf'
def f(n,bold=False,mono=False):
    return ImageFont.truetype(FONT_M if mono else (FONT_B if bold else FONT),n)
def lines(draw,text,font,maxw):
    out=[]
    for para in text.split('\n'):
        if not para.strip():
            out.append('');continue
        row=''
        for word in para.split():
            candidate=(row+' '+word).strip()
            if draw.textbbox((0,0),candidate,font=font)[2]>maxw and row:
                out.append(row);row=word
            else:row=candidate
        if row:out.append(row)
    return out
def printlines(d,text,x,y,width,size=27,color=INK,spacing=15,bold=False,mono=False):
    ff=f(size,bold,mono); ll=lines(d,text,ff,width)
    for line in ll:
        d.text((x,y),line,font=ff,fill=color)
        y+=size+spacing
    return y
def box(d,xy,fill=(20,32,61),outline=(49,80,115),r=22):
    d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=2)
def scene(n,kicker,title,lead,cards,footer,narration):
    im=Image.new('RGB',(W,H),NAVY);d=ImageDraw.Draw(im)
    # no stock graphics: all shapes original and generated for this project
    for a in range(0,1281,48):d.line((a,0,a,720),fill=(14,24,47),width=1)
    for b in range(0,721,48):d.line((0,b,1280,b),fill=(14,24,47),width=1)
    d.rounded_rectangle((66,45,390,90),radius=14,fill=(22,54,84))
    d.text((86,56),kicker.upper(),font=f(20,True),fill=CYAN)
    d.text((70,116),title,font=f(54,True),fill=INK)
    printlines(d,lead,72,192,1130,25,MUTED,12)
    y=296
    if len(cards)==3:
        cw=358
        for i,(head,body) in enumerate(cards):
            x=70+i*384;box(d,(x,y,x+cw,600))
            d.rounded_rectangle((x+22,y+24,x+57,y+59),radius=8,fill=VIOLET if i==1 else CYAN)
            d.text((x+72,y+21),head,font=f(26,True),fill=INK)
            printlines(d,body,x+24,y+102,cw-48,23,INK,14)
    elif len(cards)==2:
        for i,(head,body) in enumerate(cards):
            x=70+i*576;box(d,(x,y,x+550,600))
            d.text((x+28,y+26),head,font=f(27,True),fill=CYAN if i==0 else VIOLET)
            printlines(d,body,x+28,y+94,490,24,INK,15,mono=('compact' in head.lower()))
    else:
        head,body=cards[0];box(d,(70,y,1210,600))
        d.text((95,y+24),head,font=f(28,True),fill=CYAN)
        printlines(d,body,95,y+85,1070,28,INK,14,mono=('code' in head.lower()))
    d.line((70,649,1210,649),fill=(46,90,117),width=2)
    d.text((70,663),'LUXEDIGITALNEST  /  MIDNIGHT PRIVATE QUEST RECEIPTS',font=f(17,True),fill=MUTED)
    d.text((1114,662),f'{n:02d} / 07',font=f(18,True),fill=CYAN)
    path=OUT/f'frame_{n:02d}.png';im.save(path,optimize=True)
    return {'image':str(path),'script':narration,'footer':footer}
S=[
scene(1,'OPEN SOURCE / BUILDATHON','PRIVATE QUEST RECEIPTS',
      'Proof of task completion without publishing a full personal activity history.',
      [('REAL COMPACT SOURCE','Original Midnight Compact smart contract, Apache 2 license.'),
       ('VERIFIED CI','Compact 0.36.1 successfully compiled one circuit.'),
       ('SIX PASSING TESTS','Six real generated-runtime tests; zero failures.')],
      'Source: github.com/luxedigitalnest/ldn-midnight-private-quest-receipts',
      'Welcome to Private Quest Receipts from LuxeDigitalNest. This is an original privacy-focused prototype built in Midnight Compact. We have a genuine compiled contract, and six runtime tests that pass. We will show what is verified, how it works, and what is still unfinished.'),
scene(2,'THE PROBLEM','PROVE LESS, REVEAL LESS',
      'A task-completion receipt should not become a permanent public activity dossier.',
      [('TODAY','Accounts, addresses, timestamps and off-chain histories can expose more than the verifier needs.'),
       ('OUR DESIGN','Use a private receipt secret with an issuer-approved commitment and a published one-time nullifier.'),
       ('IMPORTANT LIMIT','Possessing a secret alone is not proof of completing a real task. Trusted issuance remains necessary.')],
      'Threat model: exposure of excess public metadata',
      'Many reward programs demand identities and activity histories to validate a single completion. Our design tries to minimize disclosure. The verifier checks a commitment and a one-time nullifier. However, a commitment without trustworthy issuer authentication cannot establish real off-chain completion.'),
scene(3,'SYSTEM DESIGN','THREE PARTS',
      'The initial contract protects a receipt witness, but does not yet implement a multi-issuer service.',
      [('ISSUER','Creates one approved commitment at contract initialization. Multi-issuer support is future work.'),
       ('PARTICIPANT','Supplies a private thirty-two-byte receipt witness to the Compact circuit.'),
       ('VERIFIER','Checks matching commitment and unused nullifier; records only the nullifier as public state.')],
      'One commitment per deployment / proof client is not yet deployed',
      'The small system has three parts. An issuer approves a commitment when a contract is created. A participant provides a private secret to the circuit. The contract checks that commitment and rejects a nullifier after it has been redeemed once. The current source supports one commitment per deployment.'),
scene(4,'SOURCE WALKTHROUGH','COMPACT CONTRACT',
      'Original Compact code: two domain-separated hashes, an approved commitment, and replay prevention.',
      [('CORE CIRCUIT','redeem(secret: Bytes<32>)\nassert(hash(secret) == approvedCommitment)\nassert(!redeemedNullifiers.member(nullifier))\nredeemedNullifiers.insert(nullifier)')],
      'Full exact implementation: contract/private-quest-receipt.compact',
      'The source has one redeem circuit. It derives a domain-separated receipt commitment from the secret, checks the approved commitment, then derives a different nullifier. If that nullifier is already present, the call rejects. Otherwise it inserts the nullifier. These source lines are condensed on screen; the full contract is in GitHub.'),
scene(5,'INDEPENDENT EVIDENCE','COMPILER + TESTS PASS',
      'GitHub Actions checked the actual generated Compact runtime, not mocked business logic.',
      [('COMPILER','Version 0.36.1\nCompiling 1 circuits\nJob conclusion: SUCCESS'),
       ('NODE TEST RUN','tests 6\npass 6\nfail 0\nRun: 44900372695')],
      'github.com/luxedigitalnest/ldn-midnight-private-quest-receipts/actions/runs/44900372695',
      'Here is independent build evidence. GitHub Actions installed the official Compact version zero point thirty-six point one, compiled one circuit, and ran the Node test suite. Six tests passed and zero failed. This is verifiable from the public workflow run linked in the project.'),
scene(6,'REPLAY + PRIVACY','WHAT THE TESTS ACTUALLY SHOW',
      'In-memory execution verifies positive and negative cases; it is not a generated ZK proof.',
      [('PASS: VALID','Correct private secret can be redeemed, and the public ledger contains the nullifier.'),
       ('PASS: REJECTION','Wrong secrets fail, repeat redemption fails, and secret bytes are absent from public ledger fields.'),
       ('NOT YET PROVEN','No deployed on-chain receipt, generated ZK proof, or security audit exists at this stage.')],
      'All tests: tests/receipt.test.mjs / 6 passed',
      'Our tests cover one valid redemption, rejection of a wrong secret, rejection of a duplicate redemption, and inspection of exposed ledger fields. The private receipt bytes are not present in those public fields. These are real in-memory generated-contract tests, not cryptographic proof generation or deployment claims.'),
scene(7,'ROADMAP / DEMO END','WHAT HAPPENS NEXT',
      'Transparent milestone status: compiler and behavioral tests complete; network verification remains.',
      [('DONE','Original contract source, open repository, license, CI, six green runtime tests.'),
       ('NEXT','Generate ZK proof; deploy with ledger-nine-compatible toolchain; verify transactions and costs.'),
       ('BEFORE PRODUCTION','Authenticate issuers, assess metadata leakage, complete security and accessibility reviews.')],
      'Project repository: github.com/luxedigitalnest/ldn-midnight-private-quest-receipts',
      'This is a compiler-verified source prototype, not a deployed product. Next we need live ZK proof execution, a testnet transaction, issuer authentication and further security review. The repository, contract, all six tests and the exact evidence are open for inspection. Thanks for reviewing Private Quest Receipts.'),
]
# Original slide deck (PDF and PowerPoint) - each slide fully fits its 16:9 viewport
pdf_images=[Image.open(x['image']).convert('RGB') for x in S]
pdf_images[0].save(OUT/'LDN_Private_Quest_Receipts_Pitch_Deck.pdf','PDF',save_all=True,append_images=pdf_images[1:],resolution=130)
ppt=Presentation();ppt.slide_width=Inches(13.333);ppt.slide_height=Inches(7.5)
for x in S:
    slide=ppt.slides.add_slide(ppt.slide_layouts[6])
    slide.shapes.add_picture(x['image'],0,0,width=ppt.slide_width,height=ppt.slide_height)
ppt.save(OUT/'LDN_Private_Quest_Receipts_Pitch_Deck.pptx')
async def tts():
    for i,s in enumerate(S,1):
        name=OUT/f'voice_{i:02d}.mp3'
        await edge_tts.Communicate(s['script'],voice='en-US-ChristopherNeural',rate='-6%').save(str(name))
        print('TTS',i,name.stat().st_size,flush=True)
def execute(args):subprocess.run(args,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
asyncio.run(tts())
mp4s=[]
for i,s in enumerate(S,1):
    a=OUT/f'voice_{i:02d}.mp3';v=OUT/f'clip_{i:02d}.mp4'
    dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(a)],capture_output=True,check=True,text=True).stdout.strip())+0.4
    execute(['ffmpeg','-y','-loglevel','error','-loop','1','-framerate','24','-i',s['image'],'-i',str(a),'-t',str(dur),'-vf','format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','24','-r','24','-c:a','aac','-b:a','160k','-movflags','+faststart',str(v)])
    mp4s.append(v);print('VIDEO segment',i,round(dur,2),flush=True)
with open(OUT/'concat.txt','w',encoding='utf-8') as o:
    for p in mp4s:o.write("file '"+p.name+"'\n")
execute(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-c','copy','-movflags','+faststart',str(OUT/'LDN_Private_Quest_Receipts_Genuine_Technical_Walkthrough.mp4')])
final=OUT/'LDN_Private_Quest_Receipts_Genuine_Technical_Walkthrough.mp4'
probe=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(final)],capture_output=True,check=True,text=True)
summary=json.loads(probe.stdout)
print('DONE',str(final),final.stat().st_size, summary['format'].get('duration'), [(st.get('codec_type'),st.get('codec_name')) for st in summary['streams']],flush=True)

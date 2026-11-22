import re,sys
S=open('vow-id-starthilfe.html',encoding='utf-8').read()
E=open('vow-id-einsteiger.html',encoding='utf-8').read()
def sec(src,i):
    m=re.search(r'<section id="%s">.*?</section>'%i,src,re.S); assert m,i; return m.group(0)
def dl(src):
    return re.search(r'<dl>(.*?)</dl>',sec(src,'begriffe'),re.S).group(1)
css=r'''
/* Layout: one narrow column for phones; a short contents row, then six numbered parts of tickable steps, then the searchable questions, fixes, and reference sections. */
:root{
  --bg:#F2F5F4; --surface:#FFFFFF; --fg:#13222A; --muted:#55666E; --line:#D5DEDC;
  --accent:#0A6B6B; --accent-soft:#DDEEEC; --warn:#9A5B00; --warn-soft:#FBEFD9; --ok:#1B7A4B; --bad:#A3302B;
  --display:"Space Grotesk","Inter",system-ui,sans-serif; --body:"Inter",system-ui,-apple-system,"Segoe UI",sans-serif;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#0E171B; --surface:#162228; --fg:#E3ECEB; --muted:#9BADB2; --line:#2A3A41;
  --accent:#56C7BC; --accent-soft:#17343A; --warn:#F0B55A; --warn-soft:#33290F; --ok:#5FCB92; --bad:#F08A84; color-scheme:dark } }
:root[data-theme="dark"]{
  --bg:#0E171B; --surface:#162228; --fg:#E3ECEB; --muted:#9BADB2; --line:#2A3A41;
  --accent:#56C7BC; --accent-soft:#17343A; --warn:#F0B55A; --warn-soft:#33290F; --ok:#5FCB92; --bad:#F08A84; color-scheme:dark }
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);font-family:var(--body);font-size:16px;line-height:1.55;
  padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:24px 56px}
.wrap{max-width:700px;margin:0 auto;display:flex;flex-direction:column;gap:36px;counter-reset:st}
h1,h2,h3{font-family:var(--display);text-wrap:balance;margin:0;line-height:1.2}
h1{font-size:clamp(1.9rem,7vw,2.6rem);font-weight:700;letter-spacing:-.01em}
h2{font-size:1.4rem;font-weight:600}
h3{font-size:1.04rem;font-weight:600}
p{margin:0}
a{color:var(--accent)}
ul{margin:0;padding-left:20px}
.eyebrow{font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:600}
.lead{font-size:1.06rem;color:var(--muted)}
header,section{display:flex;flex-direction:column;gap:14px}
section{scroll-margin-top:16px}
nav{display:flex;flex-wrap:wrap;gap:8px}
nav a{font-size:.88rem;text-decoration:none;padding:6px 12px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--fg)}
nav a:hover{border-color:var(--accent);color:var(--accent)}
.need,.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}
.need div,.fact{border-top:2px solid var(--accent);padding-top:8px;font-size:.9rem;color:var(--muted)}
.need b,.fact b{display:block;font-family:var(--display);font-size:1.05rem;color:var(--fg)}
.fact span{font-size:.88rem}
.progress{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px;display:flex;flex-direction:column;gap:8px}
.bar{height:8px;border-radius:99px;background:var(--line);overflow:hidden}
.bar i{display:block;height:100%;width:0;background:var(--accent);transition:width .2s}
@media (prefers-reduced-motion: reduce){.bar i{transition:none}}
.progress span{font-size:.9rem;color:var(--muted);font-variant-numeric:tabular-nums}
.part{font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);font-weight:600}
.steps{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}
.step{counter-increment:st;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px;display:flex;flex-direction:column;gap:8px}
.step h3::before{content:counter(st) ". "}
.step>label{display:flex;gap:8px;align-items:center;font-size:.88rem;color:var(--muted);cursor:pointer;align-self:flex-start;margin-top:2px}
.step input{width:18px;height:18px;accent-color:var(--accent)}
input:focus-visible,a:focus-visible,button:focus-visible,summary:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.step.done{border-color:var(--ok)}
.step.done h3{color:var(--ok)}
.note{background:var(--warn-soft);border-radius:10px;padding:12px 14px;font-size:.94rem}
.note b{color:var(--warn)}
.status{background:var(--accent-soft);border-radius:10px;padding:14px;display:flex;flex-direction:column;gap:8px;font-size:.95rem}
.status b{color:var(--accent)}
.dodont{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}
.dodont div{border-radius:10px;padding:12px 14px;background:var(--bg);border:1px solid var(--line);min-width:0}
.dodont b{display:block;margin-bottom:4px}
.yes b{color:var(--ok)} .no b{color:var(--bad)}
.ask{display:flex;flex-direction:column;gap:8px;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px}
.ask label{font-family:var(--display);font-weight:600}
.ask input{width:100%;font:inherit;padding:12px 14px;border-radius:10px;border:1.5px solid var(--line);background:var(--bg);color:var(--fg)}
.ask small{color:var(--muted)}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chips button{font:inherit;font-size:.86rem;padding:6px 12px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--fg);cursor:pointer}
.chips button:hover{border-color:var(--accent);color:var(--accent)}
.cat{font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:600;margin-top:10px}
details{background:var(--surface);border:1px solid var(--line);border-radius:10px}
.step details{background:var(--bg)}
summary{cursor:pointer;padding:12px 14px;font-weight:600;list-style:none;display:flex;justify-content:space-between;gap:12px}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";color:var(--accent);font-family:var(--display);font-weight:700;flex:none}
details[open] summary::after{content:"–"}
details .a{padding:0 14px 14px;display:flex;flex-direction:column;gap:8px}
#faqlist,#fixlist{display:flex;flex-direction:column;gap:8px}
#hits{font-size:.9rem;color:var(--muted)}
.addr{list-style:none;padding:0;display:flex;flex-direction:column;gap:6px}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.82rem;overflow-wrap:anywhere;user-select:all}
dl{margin:0;display:grid;grid-template-columns:minmax(100px,max-content) 1fr;gap:8px 16px}
dt{font-family:var(--display);font-weight:600}
dd{margin:0;min-width:0;color:var(--muted)}
footer{font-size:.84rem;color:var(--muted);border-top:1px solid var(--line);padding-top:16px;display:flex;flex-direction:column;gap:6px}
@media (max-width:420px){ dl{grid-template-columns:1fr;gap:2px 0} dd{margin-bottom:8px} }
'''
# how-to parts from E
t1,t2,t3=sec(E,'teil1'),sec(E,'teil2'),sec(E,'teil3')
t5=sec(E,'teil4').replace('id="teil4"','id="teil5"').replace('>Teil 4<','>Teil 5<')
t6=sec(E,'teil5').replace('id="teil5"','id="teil6"').replace('>Teil 5<','>Teil 6<')
t3=re.sub(r'\s*<p>Wie es danach weitergeht.*?</p>','',t3,flags=re.S)
old='<p>Welche Dienste Mitglieder dafür nutzen, steht in der Starthilfe unter „Woher bekomme ich VOW zum Einlösen?".</p>'
assert old in t6
t6=t6.replace(old,'<p>Welche Wege Mitglieder dafür nutzen, steht weiter unten bei den <a href="#fragen">häufigen Fragen</a> unter „Woher bekomme ich VOW zum Einlösen?".</p>')
t4='''<section id="teil4">
  <span class="part">Teil 4</span>
  <h2>Der erste Einkauf</h2>
  <p>Jetzt verbindest du Vow.id mit einem Shop, bei dem du ohnehin einkaufst. Fang mit einem einzigen Anbieter an.</p>
  <ol class="steps">
    <li class="step"><h3>Anbieter auswählen</h3>
      <p>Öffne Member Rewards → Checklist und wähle dein Land. Markiere nur die Anbieter, die du wirklich nutzt. Die Liste ist deine Merkliste; vergessene Anbieter ergänzt du später über „Edit services".</p>
      <label><input type="checkbox" id="s15"> Erledigt</label></li>
    <li class="step"><h3>Belege freischalten</h3>
      <p>Öffne „Receipts &amp; MR rights". Schalte „Collect MR rights" ein, setze das Häkchen bei „I have read and agree" und bestätige. „Shopping insights" ist freiwillig und bringt dir für deine Rewards nichts.</p>
      <label><input type="checkbox" id="s16"> Erledigt</label></li>
    <li class="step"><h3>E-Mail bei einem Shop umstellen und einkaufen</h3>
      <p>Am einfachsten ist Amazon: Trage dort unter „Anmelden &amp; Sicherheit" deine name@vow.id als Konto-E-Mail ein. Den Bestätigungscode bekommst du in dein normales Postfach weitergeleitet. Deine Mails liest du weiter dort.</p>
      <p>Kaufe dann ganz normal ein. Der Kauf erscheint unter Member Rewards → MR, zunächst mit dem Status „Pending" („Ausstehend").</p>
      <p class="note"><b>Nicht umstellen:</b> Google (und damit YouTube), Apple, Microsoft und deine Bank. Die @vow.id-Adresse nimmt nur Mails anerkannter Shops an. Bei anderen Konten können Sicherheits-Mails verloren gehen.</p>
      <label><input type="checkbox" id="s17"> Erledigt</label></li>
  </ol>
</section>'''
howto='\n\n'.join([t1,t2,t3,t4,t5,t6])
howto=re.sub(r'<h3>\d+\. ','<h3>',howto)
kurz=sec(S,'kurz')
kurz=re.sub(r'\s*<p class="note"><b>Sicherheit zuerst:.*?</p>','',kurz,flags=re.S)
kurz=kurz.replace('<h2>Das Wichtigste vorab</h2>','<h2>Was ist Vow.id?</h2>')
gl_e=dl(E); gl_s=re.sub(r'\s*<dt>BNB</dt><dd>.*?</dd>','',dl(S),flags=re.S)
begriffe='<section id="begriffe">\n  <h2>Begriffe in einem Satz</h2>\n  <dl>'+gl_e.rstrip()+gl_s+'</dl>\n</section>'
js_s=re.search(r'<script>(.*?)</script>',S,re.S).group(1)
js_s=js_s[:js_s.index('document.querySelectorAll("#check input")')]
js_e=re.search(r'<script>(.*?)</script>',E,re.S).group(1).replace('voweinst-','vowkomplett-')
head='''<title>Vow.id Komplettanleitung</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap">
<style>'''+css+'''</style>

<div class="wrap">
<header>
  <span class="eyebrow">Inoffizielle Anleitung · Stand 22. November 2026</span>
  <h1>Von null zu deiner Vow.id</h1>
  <p class="lead">Alles auf einer Seite, auch wenn du noch nie mit Krypto zu tun hattest: Wallet einrichten und absichern, bei Vow.id registrieren, den ersten Einkauf erfassen. Darunter stehen die Antworten auf die Fragen, die fast jeder stellt, und Hilfe, wenn etwas hakt.</p>
  <div class="need">
    <div><b>Etwa eine Stunde</b>ohne Zeitdruck, in deinem Tempo</div>
    <div><b>Smartphone</b>mit aktuellem System und Bildschirmsperre</div>
    <div><b>Stift und Papier</b>für deine Seed-Phrase</div>
    <div><b>Ein paar Euro</b>für die Netzwerkgebühr in BNB</div>
  </div>
  <nav aria-label="Inhalt">
    <a href="#kurz">Was ist Vow.id?</a><a href="#teil1">Wallet</a><a href="#teil2">BNB</a><a href="#teil3">Registrieren</a><a href="#teil4">Erster Einkauf</a><a href="#teil5">Token</a><a href="#teil6">Krypto kaufen</a><a href="#fragen">Fragen</a><a href="#hilfe">Hilfe</a><a href="#begriffe">Begriffe</a>
  </nav>
  <p class="note"><b>Die eine Regel, die alles schützt:</b> Deine Seed-Phrase gibst du niemals weiter und tippst sie nirgends ein, außer beim Wiederherstellen in deiner eigenen Wallet-App. Kein Support, keine Website und kein Bekannter braucht sie. Das gilt auch für deine E-Mail-PIN und deinen Bank-Code.</p>
</header>

'''
prog='''<section id="weg">
  <h2>Dein Weg in 17 Schritten</h2>
  <p>Hak ab, was erledigt ist. Dein Fortschritt bleibt auf diesem Gerät gespeichert. Hast du schon eine Wallet mit etwas BNB, beginne bei Teil 3.</p>
  <div class="progress"><div class="bar"><i id="bar"></i></div><span id="count">0 von 17 Schritten erledigt</span></div>
</section>

'''
ask='''<section id="fragen">
  <h2>Häufige Fragen</h2>
  <div class="ask">
    <label for="q">Was möchtest du wissen?</label>
    <input id="q" type="search" placeholder="z. B. Wie lese ich dann meine Mails?" autocomplete="off">
    <small id="hits">Tippe eine Frage oder ein Stichwort. Die passenden Antworten erscheinen sofort.</small>
    <div class="chips" id="chips">
      <button type="button" data-q="Geld sparen verdienen">Was bringt es?</button>
      <button type="button" data-q="Pending">Pending MR</button>
      <button type="button" data-q="Mails lesen">Mails lesen</button>
      <button type="button" data-q="Kosten">Kosten</button>
      <button type="button" data-q="Bank">Bank</button>
      <button type="button" data-q="Zweifel Risiko">Zweifel</button>
      <button type="button" data-q="">Alle Fragen</button>
    </div>
  </div>
  <div id="faqlist"></div>
</section>'''
foot='''<footer>
  <p>Diese Seite ist eine private, inoffizielle Anleitung und stammt nicht von Vow.id, N888 LIMITED oder einem Wallet-Anbieter. Sie ist keine Anlageberatung. Sie fasst die AGB und die Datenschutzerklärung von vow.id (Stand 20.11.2026) und die „New User Overview" (Ausgabe 11 vom 21.11.2026) zusammen.</p>
  <p>Wo eine Antwort auf Erfahrungen von Mitgliedern beruht und nicht auf den offiziellen Unterlagen, steht das dabei. Apps und Bildschirme ändern sich; im Zweifel gilt, was deine Wallet und vow.id selbst anzeigen.</p>
  <p>Wenn du nicht weiterkommst, schreib der Person, die dir diese Seite geschickt hat. Schick dabei nie deine Seed-Phrase, deine PIN oder einen Code mit.</p>
</footer>
</div>
'''
hilfe=sec(S,'hilfe')
out=head+kurz+'\n\n'+prog+howto+'\n\n'+ask+'\n\n'+hilfe+'\n\n'+sec(E,'freigaben')+'\n\n'+sec(E,'fehler')+'\n\n'+sec(S,'quellen')+'\n\n'+begriffe+'\n\n'+sec(S,'risiken')+'\n\n'+foot+'\n<script>'+js_s+js_e+'</script>\n'
out=out.replace('document.getElementById("fragen").scrollIntoView({behavior:"smooth"})','document.getElementById("faqlist").scrollIntoView({behavior:"smooth",block:"nearest"})')
open('vow-id-komplett.html','w',encoding='utf-8').write(out)
print(len(out),out.count('class="step"'),out.count('<section'))

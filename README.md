# SAST, DAST und Container Scan Pipeline
## Struktur und Fehlerpunkte der Anwendung
- explizit kein fokus auf Sicherheit
- Ziel ist das Testen der Scans
- Einfacher Nodeserver
- Stellt Home, Contact und About Page bereit
- Läuft in einem Container
- Genutze Sprache: Js

**Konkret eingebaute Schwachstellen:**
- Alte Node Version im Container Node:14 (Dockerfile Zeile)
- API Schlüssel in der Server.js (Zeile 5)
- Cross Site Scripting Server.js (Zeile 57)
- Keine CSRF Protection
- Kein Rate Limiting
- Nur HTTP kein HTTPS 

**Cross-Site Scripting**
> Angreifer schleust schädlichen Code in ungesicherten Anmeldeforumlaren oder Suchfeldern ein. Wenn andere Nutzer die Seite aufrufen wird der Code bei ihnen aufgerufen. => Angreifer kann Sitzungstokens stehlen. 
Beispiel Reflected XSS:
Angreifer baut bösartige URL mit einem Script und schickt link an Opfer. 
Opferbrowser rendert führt Script aus

**CSRF Protection (Crross-Site Request Forgery)**
> Angreifer nutzt legitime Sitzung aus um unerwünschte Aktionen durchzuführen. 
Anmeldung auf vertrauenswürdiger Website, besuchen einer manipulierten Seite während man immernoch eingeloggt ist. Manipulierte Seite löst im Hintergrund eine Request an die vertrauenswürdige Seite aus. cookies werden vom Browser geteilt. Server/vertrauenswürdige Website denkt das ist echt und führt Aktion aus
Schutz dagegen: CSRF Token, Anfragen die etwas ändern, enthalten zufälligen Token


**Rate Limiting**
> Wie viele Anfragen kann ein Angreifer innerhalb kurzer Zeit machen. Schützt gegen Bruteforce, Spam und Dos


# Findings 

## SAST (Semgrep)

> Verfahren Anwendungen auf Sicherheitslücken zu testen ohne diese auszuführen. Hierfür wird der Quellcode statisch anaylsiert.
Deshalb die Annahme: SAST wird insbesondere den API Key finden

``` 
Detected directly writing to a Response object from user-defined input. This bypasses any HTML escaping and may expose your application to a Cross-Site-scripting (XSS) vulnerability.                                     
Instead, use 'resp.render()' to render safely escaped HTML.           
Details: https://sg.run/vzGl                                          
                                                                    
59┆ res.send(`<h1>Search Results for: ${query}</h1>`);
```

```
User data flows into the host portion of this manually-constructed HTML. This can introduce a Cross-Site-Scripting (XSS) vulnerability if this comes
from user-provided input. Consider using a sanitization library such as DOMPurify to sanitize the HTML within.                                                                       
Details: https://sg.run/5DO3                                          
            
59┆ res.send(`<h1>Search Results for: ${query}</h1>`);
```
=> Semgrep findet Crosssite Scripting, findet aber nicht den APIKey. 

## Container Security (Trivy)
> Analysiert die Container Images in einem Projekt. 
Annahme: Er wird die alte Node Version im Dockerfile finden.

**Zusätzlich findet er auch den APIkey**
```
 ================================
Total: 1 (MEDIUM: 0, HIGH: 0, CRITICAL: 1)

CRITICAL: Stripe (stripe-secret-token)
════════════════════════════════════════
Stripe Secret Key
────────────────────────────────────────
 /usr/src/app/server.js:5 (added by 'COPY . . # buildkit')
────────────────────────────────────────
   3             const PORT = 3000;
   4   
   5 [           const API_KEY = '************************';
   6   
────────────────────────────────────────
```
## OWASP ZAP DAST Scan
> DAST: Dynamic Application Testing. Soll sicherheitslücken in laufenden Anwendungen finden. DAST Tools schicken u.a SQL Injects an die Anwendung um die Reaktion zu analysiern.
Annahme: SQL Injects, Cross Site Scriping usw sollten von diesem Scan gefunden werden. 

Im Scan selber:
```
WARN-NEW: Storable and Cacheable Content [10049] x 8 
	http://localhost:3000 (200 OK)
	http://localhost:3000/about (200 OK)
	http://localhost:3000/api/users (200 OK)
	http://localhost:3000/contact (200 OK)
	http://localhost:3000/robots.txt (404 Not Found)
``` 
Erläuterung im Report:
> Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks, including __Cross Site Scripting__ (XSS) and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. CSP provides a set of standard HTTP headers that allow website owners to declare approved sources of content that browsers should be allowed to load on that page — covered types are JavaScript, CSS, HTML frames, fonts, images and embeddable objects such as Java applets, ActiveX, audio and video files.



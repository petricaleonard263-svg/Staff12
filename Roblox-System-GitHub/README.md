# Roblox System – VS Code + GitHub + Rojo

## Ce face
Proiectul păstrează structura `System` și conectează fișierele locale la serviciile Roblox. **Rojo creează automat Script / LocalScript / ModuleScript**, cu același nume și același cod, când e conectat la Roblox Studio. Schimbările salvate în VS Code se sincronizează în Studio; nu trebuie să apeși Play pentru a le copia. `Play` doar execută scripturile din locurile în care Roblox permite execuția.

**Important:** GitHub NU transmite singur schimbările în Studio și codul nu se descarcă din GitHub în timpul jocului. Pentru GitHub folosești Git push/pull, iar pentru Studio folosești Rojo (serverul trebuie pornit și pluginul conectat). Nu încărca parole, tokenuri ori cod de administrare în repo public.

## Instalare (Windows)
1. Dezarhivează proiectul și deschide folderul `Roblox-System-GitHub` în **Visual Studio Code**.
2. Instalează extensia [Rojo pentru VS Code](https://marketplace.visualstudio.com/items?itemName=evaera.vscode-rojo). Dacă cere instalarea Rojo, acceptă. Instalează și **pluginul Rojo pentru Roblox Studio** folosind meniul extensiei (o singură dată). Sau instalează Rojo CLI și rulează `rojo plugin install`.
3. Deschide jocul tău în Roblox Studio. Din VS Code apasă **Ctrl+Shift+P** → **Rojo: Open Menu** → pornește proiectul `default.project.json` / **Start server**.
4. În Roblox Studio: **Plugins → Rojo → Connect** la serverul local (de obicei port 34872).
5. În Explorer vei vedea folderele și scripturile. Apasă **Play**. În Output apar mesaje `[Loader]` și `[System]`.
6. Modifică fișierele din `src/System` în VS Code și apasă **Ctrl+S**: apar în Studio fără copiere manuală.

> Înainte de prima conectare fă o copie de siguranță a jocului. Rojo sincronizează zonele gestionate de proiect și poate șterge sau înlocui elemente care intră în conflict în acele zone. Pentru un joc existent, testează întâi într-o copie.

## Structura în Roblox Studio

```text
ReplicatedFirst
  Loading                         (LocalScript)
ReplicatedStorage
  SharedInfo                      (ModuleScript)
ServerScriptService
  Anticheat                       (Folder)
    Config                        (Folder)
      Settings                    (ModuleScript)
    Loader                        (ModuleScript)
    Version                       (ModuleScript)
  AnticheatBoot                   (Script)
  ExampleServer                   (Script)
ServerStorage
  ExampleSavedModule              (ModuleScript)
StarterGui
StarterPack
StarterPlayer
  StarterCharacterScripts
    CharacterWelcome              (LocalScript)
  StarterPlayerScripts
    ExampleClient                 (LocalScript)
```

## Cum adaugi propriul script
- Creezi `src/System/ServerScriptService/Coins.server.luau`: în Studio apare automat un **Script** `Coins` în `ServerScriptService`; rulează la Play.
- Creezi `src/System/ServerStorage/Items.luau`: apare automat **ModuleScript** `Items` în `ServerStorage`; ca să ruleze folosește `require(game.ServerStorage.Items)` dintr-un Script de server.
- Creezi `src/System/StarterPlayer/StarterPlayerScripts/HUD.client.luau`: apare **LocalScript** `HUD` și rulează pe client.
- Creezi `src/System/ReplicatedStorage/Config.luau`: apare **ModuleScript** `Config`, disponibil clientului și serverului.
- Pentru foldere în interiorul unui serviciu: creează un subfolder local; Rojo îl transformă într-un `Folder` Roblox.
- Pentru StarterGui/StarterPack poți adăuga fișiere `.client.luau`, `.server.luau`, `.luau`, sau modele cu format Rojo; folderul gol nu generează un obiect vizibil.

**Regulă:** `Nume.server.luau` = Script; `Nume.client.luau` = LocalScript; `Nume.luau` = ModuleScript. Un fișier în `ServerStorage` nu execută singur, chiar dacă e `Script`. Un `ModuleScript` nici el nu rulează până nu e folosit cu `require`.

## Loader / Settings / Version
`ServerScriptService/AnticheatBoot.server.luau` pornește `Anticheat.Loader.Start()` la Play.
`Anticheat/Config/Settings.luau` ține setări (Enable/Debug, prag WalkSpeed), iar `Anticheat/Version.luau` ține versiunea. Este un exemplu **minimal de demonstrație**, nu un anti-cheat complet sau infailibil. `KickOnInvalidWalkSpeed = false` implicit pentru a evita eliminări accidentale.

## GitHub
Creează un repository nou gol pe GitHub, apoi deschide Terminal în acest folder:

```powershell
git init
git add .
git commit -m "Initial Roblox system"
git branch -M main
git remote add origin https://github.com/UTILIZATOR/NUME-REPO.git
git push -u origin main
```

Înlocuiește `UTILIZATOR` și `NUME-REPO`. La următoarele modificări:

```powershell
git add .
git commit -m "Update scripts"
git push
```

Când lucrezi de pe alt PC: `git pull` pentru a aduce ultima versiune, apoi conectezi Rojo la Studio. GitHub nu înlocuiește conexiunea locală Rojo.

## Limitări importante
- Doar fișierele aflate în zonele mapate în `default.project.json` se sincronizează.
- Dacă ai obiecte construite manual în Studio, sincronizarea lor înapoi în VS Code nu este garantată prin Rojo.
- Nu folosi `loadstring` și URL-uri GitHub brute ca mecanism de injectare la Play. Proiectul lucrează cu surse locale, revizuibile și versionate.
- Dacă vrei un joc complet construit din repo, instalează și CLI Rojo, apoi rulează `rojo build -o joc.rbxlx`.

param(
    [string]$Deck = "SVD_Presentation2/index.html",
    [int[]]$Slide,
    [string[]]$Id,
    [switch]$All,
    [switch]$Render,
    [string]$OutDir = "output/browser-slides",
    [int]$Width = 2048,
    [int]$Height = 1152,
    [int]$WaitMs = 10000
)

$ErrorActionPreference = "Stop"

function Find-Chrome {
    $candidates = @(
        "C:\Program Files\Google\Chrome\Application\chrome.exe",
        "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    )
    foreach ($candidate in $candidates) {
        if (Test-Path $candidate) {
            return $candidate
        }
    }
    throw "No supported browser found. Install Chrome or Edge, or update Find-Chrome in this script."
}

function Get-SlideIds([string]$HtmlPath) {
    $html = Get-Content -Raw -LiteralPath $HtmlPath
    $matches = [regex]::Matches($html, '<section id="([^"]+)" class="slide level2')
    $ids = @()
    foreach ($match in $matches) {
        $ids += $match.Groups[1].Value
    }
    if ($ids.Count -eq 0) {
        throw "No Reveal slide sections found in $HtmlPath."
    }
    return $ids
}

if ($Render) {
    quarto render "SVD_Presentation2/index.qmd"
}

$deckPath = Resolve-Path -LiteralPath $Deck
$deckDir = Split-Path -Parent $deckPath
$slideIds = Get-SlideIds $deckPath
$browser = Find-Chrome

$outRoot = New-Item -ItemType Directory -Force -Path $OutDir

$targets = @()
if ($All) {
    for ($i = 0; $i -lt $slideIds.Count; $i++) {
        $targets += [pscustomobject]@{ Number = $i + 1; Id = $slideIds[$i] }
    }
}
foreach ($n in $Slide) {
    if ($n -lt 1 -or $n -gt $slideIds.Count) {
        throw "Slide $n is outside the available range 1..$($slideIds.Count)."
    }
    $targets += [pscustomobject]@{ Number = $n; Id = $slideIds[$n - 1] }
}
foreach ($slideId in $Id) {
    if ($slideIds -notcontains $slideId) {
        throw "Slide id '$slideId' was not found. Available ids: $($slideIds -join ', ')"
    }
    $targets += [pscustomobject]@{ Number = [array]::IndexOf($slideIds, $slideId) + 1; Id = $slideId }
}
if ($targets.Count -eq 0) {
    throw "Choose at least one target: -Slide 4, -Id rotation-skalierung-rotation, or -All."
}

foreach ($target in $targets) {
    $fileName = "slide-{0:D2}-{1}.png" -f $target.Number, $target.Id
    $outPath = Join-Path $outRoot.FullName $fileName
    $uriPath = $deckPath.Path.Replace("\", "/").Replace(" ", "%20")
    $url = "file:///$uriPath#/$($target.Id)"

    & $browser `
        --headless=new `
        --disable-gpu `
        "--virtual-time-budget=$WaitMs" `
        "--window-size=$Width,$Height" `
        "--screenshot=$outPath" `
        $url | Out-Null

    Write-Output $outPath
}

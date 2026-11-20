# Scarica gli open data del Portale Offerte e li carica nel ramo "dati-grezzi" del repository.
# Da eseguire sul PC di casa alle 00:00 e alle 12:00 (Utilita di pianificazione di Windows).
# Requisiti: Git per Windows con accesso a GitHub gia configurato.
#
# Uso: powershell -ExecutionPolicy Bypass -File scarica-open-data.ps1 -Cartella C:\comparaofferte-dati

param([string]$Cartella = "$env:USERPROFILE\comparaofferte-dati")

$ErrorActionPreference = "Stop"
$base = "https://www.ilportaleofferte.it"
$repo = "https://github.com/giuseppedema94-code/comparaoffertelucegas.git"
$schemi = [ordered]@{
  "offerte_luce_placet" = "PO_Offerte_E_PLACET_(\d{8})\.csv"
  "offerte_gas_placet"  = "PO_Offerte_G_PLACET_(\d{8})\.csv"
  "parametri_luce"      = "PO_Parametri_E_(\d{8})\.csv"
  "parametri_gas"       = "PO_Parametri_G_(\d{8})\.csv"
  "offerte_luce_ml"     = "PO_Offerte_E_MLIBERO_(\d{8})\.xml"
  "offerte_gas_ml"      = "PO_Offerte_G_MLIBERO_(\d{8})\.xml"
  "offerte_dual_ml"     = "PO_Offerte_D_MLIBERO_(\d{8})\.xml"
}

function Comprimi($sorgente, $destinazione) {
  $in = [IO.File]::OpenRead($sorgente)
  $out = [IO.File]::Create($destinazione)
  $gz = New-Object IO.Compression.GZipStream($out, [IO.Compression.CompressionMode]::Compress)
  $in.CopyTo($gz); $gz.Close(); $out.Close(); $in.Close()
}

$pagina = (Invoke-WebRequest "$base/portaleOfferte/it/open-data.page" -UseBasicParsing).Content
$link = [regex]::Matches($pagina, 'href="([^"]+)"') | ForEach-Object { $_.Groups[1].Value }

$tmp = Join-Path $env:TEMP "po-open-data"
Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory $tmp | Out-Null

$data = $null
foreach ($nome in $schemi.Keys) {
  $href = $link | Where-Object { ($_ -split "/")[-1] -match "^$($schemi[$nome])$" } | Select-Object -First 1
  if (-not $href) { throw "File mancante sulla pagina Open Data: $nome" }
  $data = [regex]::Match($href, "\d{8}").Value
  $url = if ($href.StartsWith("http")) { $href } else { "$base$href" }
  Invoke-WebRequest $url -OutFile "$tmp\$nome.raw" -UseBasicParsing
}
$prezzi = $link | Where-Object { $_ -like "*/cms/documents/*.csv" } | Select-Object -First 1
if ($prezzi) {
  $url = if ($prezzi.StartsWith("http")) { $prezzi } else { "$base$prezzi" }
  Invoke-WebRequest $url -OutFile "$tmp\prezzi_storici.csv.raw" -UseBasicParsing
}

if (-not (Test-Path "$Cartella\.git")) {
  git clone --branch dati-grezzi --single-branch $repo $Cartella 2>$null
  if (-not (Test-Path "$Cartella\.git")) {
    git init -b dati-grezzi $Cartella
    git -C $Cartella remote add origin $repo
  }
}
Get-ChildItem $Cartella -Directory | Where-Object { $_.Name -match '^\d{8}$' } | Remove-Item -Recurse -Force
$dest = Join-Path $Cartella $data
New-Item -ItemType Directory $dest | Out-Null
Get-ChildItem $tmp -Filter *.raw | ForEach-Object {
  Comprimi $_.FullName (Join-Path $dest ($_.BaseName + ".gz"))
}

# Un solo commit, sempre sovrascritto: il ramo non accumula storia.
git -C $Cartella checkout --orphan nuovo 2>$null
git -C $Cartella add -A
git -C $Cartella commit -q -m "Open data $data $(Get-Date -Format 'HH:mm')"
git -C $Cartella branch -D dati-grezzi 2>$null
git -C $Cartella branch -m dati-grezzi
git -C $Cartella push -f origin dati-grezzi
Write-Output "Caricati gli open data del $data"

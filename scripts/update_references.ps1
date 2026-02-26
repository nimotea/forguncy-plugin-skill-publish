param(
    [Parameter(Mandatory=$true)]
    [string]$TargetForguncyPath
)

$ErrorActionPreference = "Stop"

function Get-ForguncyLibPath {
    param([string]$BasePath)
    
    $candidates = @(
        $BasePath,
        (Join-Path $BasePath "Website\bin"),
        (Join-Path $BasePath "Bin")
    )

    foreach ($path in $candidates) {
        if (Test-Path (Join-Path $path "GrapeCity.Forguncy.ServerApi.dll")) {
            return $path
        }
    }
    return $null
}

function Get-ForguncyExecutablePath {
    param([string]$BasePath)
    
    # Try to find Forguncy.Console.exe (common for debugging)
    $consoleExe = Join-Path $BasePath "Forguncy.Console.exe"
    if (Test-Path $consoleExe) { return $consoleExe }

    # Fallback to Designer? Or maybe user provided the Designer folder directly
    $designerExe = Join-Path $BasePath "ForguncyDesigner.exe"
    if (Test-Path $designerExe) { return $designerExe }

    return $null
}

Write-Host "Verifying Forguncy Path: $TargetForguncyPath"

if (-not (Test-Path $TargetForguncyPath)) {
    Write-Error "Path not found: $TargetForguncyPath"
}

$libPath = Get-ForguncyLibPath -BasePath $TargetForguncyPath
if (-not $libPath) {
    Write-Warning "Could not find 'GrapeCity.Forguncy.ServerApi.dll' in typical subdirectories of $TargetForguncyPath."
    Write-Warning "Will assume $TargetForguncyPath is the intended library path, but please verify."
    $libPath = $TargetForguncyPath
} else {
    Write-Host "Found libraries at: $libPath"
}

$execPath = Get-ForguncyExecutablePath -BasePath $TargetForguncyPath
if ($execPath) {
    Write-Host "Found executable at: $execPath"
}

# 1. Update .csproj files
$csprojFiles = Get-ChildItem -Filter "*.csproj" -Recurse
foreach ($csproj in $csprojFiles) {
    Write-Host "Processing $($csproj.Name)..."
    [xml]$xml = Get-Content $csproj.FullName
    $ns = @{ ns = $xml.Project.NamespaceURI }
    $changed = $false

    # Find Reference nodes with HintPath
    # Note: .NET Core SDK csproj might not have namespace in root, handling both
    $references = $xml.SelectNodes("//Reference") 
    if (-not $references) {
        $references = $xml.SelectNodes("//ns:Reference", $ns)
    }

    foreach ($ref in $references) {
        $hintPathNode = $ref.SelectSingleNode("HintPath")
        if (-not $hintPathNode) { 
            $hintPathNode = $ref.SelectSingleNode("ns:HintPath", $ns) 
        }

        # Updated Logic: 
        # 1. Use the 'Include' attribute to determine the expected DLL name. 
        #    This is more reliable than the old HintPath, especially if the old HintPath is broken (e.g. pointing to a dir).
        $includeAttr = $ref.Attributes["Include"]
        if (-not $includeAttr) { continue }
        
        # 'Include' might be "GrapeCity.Forguncy.ServerApi" or "GrapeCity.Forguncy.ServerApi, Version=..."
        $assemblyName = $includeAttr.Value.Split(',')[0].Trim()
        
        # We only care about Forguncy assemblies
        if ($assemblyName -match "GrapeCity.Forguncy" -or $assemblyName -match "^Forguncy\.") {
            $dllName = "$assemblyName.dll"
            
            $potentialNewPath = Join-Path $libPath $dllName
            $finalPath = $null

            # 1. Check primary lib path (Website\bin)
            if (Test-Path $potentialNewPath) {
                $finalPath = $potentialNewPath
            } else {
                # 2. Check designerBin path (Website\designerBin)
                # This handles design-time DLLs like GrapeCity.Forguncy.CellTypes.Design.dll
                $parentPath = Split-Path $libPath -Parent
                $designerPath = Join-Path $parentPath "designerBin"
                $potentialDesignerPath = Join-Path $designerPath $dllName
                
                if (Test-Path $potentialDesignerPath) {
                    $finalPath = $potentialDesignerPath
                }
            }

            # Only update if the target DLL actually exists
            if ($finalPath) {
                 # Create HintPath if missing, or update if different
                 if (-not $hintPathNode) {
                    $hintPathNode = $xml.CreateElement("HintPath", $ns.ns)
                    $ref.AppendChild($hintPathNode) | Out-Null
                 }

                 if ($hintPathNode.InnerText -ne $finalPath) {
                    Write-Host "  Updating reference: $assemblyName -> $finalPath"
                    $hintPathNode.InnerText = $finalPath
                    $changed = $true
                }
            } else {
                 Write-Warning "  Skipping $assemblyName : Not found in target library path ($libPath) or designerBin"
            }
        }
    }

    if ($changed) {
        $xml.Save($csproj.FullName)
        Write-Host "  Saved changes to $($csproj.Name)"
    }
}

# 2. Update launchSettings.json
$launchSettingsFiles = Get-ChildItem -Filter "launchSettings.json" -Recurse
foreach ($file in $launchSettingsFiles) {
    Write-Host "Processing $($file.Name)..."
    $content = Get-Content $file.FullName -Raw
    
    try {
        $jsonObj = ConvertFrom-Json $content
        $changed = $false
        
        if ($jsonObj.profiles) {
            foreach ($profileName in $jsonObj.profiles.PSObject.Properties.Name) {
                $profile = $jsonObj.profiles.$profileName
                if ($profile.executablePath -and $profile.executablePath -match "Forguncy") {
                     if ($execPath -and $profile.executablePath -ne $execPath) {
                        $profile.executablePath = $execPath
                        $changed = $true
                     }
                }
            }
        }
        
        if ($changed) {
            $newContent = $jsonObj | ConvertTo-Json -Depth 10
            Set-Content -Path $file.FullName -Value $newContent
            Write-Host "  Updated executablePath in $($file.Name)"
        }
    } catch {
        Write-Warning "Failed to parse or update $($file.Name): $_"
    }
}

Write-Host "Update complete."

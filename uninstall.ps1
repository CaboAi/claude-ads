#Requires -Version 5.1
<#
.SYNOPSIS
    Claude Ads Uninstaller for Windows (multi-host).
.DESCRIPTION
    Removes only paths listed in install.ps1's ownership manifest. Unrelated
    ads-* skills and agents are never discovered or deleted by namespace.
.PARAMETER Target
    Which host CLI to uninstall from. Default: claude.
#>

param(
    [ValidateSet('claude','codex','cursor','windsurf','gemini','goose')]
    [string]$Target = 'claude',
    [string]$SkillDir = '',
    [string]$AgentDir = ''
)

$ErrorActionPreference = "Stop"

function Resolve-TargetPaths {
    param([string]$T)
    switch ($T) {
        'claude'   { return @{ SkillBase = Join-Path $env:USERPROFILE ".claude\skills";                                AgentDir = Join-Path $env:USERPROFILE ".claude\agents" } }
        'codex'    { return @{ SkillBase = Join-Path $env:USERPROFILE ".codex\skills";                                 AgentDir = Join-Path $env:USERPROFILE ".codex\agents" } }
        'cursor'   { return @{ SkillBase = Join-Path $env:USERPROFILE ".cursor\extensions\claude-ads\skills";          AgentDir = Join-Path $env:USERPROFILE ".cursor\extensions\claude-ads\agents" } }
        'windsurf' { return @{ SkillBase = Join-Path $env:USERPROFILE ".windsurf\skills";                              AgentDir = Join-Path $env:USERPROFILE ".windsurf\agents" } }
        'gemini'   { return @{ SkillBase = Join-Path $env:USERPROFILE ".gemini\extensions\claude-ads\skills";          AgentDir = Join-Path $env:USERPROFILE ".gemini\extensions\claude-ads\agents" } }
        'goose'    { return @{ SkillBase = Join-Path $env:USERPROFILE ".config\goose\skills";                          AgentDir = Join-Path $env:USERPROFILE ".config\goose\agents" } }
        default    { throw "Unknown target: $T" }
    }
}

function Main {
    $paths = Resolve-TargetPaths -T $Target
    $SkillBase = if ($SkillDir) { $SkillDir } else { $paths.SkillBase }
    $AgentDirResolved = if ($AgentDir) { $AgentDir } else { $paths.AgentDir }
    $ManifestPath = Join-Path $SkillBase ".claude-ads-$Target.manifest.json"

    if (-not (Test-Path $ManifestPath -PathType Leaf)) {
        throw "Ownership manifest not found: $ManifestPath. Refusing namespace-based deletion."
    }

    $Manifest = Get-Content $ManifestPath -Raw | ConvertFrom-Json
    if ($Manifest.version -ne 1 -or $Manifest.target -ne $Target) {
        throw "Invalid or mismatched ownership manifest: $ManifestPath"
    }

    $SkillRoot = [IO.Path]::GetFullPath($SkillBase).TrimEnd('\') + '\'
    $AgentRoot = [IO.Path]::GetFullPath($AgentDirResolved).TrimEnd('\') + '\'
    function Assert-OwnedPath([string]$Path) {
        $FullPath = [IO.Path]::GetFullPath($Path)
        $InSkill = $FullPath.StartsWith($SkillRoot, [StringComparison]::OrdinalIgnoreCase)
        $InAgents = $FullPath.StartsWith($AgentRoot, [StringComparison]::OrdinalIgnoreCase)
        if (-not ($InSkill -or $InAgents)) {
            throw "Unsafe ownership-manifest path: $Path"
        }
        return $FullPath
    }

    $AllOwnedPaths = @($Manifest.files) + @($Manifest.directories) + @($Manifest.recursive_directories)
    foreach ($OwnedPath in $AllOwnedPaths) { $null = Assert-OwnedPath $OwnedPath }

    Write-Host "Uninstalling Claude Ads from $SkillBase and $AgentDirResolved..."

    foreach ($OwnedFile in @($Manifest.files)) {
        $FullPath = Assert-OwnedPath $OwnedFile
        if (Test-Path $FullPath) { Remove-Item -LiteralPath $FullPath -Force }
    }

    foreach ($OwnedDir in @($Manifest.recursive_directories)) {
        $FullPath = Assert-OwnedPath $OwnedDir
        if (Test-Path $FullPath) { Remove-Item -LiteralPath $FullPath -Recurse -Force }
    }

    foreach ($OwnedDir in @($Manifest.directories) | Sort-Object Length -Descending) {
        $FullPath = Assert-OwnedPath $OwnedDir
        if (Test-Path $FullPath) {
            Remove-Item -LiteralPath $FullPath -ErrorAction SilentlyContinue
        }
    }

    Remove-Item -LiteralPath $ManifestPath -Force

    Write-Host "[OK] Claude Ads uninstalled." -ForegroundColor Green
}

Main

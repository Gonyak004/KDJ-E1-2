param([string]$ProjectRoot = (Split-Path $PSScriptRoot -Parent))
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$logPath = Join-Path $ProjectRoot 'artifacts\logs'
$imagePath = Join-Path $ProjectRoot 'artifacts\screenshots'
New-Item -ItemType Directory -Force -Path $imagePath | Out-Null

# 실제 실행 원문을 표시한 Windows 폼을 캡처한다. 콘솔 화면 합성은 하지 않는다.
foreach ($file in (Get-ChildItem -LiteralPath $logPath -Filter '*.txt' | Sort-Object Name)) {
    $lines = @(Get-Content -LiteralPath $file.FullName -Encoding UTF8)
    $pageSize = 30
    $pageCount = [Math]::Max(1, [Math]::Ceiling($lines.Count / $pageSize))
    for ($page = 0; $page -lt $pageCount; $page++) {
        $form = New-Object System.Windows.Forms.Form
        $form.Text = "KDJ-E1-2 | 실제 실행 기록 | $($file.BaseName) | $($page + 1)/$pageCount"
        $form.ClientSize = New-Object System.Drawing.Size(1180, 820)
        $form.StartPosition = 'CenterScreen'
        $form.BackColor = [System.Drawing.Color]::FromArgb(18, 24, 38)
        $label = New-Object System.Windows.Forms.Label
        $label.Text = "세계사 타임투어  /  Gonyak004/KDJ-E1-2`r`n실제 실행 원문: artifacts/logs/$($file.Name)  ·  $($page + 1)/$pageCount"
        $label.ForeColor = [System.Drawing.Color]::FromArgb(125, 211, 252)
        $label.Font = New-Object System.Drawing.Font('Malgun Gothic', 12)
        $label.SetBounds(24, 16, 1130, 60)
        $box = New-Object System.Windows.Forms.TextBox
        $box.Multiline = $true
        $box.ReadOnly = $true
        $box.BorderStyle = 'None'
        $box.BackColor = $form.BackColor
        $box.ForeColor = [System.Drawing.Color]::FromArgb(235, 240, 248)
        $box.Font = New-Object System.Drawing.Font('Consolas', 11)
        $box.WordWrap = $false
        $box.SetBounds(24, 88, 1130, 710)
        $first = $page * $pageSize
        $last = [Math]::Min($first + $pageSize - 1, $lines.Count - 1)
        $box.Text = ($lines[$first..$last] -join "`r`n")
        $form.Controls.Add($label)
        $form.Controls.Add($box)
        $form.Show()
        $box.Select(0, 0)
        $form.Refresh()
        [System.Windows.Forms.Application]::DoEvents()
        $bitmap = New-Object System.Drawing.Bitmap($form.Width, $form.Height)
        try {
            $form.DrawToBitmap($bitmap, (New-Object System.Drawing.Rectangle(0, 0, $form.Width, $form.Height)))
            $target = Join-Path $imagePath ("{0}-{1:00}.png" -f $file.BaseName, ($page + 1))
            $bitmap.Save($target, [System.Drawing.Imaging.ImageFormat]::Png)
        } finally {
            $bitmap.Dispose()
            $form.Close()
            $form.Dispose()
        }
    }
}
Write-Output "캡처 저장 완료: $imagePath"

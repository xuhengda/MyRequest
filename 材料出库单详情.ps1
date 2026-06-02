param(
    [Parameter(Mandatory = $false)]
    [string]$AccessToken,

    [Parameter(Mandatory = $false)]
    [string]$Id
)

$baseUrl = "http://10.167.80.50/iuap-api-gateway/yonbip/scm/materialout/detail"

if ([string]::IsNullOrWhiteSpace($AccessToken)) {
    $AccessToken = Read-Host "请输入 access_token"
}

if ([string]::IsNullOrWhiteSpace($Id)) {
    $Id = Read-Host "请输入 id"
}

if ([string]::IsNullOrWhiteSpace($AccessToken) -or [string]::IsNullOrWhiteSpace($Id)) {
    Write-Error "access_token 和 id 不能为空"
    exit 1
}

$query = @{
    access_token = $AccessToken
    id = $Id
}

$queryString = ($query.GetEnumerator() | ForEach-Object {
    "{0}={1}" -f [uri]::EscapeDataString($_.Key), [uri]::EscapeDataString($_.Value)
}) -join "&"

$url = "$baseUrl`?$queryString"

try {
    $response = Invoke-RestMethod -Method Get -Uri $url -TimeoutSec 30

    if ($response -is [string]) {
        Write-Output $response
    } else {
        $response | ConvertTo-Json -Depth 20
    }
} catch {
    Write-Error $_
    exit 1
}

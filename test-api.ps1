# 尝试更多端点格式
$tests = @(
  @{model='doubao-pro-32k'; endpoint='https://ark.cn-beijing.volces.com/api/open/v1/chat/completions'},
  @{model='doubao-pro-32k'; endpoint='https://ark.cn-beijing.volces.com/api/cs/chat/v1/completions'},
  @{model='doubao-pro-32k'; endpoint='https://ark.cn-beijing.volces.com/api/ark/v1/chat/completions'},
  @{model='doubao-pro-32k'; endpoint='https://ark.cn-beijing.volces.com/api/v1/chat/completions'}
)

foreach ($test in $tests) {
  Write-Host "Testing: $($test.endpoint)"
  $body = @{model=$test.model;messages=@(@{role='user';content='hi'});max_tokens=10} | ConvertTo-Json -Compress
  try {
    $resp = Invoke-RestMethod -Uri $test.endpoint -Method POST -Headers @{'Content-Type'='application/json';'Authorization'='Bearer a6d737ce-51f4-4c56-ba60-d80e73448b53'} -Body $body
    Write-Host "SUCCESS: " ($resp | ConvertTo-Json -Compress)
  } catch {
    Write-Host "Error: " $_.Exception.Message
  }
  Write-Host "---"
}
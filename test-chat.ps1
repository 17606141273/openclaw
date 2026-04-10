$body = @{
  model = 'doubao-1-5-pro-32k-250115'
  messages = @(@{role = 'user'; content = 'hi'})
  max_tokens = 20
} | ConvertTo-Json -Compress

$resp = Invoke-RestMethod -Uri 'https://ark.cn-beijing.volces.com/api/coding/v3/chat/completions' -Method POST -Headers @{
  'Content-Type' = 'application/json'
  'Authorization' = 'Bearer a6d737ce-51f4-4c56-ba60-d80e73448b53'
  'X-Api-Version' = '2024-09-01'
} -Body $body

$resp | ConvertTo-Json -Depth 3
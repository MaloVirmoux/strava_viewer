SELECT user_id, access_token, expires_date, refresh_token
FROM users 
WHERE user_id = '{user_id}'
LIMIT 1
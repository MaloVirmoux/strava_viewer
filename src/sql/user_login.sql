INSERT INTO users (user_id, user_name, access_token, expires_date, refresh_token, last_connection) 
VALUES ('{user_id}', '{user_name}', '{access_token}', '{expires_date}', '{refresh_token}', '{last_connection}')
ON CONFLICT (user_id) DO UPDATE 
  SET user_name = excluded.user_name, 
      access_token = excluded.access_token,
      expires_date = excluded.expires_date,
      refresh_token = excluded.refresh_token,
      last_connection = excluded.last_connection;
use playlists;
/* 
 *  **tables must be created in this order due to foreign key constraints**
 *
 * TODO: cascading deletes, but not now bc we aren't ever expecting deletes.
 */
CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(30), 
  password VARCHAR(100),
  email VARCHAR(100),
  registration_cookie VARCHAR(16),
  date_registered INT,
  spotify_auth_token VARCHAR(300),
  spotify_refresh_token VARCHAR(300),
  expires_at int(11),
  time_of_last_track_played INT,
  UNIQUE KEY(username)
);

CREATE TABLE tracks (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  spotify_uri VARCHAR(100),
  spotify_id VARCHAR(100),
  duration_ms INT,
  UNIQUE KEY(spotify_uri)
);


CREATE TABLE songs_played (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  track_id INT,
  user_id INT,
  played_at INT,
  FOREIGN KEY (user_id)
    REFERENCES users(id),
  FOREIGN KEY (track_id)
    REFERENCES tracks(id)
);

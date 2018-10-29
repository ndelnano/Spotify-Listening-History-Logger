/* A database `playlists` must exist first */
use playlists;
/* 
 *  **tables must be created in this order due to foreign key constraints**
 *
 * TODO: cascading deletes, but not now bc we aren't ever expecting deletes.
 * TODO: Add indexes
 */
CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(30),
  password VARCHAR(100),
  email VARCHAR(100),
  registration_cookie VARCHAR(16),
  date_registered INT,
  is_spotify_user INT,
  is_apple_music_user INT,
  spotify_auth_token VARCHAR(300),
  spotify_refresh_token VARCHAR(300),
  expires_at int(11),
  spotify_time_of_last_track_played INT,
  apple_music_time_of_last_track_played INT
);

-- ADD TEST USER
/*
insert into users (username, email, spotify_auth_token, spotify_refresh_token, is_spotify_user, spotify_time_of_last_track_played) VALUES ('nick', 'nick@gmail.com', 'BQAnLucMC3aK4sDBbkeMV5_O8lJvTpFEh9Rk1SulAqsFOhMxKLQJqIk5XWsgMBOReFpWjhHijXJYQrESdnFFpQCql0BIOEn7lj81zqpv9N5LP8EOJaRgS4rC28HOWGMQWxvmQF94FGqaaD1mHPZkkJNJ8W-7YjIl_fnLpjOAnfeyIHnYsqjUGPLkKGs2yxUJhIZ2I-Eu12XuYQk', 'AQBrFb2y17YqOgu5YSMpIH4q-UkgdTY7Ap15RKTvV08YA1SqOdPMN8p-Ui560SETgjR5N5m3-uhBFQy7WjXAI6n6jUhQyqlYq9k6bMYpt-1l-NI1TfDPSXYJCDNRBuxuKic', '1', '-1');
*/

CREATE TABLE artists (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  spotify_id VARCHAR(100),
  spotify_uri VARCHAR(100),
  genre_set INT
);

CREATE TABLE tracks (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  spotify_uri VARCHAR(100),
  spotify_id VARCHAR(100),
  duration_ms INT,
  danceability FLOAT(8,5),
  energy FLOAT(8,5),
  song_key FLOAT(8,5),
  loudness FLOAT(8,5),
  mode INT,
  speechiness FLOAT(8,5),
  acousticness FLOAT(8,5),
  instrumentalness FLOAT(8,5),
  liveness FLOAT(8,5),
  valence FLOAT(8,5),
  tempo FLOAT(8,5),
  time_signature INT
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

CREATE TABLE genres (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  genre VARCHAR(100)
);

-- add primary key here perhaps
CREATE TABLE artists_genres (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  artist_id INT,
  genre_id INT,
  FOREIGN KEY (artist_id)
    REFERENCES artists(id),
  FOREIGN KEY (genre_id)
    REFERENCES genres(id)
);

-- table for tracking many artists on a single track
-- add primary key here perhaps
CREATE TABLE artists_for_track (
  track_id INT,
  artist_id INT,
  FOREIGN KEY (track_id)
    REFERENCES tracks(id),
  FOREIGN KEY (artist_id)
    REFERENCES artists(id)
);


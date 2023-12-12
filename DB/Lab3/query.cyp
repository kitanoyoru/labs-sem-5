// Delete all linked nodes:
MATCH (n)-[r]-()
DELETE n, r

// Delete all not linked nodes:
MATCH (n)
DELETE (n)

// Find all countries:
MATCH (country:Country)
RETURN country

// Find players who play at the Striker position::
MATCH (player:Player)-[:HAS_POSITION]->(:Position {name: "Striker"})
RETURN player

// Find positions of the player with the name "Virgil van Dijk":
MATCH (player:Player {name: "Virgil van Dijk"})-[:HAS_POSITION]->(position:Position)
RETURN position

// Find players who play for Barcelona or Real Madrid:
MATCH (club:FootballClub)-[:HAS_PLAYER]->(player:Player)
WHERE club.name IN ["Barcelona", "Real Madrid"]
RETURN player

// Find all players who play for Brazil:
MATCH (country:Country {name: "Brazil"})-[:HAS_PLAYER]->(player:Player)
RETURN player

// Find all clubs in Spain:
MATCH (country:Country {name: "Spain"})-[:HAS_CLUB]->(club:FootballClub)
RETURN club

// Find players with ages between 23 and 30:
MATCH (player:Player)
WHERE player.age >= 23 AND player.age <= 30
RETURN player

// Find the oldest player in Barcelona:
MATCH (barcelona:FootballClub {name: "Barcelona"})-[:HAS_PLAYER]->(player:Player)
RETURN player
ORDER BY player.age DESC
LIMIT 1

// Find the average age of the Croatia team:
MATCH (croatia:Country {name: "Croatia"})-[:HAS_PLAYER]->(player:Player)
RETURN avg(player.age) AS average_age

// Find the club with the most trophies:
MATCH (club:FootballClub)
RETURN club.name, club.trophy_count
ORDER BY club.trophy_count DESC
LIMIT 1

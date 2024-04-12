<?php
$search = $_POST['movie_search'];
$servername = 'mysql.eecs.ku.edu';
$username = '447s24_k801a197';
$password = 'aex4Voer';
$db = 'MOVIES';

$conn = new mysqli($servername, $username, $password, $db); // Connect to database
if ($conn->connect_error) { // Handle connection error
    die("Connection failed: ". $conn->connect_error);
}
$sql = "SELECT * FROM MOVIES WHERE TITLE LIKE '%$search%' OR DIRECTOR LIKE '%$search%' OR RELEASE_YEAR LIKE '%$search%'"; // Search Query
$result = $conn->query($sql); // Store results of query
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc() ) {
        echo $row["TITLE"]."   ".$row["DIRECTOR"]."   "$row["RELEASE_YEAR"]."<br>";
    }
    else {
        echo "No movies found";
    }
}
?>
<?php
function login(){
$db_conn = pg_connect("jdbc:postgresql://localhost:15432/user_review");
$usernameErr = $passwordErr = "";
$username = $password = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (empty($_POST["username"])) {
        $usernameErr = "Username is required";
    } else if(empty($_POST["password"])) {
        $usernameErr = "Password is required";
    }
}

$query = "SELECT * FROM bank WHERE user_name='$username' AND password='$password'";
$results = pg_query($query);

if (mysqli_num_rows($results) == 1) { // user found
    $logged_in_user = pg_fetch_assoc($results);
    $_SESSION['user'] = $logged_in_user;
    header('location: homepage-template.php');	
}else {
    echo '<script>alert("Invalid input")</script>';
    }
}

echo $passwordErr;

?>
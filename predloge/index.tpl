<html>
<head>
    <title>Blackjack</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
    <link href="/static/bootstrap.min.css" type="text/css" rel="stylesheet">
    <link href="/static/bootstrap-grid.min.css" type="text/css" rel="stylesheet">
    <!-- jQuery and JS bundle w/ Popper.js -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ho+j7jyWK8fNQe+A12Hb8AhRq26LrZ/JpcUGGOn+Y7RsweNrtN/tE3MoK7ZeZDyx" crossorigin="anonymous"></script>
    <link href="/static/probavam.css" type="text/css" rel="stylesheet">
    <link href="/static/cards.css" type="text/css" rel="stylesheet">
</head>

<header class="header">
<nav class="navbar navbar-style">
    <div class="container">
        <div class="navbar-header">
            <p class="naslov">BLACKJACK<img src="/static/okrasek.png" alt="Karte" height="100" wifth="100" /></p>
            
        </div>
        <ul class="nav navbar nav navbar-rigth">
            <li><a href="/odjava">Odjava</a></li>
        </ul>
    </div>
</nav>
</header>
<body class="playingCards fourColours rotateHand">
    <div class="container">
    <div class="row row-height1">
        <div class="col-lg-4">
        </div>
        <div class="col-lg-4">
        <div class="prijava">
        <div class="padding">
        <h2>Pozdravljeni v igri Blackjack {{uporabnik[1]}} !</h2><br />
        Na razpolago imate še {{uporabnik[3]}} enot denarja<br />
        <ul>
        <li><a href="/igra">Prični z igranjem</a></li>
        </ul>
        </div>
        </div>
        
        </div>
        <div class="col-lg-4">
        </div>
    </div>
    </div>
    
    
<div class="footer">
    <hr />
    <div style="font-size: small">
    Powered by Python
    </div>
</div>
</body>
</html>

    
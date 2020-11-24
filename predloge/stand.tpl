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
    <div class="conatiner">
    <div class="row">
    </div>
    </div>
    <div class="conatiner">
    <div class="row row-height1">
        <div class="col-lg-4">
            <div class="col-lg-12 podatki">
            <div class="obroba">
            <h5>IGRALCEVI PODATKI</h5>
            Uporabnik: {{uporabnik[1]}}<br />
            Denar: {{uporabnik[3]}}<br />
            </div>
        </div>
        </div>
        <div class="col-lg-4">
            <div class="diler_karte">
            <h3>Dilerjeve karte<p class="sestevek">(
                {{aktivna_igra['dilerjeva_vsota']}}
                )</p>
            </h3>
            % for karta in aktivna_igra['dilerjeve_karte']:
            <div class="card rank-{{karta['vrednost']}} {{karta['barva']}}">
                <span class="rank">{{karta['vrednost']}}</span>
                <span class="suit">&{{karta['barva']}};</span>
            </div>
            % end
            </div>
        </div>
        <div class="col-lg-4">
            <div class="card back deck">*</div>
        </div>
    </div>
    </div>
    <div class="conatiner">
    <div class="row row-height2">
        <div class="col-lg-4">
        </div>
        <div class="col-lg-4">
        </div>
        <div class="col-lg-4">
        </div>
    </div>
    </div>
    <div class="conatiner">
    <div class="row row-height3">
        <div class="col-lg-4">
        <div class="kovanac"><img class="coin" src="/static/coin3.png" alt="Kovancek" height=60 width=60 />
        <p>{{igra_podatki[3]}}</p>
        </div>
        </div>
        <div class="col-lg-4">
        <h3>Igralceve karte<p class="sestevek">({{aktivna_igra['igralceva_vsota']}})</p></h3>
        % for karta in aktivna_igra['igralceve_karte']: 
        <div class="card rank-{{karta['vrednost']}} {{karta['barva']}}">
            <span class="rank">{{karta['vrednost']}}</span>
            <span class="suit">&{{karta['barva']}};</span>
        </div> 
        % end
        
        </div>
        <div class="col-lg-4">
            <table>
                <tr>
                    <td><button class="button">HIT</button></td>
                    <td><button class="button">STAND</button></td>
                </tr>
                <tr>
                    <td><button class="button">DOUBLE DOWN</button></td>
                </tr>
            </table>
        </div>
    </div>
    </div>
    
<script type="text/javascript">
setTimeout(function(){
    window.location="/igra/{{igra_podatki[0]}}";
    }, 3000);
</script>    
<div class="footer">
    <hr />
    <div style="font-size: small">
    Powered by Python
    </div>
</div>
</body>
</html>

    
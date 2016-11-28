//if ( ! Detector.webgl ) Detector.addGetWebGLMessage();
// var threeContainer = document.getElementById('three-container');
//
// threeContainer.innerWidth = 1157;
// threeContainer.innerHeight = 800;

 //var SCREEN_WIDTH = document.getElementById('three-container').innerWidth;
 //var SCREEN_HEIGHT = document.getElementById('three-container').innerHeight;
var crossWindDebug = false;


var SCREEN_WIDTH = 1100;
var SCREEN_HEIGHT = 700;
var container,stats;
var camera, scene1, renderer;
var arrowHelper;
var mouseX = 0, mouseY = 0;
var windowHalfX = SCREEN_WIDTH / 2;
var windowHalfY = SCREEN_HEIGHT / 2;

var mesh3;

var largeArrowSize = 2500;
var mediumArrowSize = 2000;
var smallArrowSize = 1750;

var largeLengthDivider = 1.75;
var mediumLengthDivider = 2;
var smallLengthDivider = 2.5;

var runwayDirectionDeg = 330;

var rad = (runwayDirectionDeg * Math.PI)/180;

init();
animate();


function init() {
  container = document.createElement( 'div' );
	document.getElementById('three-container').appendChild( container );
	renderer = new THREE.WebGLRenderer( { antialias: true } );

  camera = new THREE.PerspectiveCamera( 35, SCREEN_WIDTH / SCREEN_HEIGHT, 1, 25000 );
  camera.position.z = 20000;
  scene1 = new THREE.Scene();
  //scene1.fog = new THREE.Fog( 0xf2f7ff, 1, 25000 );
  scene1.add( new THREE.AmbientLight( 0xeef0ff ) );
  //var light1 = new THREE.DirectionalLight( 0xffffff, 2 );
  //light1.position.set( 1, 1, 1 );
  //scene1.add( light1 );
  // GROUND
  var textureLoader = new THREE.TextureLoader();
  // var maxAnisotropy = renderer.getMaxAnisotropy();
  var texture1 = textureLoader.load("static/img/compassTexture.jpg");
  var texture2 = textureLoader.load("static/img/landingStrip.jpg");
  var texture3 = textureLoader.load("static/img/planeImage.jpg");
  var material1 = new THREE.MeshPhongMaterial( { color: 0xffffff, map: texture1 } );
  var material2 = new THREE.MeshPhongMaterial( { color: 0xffffff, map: texture2 } );
  var material3 = new THREE.MeshPhongMaterial( { color: 0xffffff, map: texture3 } );
  //texture1.anisotropy = maxAnisotropy;
  //texture1.wrapS = texture1.wrapT = THREE.RepeatWrapping;
  //texture1.repeat.set( 512, 512 );
  				// if ( maxAnisotropy > 0 ) {
  				// 	document.getElementById( "val_left" ).innerHTML = texture1.anisotropy;
  				// 	document.getElementById( "val_right" ).innerHTML = texture2.anisotropy;
  				// } else {
  				// 	document.getElementById( "val_left" ).innerHTML = "not supported";
  				// 	document.getElementById( "val_right" ).innerHTML =  "not supported";
  				// }
  				//
    var geometry = new THREE.PlaneBufferGeometry( 125, 125 );
    var geometry2 = new THREE.PlaneBufferGeometry( 25, 50 );
    var geometry3 = new THREE.PlaneBufferGeometry( 60, 60 );
    var mesh1 = new THREE.Mesh( geometry, material1 );
    var mesh2 = new THREE.Mesh( geometry, material2 );
    mesh3 = new THREE.Mesh( geometry3, material3 );
    //mesh1.rotation.x = - Math.PI / 2;
    mesh1.scale.set( 100, 100, 100 );
    scene1.add( mesh1 );

    mesh2.scale.set(15, 50, 25);
    //mesh2.rotation.z =  Math.PI / 7;
    mesh2.rotation.z =  - (rad);
    mesh2.position.x += 50;
    mesh2.position.y += 50;
    scene1.add(mesh2);

    mesh3.scale.set(30, 65, 25);
    //mesh2.rotation.z =  Math.PI / 7;
    mesh3.rotation.z =  - (rad);
    mesh3.position.x += 50;
    mesh3.position.y += 50;
    //scene1.add(mesh3);

    var degrees = 90;

    if (degrees > 65 && degrees < 180)
    {
      degrees += (180-degrees)/25%3 + 1;
    }

    var radDir = ((degrees+90) * Math.PI)/180;
    //var xIn = 315; //(-cos(deg+90)*5000)+65
    //var yIn = 315; //sin(deg+90)*5000-85

    xIn = (-1*Math.cos(radDir)*5000)+65;
    console.log(Math.cos(radDir));
    console.log(xIn);
    yIn = Math.sin(radDir)*5200 - 85;
    console.log(yIn);

    //the origin of the compass on the texture has an offset x of 150 and extended y of 300
    var rx = 150;
    // if(degrees > 180)
    //    ry = 300;
    // else
    //    ry = 200;
    var ry = 200;
    var x = xIn + rx;
    var y = ((yIn + ry)*yIn)/yIn;

    var from = new THREE.Vector3( x, y, 0 );
    var to = new THREE.Vector3( 0, 0, 0 );
    var direction = to.clone().sub(from);
    var length = direction.length()/1.75;
    arrowHelper = new THREE.ArrowHelper(direction.normalize(), from, length, 0xff0000, 2500, 2500 );
    arrowHelper.z = 200;
    scene1.add( arrowHelper );

  	// RENDERER
  	//renderer.setClearColor( scene1.fog.color );
    renderer.setClearColor(0xffffff)
  	renderer.setPixelRatio( window.devicePixelRatio );
  	renderer.setSize( SCREEN_WIDTH, SCREEN_HEIGHT );
  	renderer.autoClear = false;
  	renderer.domElement.style.position = "relative";
  	container.appendChild( renderer.domElement );
  // 				document.addEventListener( 'mousemove', onDocumentMouseMove, false );
}

function animate() {
	requestAnimationFrame( animate );
  //placeArrow(330);
	render();
}

//Rotates the plane image 180 degrees to use the oposite runway
function changeRunway()
{
  mesh3.rotation.z -= Math.PI;
}

function placeArrow(degrees) {

  scene1.remove(arrowHelper);
  if (degrees > 65 && degrees < 180)
  {
    degrees += (180-degrees)/25%3 + 1;
  }

  var radDir = ((degrees+90) * Math.PI)/180;
  //var xIn = 315; //(-cos(deg+90)*5000)+65
  //var yIn = 315; //sin(deg+90)*5000-85

  xIn = (-1*Math.cos(radDir)*5000)+65;
  console.log(Math.cos(radDir));
  console.log(xIn);
  yIn = Math.sin(radDir)*5200 - 85;
  console.log(yIn);

  //the origin of the compass on the texture has an offset x of 150 and extended y of 300
  var rx = 150;
  // if(degrees > 180)
  //    ry = 300;
  // else
  //    ry = 200;
  var ry = 200;
  var x = xIn + rx;
  var y = ((yIn + ry)*yIn)/yIn;

  var from = new THREE.Vector3( x, y, 0 );
  var to = new THREE.Vector3( 0, 0, 0 );
  var direction = to.clone().sub(from);
  var length = direction.length()/2.5;
  arrowHelper = new THREE.ArrowHelper(direction.normalize(), from, length, 0xff0000, 1750, 1750 );
  arrowHelper.z = 200;
  scene1.add( arrowHelper );
}

function degreeUpdateButtonClick() {

  var degrees = parseInt(document.getElementById('degreeInput').value);
  console.log(degrees);

  var degreeSpan = document.getElementById('windDirectionNumber');
  degreeSpan.innerHTML = degrees.toString() + "&deg;";

  placeArrow(degrees);

  }

  function knotsUpdateButtonClick() {
    var knotsSpan = document.getElementById('windSpeedNumber');
    var knotsInput = document.getElementById('knotsInput').value;

    console.log(knotsInput);
    knotsSpan.innerHTML = knotsInput.toString();


    //Maybe change arrow size here...
  }

function render() {
				//camera.position.x += ( mouseX - camera.position.x ) * .05;
        //camera.position.x = 0;
        //camera.position.y = 0;
				//camera.position.y = THREE.Math.clamp( camera.position.y + ( - ( mouseY - 200 ) - camera.position.y ) * .05, 50, 1000 );
				camera.lookAt( scene1.position );
				renderer.clear();
				//renderer.setScissorTest( true );
				//renderer.setScissor( 0, 0, SCREEN_WIDTH/2 - 2, SCREEN_HEIGHT );
				renderer.render( scene1, camera );
				//renderer.setScissor( SCREEN_WIDTH/2, 0, SCREEN_WIDTH/2 - 2, SCREEN_HEIGHT  );
				//renderer.setScissorTest( false );
			}


function setCrossWindWarning() {
  var crossWindDiv = document.getElementById('crossWindWarning');

  $(crossWindDiv).removeClass("hiddenBlock");
}

function clearCrossWindWarning() {
  var crossWindDiv = document.getElementById('crossWindWarning');

  $(crossWindDiv).addClass("hiddenBlock");
}

function showPeakGust() {
  var peakGustTR = document.getElementById('peakGustRow');

  $(peakGustTR).removeClass("hiddenBlock");
}

function hidePeakGust() {
  var peakGustTR = document.getElementById('peakGustRow');

  $(peakGustTR).addClass("hiddenBlock");
}


function getWindData() {
	$.getJSON("api/data/", function(result) {

		console.log(result);
		var knotsSpan = document.getElementById('windSpeedNumber');
		knotsSpan.innerHTML = result.windSpeed.toString();

		var degreeSpan = document.getElementById('windDirectionNumber');
  		degreeSpan.innerHTML = result.windDir.toString() + "&deg;";

		var peakGustSpan = document.getElementById('peakGustNumber');

		if(result.peakGust && parseInt(result.peakGust) >= 5) {
			console.log('Showing Peak Gust');			

			showPeakGust();
			peakGustSpan.innerHTML = result.peakGust.toString();
		}
		else {
			console.log('Hiding Peak Gust');
		
			hidePeakGust();
		}

		if(crossWindDebug == false)
		{
			if(result.crossWindFlag && result.crossWindFlag == 'true') {
				console.log('Set Crosswind Warning Flag');
				setCrossWindWarning();
			}
			else {
				console.log('Clear Crosswind Warning Flag');
				clearCrossWindWarning();
			}
		}

		placeArrow(parseInt(result.windDir));
	});
}

var demoFlag = false;

window.setInterval(function() {
	if(!demoFlag)
		getWindData();
}, 2000);

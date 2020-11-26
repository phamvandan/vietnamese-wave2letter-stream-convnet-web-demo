//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext; //audio context to help us record
var constraints = {audio: true, video: false};
var stream_obj = navigator.mediaDevices.getUserMedia(constraints);

function startRecording() {
    console.log("start recording");
    var constraints = {audio: true, video: false};
    navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
        console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
        audioContext = new AudioContext();
        /*  assign to gumStream for later use  */
        gumStream = stream;
        /* use the stream */
        input = audioContext.createMediaStreamSource(stream);
        /*
            Create the Recorder object and configure to record mono sound (1 channel)
            Recording 2 channels  will double the file size
        */
        rec = new Recorder(input, {numChannels: 1});
//        //start the recording process
        console.log("typeof rec");
        console.log(typeof rec);
        rec.record();

    }).catch(function (err) {
        //enable the record button if getUserMedia() fails
    });
//    rec.stop();
}

var next = true;
setInterval(function() {
    if(next === true) {
        runSpeechRecognition();
    }
}, 0);

function stopRecording() {
//    rec = "stop recording"
    console.log("stop recording and save audio");
    //tell the recorder to stop the recording
    rec.stop();
    //stop microphone access
    gumStream.getAudioTracks()[0].stop();
    //create the wav blob and pass it on to createDownloadLink
    rec.exportWAV(createDownloadLink);
}


function createDownloadLink(blob) {
    console.log("exporting");
    var filename = ".wav";
//    if (Array.isArray(blob) && blob.length) {
    let xhr = new XMLHttpRequest();
    var fd = new FormData();
    console.log(blob[1]);
    fd.append("audio_data", blob, filename);
    xhr.open("POST", "https://"+dbHost+"/save_audios", true);
    xhr.send(fd);
    var myurl = "https://"+dbHost+"/speech_to_text";
    $.get(myurl, function(data, status){
        document.getElementById('text').value += data + " ";
    });
    next = true;
    // alert("tải lên thành công");
    // window.location = "/record_audio";
//    }else{
//        alert("Chưa đủ file thu âm!");
//    }
}
var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;

/* JS comes here */
function runSpeechRecognition() {
    // get output div reference
//    var output = document.getElementById("output");
    // get action element reference
//    var action = document.getElementById("action");
    // new speech recognition object
//    do{
    next = false;
    var recognition = new SpeechRecognition();
    // This runs when the speech recognition service starts
    recognition.onstart = function() {
        action.innerHTML = "<small>listening, please speak...</small>";
        startRecording();
    };
    recognition.onspeechend = function() {
        action.innerHTML = "<small>stopped listening, hope you are done...</small>";
        recognition.abort();
        stopRecording();
    };

    // This runs when the speech recognition service returns result
    // recognition.onresult = function(event) {
    //     var transcript = event.results[0][0].transcript;
    //     var confidence = event.results[0][0].confidence;
    //     output.innerHTML = "<b>Text:</b> " + transcript + "<br/> <b>Confidence:</b> " + confidence*100+"%";
    //     output.classList.remove("hide");
    // };

     // start recognition
     recognition.start();
//         console.log(next);
//    }while(1==1);
}
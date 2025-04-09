document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.getElementById('startRecording');
    const stopButton = document.getElementById('stopRecording');
    const currentEmotion = document.getElementById('currentEmotion');
    const emotionHistory = document.getElementById('emotionHistory');
    
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;

    // Update emotion history
    function updateEmotionHistory() {
        fetch('/api/emotions/recent')
            .then(response => response.json())
            .then(emotions => {
                emotionHistory.innerHTML = '';
                emotions.forEach(emotion => {
                    const time = new Date(emotion.timestamp).toLocaleTimeString();
                    const div = document.createElement('div');
                    div.className = 'history-item';
                    div.innerHTML = `
                        <span>${emotion.emotion}</span>
                        <span>${time}</span>
                    `;
                    emotionHistory.appendChild(div);
                });
            })
            .catch(error => console.error('Error fetching emotion history:', error));
    }

    // Request microphone access
    startButton.addEventListener('click', async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            startRecording(stream);
            startButton.disabled = true;
            stopButton.disabled = false;
            isRecording = true;
        } catch (err) {
            console.error('Error accessing microphone:', err);
            alert('Error accessing microphone. Please ensure you have granted microphone permissions.');
        }
    });

    // Stop recording
    stopButton.addEventListener('click', () => {
        mediaRecorder.stop();
        startButton.disabled = false;
        stopButton.disabled = true;
        isRecording = false;
    });

    // Start recording function
    function startRecording(stream) {
        audioChunks = [];
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.addEventListener('dataavailable', event => {
            audioChunks.push(event.data);
        });

        mediaRecorder.addEventListener('stop', () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            stream.getTracks().forEach(track => track.stop());
            
            // For the real ml client send this audio data 
            // For now, I have a random method to simulate receiving emotions 
            simulateEmotionDetection();
        });

        // Start recording in 5-second chunks
        mediaRecorder.start(5000);
        
        // Set up interval for continuous chunks
        setInterval(() => {
            if (isRecording) {
                mediaRecorder.stop();
                mediaRecorder.start(5000);
                simulateEmotionDetection();
            }
        }, 5000);
    }

    // PLACEHOLDER function to simulate emotion detection
    function simulateEmotionDetection() {
        const emotions = ['happy', 'sad', 'angry', 'neutral', 'surprised'];
        const randomEmotion = emotions[Math.floor(Math.random() * emotions.length)];
        
        fetch('/api/emotions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                emotion: randomEmotion,
                confidence: Math.random().toFixed(2)
            })
        })
        .then(response => response.json())
        .then(() => {
            currentEmotion.textContent = randomEmotion;
            updateEmotionHistory();
        })
        .catch(error => console.error('Error saving emotion:', error));
    }

    // Initial emotion history load
    updateEmotionHistory();
}); 
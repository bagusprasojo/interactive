// static/kuis/firebase-client.js
const firebaseConfig = {
            apiKey: "AIzaSyAXcHVUrzqNTIilF-Xnncik_uQ_KVbngLY",
            authDomain: "quickstart-1583738730654.firebaseapp.com",
            databaseURL: "https://quickstart-1583738730654-default-rtdb.asia-southeast1.firebasedatabase.app",
            projectId: "quickstart-1583738730654",
            storageBucket: "quickstart-1583738730654.appspot.com",
            messagingSenderId: "314267506700",
            appId: "1:314267506700:web:079c361a35ea5d9e523629"
        };

firebase.initializeApp(firebaseConfig);
const db = firebase.database();

// Real-time soal aktif
function listenSoal(kuisId, callback) {
    // const db = firebase.database();
    const ref = db.ref(`kuis/${kuisId}/soal_aktif`);

    ref.on('value', (snapshot) => {
        const soalKe = snapshot.val();
        if (soalKe !== null && soalKe >= 0) {
            callback(soalKe);
        }
    });
}

// Real-time leaderboard
function listenLeaderboard(kuisId, updateLeaderboard) {
    db.ref(`leaderboard/${kuisId}`).on('value', (snapshot) => {
        const data = snapshot.val();

        console.log("Leaderboard data:", data);
        if (data) {
            updateLeaderboard(data);
        }
    });
}

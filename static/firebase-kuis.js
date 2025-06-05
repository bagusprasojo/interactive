// static/firebase-kuis.js

import { initializeApp } from "https://www.gstatic.com/firebasejs/11.8.1/firebase-app.js";
import { getDatabase, ref, set } from "https://www.gstatic.com/firebasejs/11.8.1/firebase-database.js";

const firebaseConfig = {
  apiKey: "AIzaSyAXcHVUrzqNTIilF-Xnncik_uQ_KVbngLY",
  authDomain: "quickstart-1583738730654.firebaseapp.com",
  databaseURL: "https://quickstart-1583738730654.firebaseio.com",
  projectId: "quickstart-1583738730654",
  storageBucket: "quickstart-1583738730654.firebasestorage.app",
  messagingSenderId: "314267506700",
  appId: "1:314267506700:web:079c361a35ea5d9e523629"
};

const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

window.submitJawaban = function(soal_id, pilihan) {
  const userId = Math.floor(Math.random() * 100000);
  set(ref(db, 'jawaban/' + soal_id + '/' + userId), pilihan);
  alert("Jawaban Anda telah disimpan: " + pilihan);
};

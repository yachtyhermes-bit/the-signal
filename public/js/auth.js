(function() {
  'use strict';

  // Placeholder Firebase config — swap in real values when ready
  const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_PROJECT.firebaseapp.com",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_PROJECT.appspot.com",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
  };

  const authToggle = document.getElementById('authToggle');
  const authDropdown = document.getElementById('authDropdown');
  const authLabel = document.getElementById('authLabel');
  const authUserInfo = document.getElementById('authUserInfo');
  const authOptions = document.getElementById('authOptions');
  const authAvatar = document.getElementById('authAvatar');
  const authName = document.getElementById('authName');
  const authSignOut = document.getElementById('authSignOut');
  const authGoogle = document.getElementById('authGoogle');
  const authGithub = document.getElementById('authGithub');
  const authEmail = document.getElementById('authEmail');

  if (!authToggle) return;

  let firebaseApp = null;
  let firebaseAuth = null;
  let firebaseInitialized = false;

  // Try to initialize Firebase if SDK is loaded
  function initFirebase() {
    if (firebaseInitialized) return;
    try {
      if (typeof firebase !== 'undefined' && firebase.initializeApp) {
        firebaseApp = firebase.initializeApp(firebaseConfig, 'thesignal');
        firebaseAuth = firebaseApp.auth();
        firebaseInitialized = true;
        console.log('Auth: Firebase initialized');

        // Listen for auth state changes
        firebaseAuth.onAuthStateChanged(function(user) {
          if (user) {
            updateUIForUser(user);
            saveUserSession(user);
          } else {
            updateUIForGuest();
            clearUserSession();
          }
        });
      } else {
        console.log('Auth: Firebase SDK not loaded. Drop-in UI functional.');
      }
    } catch (err) {
      console.warn('Auth: Firebase init failed —', err.message);
    }
  }

  // Session persistence via localStorage for page refresh
  function saveUserSession(user) {
    try {
      localStorage.setItem('thesignal_user', JSON.stringify({
        displayName: user.displayName,
        email: user.email,
        photoURL: user.photoURL,
        uid: user.uid
      }));
    } catch (e) {}
  }

  function clearUserSession() {
    try { localStorage.removeItem('thesignal_user'); } catch (e) {}
  }

  function getStoredUser() {
    try {
      var data = localStorage.getItem('thesignal_user');
      return data ? JSON.parse(data) : null;
    } catch (e) { return null; }
  }

  function updateUIForUser(user) {
    if (!user) return;
    if (authLabel) authLabel.textContent = user.displayName || user.email || 'User';
    if (authUserInfo) authUserInfo.style.display = 'flex';
    if (authOptions) authOptions.style.display = 'none';
    if (authAvatar) {
      authAvatar.src = user.photoURL || '';
      authAvatar.style.display = user.photoURL ? 'block' : 'none';
    }
    if (authName) authName.textContent = user.displayName || user.email || 'User';
  }

  function updateUIForGuest() {
    if (authLabel) authLabel.textContent = 'Sign In';
    if (authUserInfo) authUserInfo.style.display = 'none';
    if (authOptions) authOptions.style.display = 'flex';
    if (authAvatar) authAvatar.style.display = 'none';
  }

  // Restore session on page load
  var storedUser = getStoredUser();
  if (storedUser) {
    updateUIForUser(storedUser);
  }

  // Dropdown toggle
  authToggle.addEventListener('click', function(e) {
    e.stopPropagation();
    var isOpen = authDropdown.classList.contains('active');
    // Close all dropdowns
    document.querySelectorAll('.auth-dropdown.active').forEach(function(d) {
      d.classList.remove('active');
    });
    if (!isOpen) {
      authDropdown.classList.add('active');
    }
  });

  // Close dropdown when clicking outside
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.auth-container')) {
      authDropdown.classList.remove('active');
    }
  });

  // Auth action handlers
  function showNotConfigured() {
    if (authLabel) authLabel.textContent = 'Coming Soon';
    setTimeout(function() {
      var stored = getStoredUser();
      if (authLabel) authLabel.textContent = stored ? (stored.displayName || stored.email || 'User') : 'Sign In';
    }, 2000);
  }

  if (authGoogle) {
    authGoogle.addEventListener('click', function() {
      if (!firebaseInitialized) { showNotConfigured(); return; }
      try {
        var provider = new firebase.auth.GoogleAuthProvider();
        firebaseAuth.signInWithPopup(provider);
      } catch(e) { showNotConfigured(); }
    });
  }

  if (authGithub) {
    authGithub.addEventListener('click', function() {
      if (!firebaseInitialized) { showNotConfigured(); return; }
      try {
        var provider = new firebase.auth.GithubAuthProvider();
        firebaseAuth.signInWithPopup(provider);
      } catch(e) { showNotConfigured(); }
    });
  }

  if (authEmail) {
    authEmail.addEventListener('click', function() {
      // Could show an email/password form; for now show a prompt
      var email = prompt('Enter your email to sign in (Firebase not configured — this is a placeholder):');
      if (email) {
        showNotConfigured();
      }
    });
  }

  if (authSignOut) {
    authSignOut.addEventListener('click', function() {
      if (firebaseInitialized && firebaseAuth) {
        firebaseAuth.signOut();
      }
      updateUIForGuest();
      clearUserSession();
      authDropdown.classList.remove('active');
    });
  }

  // Try Firebase init after a short delay (in case scripts load asynchronously)
  setTimeout(initFirebase, 500);

})();

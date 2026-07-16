/**
 * BoardPrep AI 2.0 - Core Utilities and App State
 */

class AppConfig {
  static API_BASE_URL = window.location.origin.includes('localhost') || window.location.origin.includes('127.0.0.1')
    ? 'http://127.0.0.1:5000'
    : 'https://boardprep-backend.onrender.com'; // Fallback to Render URL or override dynamically
}

// Global Auth helper
const getAuthHeaders = async () => {
  const user = firebase.auth().currentUser;
  if (user) {
    const idToken = await user.getIdToken(true);
    return {
      'Authorization': `Bearer ${idToken}`,
      'Content-Type': 'application/json'
    };
  }
  return {
    'Content-Type': 'application/json'
  };
};

// UI Notifications / Toast system
const showToast = (message, type = 'info') => {
  const toastContainer = document.getElementById('toast-container') || createToastContainer();
  const toast = document.createElement('div');
  toast.className = `flex items-center w-full max-w-xs p-4 text-gray-100 rounded-lg shadow-lg glass transition-all duration-300 transform translate-y-2 opacity-0 border-l-4 ${
    type === 'success' ? 'border-emerald-500' : type === 'error' ? 'border-rose-500' : 'border-indigo-500'
  }`;

  toast.innerHTML = `
    <div class="ms-3 text-sm font-normal">${message}</div>
    <button type="button" class="ms-auto -mx-1.5 -my-1.5 text-gray-400 hover:text-white rounded-lg focus:ring-2 p-1.5 inline-flex items-center justify-center h-8 w-8" onclick="this.parentElement.remove()">
      <span class="sr-only">Close</span>
      <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
      </svg>
    </button>
  `;

  toastContainer.appendChild(toast);

  // Animate Entrance
  setTimeout(() => {
    toast.classList.remove('translate-y-2', 'opacity-0');
  }, 10);

  // Auto dismiss
  setTimeout(() => {
    toast.classList.add('translate-y-2', 'opacity-0');
    setTimeout(() => toast.remove(), 300);
  }, 4000);
};

const createToastContainer = () => {
  const container = document.createElement('div');
  container.id = 'toast-container';
  container.className = 'fixed bottom-5 right-5 z-50 flex flex-col gap-2';
  document.body.appendChild(container);
  return container;
};

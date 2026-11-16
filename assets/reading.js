const checkbox = document.querySelector('#read');
const status = document.querySelector('#storage-status');
const key = 'study-notes:read:' + location.pathname;
try { checkbox.checked = localStorage.getItem(key) === 'true'; }
catch { status.textContent = '此瀏覽器無法保存閱讀紀錄，本次仍可勾選。'; }
checkbox.addEventListener('change', () => {
  try { localStorage.setItem(key, String(checkbox.checked)); status.textContent = '閱讀紀錄已儲存於目前瀏覽器。'; }
  catch { status.textContent = '無法儲存閱讀紀錄，重新整理後可能不會保留。'; }
});

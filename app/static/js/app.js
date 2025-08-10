window.toast = function(msg){
  const el = document.getElementById('toast');
  if(!el) return;
  el.textContent = msg;
  el.classList.remove('hidden');
  setTimeout(()=> el.classList.add('hidden'), 2500);
};

document.addEventListener('htmx:requestError', ()=> toast('Erro ao carregar'));
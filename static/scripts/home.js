const searchButton = document.querySelector('.searchButton');
const searchTerm = document.querySelector('.searchTerm');
const endpoint = '/search';

searchButton.addEventListener('click', function() {
  const inputValue = searchTerm.value;
  const currentHost = window.location.host;
  const protocol = window.location.protocol;
  const url = `${protocol}//${currentHost}${endpoint}?query=${encodeURIComponent(inputValue)}`;
  window.location.href = url;
});
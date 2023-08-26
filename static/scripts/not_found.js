const backButton = document.querySelector('.backButton');

backButton.addEventListener('click', function() {
  const currentHost = window.location.host;
  const protocol = window.location.protocol;
  const url = `${protocol}//${currentHost}`;
  window.location.href = url;
});
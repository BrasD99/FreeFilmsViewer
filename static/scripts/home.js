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

searchTerm.addEventListener("keyup", function(event) {
  if (event.keyCode === 13) { // 13 represents the Enter key
    event.preventDefault(); // Prevent form submission

    // Trigger the click event on the search button
    searchButton.click();
  }
});